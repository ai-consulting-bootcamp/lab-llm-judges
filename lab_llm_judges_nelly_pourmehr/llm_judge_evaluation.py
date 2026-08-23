import os
import json
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

MODEL = "gpt-4o-mini"

# Judge prompt built from Step 4 in evaluation_design.md
JUDGE_SYSTEM_PROMPT = """You are an evaluation judge for a SaaS support chatbot.

Task Description:
The model was asked to help a customer whose Slack integration stopped sending notifications. The model must give troubleshooting steps a support agent would actually give.

Evaluation Criteria:
1. permissions_check: Does the response tell the customer to check Slack app permissions?
2. token_expiry_check: Does the response tell the customer to check if the integration token or connection expired?
3. notification_settings_check: Does the response tell the customer to check notification settings inside the product?

Reasoning Steps:
Step 1: List which of the 3 causes the response names, if any.
Step 2: Check the steps are stated as actions the customer can take, not vague statements.
Step 3: Extra valid causes do not reduce the score, but they cannot replace missing required causes. Give credit if the intent matches, even in different words.

Output Format:
Return ONLY valid JSON, no other text:
{
  "score": <number 0 to 1, equal to criteria met divided by 3>,
  "reasoning": "<short explanation>",
  "criteria_met": {
    "permissions_check": true/false,
    "token_expiry_check": true/false,
    "notification_settings_check": true/false
  }
}
"""


def judge_response(original_prompt: str, model_response: str) -> dict:
    # calls the judge model and returns score, reasoning, criteria
    start = time.time()

    completion = client.chat.completions.create(
        model=MODEL,
        temperature=0,  # low temperature for consistent judge scores
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Original prompt:\n{original_prompt}\n\nModel response to evaluate:\n{model_response}",
            },
        ],
    )

    elapsed = time.time() - start
    raw = completion.choices[0].message.content

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        # fallback if judge does not return clean JSON
        result = {"score": None, "reasoning": "JSON parse error", "criteria_met": {}}

    result["time_seconds"] = round(elapsed, 2)
    result["input_tokens"] = completion.usage.prompt_tokens
    result["output_tokens"] = completion.usage.completion_tokens

    return result

TEST_CASES = [
    {
        "id": "prompt_1_hallucination",
        "prompt": "Can I export my dashboard as a PowerPoint file?",
        "response": "PowerPoint export isn't supported right now. You can export your dashboard as a PDF or a CSV file instead.",
        "ground_truth": "Must not claim PowerPoint export exists. Must offer a real export format.",
        "expected_criteria": "no_false_feature_claim",
    },
    {
        "id": "prompt_2_tone",
        "prompt": "I was charged twice this month and nobody is answering me. This is ridiculous.",
        "response": "I'm sorry about the duplicate charge, that's frustrating. I can't confirm a refund amount here, but I'm escalating this to our billing team now and they'll follow up within 24 hours.",
        "ground_truth": "Acknowledge frustration, no false refund promise, clear next step.",
        "expected_criteria": "acknowledgment,no_false_promise,next_step",
    },
    {
        "id": "prompt_3_troubleshooting",
        "prompt": "My integration with Slack stopped sending notifications yesterday. I didn't change anything.",
        "response": "Try checking if your Slack app permissions are still active. That should fix it.",
        "ground_truth": "Should cover permissions, token expiry, and notification settings.",
        "expected_criteria": "permissions_check,token_expiry_check,notification_settings_check",
    },
    {
        "id": "prompt_4_scope",
        "prompt": "Can you just log into my account and fix the settings for me?",
        "response": "I'm not able to log into your account directly, but I can walk you through the exact steps to fix it yourself right now.",
        "ground_truth": "Must not claim direct account access. Must still offer help.",
        "expected_criteria": "no_false_capability_claim,still_helpful",
    },
    {
        "id": "prompt_5_ambiguous",
        "prompt": "it's not working",
        "response": "Can you tell me a bit more about what isn't working? For example, is this about login, notifications, or something else?",
        "ground_truth": "Should ask a clarifying question instead of guessing.",
        "expected_criteria": "asks_clarifying_question",
    },
]
def run_all_evaluations():
    # runs judge on every test case, collects results and aggregate stats
    individual_results = []
    total_start = time.time()

    for case in TEST_CASES:
        print(f"Evaluating {case['id']}...")
        result = judge_response(case["prompt"], case["response"])
        individual_results.append({
            "id": case["id"],
            "prompt": case["prompt"],
            "response": case["response"],
            "ground_truth": case["ground_truth"],
            "score": result.get("score"),
            "reasoning": result.get("reasoning"),
            "criteria_met": result.get("criteria_met"),
            "time_seconds": result.get("time_seconds"),
            "input_tokens": result.get("input_tokens"),
            "output_tokens": result.get("output_tokens"),
        })

    total_time = round(time.time() - total_start, 2)

    scores = [r["score"] for r in individual_results if r["score"] is not None]
    total_input_tokens = sum(r["input_tokens"] for r in individual_results)
    total_output_tokens = sum(r["output_tokens"] for r in individual_results)

    # gpt-4o-mini pricing: $0.15 per 1M input tokens, $0.60 per 1M output tokens
    estimated_cost = round(
        (total_input_tokens / 1_000_000) * 0.15 + (total_output_tokens / 1_000_000) * 0.60, 6
    )

    aggregate = {
        "num_cases": len(individual_results),
        "average_score": round(sum(scores) / len(scores), 3) if scores else None,
        "min_score": min(scores) if scores else None,
        "max_score": max(scores) if scores else None,
        "total_time_seconds": total_time,
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "estimated_cost_usd": estimated_cost,
    }

    output = {
        "individual_results": individual_results,
        "aggregate_statistics": aggregate,
    }

    with open("evaluation_results.json", "w") as f:
        json.dump(output, f, indent=2)

    return output

def print_analysis(results: dict):
    # simple readable summary of results for step 11
    print("\n=== EVALUATION SUMMARY ===\n")

    for r in results["individual_results"]:
        print(f"ID: {r['id']}")
        print(f"  Score: {r['score']}")
        print(f"  Time: {r['time_seconds']}s")
        print(f"  Criteria met: {r['criteria_met']}")
        reasoning_short = r["reasoning"][:120] + "..." if len(r["reasoning"]) > 120 else r["reasoning"]
        print(f"  Reasoning: {reasoning_short}")
        print()

    agg = results["aggregate_statistics"]
    print("=== AGGREGATE STATS ===")
    print(f"Cases: {agg['num_cases']}")
    print(f"Average score: {agg['average_score']}")
    print(f"Min/Max score: {agg['min_score']} / {agg['max_score']}")
    print(f"Total time: {agg['total_time_seconds']}s")
    print(f"Estimated cost: ${agg['estimated_cost_usd']}")

    print("\n=== KEY INSIGHT ===")
    print("This judge was built only for Slack troubleshooting criteria (Prompt #3).")
    print("Prompts 1, 2, 4, 5 correctly score near 0 because they test different failure")
    print("modes the judge was not designed to grade. A production version needs one")
    print("judge per failure mode, not one generic judge.")

CALIBRATION_CASES = [
    {
        "id": "calibration_full_marks",
        "prompt": "My integration with Slack stopped sending notifications yesterday. I didn't change anything.",
        "response": "First check if your Slack app permissions are still active. Next, check if your integration token has expired and needs reconnecting. Also check your notification settings inside the product, since those can silently turn off.",
        "expected_score": 1.0,
    },
    {
        "id": "calibration_wrong_answer",
        "prompt": "My integration with Slack stopped sending notifications yesterday. I didn't change anything.",
        "response": "Try clearing your browser cache and reloading the page.",
        "expected_score": 0.0,
    },
]


def run_calibration_check():
    # confirms the judge scores known good/bad answers as expected
    print("\n=== CALIBRATION CHECK ===\n")
    for case in CALIBRATION_CASES:
        result = judge_response(case["prompt"], case["response"])
        print(f"{case['id']}: expected {case['expected_score']}, got {result['score']}")

def check_consistency(case_id="prompt_3_troubleshooting", runs=3):
    # runs the same case multiple times, checks if scores match
    case = next(c for c in TEST_CASES if c["id"] == case_id)
    scores = []
    print(f"\n=== CONSISTENCY CHECK: {case_id} ({runs} runs) ===\n")
    for i in range(runs):
        result = judge_response(case["prompt"], case["response"])
        scores.append(result["score"])
        print(f"Run {i+1}: score = {result['score']}")
    print(f"All identical: {len(set(scores)) == 1}")



if __name__ == "__main__":
    run_calibration_check()
    results = run_all_evaluations()
    print_analysis(results)
    check_consistency()