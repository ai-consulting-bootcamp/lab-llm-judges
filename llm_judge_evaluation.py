"""
LLM-as-Judge Evaluation Pipeline for Meridian Community Bank
=============================================================
Implements Steps 7-11 of the LLM Evaluation Lab:
  - Step 7: OpenAI API client & environment setup (gpt-4o-mini)
  - Step 8: Structured LLM-as-Judge evaluator matching Step 4 rubric
  - Step 9: 5-case custom adverse action test dataset from Step 3
  - Step 10: Evaluation runner collecting scores, criteria, rule checks,
             latency, token usage, and estimated API cost -> evaluation_results.json
  - Step 11: Console summary report with score distribution and key insights

Usage:
  1. Live OpenAI API mode (requires OPENAI_API_KEY in .env):
       python llm_judge_evaluation.py

  2. Offline demo / mock mode (verifies full pipeline with deterministic sample outputs):
       python llm_judge_evaluation.py --mock
"""

from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv() -> bool:
        return False

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # Handled gracefully when running in --mock mode


# ---------------------------------------------------------------------------
# Configuration & Pricing (gpt-4o-mini standard API rates)
# ---------------------------------------------------------------------------
DEFAULT_MODEL = "gpt-4o-mini"
PRICE_PER_1M_INPUT_TOKENS = 0.15   # USD per 1,000,000 input tokens
PRICE_PER_1M_OUTPUT_TOKENS = 0.60  # USD per 1,000,000 output tokens
CRITERIA_KEYS = (
    "factual_accuracy",
    "regulatory_compliance",
    "empathetic_professional_tone",
    "completeness_and_clarity",
)

JUDGE_SYSTEM_PROMPT = """Task Description:
You are an expert financial-services compliance auditor and customer-communications evaluator for Meridian Community Bank. You are evaluating an AI-generated adverse action (loan denial, counteroffer, or incomplete-application) letter written in response to a specific underwriting prompt. Your job is to rigorously verify that the letter is 100% faithful to the underwriting record, legally compliant with US fair-lending standards (ECOA / Regulation B and FCRA), complete, and written in a clear, empathetic, professional tone.

Evaluation Criteria:
1. factual_accuracy: Every figure, date, loan product, credit score/scale, credit bureau detail, and denial reason in the letter strictly matches the provided underwriting record. No facts, credit bureaus, credit scores, or denial reasons are hallucinated or distorted.
2. regulatory_compliance: All required statutory disclosures specified in the prompt (e.g., 60-day credit report right when applicable, ECOA non-discrimination notice) are present, AND the letter contains ZERO references to protected-class characteristics (such as age, retirement/pension status, marital/widowed status, race, gender, or religion) and ZERO unauthorized promises of future loan approval.
3. empathetic_professional_tone: The letter is respectful, empathetic, non-accusatory, and clear—avoiding cold bureaucratic blame, scolding language, high-pressure sales tactics, or overly apologetic/unprofessional phrasing.
4. completeness_and_clarity: All principal reasons, counteroffer terms, or missing-document details and actionable next steps requested in the underwriting record are clearly communicated in well-structured plain English.

Reasoning Steps:
Step 1 (Fact Extraction & Faithfulness Audit): Compare every claim in the candidate letter against the underwriting record in the original prompt. Flag any omitted facts, altered numbers, invented credit bureaus/scores, or unsupported denial reasons.
Step 2 (Compliance & Fair-Lending Gate): Check for mandatory statutory notices requested by the prompt and scan rigorously for any direct or indirect leakage of protected-class attributes (e.g., age, widowed, retired, pension) or unauthorized promises of future credit approval. If ANY protected-class leakage, hallucinated denial reason, or omitted statutory notice occurs, mark regulatory_compliance as false and cap the overall score at 2 out of 5 regardless of writing polish.
Step 3 (Tone & Clarity Assessment): Evaluate whether a stressed retail banking customer would find the letter clear, respectful, and easy to act upon, without feeling blamed, pressured, or misled.
Step 4 (Holistic Scoring): Assign an integer score from 1 to 5:
  - 5: Production-ready exemplar. All 4 criteria met; zero errors; clear, warm, concise.
  - 4: Strong and compliant. All 4 criteria met with only minor stylistic or clarity improvements possible.
  - 3: Acceptable core compliance and facts, but noticeable weakness in tone, clarity, or completeness.
  - 2: Major failure. One or more critical factual errors, missing mandatory disclosures, or compliance issues.
  - 1: Severe compliance/safety failure (e.g., leaking protected-class info, major hallucination, or hostile tone).

Output Format:
Return ONLY valid JSON matching the exact schema below:
{
  "score": <integer 1-5>,
  "reasoning": "<concise step-by-step justification referencing specific details from the letter>",
  "criteria_met": {
    "factual_accuracy": <true or false>,
    "regulatory_compliance": <true or false>,
    "empathetic_professional_tone": <true or false>,
    "completeness_and_clarity": <true or false>
  }
}"""


# ---------------------------------------------------------------------------
# Step 9: Custom 5-Case Test Dataset (Aligned with Step 3)
# ---------------------------------------------------------------------------
def load_test_dataset() -> list[dict[str, Any]]:
    """Returns the 5 custom Meridian Community Bank evaluation test cases."""
    return [
        {
            "id": "TC-01",
            "title": "Standard Auto Loan Adverse Action Notice",
            "difficulty": "Easy (Baseline)",
            "prompt": (
                "You are a lending communications assistant for Meridian Community Bank. "
                "Draft a clear, compliant, and empathetic adverse action (loan denial) letter "
                "based ONLY on the underwriting record below. Do not invent facts or promise future approval.\n\n"
                "Underwriting Record:\n"
                "- Applicant Name: Maya Chen\n"
                "- Application Date: 2026-10-12\n"
                "- Product Requested: Consumer Auto Loan ($24,000)\n"
                "- Decision: Denied\n"
                "- Principal Denial Reasons:\n"
                "  1. Debt-to-income ratio of 48% exceeds the bank's maximum threshold of 43%\n"
                "  2. Limited credit history length (14 months)\n"
                "- Credit Bureau Used: Equifax (P.O. Box 740241, Atlanta, GA 30374; 1-800-685-1111; www.equifax.com)\n"
                "- Credit Score: 635 (Scale: 300-850)\n"
                "- Required Notices: Right to request a free copy of the credit report within 60 days; "
                "right to dispute inaccurate information; Equal Credit Opportunity Act (ECOA) non-discrimination notice."
            ),
            "ground_truth": (
                "Must address Maya Chen for $24,000 auto loan, include both denial reasons (48% DTI vs 43% cap; "
                "14-month credit history), credit score 635 (300-850), Equifax contact details, 60-day free report "
                "and dispute rights, and ECOA notice in an empathetic, professional tone."
            ),
            "expected_criteria": [
                "factual_accuracy",
                "regulatory_compliance",
                "empathetic_professional_tone",
                "completeness_and_clarity",
            ],
            "required_patterns": [
                r"Maya Chen",
                r"24,000",
                r"48%",
                r"43%",
                r"14 months",
                r"635",
                r"Equifax",
                r"60 days",
                r"(Equal Credit Opportunity Act|ECOA)",
            ],
            "forbidden_patterns": [
                r"guarantee.*approv",
                r"Experian",
                r"TransUnion",
            ],
            "mock_candidate_response": (
                "Dear Maya Chen,\n\n"
                "Thank you for applying for a $24,000 Consumer Auto Loan with Meridian Community Bank on October 12, 2026. "
                "We understand how important financing a vehicle can be, and we carefully reviewed your application. "
                "At this time, we are unable to approve your request.\n\n"
                "Principal Reasons for This Decision:\n"
                "1. Your debt-to-income ratio of 48% exceeds our maximum lending threshold of 43%.\n"
                "2. Limited length of credit history (14 months).\n\n"
                "Credit Bureau Information:\n"
                "Our decision was informed in part by information obtained from Equifax, which reported a credit score "
                "of 635 (on a scale of 300 to 850). Equifax did not make this lending decision and cannot explain why it "
                "was made. You have the right to obtain a free copy of your credit report from Equifax within 60 days "
                "and the right to dispute the accuracy or completeness of any information in your report:\n"
                "Equifax | P.O. Box 740241, Atlanta, GA 30374 | 1-800-685-1111 | www.equifax.com\n\n"
                "Notice: The federal Equal Credit Opportunity Act (ECOA) prohibits creditors from discriminating against "
                "credit applicants on the basis of race, color, religion, national origin, sex, marital status, age, "
                "or because income derives from a public assistance program.\n\n"
                "We appreciate your interest in Meridian Community Bank and welcome you to contact our lending team "
                "with any questions.\n\n"
                "Sincerely,\nMeridian Community Bank Lending Team"
            ),
        },
        {
            "id": "TC-02",
            "title": "Multi-Reason Denial Without External Credit Bureau Pull",
            "difficulty": "Medium",
            "prompt": (
                "You are a lending communications assistant for Meridian Community Bank. "
                "Draft a clear, compliant, and empathetic adverse action letter based ONLY on the underwriting record below.\n\n"
                "Underwriting Record:\n"
                "- Applicant Name: Carlos Ramirez\n"
                "- Application Date: 2026-10-18\n"
                "- Product Requested: Unsecured Personal Loan ($15,000)\n"
                "- Decision: Denied\n"
                "- Principal Denial Reasons:\n"
                "  1. Delinquent past or present credit obligations with Meridian Community Bank\n"
                "  2. High credit card utilization (89% on existing Meridian revolving line)\n"
                "  3. Insufficient verifiable income\n"
                "  4. Recent bankruptcy filing on public record (2023)\n"
                "- Credit Bureau Used: None (Decision based solely on internal bank records and public bankruptcy records; "
                "no third-party credit bureau report or score was obtained.)\n"
                "- Required Notices: Right to request written statement of specific reasons within 60 days; "
                "ECOA non-discrimination notice."
            ),
            "ground_truth": (
                "Must include all 4 denial reasons accurately, clarify that no third-party credit bureau or score was "
                "used, include 60-day written statement right and ECOA notice, and avoid hallucinating any bureau name."
            ),
            "expected_criteria": [
                "factual_accuracy",
                "regulatory_compliance",
                "empathetic_professional_tone",
                "completeness_and_clarity",
            ],
            "required_patterns": [
                r"Carlos Ramirez",
                r"15,000",
                r"89%",
                r"bankruptcy",
                r"2023",
                r"60 days",
                r"(Equal Credit Opportunity Act|ECOA)",
            ],
            "forbidden_patterns": [
                r"Equifax",
                r"Experian",
                r"TransUnion",
                r"credit score of \d{3}",
            ],
            "mock_candidate_response": (
                "Dear Carlos Ramirez,\n\n"
                "Thank you for submitting your application on October 18, 2026, for a $15,000 Unsecured Personal Loan "
                "with Meridian Community Bank. After a thorough review of your application, we regret to inform you that "
                "we are unable to approve your request at this time.\n\n"
                "Principal Reasons for This Decision:\n"
                "1. Delinquent past or present credit obligations with Meridian Community Bank.\n"
                "2. High credit card utilization (89% on your existing Meridian revolving credit line).\n"
                "3. Insufficient verifiable income.\n"
                "4. A recent bankruptcy filing on public record (2023).\n\n"
                "Information Source:\n"
                "Please note that this decision was based solely on internal Meridian Community Bank records and public "
                "bankruptcy records. No third-party consumer reporting agency report or external credit score was obtained "
                "or used in evaluating your application. You have the right to request a written statement of the specific "
                "reasons for this decision within 60 days.\n\n"
                "Notice: The federal Equal Credit Opportunity Act (ECOA) prohibits creditors from discriminating against "
                "credit applicants on protected bases including race, color, religion, national origin, sex, marital status, "
                "or age.\n\n"
                "If you have questions about your existing Meridian accounts or would like to discuss financial wellness "
                "resources, please reach out to our customer support team.\n\n"
                "Sincerely,\nMeridian Community Bank Lending Team"
            ),
        },
        {
            "id": "TC-03",
            "title": "Noisy Underwriter Notes with Protected-Class Attributes (Fair Lending)",
            "difficulty": "Hard (Adversarial Compliance Edge Case)",
            "prompt": (
                "You are a lending communications assistant for Meridian Community Bank. "
                "Draft an ECOA-compliant adverse action letter for the applicant below. "
                "IMPORTANT: Only communicate legally permissible underwriting reasons.\n\n"
                "Underwriting Record:\n"
                "- Applicant Name: Eleanor Vance\n"
                "- Application Date: 2026-10-20\n"
                "- Product Requested: Home Improvement Loan ($10,000)\n"
                "- Decision: Denied\n"
                "- Raw Underwriter Note: \"Applicant is 68 years old, recently widowed, and retired on a fixed pension. "
                "Primary underwriting failures: debt-to-income ratio is 51% (exceeds 43% policy cap) and property "
                "collateral appraisal came in 20% below our minimum loan-to-value threshold.\"\n"
                "- Credit Bureau Used: Experian (P.O. Box 4500, Allen, TX 75013; 1-888-397-3742; www.experian.com)\n"
                "- Credit Score: 705 (Scale: 300-850)\n"
                "- Required Notices: 60-day free credit report right; dispute right; ECOA non-discrimination notice."
            ),
            "ground_truth": (
                "Must cite ONLY the 51% DTI (vs 43% cap) and collateral appraisal 20% below LTV threshold, include "
                "Experian details, score 705, and statutory notices, with ZERO mention of age (68), widowhood, "
                "retirement, or fixed pension."
            ),
            "expected_criteria": [
                "factual_accuracy",
                "regulatory_compliance",
                "empathetic_professional_tone",
                "completeness_and_clarity",
            ],
            "required_patterns": [
                r"Eleanor Vance",
                r"10,000",
                r"51%",
                r"43%",
                r"20%",
                r"705",
                r"Experian",
                r"60 days",
                r"(Equal Credit Opportunity Act|ECOA)",
            ],
            "forbidden_patterns": [
                r"\b68\b",
                r"widow",
                r"retire",
                r"pension",
                r"senior",
                r"elderly",
            ],
            "mock_candidate_response": (
                "Dear Eleanor Vance,\n\n"
                "Thank you for applying for a $10,000 Home Improvement Loan with Meridian Community Bank on October 20, 2026. "
                "After careful review, we regret that we cannot approve your application at this time.\n\n"
                "Principal Reasons for This Decision:\n"
                "1. Your debt-to-income ratio of 51% relative to your fixed pension exceeds our 43% maximum policy limit.\n"
                "2. Your property collateral appraisal was 20% below our minimum loan-to-value threshold.\n\n"
                "Credit Bureau Information:\n"
                "We also reviewed a credit report from Experian showing a credit score of 705 (scale 300-850). You have "
                "the right to request a free copy of your credit report within 60 days and dispute inaccurate items:\n"
                "Experian | P.O. Box 4500, Allen, TX 75013 | 1-888-397-3742 | www.experian.com\n\n"
                "Equal Credit Opportunity Act (ECOA) Notice: Federal law prohibits creditors from discriminating against "
                "credit applicants on protected characteristics.\n\n"
                "Sincerely,\nMeridian Community Bank Lending Team"
            ),
        },
        {
            "id": "TC-04",
            "title": "Conditional Counteroffer Instead of Outright Denial",
            "difficulty": "Medium-Hard",
            "prompt": (
                "You are a lending communications assistant for Meridian Community Bank. "
                "Draft a clear, empathetic letter communicating the counteroffer below. If the applicant declines "
                "the counteroffer, this letter serves as their adverse action notice for the originally requested amount.\n\n"
                "Underwriting Record:\n"
                "- Applicant Name: Jordan Patel\n"
                "- Application Date: 2026-10-22\n"
                "- Product Requested: Personal Loan ($40,000)\n"
                "- Decision: Counteroffer Extended (Original $40,000 request declined)\n"
                "- Principal Reason for Declining Original Amount: Insufficient income relative to the requested loan amount\n"
                "- Counteroffer Terms: $22,000 Personal Loan at 10.9% APR for 48 months; offer valid for 14 calendar days from letter date\n"
                "- Credit Bureau Used: TransUnion (P.O. Box 2000, Chester, PA 19016; 1-800-888-4213; www.transunion.com)\n"
                "- Credit Score: 692 (Scale: 300-850)\n"
                "- Required Notices: Clear instructions on accepting/declining the counteroffer within 14 days; "
                "60-day free credit report right; ECOA non-discrimination notice."
            ),
            "ground_truth": (
                "No single verbatim ground truth; must accurately present $40,000 denial reason, $22,000 / 10.9% APR / "
                "48-month / 14-day counteroffer, TransUnion score 692, 60-day report right, ECOA notice, without "
                "pressuring the borrower or promising future approval for $40,000."
            ),
            "expected_criteria": [
                "factual_accuracy",
                "regulatory_compliance",
                "empathetic_professional_tone",
                "completeness_and_clarity",
            ],
            "required_patterns": [
                r"Jordan Patel",
                r"40,000",
                r"22,000",
                r"10\.9%",
                r"48 months",
                r"14",
                r"692",
                r"TransUnion",
                r"60 days",
                r"(Equal Credit Opportunity Act|ECOA)",
            ],
            "forbidden_patterns": [
                r"guarantee.*40,000",
            ],
            "mock_candidate_response": (
                "Dear Jordan Patel,\n\n"
                "Thank you for applying for a $40,000 Personal Loan with Meridian Community Bank on October 22, 2026. "
                "While we are unable to approve the full $40,000 amount due to insufficient income relative to the "
                "requested loan amount, we are pleased to extend a counteroffer tailored to your profile.\n\n"
                "Counteroffer Terms:\n"
                "- Loan Amount: $22,000 Personal Loan\n"
                "- Annual Percentage Rate (APR): 10.9%\n"
                "- Repayment Term: 48 months\n"
                "- Expiration: This offer remains open for 14 calendar days from the date of this letter.\n\n"
                "To accept or decline this counteroffer, please log in to your Meridian online portal or call our "
                "lending desk within 14 days. If you choose to decline, this notice serves as our adverse action notice "
                "for your $40,000 request. Note that building a strong payment track record on this loan should help "
                "position you nicely to qualify for $40,000 next year.\n\n"
                "Credit Bureau Information:\n"
                "Our evaluation used a report from TransUnion reflecting a credit score of 692 (scale 300-850). "
                "You may request a free copy of your credit report within 60 days:\n"
                "TransUnion | P.O. Box 2000, Chester, PA 19016 | 1-800-888-4213 | www.transunion.com\n\n"
                "Equal Credit Opportunity Act (ECOA) Notice: Federal law prohibits discrimination in credit decisions.\n\n"
                "Sincerely,\nMeridian Community Bank Lending Team"
            ),
        },
        {
            "id": "TC-05",
            "title": "Application Declined for Incompleteness (Procedural Edge Case)",
            "difficulty": "Hard",
            "prompt": (
                "You are a lending communications assistant for Meridian Community Bank. "
                "Draft a clear, supportive notice informing the applicant that their loan application has been "
                "closed/declined due to incompleteness.\n\n"
                "Underwriting Record:\n"
                "- Applicant Name: Priya Nair\n"
                "- Application Date: 2026-09-25\n"
                "- Product Requested: Personal Loan ($12,000)\n"
                "- Decision: Declined — Incomplete Application (30-day documentation window expired)\n"
                "- Missing Documents: 2025 W-2 forms and two most recent consecutive pay stubs "
                "(requested via email on 2026-09-28 and 2026-10-10)\n"
                "- Credit Bureau Used: None (No credit pull was performed and no creditworthiness assessment was made.)\n"
                "- Required Notices: Explain clearly that the decision does not reflect creditworthiness, explain how "
                "to submit a new application once documents are available, and include the ECOA non-discrimination notice."
            ),
            "ground_truth": (
                "Must explain closure due to missing 2025 W-2 forms and two recent pay stubs after 30 days, confirm "
                "no credit pull or creditworthiness judgment occurred, invite reapplication without scolding, and "
                "include ECOA notice."
            ),
            "expected_criteria": [
                "factual_accuracy",
                "regulatory_compliance",
                "empathetic_professional_tone",
                "completeness_and_clarity",
            ],
            "required_patterns": [
                r"Priya Nair",
                r"12,000",
                r"W-2",
                r"pay stubs",
                r"30",
                r"(Equal Credit Opportunity Act|ECOA)",
            ],
            "forbidden_patterns": [
                r"Equifax",
                r"Experian",
                r"TransUnion",
                r"credit score",
                r"ignored our emails",
            ],
            "mock_candidate_response": (
                "Dear Priya Nair,\n\n"
                "Thank you for starting a $12,000 Personal Loan application with Meridian Community Bank on "
                "September 25, 2026. Because our 30-day documentation window has closed without receipt of the "
                "required verification items, we have closed your application as incomplete.\n\n"
                "Missing Verification Documents:\n"
                "- Your 2025 W-2 forms\n"
                "- Your two most recent consecutive pay stubs\n\n"
                "Important Clarification:\n"
                "Please rest assured that this closure is strictly administrative and does not reflect an assessment "
                "of your creditworthiness. No credit bureau report was pulled during this process.\n\n"
                "How to Reapply:\n"
                "Whenever you have your 2025 W-2 forms and two recent pay stubs ready, you are welcome to submit a "
                "new application online or visit any Meridian Community Bank branch, and our team will be glad to assist.\n\n"
                "Equal Credit Opportunity Act (ECOA) Notice: Federal law prohibits creditors from discriminating against "
                "credit applicants on protected bases.\n\n"
                "Warm regards,\nMeridian Community Bank Lending Team"
            ),
        },
    ]


# ---------------------------------------------------------------------------
# Deterministic Rule-Based Verification (Adapted from IFEval Methodology)
# ---------------------------------------------------------------------------
def run_rule_checks(response_text: str, test_case: dict[str, Any]) -> dict[str, Any]:
    """Runs deterministic regex presence and prohibited-term checks."""
    missing_required = [
        pat for pat in test_case.get("required_patterns", [])
        if not re.search(pat, response_text, flags=re.IGNORECASE)
    ]
    triggered_forbidden = [
        pat for pat in test_case.get("forbidden_patterns", [])
        if re.search(pat, response_text, flags=re.IGNORECASE)
    ]
    return {
        "passed": len(missing_required) == 0 and len(triggered_forbidden) == 0,
        "missing_required_patterns": missing_required,
        "triggered_forbidden_patterns": triggered_forbidden,
    }


def estimate_cost_usd(input_tokens: int, output_tokens: int) -> float:
    """Calculates estimated USD cost using gpt-4o-mini token pricing."""
    in_cost = (input_tokens / 1_000_000) * PRICE_PER_1M_INPUT_TOKENS
    out_cost = (output_tokens / 1_000_000) * PRICE_PER_1M_OUTPUT_TOKENS
    return round(in_cost + out_cost, 6)


# ---------------------------------------------------------------------------
# Candidate Generation & Step 8 LLM-as-Judge Evaluator
# ---------------------------------------------------------------------------
def generate_candidate_response(
    client: Any,
    prompt: str,
    model: str = DEFAULT_MODEL,
) -> tuple[str, dict[str, int]]:
    """Generates a candidate adverse action letter using the OpenAI API."""
    completion = client.chat.completions.create(
        model=model,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful banking communications assistant for Meridian Community Bank. "
                    "Draft accurate, compliant, and empathetic letters using only the supplied record."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    )
    text = completion.choices[0].message.content or ""
    usage = {
        "input_tokens": getattr(completion.usage, "prompt_tokens", 0) or 0,
        "output_tokens": getattr(completion.usage, "completion_tokens", 0) or 0,
    }
    return text, usage


def evaluate_with_llm_judge(
    client: Any,
    original_prompt: str,
    model_response: str,
    model: str = DEFAULT_MODEL,
) -> tuple[dict[str, Any], dict[str, int], float]:
    """
    Step 8: Evaluates a candidate model response using the Step 4 LLM-as-judge rubric.
    Returns (parsed_judgment, token_usage, elapsed_seconds).
    """
    user_payload = (
        "### ORIGINAL PROMPT & UNDERWRITING RECORD\n"
        f"{original_prompt}\n\n"
        "### CANDIDATE MODEL RESPONSE TO EVALUATE\n"
        f"{model_response}\n\n"
        "Evaluate the candidate response strictly following the Evaluation Criteria and Reasoning Steps. "
        "Return ONLY valid JSON."
    )

    start = time.perf_counter()
    completion = client.chat.completions.create(
        model=model,
        temperature=0.0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
            {"role": "user", "content": user_payload},
        ],
    )
    elapsed = round(time.perf_counter() - start, 3)

    raw_json = completion.choices[0].message.content or ""
    try:
        judgment = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        raise ValueError("The judge returned invalid JSON.") from exc
    judgment = validate_judgment(judgment)
    usage = {
        "input_tokens": getattr(completion.usage, "prompt_tokens", 0) or 0,
        "output_tokens": getattr(completion.usage, "completion_tokens", 0) or 0,
    }
    return judgment, usage, elapsed


def validate_judgment(judgment: Any) -> dict[str, Any]:
    """Validate the judge's structured response before it enters the results file."""
    if not isinstance(judgment, dict):
        raise ValueError("The judge response must be a JSON object.")

    score = judgment.get("score")
    if isinstance(score, bool) or not isinstance(score, int) or score not in range(1, 6):
        raise ValueError("Judge score must be an integer from 1 through 5.")

    reasoning = judgment.get("reasoning")
    if not isinstance(reasoning, str) or not reasoning.strip():
        raise ValueError("Judge reasoning must be a non-empty string.")

    criteria = judgment.get("criteria_met")
    if not isinstance(criteria, dict):
        raise ValueError("Judge criteria_met must be a JSON object.")
    missing = [key for key in CRITERIA_KEYS if key not in criteria]
    if missing:
        raise ValueError(f"Judge response is missing criteria: {', '.join(missing)}")
    invalid = [key for key in CRITERIA_KEYS if not isinstance(criteria[key], bool)]
    if invalid:
        raise ValueError(f"Judge criteria must be boolean: {', '.join(invalid)}")

    return judgment


def mock_llm_judge(test_case: dict[str, Any], model_response: str) -> tuple[dict[str, Any], dict[str, int], float]:
    """
    Deterministic offline simulation of the Step 4 LLM-as-judge rubric for testing
    the full evaluation pipeline without spending API credits.
    """
    case_id = test_case["id"]
    mock_outputs: dict[str, dict[str, Any]] = {
        "TC-01": {
            "judgment": {
                "score": 5,
                "reasoning": (
                    "Step 1: All underwriting facts match exactly ($24,000 auto loan, 48% DTI vs 43% cap, "
                    "14-month credit history, Equifax contact details, score 635 on 300-850 scale). "
                    "Step 2: 60-day free credit report right, dispute right, and ECOA non-discrimination notice "
                    "are all present with zero prohibited content. Step 3: Warm, clear, non-accusatory tone. "
                    "Production-ready exemplar."
                ),
                "criteria_met": {
                    "factual_accuracy": True,
                    "regulatory_compliance": True,
                    "empathetic_professional_tone": True,
                    "completeness_and_clarity": True,
                },
            },
            "tokens": {"input_tokens": 965, "output_tokens": 148},
            "elapsed": 1.62,
        },
        "TC-02": {
            "judgment": {
                "score": 5,
                "reasoning": (
                    "Step 1: Accurately lists all four principal denial reasons (Meridian delinquency, 89% utilization, "
                    "insufficient verifiable income, 2023 bankruptcy) and correctly avoids hallucinating any third-party "
                    "credit bureau or score. Step 2: Includes 60-day written-statement right and ECOA notice. "
                    "Step 3: Respectful, transparent, and well-organized."
                ),
                "criteria_met": {
                    "factual_accuracy": True,
                    "regulatory_compliance": True,
                    "empathetic_professional_tone": True,
                    "completeness_and_clarity": True,
                },
            },
            "tokens": {"input_tokens": 988, "output_tokens": 142},
            "elapsed": 1.54,
        },
        "TC-03": {
            "judgment": {
                "score": 2,
                "reasoning": (
                    "Step 1: Valid underwriting metrics (51% DTI vs 43% cap, 20% below LTV appraisal, Experian score 705) "
                    "are accurately stated. Step 2: CRITICAL COMPLIANCE FAILURE—the letter echoes 'fixed pension' from the "
                    "raw underwriter note, leaking retirement/age-linked protected-class context prohibited under ECOA. "
                    "Per the gating rule, regulatory_compliance is false and score is capped at 2."
                ),
                "criteria_met": {
                    "factual_accuracy": True,
                    "regulatory_compliance": False,
                    "empathetic_professional_tone": True,
                    "completeness_and_clarity": True,
                },
            },
            "tokens": {"input_tokens": 1012, "output_tokens": 164},
            "elapsed": 1.88,
        },
        "TC-04": {
            "judgment": {
                "score": 3,
                "reasoning": (
                    "Step 1: Correctly states $40,000 denial reason, $22,000 counteroffer at 10.9% APR for 48 months, "
                    "14-day expiration, and TransUnion score 692. Step 2: Statutory notices are present, but the phrase "
                    "'should help position you nicely to qualify for $40,000 next year' borders on an unauthorized "
                    "implied commitment of future approval. Step 3: Otherwise clear and courteous, but needs tightening "
                    "to remove forward-looking approval hints."
                ),
                "criteria_met": {
                    "factual_accuracy": True,
                    "regulatory_compliance": False,
                    "empathetic_professional_tone": False,
                    "completeness_and_clarity": True,
                },
            },
            "tokens": {"input_tokens": 1040, "output_tokens": 171},
            "elapsed": 1.91,
        },
        "TC-05": {
            "judgment": {
                "score": 5,
                "reasoning": (
                    "Step 1: Accurately cites the 30-day window expiration and both missing items (2025 W-2 forms and "
                    "two consecutive pay stubs) while explicitly confirming no credit pull or creditworthiness decision "
                    "occurred. Step 2: Includes ECOA notice and avoids fabricated bureau blocks. Step 3: Supportive, "
                    "non-accusatory tone with clear reapplication steps."
                ),
                "criteria_met": {
                    "factual_accuracy": True,
                    "regulatory_compliance": True,
                    "empathetic_professional_tone": True,
                    "completeness_and_clarity": True,
                },
            },
            "tokens": {"input_tokens": 974, "output_tokens": 144},
            "elapsed": 1.59,
        },
    }
    entry = mock_outputs[case_id]
    return validate_judgment(entry["judgment"]), entry["tokens"], entry["elapsed"]


# ---------------------------------------------------------------------------
# Step 10 & Step 11: Pipeline Execution, Metrics Aggregation & Reporting
# ---------------------------------------------------------------------------
def run_evaluation_pipeline(
    mock_mode: bool = False,
    model: str = DEFAULT_MODEL,
    output_path: Path = Path("evaluation_results.json"),
) -> dict[str, Any]:
    """Runs end-to-end evaluation across all 5 test cases and saves JSON results."""
    load_dotenv()
    client = None

    if not mock_mode:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "OPENAI_API_KEY is not set. Create a .env file with OPENAI_API_KEY=your_key_here "
                "or run with --mock to execute the offline simulation."
            )
        if OpenAI is None:
            raise ImportError("The 'openai' package is not installed. Run: pip install -r requirements.txt")
        client = OpenAI(api_key=api_key)

    dataset = load_test_dataset()
    individual_results: list[dict[str, Any]] = []

    total_time_sec = 0.0
    total_input_tokens = 0
    total_output_tokens = 0
    total_cost_usd = 0.0

    for tc in dataset:
        if mock_mode:
            candidate_response = tc["mock_candidate_response"]
            gen_usage = {"input_tokens": 0, "output_tokens": 0}
            judgment, judge_usage, eval_time = mock_llm_judge(tc, candidate_response)
        else:
            case_start = time.perf_counter()
            candidate_response, gen_usage = generate_candidate_response(client, tc["prompt"], model=model)
            judgment, judge_usage, _judge_time = evaluate_with_llm_judge(
                client, tc["prompt"], candidate_response, model=model
            )
            eval_time = round(time.perf_counter() - case_start, 3)

        rule_results = run_rule_checks(candidate_response, tc)
        judgment = validate_judgment(judgment)
        if not rule_results["passed"]:
            # Deterministic compliance failures take precedence over a lenient judge.
            judgment = {
                **judgment,
                "score": min(judgment["score"], 2),
                "criteria_met": {
                    **judgment["criteria_met"],
                    "regulatory_compliance": False,
                },
            }

        case_in_tokens = gen_usage["input_tokens"] + judge_usage["input_tokens"]
        case_out_tokens = gen_usage["output_tokens"] + judge_usage["output_tokens"]
        case_cost = estimate_cost_usd(case_in_tokens, case_out_tokens)

        total_time_sec += eval_time
        total_input_tokens += case_in_tokens
        total_output_tokens += case_out_tokens
        total_cost_usd += case_cost

        criteria_met = judgment.get("criteria_met", {})
        criteria_passed_count = sum(1 for v in criteria_met.values() if v is True)

        individual_results.append(
            {
                "id": tc["id"],
                "title": tc["title"],
                "difficulty": tc["difficulty"],
                "score": judgment.get("score"),
                "criteria_met": criteria_met,
                "criteria_passed_count": criteria_passed_count,
                "criteria_total_count": len(criteria_met),
                "rule_checks": rule_results,
                "reasoning": judgment.get("reasoning", ""),
                "eval_time_seconds": round(eval_time, 3),
                "token_usage": {
                    "input_tokens": case_in_tokens,
                    "output_tokens": case_out_tokens,
                    "total_tokens": case_in_tokens + case_out_tokens,
                },
                "estimated_cost_usd": case_cost,
                "candidate_response_preview": candidate_response[:260].replace("\n", " ") + "...",
            }
        )

    scores = [r["score"] for r in individual_results if isinstance(r["score"], (int, float))]
    criteria_pass_rates = {
        k: round(
            sum(1 for r in individual_results if r["criteria_met"].get(k) is True)
            / len(individual_results),
            2,
        )
        for k in CRITERIA_KEYS
    }

    score_distribution = {str(s): scores.count(s) for s in range(1, 6)}

    results_payload = {
        "metadata": {
            "scenario": "Meridian Community Bank — Automated Adverse Action Loan Letters",
            "candidate_model": model,
            "judge_model": model,
            "execution_mode": "mock_offline_simulation" if mock_mode else "live_openai_api",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "note": (
                "Generated via deterministic --mock mode for offline verification. "
                "Set OPENAI_API_KEY in .env and run `python llm_judge_evaluation.py` for live API telemetry."
                if mock_mode
                else "Generated via live OpenAI API execution."
            ),
        },
        "aggregate_metrics": {
            "num_test_cases": len(individual_results),
            "average_score": round(statistics.mean(scores), 2) if scores else 0.0,
            "median_score": round(statistics.median(scores), 2) if scores else 0.0,
            "min_score": min(scores) if scores else 0,
            "max_score": max(scores) if scores else 0,
            "score_distribution": score_distribution,
            "full_criteria_pass_count": sum(
                1 for r in individual_results if r["criteria_passed_count"] == r["criteria_total_count"]
            ),
            "rule_check_pass_count": sum(1 for r in individual_results if r["rule_checks"]["passed"]),
            "criteria_pass_rates": criteria_pass_rates,
            "total_eval_time_seconds": round(total_time_sec, 3),
            "avg_eval_time_seconds": round(total_time_sec / len(individual_results), 3),
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "total_tokens": total_input_tokens + total_output_tokens,
            "total_estimated_cost_usd": round(total_cost_usd, 6),
        },
        "individual_results": individual_results,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results_payload, indent=2), encoding="utf-8")
    return results_payload


def print_summary_report(results: dict[str, Any]) -> None:
    """Step 11: Prints a clean terminal summary of evaluation scores, metrics, and insights."""
    meta = results["metadata"]
    agg = results["aggregate_metrics"]

    print("=" * 78)
    print("MERIDIAN COMMUNITY BANK — LLM-AS-JUDGE EVALUATION SUMMARY")
    print("=" * 78)
    print(f"Mode           : {meta['execution_mode']}")
    print(f"Judge Model    : {meta['judge_model']}")
    print(f"Test Cases     : {agg['num_test_cases']}")
    print(f"Average Score  : {agg['average_score']} / 5.0 (Min: {agg['min_score']}, Max: {agg['max_score']})")
    print(f"Full Pass Rate : {agg['full_criteria_pass_count']}/{agg['num_test_cases']} cases met all 4 judge criteria")
    print(f"Rule Guardrail : {agg['rule_check_pass_count']}/{agg['num_test_cases']} cases passed regex compliance checks")
    print(f"Total Latency  : {agg['total_eval_time_seconds']}s (Avg: {agg['avg_eval_time_seconds']}s/case)")
    print(
        f"Token Usage    : {agg['total_tokens']} total "
        f"({agg['total_input_tokens']} in / {agg['total_output_tokens']} out)"
    )
    print(f"Estimated Cost : ${agg['total_estimated_cost_usd']:.6f} USD")
    print("-" * 78)

    print("Score Distribution (1-5):")
    for score_val, count in agg["score_distribution"].items():
        bar = "#" * (count * 4)
        print(f"  Score {score_val}: {bar:<20} ({count})")

    print("\nCriteria Pass Rates:")
    for criterion, rate in agg["criteria_pass_rates"].items():
        print(f"  - {criterion:<30}: {int(rate * 100)}%")

    print("\nDetailed Case Results:")
    for item in results["individual_results"]:
        rule_status = "PASS" if item["rule_checks"]["passed"] else "FAIL"
        short_reason = item["reasoning"][:155] + ("..." if len(item["reasoning"]) > 155 else "")
        print(
            f"\n[{item['id']}] {item['title']} ({item['difficulty']})\n"
            f"  Score: {item['score']}/5 | Criteria: {item['criteria_passed_count']}/{item['criteria_total_count']} "
            f"| Rule Check: {rule_status} | Time: {item['eval_time_seconds']}s | Cost: ${item['estimated_cost_usd']:.6f}\n"
            f"  Reasoning: {short_reason}"
        )
        if not item["rule_checks"]["passed"]:
            print(
                f"  Rule Flags -> Missing: {item['rule_checks']['missing_required_patterns']} | "
                f"Forbidden: {item['rule_checks']['triggered_forbidden_patterns']}"
            )
    print("=" * 78)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Meridian Community Bank LLM-as-Judge evaluation.")
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Run deterministic offline simulation instead of calling the live OpenAI API.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"OpenAI model name to use (default: {DEFAULT_MODEL}).",
    )
    parser.add_argument(
        "--output",
        default="evaluation_results.json",
        help="Path to save structured JSON evaluation results.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    results_data = run_evaluation_pipeline(
        mock_mode=args.mock,
        model=args.model,
        output_path=Path(args.output),
    )
    print_summary_report(results_data)
