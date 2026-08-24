#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent
RESULTS_PATH = ROOT / "evaluation_results.json"
DEFAULT_MODEL = "gpt-4o-mini"
GPT_4O_MINI_INPUT_COST_PER_1M = 0.15
GPT_4O_MINI_OUTPUT_COST_PER_1M = 0.60


def load_env_file(path: Path = ROOT / ".env") -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


try:
    from dotenv import load_dotenv  # type: ignore
except Exception:  # pragma: no cover
    load_dotenv = None

try:
    from openai import OpenAI  # type: ignore
except Exception:  # pragma: no cover
    OpenAI = None


RETAIL_POLICY = """Retail policy assumptions:
- Returns are allowed within 30 days of delivery with proof of purchase.
- Opened items are only returnable if defective.
- Damaged or missing items should be handled with apology, evidence collection if needed, and a replacement or refund path.
- Product compatibility must not be guessed if the model or specification is missing.
- Complaints should be acknowledged and moved toward a concrete resolution or escalation.
"""


JUDGE_SCHEMA = {
    "name": "retail_customer_service_judge",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "score": {"type": "integer", "minimum": 1, "maximum": 5},
            "reasoning": {"type": "string"},
            "criteria_met": {
                "type": "object",
                "properties": {
                    "helpfulness": {"type": "boolean"},
                    "tone": {"type": "boolean"},
                    "policy_adherence": {"type": "boolean"},
                    "resolution_quality": {"type": "boolean"},
                },
                "required": ["helpfulness", "tone", "policy_adherence", "resolution_quality"],
                "additionalProperties": False,
            },
        },
        "required": ["score", "reasoning", "criteria_met"],
        "additionalProperties": False,
    },
}


JUDGE_SYSTEM_PROMPT = """You are a strict but fair evaluator for a retail customer service chatbot.
Score the assistant response only on the provided rubric.
Return valid JSON that matches the schema exactly.
Do not include markdown or extra keys.
"""


def judge_prompt(prompt: str, response: str) -> str:
    return f"""{RETAIL_POLICY}

Task Description:
Evaluate a retail customer service assistant response to the user prompt below.

Evaluation Criteria:
1. Helpfulness: Does the response directly address the customer's issue and provide a useful next step?
2. Tone: Is the response calm, respectful, empathetic, and free of blame?
3. Policy adherence: Does the response avoid inventing policy or making unsupported promises?
4. Resolution quality: Does the response clearly move the case toward closure, escalation, or the correct support path?

Reasoning Steps:
Step 1: Check whether the response answers the customer with the correct retail policy or a careful uncertainty statement.
Step 2: Check whether the tone is supportive and de-escalating.
Step 3: Check whether the response gives a concrete next action that a support agent or customer can follow.

User Prompt:
{prompt}

Assistant Response:
{response}
"""


@dataclass
class TestCase:
    case_id: str
    title: str
    prompt: str
    candidate_response: str
    expected_criteria: Dict[str, bool]
    ground_truth: str


TEST_CASES: List[TestCase] = [
    TestCase(
        case_id="retail-1",
        title="Late Return Request",
        prompt="A customer says: 'I bought a speaker 37 days ago and opened it, but I do not like the sound. Can I return it for a refund?'",
        candidate_response=(
            "No. The 30-day return window has passed, so this would not qualify for a standard refund. "
            "If the speaker is defective, send the order number and I can help with the review."
        ),
        expected_criteria={
            "helpfulness": True,
            "tone": True,
            "policy_adherence": True,
            "resolution_quality": True,
        },
        ground_truth="Explain that the return window has passed and offer a defect review or escalation path.",
    ),
    TestCase(
        case_id="retail-2",
        title="Damaged Arrival Complaint",
        prompt="A customer says: 'My order arrived with a cracked item and one accessory missing. I am pretty angry.'",
        candidate_response=(
            "I am very sorry this happened. Please send your order number and photos of the damage if you can, "
            "and we will help arrange a replacement or refund according to policy. I understand how frustrating this is."
        ),
        expected_criteria={
            "helpfulness": True,
            "tone": True,
            "policy_adherence": True,
            "resolution_quality": True,
        },
        ground_truth="Apologize, gather the needed details, and move directly to replacement or refund handling.",
    ),
    TestCase(
        case_id="retail-3",
        title="Product Compatibility Question",
        prompt="A customer asks: 'Will your USB-C charger work with a 2021 Dell XPS 13 and fast charge it?'",
        candidate_response=(
            "It probably works with most USB-C chargers. If you send the exact model, I can confirm."
        ),
        expected_criteria={
            "helpfulness": True,
            "tone": True,
            "policy_adherence": True,
            "resolution_quality": True,
        },
        ground_truth="Avoid guessing and request the missing charger details before confirming compatibility.",
    ),
    TestCase(
        case_id="retail-4",
        title="Missing Tracking Update",
        prompt="A customer says: 'Your tracking page has not updated in four days. Where is my package?'",
        candidate_response=(
            "Please contact the carrier."
        ),
        expected_criteria={
            "helpfulness": True,
            "tone": True,
            "policy_adherence": True,
            "resolution_quality": True,
        },
        ground_truth="Acknowledge the problem and explain the next action without pretending to know the package location.",
    ),
    TestCase(
        case_id="retail-5",
        title="Price Match Complaint",
        prompt="A customer says: 'I bought this jacket last week and now it is on sale. I want the difference refunded.'",
        candidate_response=(
            "Sure, I can refund the difference right away if you send the order number."
        ),
        expected_criteria={
            "helpfulness": True,
            "tone": True,
            "policy_adherence": True,
            "resolution_quality": True,
        },
        ground_truth="Do not invent the policy; check eligibility and offer a verification path.",
    ),
]


def approx_tokens(text: str) -> int:
    return max(1, math.ceil(len(text.split()) * 1.3))


def estimate_cost_usd(input_tokens: int, output_tokens: int, model: str) -> float:
    if model != DEFAULT_MODEL:
        return 0.0
    return (
        (input_tokens / 1_000_000) * GPT_4O_MINI_INPUT_COST_PER_1M
        + (output_tokens / 1_000_000) * GPT_4O_MINI_OUTPUT_COST_PER_1M
    )


def heuristic_judge(case: TestCase) -> Dict[str, Any]:
    text = case.candidate_response.lower()

    empathy_markers = r"\b(sorry|understand|appreciate|glad to help|i can help|thanks for letting)\b"
    harsh_markers = r"\b(don't bother|obviously|your fault|can't do anything|whatever)\b"
    next_step_markers = r"\b(order number|next step|send|check|review|verify|replacement|refund|escalat|track|policy)\b"
    unsupported_policy_markers = r"\b(full refund|guaranteed refund|always eligible|definitely works|right away)\b"

    helpfulness = bool(re.search(next_step_markers, text)) and not bool(re.search(r"\b(i don't know\b|\bi am not sure\b)", text))
    tone = bool(re.search(empathy_markers, text)) and not bool(re.search(harsh_markers, text))
    policy_adherence = not bool(re.search(unsupported_policy_markers, text))
    resolution_quality = bool(re.search(r"\b(refund|replacement|verify|review|escalat|check|track)\b", text))

    criteria = {
        "helpfulness": helpfulness,
        "tone": tone,
        "policy_adherence": policy_adherence,
        "resolution_quality": resolution_quality,
    }
    score = 1 + sum(1 for value in criteria.values() if value)
    if helpfulness and tone and policy_adherence and resolution_quality:
        score = 5

    reasoning_bits = []
    if helpfulness:
        reasoning_bits.append("The response gives a useful next step.")
    else:
        reasoning_bits.append("The response is not concrete enough.")
    if tone:
        reasoning_bits.append("The tone is calm and empathetic.")
    else:
        reasoning_bits.append("The tone is too sharp or dismissive.")
    if policy_adherence:
        reasoning_bits.append("It avoids inventing policy.")
    else:
        reasoning_bits.append("It makes an unsupported policy claim.")
    if resolution_quality:
        reasoning_bits.append("It moves toward a resolution path.")
    else:
        reasoning_bits.append("It does not clearly resolve the issue.")

    input_tokens = approx_tokens(case.prompt) + approx_tokens(case.candidate_response) + approx_tokens(judge_prompt(case.prompt, case.candidate_response))
    output_text = json.dumps(
        {
            "score": score,
            "reasoning": " ".join(reasoning_bits),
            "criteria_met": criteria,
        },
        ensure_ascii=True,
    )
    output_tokens = approx_tokens(output_text)
    estimated_cost = estimate_cost_usd(input_tokens, output_tokens, DEFAULT_MODEL)

    return {
        "score": score,
        "reasoning": " ".join(reasoning_bits),
        "criteria_met": criteria,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "estimated_cost_usd": round(estimated_cost, 6),
        "judge_mode": "offline_heuristic",
    }


def openai_judge(case: TestCase, model: str = DEFAULT_MODEL) -> Dict[str, Any]:
    if OpenAI is None:
        raise RuntimeError("openai package is not installed")
    client = OpenAI()
    prompt_text = judge_prompt(case.prompt, case.candidate_response)
    payload = {
        "model": model,
        "input": [
            {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
            {"role": "user", "content": prompt_text},
        ],
        "text": {"format": {"type": "json_schema", **JUDGE_SCHEMA}},
    }
    start = time.perf_counter()
    response = client.responses.create(**payload)
    elapsed = time.perf_counter() - start

    raw_text = getattr(response, "output_text", None)
    if not raw_text:
        # Fallback for SDK response variants
        raw_text = ""
        for output_item in getattr(response, "output", []) or []:
            if getattr(output_item, "type", None) == "message":
                for content_item in getattr(output_item, "content", []) or []:
                    if getattr(content_item, "type", None) == "output_text":
                        raw_text += getattr(content_item, "text", "")

    parsed = json.loads(raw_text)
    usage = getattr(response, "usage", None)
    input_tokens = getattr(usage, "input_tokens", None) if usage else None
    output_tokens = getattr(usage, "output_tokens", None) if usage else None
    estimated_cost = None
    if input_tokens is not None and output_tokens is not None:
        estimated_cost = estimate_cost_usd(int(input_tokens), int(output_tokens), model)
    return {
        "score": int(parsed["score"]),
        "reasoning": parsed["reasoning"],
        "criteria_met": parsed["criteria_met"],
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "estimated_cost_usd": round(estimated_cost, 6) if estimated_cost is not None else None,
        "judge_mode": "openai",
        "response_id": getattr(response, "id", None),
        "elapsed_seconds": elapsed,
    }


def run_case(case: TestCase, mode: str, model: str) -> Dict[str, Any]:
    start = time.perf_counter()
    if mode == "openai":
        judged = openai_judge(case, model=model)
    else:
        judged = heuristic_judge(case)
    elapsed = time.perf_counter() - start
    judged.setdefault("elapsed_seconds", elapsed)
    judged["elapsed_seconds"] = round(float(judged["elapsed_seconds"]), 4)
    judged["prompt_tokens_estimate"] = approx_tokens(case.prompt)
    judged["response_tokens_estimate"] = approx_tokens(case.candidate_response)
    return {
        "case_id": case.case_id,
        "title": case.title,
        "prompt": case.prompt,
        "ground_truth": case.ground_truth,
        "candidate_response": case.candidate_response,
        "expected_criteria": case.expected_criteria,
        "judge_result": judged,
    }


def aggregate(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    scores = [item["judge_result"]["score"] for item in results]
    total_elapsed = sum(item["judge_result"]["elapsed_seconds"] for item in results)
    total_cost = sum(float(item["judge_result"].get("estimated_cost_usd") or 0.0) for item in results)
    criteria_keys = list(TEST_CASES[0].expected_criteria.keys())
    criteria_counts = {key: 0 for key in criteria_keys}
    for item in results:
        for key in criteria_keys:
            if item["judge_result"]["criteria_met"].get(key):
                criteria_counts[key] += 1
    return {
        "case_count": len(results),
        "average_score": round(mean(scores), 2) if scores else None,
        "min_score": min(scores) if scores else None,
        "max_score": max(scores) if scores else None,
        "total_elapsed_seconds": round(total_elapsed, 4),
        "total_estimated_cost_usd": round(total_cost, 6),
        "criteria_coverage": criteria_counts,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a retail customer service LLM judge evaluation.")
    parser.add_argument("--offline", action="store_true", help="Use the deterministic offline judge.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenAI model to use in live mode.")
    parser.add_argument("--output", default=str(RESULTS_PATH), help="Path to write evaluation_results.json.")
    args = parser.parse_args()

    load_env_file()
    if load_dotenv is not None:
        load_dotenv()

    api_key_available = bool(os.getenv("OPENAI_API_KEY"))
    mode = "openai" if api_key_available and not args.offline else "offline"

    results = [run_case(case, mode=mode, model=args.model) for case in TEST_CASES]
    payload = {
        "scenario": "Retail customer service chatbot",
        "mode": mode,
        "model": args.model if mode == "openai" else None,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "results": results,
        "summary": aggregate(results),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2))


if __name__ == "__main__":
    main()
