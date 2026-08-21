import json
import os
import time

from dotenv import load_dotenv
from openai import OpenAI


# ---------------------------------------------------------
# Environment and OpenAI client
# ---------------------------------------------------------

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ---------------------------------------------------------
# Test dataset
# ---------------------------------------------------------

test_cases = [
    {
        "id": "T1",
        "name": "Evidence Sufficiency",
        "prompt": """
A tender requirement states:

"Demonstrate experience delivering offshore wind projects
with a capacity greater than 100 MW."

The retrieved company evidence contains:

- NorthWind Farm — 48 MW
- SunVale Solar Park — 35 MW
- Coastal Wind Extension — 22 MW

Based only on the provided evidence, assess whether the
company can demonstrate experience with an offshore wind
project greater than 100 MW.

Do not introduce information that is not contained in
the evidence.
""",
        "candidate_response": """
INSUFFICIENT.

The provided evidence does not demonstrate experience with
an offshore wind project greater than 100 MW. The largest
project listed is NorthWind Farm at 48 MW.
"""
    },

    {
        "id": "T2",
        "name": "Evidence-Based Project Identification",
        "prompt": """
Using only the provided company evidence, identify the
project references relevant to renewable-energy experience.

For each project provide:
- Project name
- Technology
- Capacity

Evidence:

- NorthWind Farm — Wind — 48 MW
- SunVale Solar Park — Solar — 35 MW
- Coastal Wind Extension — Wind — 22 MW

Do not add information that is not contained in the evidence.
""",
        "candidate_response": """
Relevant projects:

1. NorthWind Farm — Wind — 48 MW
2. SunVale Solar Park — Solar — 35 MW
3. Coastal Wind Extension — Wind — 22 MW
"""
    },

    {
        "id": "T3",
        "name": "Multi-Document Reasoning",
        "prompt": """
Assess the following tender requirement:

The company must demonstrate:
1. Relevant quality certification.
2. Renewable-energy project experience.
3. Engineering and procurement support experience.

Evidence:

Document A:
The company has ISO 9001 certification.

Document B:
The company has renewable-energy project references.

Document C:
The company has engineering and procurement support
capabilities.

Identify which parts of the requirement are supported
and what evidence supports each part.
""",
        "candidate_response": """
The company has ISO 9001 certification and renewable-energy
project experience. However, there is insufficient evidence
to confirm engineering and procurement support experience.
"""
    },

    {
        "id": "T4",
        "name": "Instruction Following",
        "prompt": """
Assess the tender requirement using exactly these four
sections:

STATUS
EVIDENCE
GAP
RECOMMENDATION

Do not add any other sections.

Evidence:
The company has ISO 9001 certification relevant to the
requirement.
""",
        "candidate_response": """
STATUS: SUPPORTED

EVIDENCE: The company has ISO 9001 certification.

CONCLUSION: The requirement is therefore satisfied.
"""
    },

    {
        "id": "T5",
        "name": "Contradictory Evidence",
        "prompt": """
Two company documents contain conflicting information:

Document A:
Project X — 48 MW

Document B:
Project X — 120 MW

The tender requires experience with a project greater
than 100 MW.

Assess whether the company can currently claim that
Project X satisfies the requirement.

Identify the conflict and explain what should happen
before making the claim.
""",
        "candidate_response": """
Yes. Project X is 120 MW according to Document B, so the
company can claim that it has experience with a project
greater than 100 MW.
"""
    }
]


# ---------------------------------------------------------
# LLM-as-Judge function
# ---------------------------------------------------------

def evaluate_response(prompt, candidate_response):
    """Evaluate one candidate response and collect metrics."""

    start_time = time.perf_counter()

    judge_prompt = f"""
You are an evaluator for a Retrieval-Augmented Generation
(RAG) system used to analyze tender requirements.

Evaluate the candidate response against the original task
and supplied evidence.

ORIGINAL TASK:
{prompt}

CANDIDATE RESPONSE:
{candidate_response}

Evaluate these four criteria:

1. Evidence grounding:
Does the response rely only on the supplied evidence?

2. Correct compliance judgment:
Does the response correctly determine whether the
requirement is supported?

3. Hallucination avoidance:
Does the response avoid inventing information?

4. Explanation quality:
Does the response clearly explain its conclusion?

Score from 1 to 5:

1 = Very poor
2 = Poor
3 = Acceptable
4 = Good
5 = Excellent

Return ONLY JSON in this structure:

{{
    "score": 1,
    "reasoning": "Brief explanation",
    "criteria_met": {{
        "evidence_grounding": true,
        "correct_compliance_judgment": true,
        "hallucination_avoidance": true,
        "explanation_quality": true
    }}
}}
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=judge_prompt
    )

    evaluation_time = time.perf_counter() - start_time

    result_text = response.output_text.strip()

    # Remove Markdown code fences if the judge adds them.
    if result_text.startswith("```"):
        result_text = result_text.replace("```json", "", 1)
        result_text = result_text.replace("```", "", 1)
        result_text = result_text.strip()

    try:
        result = json.loads(result_text)

    except json.JSONDecodeError:
        print("The judge returned invalid JSON:")
        print(result_text)

        result = {
            "score": None,
            "reasoning": "Invalid JSON returned by judge.",
            "criteria_met": {}
        }

    # API usage information
    usage = getattr(response, "usage", None)

    input_tokens = getattr(usage, "input_tokens", None)
    output_tokens = getattr(usage, "output_tokens", None)
    total_tokens = getattr(usage, "total_tokens", None)

    result["evaluation_time_seconds"] = round(evaluation_time, 3)
    result["input_tokens"] = input_tokens
    result["output_tokens"] = output_tokens
    result["total_tokens"] = total_tokens

    return result


# ---------------------------------------------------------
# Run evaluation
# ---------------------------------------------------------

results = []

for test_case in test_cases:

    print(
        f"\nEvaluating {test_case['id']} — "
        f"{test_case['name']}"
    )

    result = evaluate_response(
        test_case["prompt"],
        test_case["candidate_response"]
    )

    result["id"] = test_case["id"]
    result["name"] = test_case["name"]

    results.append(result)

    print(f"Score: {result['score']}/5")
    print(f"Reasoning: {result['reasoning']}")
    print(
        f"Time: {result['evaluation_time_seconds']} seconds"
    )


# ---------------------------------------------------------
# Calculate summary
# ---------------------------------------------------------

valid_scores = [
    result["score"]
    for result in results
    if result["score"] is not None
]

if valid_scores:

    average_score = sum(valid_scores) / len(valid_scores)

    minimum_score = min(valid_scores)
    maximum_score = max(valid_scores)

else:

    average_score = None
    minimum_score = None
    maximum_score = None


total_time = sum(
    result["evaluation_time_seconds"]
    for result in results
)

total_input_tokens = sum(
    result["input_tokens"] or 0
    for result in results
)

total_output_tokens = sum(
    result["output_tokens"] or 0
    for result in results
)

total_tokens = sum(
    result["total_tokens"] or 0
    for result in results
)


# ---------------------------------------------------------
# Display summary
# ---------------------------------------------------------

print("\n===== EVALUATION SUMMARY =====")

print(f"Tests evaluated: {len(valid_scores)}")

if valid_scores:
    print(f"Average score: {average_score:.2f}/5")
    print(f"Minimum score: {minimum_score}/5")
    print(f"Maximum score: {maximum_score}/5")
else:
    print("No valid scores returned.")

print(f"Total evaluation time: {total_time:.3f} seconds")
print(f"Total input tokens: {total_input_tokens}")
print(f"Total output tokens: {total_output_tokens}")
print(f"Total tokens: {total_tokens}")


# ---------------------------------------------------------
# Save results
# ---------------------------------------------------------

summary = {
    "tests_evaluated": len(valid_scores),
    "average_score": (
        round(average_score, 2)
        if valid_scores
        else None
    ),
    "minimum_score": minimum_score,
    "maximum_score": maximum_score,
    "total_evaluation_time_seconds": round(
        total_time, 3
    ),
    "total_input_tokens": total_input_tokens,
    "total_output_tokens": total_output_tokens,
    "total_tokens": total_tokens
}


evaluation_output = {
    "project": "TenderAI",
    "model": "gpt-4o-mini",
    "evaluation_type": "LLM-as-Judge",
    "results": results,
    "summary": summary
}


with open(
    "evaluation_results.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        evaluation_output,
        file,
        indent=2,
        ensure_ascii=False
    )


print("\n===== RESULTS SAVED =====")
print("evaluation_results.json created successfully.")