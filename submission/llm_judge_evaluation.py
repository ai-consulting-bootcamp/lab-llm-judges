import os
import json
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"

JUDGE_SYSTEM_PROMPT = """You are an evaluation judge assessing an LLM-generated 
negotiation-prep summary for a should-cost analysis.

Task Description:
The model was given a should-cost breakdown (which may have all fields 
present, or may have one or more fields missing/marked N/A/ambiguous) and 
asked to write a negotiation-prep summary. Correct behavior depends on the 
input: if data is complete, the summary should use it confidently; if any 
field is missing or ambiguous, the summary must explicitly flag that gap 
and avoid presenting any total or conclusion that silently depends on the 
missing data as if it were confirmed fact.

Evaluation Criteria:
1. Gap Acknowledgment: First determine from the ORIGINAL PROMPT whether any 
   cost field was actually missing, N/A, or genuinely ambiguous. If yes, 
   does the summary explicitly acknowledge that gap? If no fields were 
   missing, this criterion is automatically met (nothing to acknowledge).
2. No Fabricated Totals: Does the summary avoid stating a specific total or 
   gap figure that relies on data NOT present in the original prompt? If 
   all needed data was present and the total is arithmetically correct, 
   this criterion is met.
3. Actionable Despite Gap: Does the summary give the buyer something useful 
   to act on, whether or not data was missing?

Reasoning Steps:
Step 1: Re-read the ORIGINAL PROMPT and list which cost fields were 
        actually provided vs. missing/ambiguous.
Step 2: Compare that against what the summary claims. Flag any total or 
        gap figure in the summary that uses a field you determined was 
        missing in Step 1.
Step 3: Check whether missing fields (if any) were explicitly named in the 
        summary, and whether the summary still gave actionable guidance.

Respond ONLY with valid JSON in this exact format, no other text:
{
  "score": <float 0-1>,
  "reasoning": "<explanation of the score, including what data you determined was present vs. missing>",
  "criteria_met": {
    "gap_acknowledgment": <true/false>,
    "no_fabricated_totals": <true/false>,
    "actionable_despite_gap": <true/false>
  }
}
"""

def judge_response(original_prompt: str, model_response: str) -> dict:
    """Evaluates a model's should-cost summary using the LLM-as-judge 
    criteria from Step 4. Returns a dict with score, reasoning, and 
    per-criterion pass/fail."""
    
    user_message = f"""Original prompt given to the model:
{original_prompt}

Model's response to evaluate:
{model_response}

Evaluate this response according to the criteria above."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        response_format={"type": "json_object"},
        temperature=0
    )
    
    result = json.loads(response.choices[0].message.content)
    return result

TEST_CASES = [
    {
        "id": "prompt_1_baseline",
        "prompt": "Given this should-cost breakdown for a stamped bracket [material: $2.10/unit, labor: $1.85/unit, overhead: $0.95/unit, freight: $0.40/unit, total should-cost: $5.30/unit vs. supplier quote: $6.75/unit], write a 3-sentence negotiation-prep summary identifying the top cost driver and the gap to target.",
        "ground_truth": "Top driver: material ($2.10). Gap: $1.45/unit (27% over should-cost).",
        "expected_criteria": ["correct_driver", "correct_gap"]
    },
    {
        "id": "prompt_2_missing_data",
        "prompt": "Given this should-cost breakdown where freight cost is missing/unknown [material: $2.10, labor: $1.85, overhead: $0.95, freight: N/A, supplier quote: $6.75], write a negotiation-prep summary.",
        "ground_truth": None,
        "expected_criteria": ["gap_acknowledgment", "no_fabricated_totals", "actionable_despite_gap"]
    },
    {
        "id": "prompt_3_ambiguous_ranking",
        "prompt": "Given a should-cost breakdown with two closely-priced components [tooling amortization: $1.42/unit, material: $1.38/unit, labor: $1.10/unit], identify and justify the primary cost driver for negotiation focus.",
        "ground_truth": "Tooling amortization is marginally higher, but the two are close enough to warrant hedged confidence.",
        "expected_criteria": ["correct_identification", "appropriate_hedging"]
    },
    {
        "id": "prompt_4_tone",
        "prompt": "Rewrite this raw analyst note into negotiation-ready language: 'Supplier is charging way too much for labor, basically robbing us, need to hammer them on this.'",
        "ground_truth": None,
        "expected_criteria": ["professional_tone", "retains_factual_claim"]
    },
    {
        "id": "prompt_5_multicurrency",
        "prompt": "Given a should-cost calc where material is priced in EUR (€1.85, converted at 1.08 USD/EUR), labor in USD ($1.90), and freight quoted in a mixed incoterm (FOB Shanghai, buyer pays freight separately at $0.55/unit), write a summary of total landed cost per unit in USD and flag any assumptions made.",
        "ground_truth": "Total ≈ $4.45/unit (material $2.00 + labor $1.90 + freight $0.55). Should flag FOB/freight-responsibility assumption.",
        "expected_criteria": ["correct_arithmetic", "flags_assumption"]
    }
]

def generate_response(prompt: str) -> str:
    """Generates a model response for a given should-cost prompt using 
    the same model that would be used in production."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

def run_evaluation():
    """Runs all test cases through generate → judge, collecting scores, 
    timing, and token usage. Saves results to evaluation_results.json."""
    
    results = []
    total_start = time.time()

    for case in TEST_CASES:
        print(f"Running: {case['id']}...")
        
        gen_start = time.time()
        model_response = generate_response(case["prompt"])
        gen_time = time.time() - gen_start

        judge_start = time.time()
        judgment = judge_response(case["prompt"], model_response)
        judge_time = time.time() - judge_start

        results.append({
            "id": case["id"],
            "prompt": case["prompt"],
            "model_response": model_response,
            "ground_truth": case["ground_truth"],
            "score": judgment["score"],
            "reasoning": judgment["reasoning"],
            "criteria_met": judgment["criteria_met"],
            "generation_time_sec": round(gen_time, 2),
            "judge_time_sec": round(judge_time, 2)
        })

    total_time = time.time() - total_start
    scores = [r["score"] for r in results]

    summary = {
        "individual_results": results,
        "aggregate": {
            "average_score": round(sum(scores) / len(scores), 3),
            "min_score": min(scores),
            "max_score": max(scores),
            "total_time_sec": round(total_time, 2),
            "num_cases": len(results)
        }
    }

    with open("evaluation_results.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return summary


if __name__ == "__main__":
    summary = run_evaluation()
    print(json.dumps(summary["aggregate"], indent=2))