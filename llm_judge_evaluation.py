import os
import json
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"

def judge_complaint_response(customer_message, bot_response):
    judge_prompt = f"""You are evaluating a retail customer service chatbot's response to a frustrated customer.

TASK DESCRIPTION:
The chatbot received a message from a customer whose order has arrived late three times and arrived damaged this time. The customer says they are considering never shopping at the store again. The chatbot's job was to de-escalate, acknowledge the customer's frustration, and offer a concrete resolution consistent with policy: damaged items get a full refund or replacement, no time limit beyond 90 days.

EVALUATION CRITERIA:
1. Empathy/Acknowledgment: Does the response genuinely acknowledge the customer's frustration and the pattern of repeated failures (not just the single damaged item)?
2. Concrete Resolution: Does the response offer a specific, policy-consistent next step (refund or replacement), not just a vague "we'll look into it"?
3. Tone Appropriateness: Is the tone calm, respectful, and non-defensive, avoiding both robotic dismissiveness and empty over-apologizing?

REASONING STEPS:
Step 1: Check if the response acknowledges the customer's emotional state and the repeated pattern of issues, not just the immediate complaint.
Step 2: Check if a specific, policy-consistent resolution is offered.
Step 3: Assess overall tone as if you were the frustrated customer receiving this reply.

CUSTOMER MESSAGE:
{customer_message}

CHATBOT RESPONSE:
{bot_response}

Respond ONLY with valid JSON in this exact format, no other text:
{{
  "score": <integer 1-5>,
  "reasoning": "<your explanation>",
  "criteria_met": {{
    "empathy_acknowledgment": <true or false>,
    "concrete_resolution": <true or false>,
    "tone_appropriateness": <true or false>
  }}
}}"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": judge_prompt}],
        temperature=0,
        response_format={"type": "json_object"}
    )

    result = json.loads(response.choices[0].message.content)
    result["input_tokens"] = response.usage.prompt_tokens
    result["output_tokens"] = response.usage.completion_tokens
    return result

test_cases = [
    {
        "id": "complaint_good",
        "customer_message": "This is the THIRD time my order has arrived late and now it's damaged too. I am extremely frustrated and considering never shopping here again.",
        "bot_response": "I'm so sorry to hear about this repeated issue — that's genuinely frustrating, especially after three late deliveries in a row. Since the item arrived damaged, I can process a full refund or send a replacement right away, whichever you'd prefer. Which would you like?"
    },
    {
        "id": "complaint_generic",
        "customer_message": "This is the THIRD time my order has arrived late and now it's damaged too. I am extremely frustrated and considering never shopping here again.",
        "bot_response": "We're sorry for the inconvenience. Please contact customer support for further assistance."
    },
    {
        "id": "complaint_no_resolution",
        "customer_message": "This is the THIRD time my order has arrived late and now it's damaged too. I am extremely frustrated and considering never shopping here again.",
        "bot_response": "I completely understand your frustration and I'm so sorry you've had such a rough experience with us. We really value you as a customer and want you to know we hear you."
    },
    {
        "id": "complaint_dismissive",
        "customer_message": "This is the THIRD time my order has arrived late and now it's damaged too. I am extremely frustrated and considering never shopping here again.",
        "bot_response": "Damaged items can be returned within 90 days for a refund or replacement."
    }
]

if __name__ == "__main__":
    INPUT_COST_PER_TOKEN = 0.15 / 1_000_000
    OUTPUT_COST_PER_TOKEN = 0.60 / 1_000_000

    results = []

    for case in test_cases:
        start = time.time()
        result = judge_complaint_response(case["customer_message"], case["bot_response"])
        elapsed = time.time() - start

        result["id"] = case["id"]
        result["time_seconds"] = round(elapsed, 2)
        result["cost_usd"] = round(
            result["input_tokens"] * INPUT_COST_PER_TOKEN
            + result["output_tokens"] * OUTPUT_COST_PER_TOKEN,
            6
        )
        results.append(result)

        print(f"--- {case['id']} ---")
        print(f"Score: {result['score']} | Time: {result['time_seconds']}s | Cost: ${result['cost_usd']}")
        print(f"Reasoning: {result['reasoning']}")
        print()

    scores = [r["score"] for r in results]
    total_time = sum(r["time_seconds"] for r in results)
    total_cost = sum(r["cost_usd"] for r in results)

    criteria_totals = {"empathy_acknowledgment": 0, "concrete_resolution": 0, "tone_appropriateness": 0}
    for r in results:
        for k, v in r["criteria_met"].items():
            if v:
                criteria_totals[k] += 1

    summary = {
        "individual_results": results,
        "aggregate_stats": {
            "average_score": round(sum(scores) / len(scores), 2),
            "min_score": min(scores),
            "max_score": max(scores),
            "total_time_seconds": round(total_time, 2),
            "total_cost_usd": round(total_cost, 6),
            "num_cases": len(results),
            "criteria_pass_counts": criteria_totals
        }
    }

    with open("evaluation_results.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("=== CRITERIA PERFORMANCE (out of {}) ===".format(len(results)))
    for k, v in criteria_totals.items():
        print(f"{k}: {v}/{len(results)}")

    print()
    print("=== SUMMARY ===")
    print(json.dumps(summary["aggregate_stats"], indent=2))