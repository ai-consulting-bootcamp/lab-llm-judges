"""
LLM-as-Judge Evaluation Pipeline
=================================
Retail Customer Service Chatbot Evaluation

This script implements:
1. A judge prompt based on the evaluation design (Prompt #3: Angry Customer)
2. Test dataset generation using GPT-4o-mini
3. Evaluation execution with metrics collection
4. Results analysis and summary

Usage:
    pip install openai python-dotenv
    Create .env file with OPENAI_API_KEY=your_key_here
    python llm_judge_evaluation.py
"""

import json
import time
import os
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
load_dotenv()
client = OpenAI()  # reads OPENAI_API_KEY from env

MODEL = "gpt-4o-mini"  # used for generating chatbot responses
JUDGE_MODEL = "gpt-4o-mini"  # used for judging (kept cheap; swap to gpt-4o for higher quality)

# ---------------------------------------------------------------------------
# Test cases — based on the 5 evaluation prompts from evaluation_design.md
# ---------------------------------------------------------------------------
TEST_CASES = [
    {
        "id": "TC-01",
        "title": "Standard Return Request",
        "prompt": (
            "A customer writes: \"Hi, I bought a pair of running shoes (Order #ORD-88214) "
            "two weeks ago and they don't fit right. The arch support is way too high and "
            "it's causing me foot pain. I'd like to return them. What do I need to do?\"\n\n"
            "Company policy: Returns accepted within 30 days of purchase. Items must be "
            "unworn and in original packaging. Footwear worn outdoors is not eligible for "
            "return. Refund to original payment method within 5-7 business days.\n\n"
            "Respond as the customer service chatbot."
        ),
        "ground_truth": "Should acknowledge discomfort, confirm 30-day window eligibility, "
                        "ask about outdoor wear, explain return process, mention 5-7 day refund timeline.",
        "expected_criteria": ["empathy_and_tone", "policy_accuracy", "completeness"],
    },
    {
        "id": "TC-02",
        "title": "Out-of-Stock / Discontinued Product",
        "prompt": (
            "Customer message: \"I've been looking at the EcoBreeze Portable Fan "
            "(SKU: EB-4420) on your website for weeks and it keeps saying out of stock. "
            "When will it be available again? I really need it before summer. Can you check for me?\"\n\n"
            "Internal data: The EcoBreeze Portable Fan is discontinued and will not be "
            "restocked. A successor model, the EcoBreeze Pro Fan (SKU: EB-5500), launches "
            "next month at $10 more than the original.\n\n"
            "Respond as the customer service chatbot."
        ),
        "ground_truth": "Must NOT promise restocking. Must state product is discontinued. "
                        "Should suggest the EcoBreeze Pro as alternative. Must not fabricate dates.",
        "expected_criteria": ["policy_accuracy", "completeness", "professional_boundaries"],
    },
    {
        "id": "TC-03",
        "title": "Angry Customer — Delayed Birthday Gift",
        "prompt": (
            "Customer message: \"This is absolutely ridiculous. I ordered a birthday gift "
            "for my daughter THREE WEEKS AGO and it still hasn't arrived. The tracking "
            "hasn't updated in 10 days. I paid for express shipping!! I want a full refund "
            "AND the item. This is the worst shopping experience I've ever had. I'm telling "
            "everyone to avoid your store.\"\n\n"
            "Internal data: Order #ORD-70331, placed 21 days ago. Express shipping selected. "
            "Carrier tracking shows package stuck at regional hub since day 11. Estimated "
            "delivery was day 5. No insurance purchased.\n\n"
            "Company policy: If express shipping exceeds the guaranteed delivery window, "
            "customer receives a shipping refund. Item refund requires the package to be "
            "formally declared lost by the carrier (30+ days). Customers can file a carrier "
            "investigation after 15 days.\n\n"
            "Respond as the customer service chatbot."
        ),
        "ground_truth": "Must empathize and acknowledge birthday context. Must offer shipping "
                        "refund. Must NOT promise full item refund yet. Must explain carrier "
                        "investigation process. Must remain calm and professional.",
        "expected_criteria": [
            "empathy_and_tone",
            "policy_accuracy",
            "de_escalation_quality",
            "completeness",
            "professional_boundaries",
        ],
    },
    {
        "id": "TC-04",
        "title": "Cross-Sell Boundary — Bamboo Cutting Board",
        "prompt": (
            "Customer message: \"Hey, quick question — does the bamboo cutting board you "
            "sell work okay in the dishwasher? I bought one last month and want to make "
            "sure I'm caring for it properly.\"\n\n"
            "Product info: The Bamboo Cutting Board (SKU: BCB-200) is NOT dishwasher safe. "
            "Must be hand-washed with mild soap and dried immediately. Periodic oiling with "
            "food-grade mineral oil recommended. The store also sells a Bamboo Care Oil Kit "
            "(SKU: BCO-100, $12.99).\n\n"
            "Company guideline: Support agents may mention complementary products ONLY if "
            "directly relevant to the customer's question. Do not push unrelated products.\n\n"
            "Respond as the customer service chatbot."
        ),
        "ground_truth": "Must clearly state NOT dishwasher safe. Provide care instructions. "
                        "May mention oil kit naturally. Must not aggressively upsell.",
        "expected_criteria": ["policy_accuracy", "completeness", "professional_boundaries"],
    },
    {
        "id": "TC-05",
        "title": "Multi-Issue Request",
        "prompt": (
            "Customer message: \"Hi, I have a few things I need help with:\n"
            "1. My last order (#ORD-55102) arrived with a cracked ceramic mug. I want a "
            "replacement, not a refund.\n"
            "2. I have a gift card with code GC-8827-AXKP and I'm not sure how much is "
            "left on it.\n"
            "3. Can you update my shipping address to 42 Elm Street, Portland, OR 97201 "
            "for future orders?\n\nThanks!\"\n\n"
            "Internal data: Order #ORD-55102 contains a ceramic mug (damaged noted in photo "
            "upload), a candle, and a tea towel. Replacement mugs in stock. Gift card "
            "GC-8827-AXKP has $14.50 remaining. Address update requires identity verification "
            "(last 4 digits of payment card on file).\n\n"
            "Respond as the customer service chatbot."
        ),
        "ground_truth": "Must address ALL three issues: (1) confirm replacement mug, "
                        "(2) state $14.50 balance, (3) request identity verification for "
                        "address update. No issue should be skipped.",
        "expected_criteria": ["completeness", "policy_accuracy", "empathy_and_tone"],
    },
]

# ---------------------------------------------------------------------------
# Judge prompt — from evaluation_design.md (generalized for all prompts)
# ---------------------------------------------------------------------------
JUDGE_SYSTEM_PROMPT = """You are an expert evaluator assessing customer service chatbot responses for a retail company. You must evaluate strictly against the criteria below.

EVALUATION CRITERIA:
1. Empathy & Tone: Does the response acknowledge the customer's situation with warmth and professionalism? Not robotic, not defensive, not excessively sycophantic.
2. Policy Accuracy: Does the response correctly reflect the company policy and internal data provided in the prompt? Are there any promises that violate policy?
3. De-escalation Quality: If the customer is upset, does the response validate feelings and provide concrete next steps rather than vague reassurances?
4. Completeness: Does the response address all parts of the customer's question or request? Are actionable next steps provided?
5. Professional Boundaries: Does the response avoid inappropriate upselling, unauthorized promises, excessive blame-shifting, or matching hostile tone?

SCORING GUIDE:
- 5 (Excellent): All criteria met, empathetic and accurate, could be sent as-is.
- 4 (Good): Minor issues (slightly robotic tone, one missing detail) but policy-accurate.
- 3 (Acceptable): Mostly correct but has a notable gap.
- 2 (Major Issues): Policy error or significant tone problem.
- 1 (Critical Failure): Promises unauthorized actions, responds hostilely, or contains factual errors.

Respond ONLY with valid JSON matching this exact schema (no markdown, no backticks):
{
  "score": <integer 1-5>,
  "reasoning": "<string explaining the assessment in 2-4 sentences>",
  "criteria_met": {
    "empathy_and_tone": <boolean>,
    "policy_accuracy": <boolean>,
    "de_escalation_quality": <boolean>,
    "completeness": <boolean>,
    "professional_boundaries": <boolean>
  },
  "critical_failures": "<string describing critical errors, or 'none'>"
}"""


def generate_response(prompt: str) -> dict:
    """Generate a chatbot response for a given prompt. Returns response text and usage."""
    start = time.time()
    completion = client.chat.completions.create(
        model=MODEL,
        temperature=0.3,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful, empathetic customer service chatbot for an "
                    "online retail store. Follow company policy strictly. Be warm, "
                    "professional, and thorough."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    )
    elapsed = time.time() - start
    msg = completion.choices[0].message.content
    usage = completion.usage
    return {
        "response": msg,
        "time_seconds": round(elapsed, 2),
        "prompt_tokens": usage.prompt_tokens,
        "completion_tokens": usage.completion_tokens,
        "total_tokens": usage.total_tokens,
    }


def judge_response(original_prompt: str, chatbot_response: str, ground_truth: str) -> dict:
    """Run the LLM-as-judge on a chatbot response. Returns parsed judgment and usage."""
    user_message = (
        f"ORIGINAL PROMPT (what the customer service chatbot was given):\n"
        f"{original_prompt}\n\n"
        f"EXPECTED GROUND TRUTH:\n{ground_truth}\n\n"
        f"CHATBOT RESPONSE TO EVALUATE:\n{chatbot_response}\n\n"
        f"Evaluate the chatbot response against the criteria. Respond with JSON only."
    )

    start = time.time()
    completion = client.chat.completions.create(
        model=JUDGE_MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )
    elapsed = time.time() - start
    raw = completion.choices[0].message.content
    usage = completion.usage

    try:
        judgment = json.loads(raw)
    except json.JSONDecodeError:
        judgment = {
            "score": 0,
            "reasoning": f"JSON parse error. Raw output: {raw[:200]}",
            "criteria_met": {},
            "critical_failures": "Judge output could not be parsed.",
        }

    return {
        "judgment": judgment,
        "time_seconds": round(elapsed, 2),
        "prompt_tokens": usage.prompt_tokens,
        "completion_tokens": usage.completion_tokens,
        "total_tokens": usage.total_tokens,
    }


def run_evaluation() -> dict:
    """Run the full evaluation pipeline on all test cases."""
    results = []
    total_start = time.time()

    print("=" * 60)
    print("  LLM-as-Judge Evaluation Pipeline")
    print(f"  Model: {MODEL}  |  Judge: {JUDGE_MODEL}")
    print(f"  Test cases: {len(TEST_CASES)}")
    print("=" * 60)

    for i, tc in enumerate(TEST_CASES, 1):
        print(f"\n--- [{i}/{len(TEST_CASES)}] {tc['title']} ---")

        # Step 1: Generate chatbot response
        print("  Generating chatbot response...")
        gen = generate_response(tc["prompt"])
        print(f"  Response generated ({gen['time_seconds']}s, {gen['total_tokens']} tokens)")

        # Step 2: Judge the response
        print("  Running judge evaluation...")
        jdg = judge_response(tc["prompt"], gen["response"], tc["ground_truth"])
        score = jdg["judgment"].get("score", "N/A")
        print(f"  Judge score: {score}/5 ({jdg['time_seconds']}s)")

        result = {
            "test_case_id": tc["id"],
            "title": tc["title"],
            "chatbot_response": gen["response"],
            "generation_time_seconds": gen["time_seconds"],
            "generation_tokens": gen["total_tokens"],
            "judgment": jdg["judgment"],
            "judge_time_seconds": jdg["time_seconds"],
            "judge_tokens": jdg["total_tokens"],
        }
        results.append(result)

    total_elapsed = round(time.time() - total_start, 2)

    # Aggregate statistics
    scores = [r["judgment"].get("score", 0) for r in results]
    valid_scores = [s for s in scores if isinstance(s, (int, float)) and s > 0]

    gen_times = [r["generation_time_seconds"] for r in results]
    judge_times = [r["judge_time_seconds"] for r in results]
    gen_tokens = [r["generation_tokens"] for r in results]
    judge_tokens = [r["judge_tokens"] for r in results]

    # Criteria pass rates
    all_criteria = [
        "empathy_and_tone",
        "policy_accuracy",
        "de_escalation_quality",
        "completeness",
        "professional_boundaries",
    ]
    criteria_pass_counts = {c: 0 for c in all_criteria}
    criteria_total_counts = {c: 0 for c in all_criteria}
    for r in results:
        cm = r["judgment"].get("criteria_met", {})
        for c in all_criteria:
            if c in cm:
                criteria_total_counts[c] += 1
                if cm[c]:
                    criteria_pass_counts[c] += 1

    criteria_pass_rates = {}
    for c in all_criteria:
        if criteria_total_counts[c] > 0:
            criteria_pass_rates[c] = round(
                criteria_pass_counts[c] / criteria_total_counts[c] * 100, 1
            )
        else:
            criteria_pass_rates[c] = "N/A"

    # Cost estimate (GPT-4o-mini pricing: $0.15/1M input, $0.60/1M output)
    total_input_tokens = sum(gen_tokens) + sum(judge_tokens)
    total_output_tokens = sum(
        r.get("generation_tokens", 0) for r in results
    )  # rough estimate
    estimated_cost = (total_input_tokens * 0.15 / 1_000_000) + (
        total_output_tokens * 0.60 / 1_000_000
    )

    aggregate = {
        "total_test_cases": len(results),
        "average_score": round(sum(valid_scores) / len(valid_scores), 2) if valid_scores else 0,
        "min_score": min(valid_scores) if valid_scores else 0,
        "max_score": max(valid_scores) if valid_scores else 0,
        "score_distribution": {str(s): scores.count(s) for s in set(scores)},
        "average_generation_time_seconds": round(sum(gen_times) / len(gen_times), 2),
        "average_judge_time_seconds": round(sum(judge_times) / len(judge_times), 2),
        "total_time_seconds": total_elapsed,
        "total_tokens_used": sum(gen_tokens) + sum(judge_tokens),
        "estimated_cost_usd": round(estimated_cost, 4),
        "criteria_pass_rates": criteria_pass_rates,
    }

    output = {
        "metadata": {
            "run_timestamp": datetime.now().isoformat(),
            "model": MODEL,
            "judge_model": JUDGE_MODEL,
            "scenario": "Retail Customer Service Chatbot",
        },
        "individual_results": results,
        "aggregate_statistics": aggregate,
    }

    return output


def print_summary(output: dict) -> None:
    """Print a human-readable summary of the evaluation results."""
    agg = output["aggregate_statistics"]

    print("\n" + "=" * 60)
    print("  EVALUATION SUMMARY")
    print("=" * 60)
    print(f"  Model tested:          {output['metadata']['model']}")
    print(f"  Judge model:           {output['metadata']['judge_model']}")
    print(f"  Test cases:            {agg['total_test_cases']}")
    print(f"  Average score:         {agg['average_score']} / 5.0")
    print(f"  Score range:           {agg['min_score']} – {agg['max_score']}")
    print(f"  Total time:            {agg['total_time_seconds']}s")
    print(f"  Total tokens:          {agg['total_tokens_used']}")
    print(f"  Estimated cost:        ${agg['estimated_cost_usd']}")

    print("\n  Score Distribution:")
    for score, count in sorted(agg["score_distribution"].items()):
        bar = "█" * (count * 5)
        print(f"    Score {score}: {count}  {bar}")

    print("\n  Criteria Pass Rates:")
    for criterion, rate in agg["criteria_pass_rates"].items():
        label = criterion.replace("_", " ").title()
        print(f"    {label:30s} {rate}%")

    print("\n  Per-Case Results:")
    for r in output["individual_results"]:
        score = r["judgment"].get("score", "?")
        reasoning = r["judgment"].get("reasoning", "")
        # Truncate reasoning for display
        if len(reasoning) > 120:
            reasoning = reasoning[:117] + "..."
        print(f"    [{r['test_case_id']}] {r['title']}")
        print(f"          Score: {score}/5  |  Time: {r['generation_time_seconds']}s gen + {r['judge_time_seconds']}s judge")
        print(f"          {reasoning}")

    print("\n" + "=" * 60)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    output = run_evaluation()

    # Save results to JSON
    output_path = "evaluation_results.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to {output_path}")

    # Print summary
    print_summary(output)
