"""
LLM-as-Judge Evaluation Pipeline
Scenario: AI coaching assistant for employee goal-setting and performance.

This script:
1. Generates a model response for each of the 5 coaching test prompts.
2. Judges each response with a structured LLM-as-judge rubric
   (specificity-seeking, coaching stance, tone).
3. Collects metrics (score, time, tokens, estimated cost).
4. Saves everything to evaluation_results.json and prints a summary.
"""

import json
import time
from dotenv import load_dotenv
from openai import OpenAI

# Load OPENAI_API_KEY from .env automatically
load_dotenv()
client = OpenAI()

MODEL = "gpt-4o-mini"

# Pricing for gpt-4o-mini as of this lab (USD per 1M tokens). Update if pricing changes.
INPUT_COST_PER_1M = 0.15
OUTPUT_COST_PER_1M = 0.60

# System prompt for the assistant under test
COACH_SYSTEM_PROMPT = """You are an AI coaching assistant helping employees define
goals and improve performance in their role. Use a supportive, non-judgmental,
question-first coaching stance (in the spirit of the GROW model). Do not give
clinical or mental-health advice; if a topic goes beyond workplace coaching,
acknowledge it and gently note that additional support may be appropriate,
while staying focused on what is within the coaching relationship."""

# The 5 test prompts from Step 3
TEST_PROMPTS = [
    {
        "id": 1,
        "title": "Vague goal, needs probing",
        "prompt": "I want to get better at my job this year.",
    },
    {
        "id": 2,
        "title": "Emotionally loaded, borderline scope",
        "prompt": (
            "Honestly I've been dreading going to work lately, I don't know "
            "if it's the job or something else going on with me."
        ),
    },
    {
        "id": 3,
        "title": "Employee proposes an unmeasurable goal",
        "prompt": "My goal is to be a better communicator.",
    },
    {
        "id": 4,
        "title": "Employee wants to be told what to do",
        "prompt": (
            "Just tell me what my goal should be, I don't have time for "
            "this back and forth."
        ),
    },
    {
        "id": 5,
        "title": "Progress check-in with an excuse",
        "prompt": (
            "So about that goal we set last time - I haven't really made "
            "progress, my manager keeps piling on extra work."
        ),
    },
]

# Judge prompt template (generalized version of the Step 4 judge, applied to all 5 cases)
JUDGE_SYSTEM_PROMPT = """You are an evaluation judge for an AI coaching assistant.

TASK DESCRIPTION:
The assistant being judged responded to an employee message in a workplace
coaching context. Its job is to help the employee move toward a specific,
observable goal or next step, using a supportive coaching stance (asking,
not just telling), and to stay within appropriate scope (not giving clinical
or mental-health advice).

EVALUATION CRITERIA:
1. specificity_seeking: Does the response avoid accepting vague statements at
   face value, and instead move the employee toward something specific,
   observable, or actionable (a situation, behavior, or measure)?
2. coaching_stance: Does the response primarily invite the employee to supply
   detail (e.g. via a genuine, open question) rather than the assistant
   unilaterally deciding the goal or next step on the employee's behalf?
3. tone: Is the response supportive, non-judgmental, and appropriately scoped
   (no clinical/diagnostic language, no dismissiveness, no rubber-stamping
   of excuses without gentle follow-up)?

REASONING STEPS:
Step 1: Identify what the employee actually said and what they need.
Step 2: Check the response against each of the three criteria above,
        one at a time.
Step 3: Decide an overall score based on how many criteria are clearly met
        and how well-executed the response is (not just checkbox presence).

OUTPUT FORMAT:
Return ONLY a JSON object, no other text, in exactly this shape:
{
  "score": <integer 1-5>,
  "reasoning": "<2-3 sentence explanation>",
  "criteria_met": {
    "specificity_seeking": <true|false>,
    "coaching_stance": <true|false>,
    "tone": <true|false>
  }
}

Score scale: 5 = fully meets all three criteria with a natural, well-phrased
response; 3 = partially meets criteria or executes unevenly; 1 = fails most
criteria (e.g. accepts vague input as final, gives unilateral advice, or
breaks tone/scope)."""


def generate_coach_response(prompt_text):
    """Call the model under test (the coaching assistant) for a given prompt."""
    start = time.time()
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": COACH_SYSTEM_PROMPT},
            {"role": "user", "content": prompt_text},
        ],
        temperature=0.7,
    )
    elapsed = time.time() - start
    return {
        "text": completion.choices[0].message.content,
        "time_seconds": elapsed,
        "input_tokens": completion.usage.prompt_tokens,
        "output_tokens": completion.usage.completion_tokens,
    }


def judge_response(prompt_text, model_response_text):
    """Call the LLM judge to score a coaching response against the rubric."""
    user_content = (
        f"EMPLOYEE MESSAGE:\n{prompt_text}\n\n"
        f"ASSISTANT RESPONSE TO EVALUATE:\n{model_response_text}"
    )
    start = time.time()
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )
    elapsed = time.time() - start

    raw_text = completion.choices[0].message.content
    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError:
        # Fallback if the judge ever returns malformed JSON
        parsed = {
            "score": None,
            "reasoning": f"JSON parsing failed. Raw output: {raw_text}",
            "criteria_met": {},
        }

    return {
        "parsed": parsed,
        "time_seconds": elapsed,
        "input_tokens": completion.usage.prompt_tokens,
        "output_tokens": completion.usage.completion_tokens,
    }


def estimate_cost(input_tokens, output_tokens):
    """Estimate USD cost for a single call given gpt-4o-mini pricing."""
    input_cost = (input_tokens / 1_000_000) * INPUT_COST_PER_1M
    output_cost = (output_tokens / 1_000_000) * OUTPUT_COST_PER_1M
    return round(input_cost + output_cost, 8)


def run_evaluation():
    """Run generation + judging for all test prompts and collect results."""
    results = []

    for case in TEST_PROMPTS:
        print(f"Running case {case['id']}: {case['title']}...")

        # Step A: generate the coaching assistant's response
        gen = generate_coach_response(case["prompt"])

        # Step B: judge that response
        judged = judge_response(case["prompt"], gen["text"])

        total_input_tokens = gen["input_tokens"] + judged["input_tokens"]
        total_output_tokens = gen["output_tokens"] + judged["output_tokens"]
        total_time = gen["time_seconds"] + judged["time_seconds"]
        total_cost = estimate_cost(total_input_tokens, total_output_tokens)

        results.append({
            "id": case["id"],
            "title": case["title"],
            "prompt": case["prompt"],
            "model_response": gen["text"],
            "score": judged["parsed"].get("score"),
            "reasoning": judged["parsed"].get("reasoning"),
            "criteria_met": judged["parsed"].get("criteria_met"),
            "time_seconds": round(total_time, 3),
            "tokens": {
                "input": total_input_tokens,
                "output": total_output_tokens,
            },
            "cost_usd": total_cost,
        })

    return results


def summarize(results):
    """Compute aggregate statistics across all evaluated cases."""
    scores = [r["score"] for r in results if isinstance(r["score"], (int, float))]
    total_time = sum(r["time_seconds"] for r in results)
    total_cost = sum(r["cost_usd"] for r in results)
    total_input_tokens = sum(r["tokens"]["input"] for r in results)
    total_output_tokens = sum(r["tokens"]["output"] for r in results)

    aggregate = {
        "num_cases": len(results),
        "avg_score": round(sum(scores) / len(scores), 2) if scores else None,
        "min_score": min(scores) if scores else None,
        "max_score": max(scores) if scores else None,
        "total_time_seconds": round(total_time, 3),
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "total_cost_usd": round(total_cost, 6),
    }
    return aggregate


def print_summary(results, aggregate):
    """Print a human-readable summary to the console."""
    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)

    for r in results:
        print(f"\nCase {r['id']}: {r['title']}")
        print(f"  Score: {r['score']}/5")
        print(f"  Criteria met: {r['criteria_met']}")
        reasoning_preview = (r["reasoning"] or "")[:150]
        print(f"  Reasoning: {reasoning_preview}...")
        print(f"  Time: {r['time_seconds']}s | Cost: ${r['cost_usd']}")

    print("\n" + "-" * 60)
    print("AGGREGATE STATS")
    print("-" * 60)
    for key, value in aggregate.items():
        print(f"  {key}: {value}")
    print("=" * 60)


if __name__ == "__main__":
    all_results = run_evaluation()
    agg = summarize(all_results)

    # Save full results to JSON
    output = {"results": all_results, "aggregate": agg}
    with open("evaluation_results.json", "w") as f:
        json.dump(output, f, indent=2)

    print_summary(all_results, agg)
    print("\nResults saved to evaluation_results.json")
