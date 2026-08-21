"""Run a five-case MIRA proof-of-concept evaluation with an LLM judge."""

from __future__ import annotations

import json
import os
import re
import statistics
import time
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


OUTPUT_PATH = Path(__file__).with_name("evaluation_results.json")
EVALUATED_MODEL = os.getenv("MIRA_EVALUATED_MODEL", "gpt-4o-mini")
JUDGE_MODEL = os.getenv("MIRA_JUDGE_MODEL", "gpt-4o-mini")
MAX_ATTEMPTS = 2

# Pricing changes over time. Keep these as None unless verified immediately
# before a run; when unset, the output reports estimated_cost_usd as null.
INPUT_USD_PER_MILLION_TOKENS: float | None = None
OUTPUT_USD_PER_MILLION_TOKENS: float | None = None

CRITERIA_KEYS = (
    "instruction_adherence",
    "preference_fidelity",
    "campaign_consistency",
    "specificity",
    "no_unsupported_assumptions",
)

TEST_CASES = [
    {
        "id": "explicit-visual-preferences",
        "title": "Explicit visual preference adherence",
        "prompt": (
            "Create a three-part editorial direction for a small architecture studio. "
            "Use only a muted neutral palette, an architectural concrete setting, hard "
            "directional light, and minimal styling. Avoid saturated colours, soft romantic "
            "light, decorative props, and outdoor nature imagery. Include palette, lighting, "
            "styling, and composition sections."
        ),
        "ground_truth": "Three parts and four named sections; required aesthetics retained; prohibited aesthetics absent.",
        "expected_criteria": ["instruction_adherence", "preference_fidelity", "specificity"],
    },
    {
        "id": "user-input-precedence",
        "title": "User input precedence",
        "prompt": (
            "Develop a campaign direction for a wellness founder. Background context might "
            "suggest calm beige minimalism, but the user's direct choice is vivid cobalt and "
            "orange, playful asymmetry, direct flash, and an energetic urban night setting. "
            "Treat the direct choice as authoritative. Do not revert to beige minimalism. "
            "Explain the decision briefly and propose three frames."
        ),
        "ground_truth": "Direct cobalt/orange, asymmetry, flash, and urban-night choices override beige minimalism.",
        "expected_criteria": ["instruction_adherence", "preference_fidelity", "campaign_consistency"],
    },
    {
        "id": "campaign-consistency",
        "title": "Five-frame campaign consistency",
        "prompt": (
            "Create a five-frame editorial campaign for an independent ceramic artist. The "
            "direction is quiet precision: chalk, charcoal, and clay colours; hard morning "
            "side-light; a raw plaster studio; restrained styling; tactile close-ups; no "
            "greenery and no glossy luxury cues. For each frame specify subject, composition, "
            "lighting, palette, and continuity link. Keep all five frames part of one coherent story."
        ),
        "ground_truth": "No unique answer; five frames must retain every explicit visual rule and form one coherent sequence.",
        "expected_criteria": list(CRITERIA_KEYS),
    },
    {
        "id": "hallucination-resistance",
        "title": "Hallucination resistance",
        "prompt": (
            "The only known facts are: the client makes hand-bound notebooks and wants an "
            "editorial campaign that feels precise and tactile. Propose an initial direction. "
            "Clearly label unknowns and questions. Do not invent the client's age, location, "
            "personality, customer demographics, personal history, preferred colours, or business scale."
        ),
        "ground_truth": "Unknown personal, audience, location, palette, and business details remain unknown or are asked as questions.",
        "expected_criteria": ["instruction_adherence", "specificity", "no_unsupported_assumptions"],
    },
    {
        "id": "specificity-usefulness",
        "title": "Specificity and usefulness",
        "prompt": (
            "Give actionable editorial direction for a sustainable furniture maker launching "
            "one chair. Include precise choices for styling, lighting, a named colour palette, "
            "composition, location/atmosphere, and a five-shot sequence. Avoid empty phrases "
            "such as 'authentic,' 'elevated,' or 'timeless' unless each is translated into a concrete visual decision."
        ),
        "ground_truth": "No unique answer; all requested production categories and five shots should contain concrete choices.",
        "expected_criteria": ["instruction_adherence", "campaign_consistency", "specificity"],
    },
]

JUDGE_SYSTEM_PROMPT = """You are an impartial evaluator of MIRA, an AI Creative Director.
Assess only the supplied task and response. Direct user answers and visual choices take
precedence over inferred context. Do not reward length, polish, or familiar style by itself.

Criteria:
1. instruction_adherence: all explicit output requirements and exclusions are followed.
2. preference_fidelity: supplied visual and creative preferences are preserved.
3. campaign_consistency: styling, colour, light, composition, atmosphere, and sequence do not contradict each other.
4. specificity: choices are concrete and practically useful rather than generic.
5. no_unsupported_assumptions: biography, audience, identity, and preferences are not invented.

Score anchors: 1=major failure; 2=several important failures; 3=acceptable but inconsistent;
4=strong with minor issues; 5=fully meets requirements.

First identify explicit requirements, compare the response with them, note contradictions or
unsupported additions, assess consistency and usefulness, then assign one overall score.
Return JSON only with this shape:
{"score": 1, "reasoning": "concise evidence-based explanation", "criteria_met":
{"instruction_adherence": false, "preference_fidelity": false,
"campaign_consistency": false, "specificity": false,
"no_unsupported_assumptions": false}}"""


def usage_dict(completion: Any) -> dict[str, int]:
    usage = getattr(completion, "usage", None)
    return {
        "input_tokens": int(getattr(usage, "prompt_tokens", 0) or 0),
        "output_tokens": int(getattr(usage, "completion_tokens", 0) or 0),
        "total_tokens": int(getattr(usage, "total_tokens", 0) or 0),
    }


def extract_json(text: str) -> dict[str, Any]:
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE)
    try:
        value = json.loads(cleaned)
    except json.JSONDecodeError:
        start, end = cleaned.find("{"), cleaned.rfind("}")
        if start < 0 or end <= start:
            raise ValueError("Judge response did not contain a JSON object")
        value = json.loads(cleaned[start : end + 1])
    if not isinstance(value, dict):
        raise ValueError("Judge JSON must be an object")
    score = value.get("score")
    if isinstance(score, bool) or not isinstance(score, (int, float)) or not 1 <= score <= 5:
        raise ValueError("Judge score must be a number from 1 to 5")
    criteria = value.get("criteria_met")
    if not isinstance(criteria, dict) or any(not isinstance(criteria.get(key), bool) for key in CRITERIA_KEYS):
        raise ValueError("criteria_met must include all five boolean criteria")
    if not isinstance(value.get("reasoning"), str) or not value["reasoning"].strip():
        raise ValueError("Judge reasoning must be a non-empty string")
    value["score"] = float(score)
    return value


def estimate_cost(usage: dict[str, int]) -> float | None:
    if INPUT_USD_PER_MILLION_TOKENS is None or OUTPUT_USD_PER_MILLION_TOKENS is None:
        return None
    return round(
        usage["input_tokens"] * INPUT_USD_PER_MILLION_TOKENS / 1_000_000
        + usage["output_tokens"] * OUTPUT_USD_PER_MILLION_TOKENS / 1_000_000,
        8,
    )


def generate_response(client: OpenAI, case: dict[str, Any]) -> tuple[str, dict[str, int]]:
    completion = client.chat.completions.create(
        model=EVALUATED_MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": "You are MIRA, an AI Creative Director. Follow direct user choices exactly and do not invent unsupported client facts."},
            {"role": "user", "content": case["prompt"]},
        ],
    )
    return completion.choices[0].message.content or "", usage_dict(completion)


def judge_response(client: OpenAI, case: dict[str, Any], response: str) -> tuple[dict[str, Any], dict[str, int]]:
    user_message = json.dumps(
        {"task": case["prompt"], "ground_truth_or_constraints": case["ground_truth"], "response_to_evaluate": response},
        ensure_ascii=False,
    )
    last_error: Exception | None = None
    for _ in range(MAX_ATTEMPTS):
        try:
            completion = client.chat.completions.create(
                model=JUDGE_MODEL,
                temperature=0,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
            )
            return extract_json(completion.choices[0].message.content or ""), usage_dict(completion)
        except Exception as exc:  # retry provider and parsing failures once
            last_error = exc
    raise RuntimeError(f"Judge failed after {MAX_ATTEMPTS} attempts: {last_error}")


def add_usage(first: dict[str, int], second: dict[str, int]) -> dict[str, int]:
    return {key: first[key] + second[key] for key in first}


def main() -> int:
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY is not set. Copy .env.example to .env and add the key.")
        return 1

    client = OpenAI()
    started = time.perf_counter()
    results: list[dict[str, Any]] = []

    for index, case in enumerate(TEST_CASES, start=1):
        print(f"[{index}/{len(TEST_CASES)}] Running {case['id']}: {case['title']}")
        case_started = time.perf_counter()
        try:
            response, generation_usage = generate_response(client, case)
            judgment, judge_usage = judge_response(client, case, response)
            combined_usage = add_usage(generation_usage, judge_usage)
            results.append(
                {
                    **case,
                    "status": "completed",
                    "model_response": response,
                    "score": judgment["score"],
                    "reasoning": judgment["reasoning"],
                    "criteria_met": judgment["criteria_met"],
                    "elapsed_seconds": round(time.perf_counter() - case_started, 3),
                    "usage": {"generation": generation_usage, "judge": judge_usage, "combined": combined_usage},
                    "estimated_cost_usd": estimate_cost(combined_usage),
                    "error": None,
                }
            )
            print(f"  completed — score {judgment['score']:.1f}")
        except Exception as exc:
            results.append(
                {
                    **case,
                    "status": "failed",
                    "elapsed_seconds": round(time.perf_counter() - case_started, 3),
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
            print(f"  failed — {type(exc).__name__}: {exc}")

    total_runtime = round(time.perf_counter() - started, 3)
    completed = [item for item in results if item["status"] == "completed"]
    scores = [item["score"] for item in completed]
    total_usage = {
        key: sum(item["usage"]["combined"][key] for item in completed)
        for key in ("input_tokens", "output_tokens", "total_tokens")
    }
    known_costs = [item["estimated_cost_usd"] for item in completed if item["estimated_cost_usd"] is not None]
    aggregate = {
        "number_of_cases": len(TEST_CASES),
        "completed_cases": len(completed),
        "failed_cases": len(TEST_CASES) - len(completed),
        "average_score": round(statistics.mean(scores), 3) if scores else None,
        "minimum_score": min(scores) if scores else None,
        "maximum_score": max(scores) if scores else None,
        "total_runtime_seconds": total_runtime,
        "average_runtime_seconds": round(total_runtime / len(TEST_CASES), 3),
        "total_usage": total_usage,
        "estimated_total_cost_usd": round(sum(known_costs), 8) if len(known_costs) == len(completed) and completed else None,
    }
    payload = {
        "status": "completed" if len(completed) == len(TEST_CASES) else "completed_with_errors",
        "evaluated_model": EVALUATED_MODEL,
        "judge_model": JUDGE_MODEL,
        "dataset_size": len(TEST_CASES),
        "cost_note": "Unavailable unless current pricing constants are verified and configured in the script.",
        "statistical_note": "N=5 is a severely underpowered proof of concept and does not support strong model-comparison claims.",
        "results": results,
        "aggregate": aggregate,
    }
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Saved results to {OUTPUT_PATH}")
    print(json.dumps(aggregate, indent=2))
    return 0 if completed else 2


if __name__ == "__main__":
    raise SystemExit(main())
