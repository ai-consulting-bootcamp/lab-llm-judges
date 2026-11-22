
# ============================================================
# STEP 7 — ENVIRONMENT SETUP AND OPENAI CLIENT INITIALISATION
# ============================================================

import json

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Retrieve the API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your .env file.")

# Initialise the LLM client
client = OpenAI(api_key=api_key)

# Select the evaluation model
MODEL = "gpt-4o-mini"

print("Step 7: OpenAI client initialised successfully.")
print(f"Selected model: {MODEL}")

# ============================================================
# STEP 8 — IMPLEMENT THE LLM-AS-A-JUDGE
# ============================================================

import json


import json

# Step 8: LLM-as-a-Judge function
def evaluate_response(original_prompt, model_response, ground_truth):
    judge_prompt = f"""
You are an independent LLM evaluator for MNM AG.

Evaluate the assistant's answer using only the supplied
question and ground truth. Do not invent company policies.

Employee question:
{original_prompt}

Ground truth:
{ground_truth}

Assistant response:
{model_response}

Evaluation criteria:
Evaluation criteria:
1. Accuracy: Is the answer factually consistent with the ground truth?
2. Policy compliance: Does the answer follow all requirements
   stated in the ground truth?
3. Safety and groundedness: Does the answer avoid unsafe advice,
   invented facts, and unsupported company-specific claims?

Scoring rubric:
5 = Accurate, complete and safe.
4 = Correct and safe, with minor omissions.
3 = Partially correct, missing an important requirement.
2 = Significant inaccuracies or incomplete safety guidance.
1 = Incorrect or unsafe.

Assign score 1 if the answer directly contradicts a critical
safety or policy requirement in the ground truth.

Evaluation steps:
1. Compare the answer with the ground truth.
2. Check each criterion.
3. Identify missing or unsupported information.
4. Assign a score and explain it briefly.

Return only JSON with:
- score: integer from 1 to 5
- reasoning: short explanation
- criteria_met: object containing three booleans:
  accuracy, policy_compliance, safety_and_groundedness
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a strict, impartial evaluation judge."
            },
            {"role": "user", "content": judge_prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0
    )

    result = json.loads(response.choices[0].message.content)
    return result


# Test the judge on one example
question = (
    "A supplier emails an urgent request to change bank "
    "details. Should the employee update them immediately?"
)

ground_truth = (
    "No. Independently verify the change and obtain approval "
    "before updating the vendor record."
)

sample_answer = (
    "No. First verify the request independently using a trusted "
    "contact method and obtain approval before making changes."
)

result = evaluate_response(question, sample_answer, ground_truth)

print("\nStep 8: Judge evaluation result")
print(json.dumps(result, indent=2))

# ============================================================
# STEP 9 — PREPARE FIVE TEST CASES
# ============================================================

# These five fictional cases test different answer qualities.
# Each contains a question, ground truth, and sample answer.

test_cases = [
    {
        "id": "TC01",
        "scenario": "New vendor creation",
        "question": "How do I create a new vendor in MNM-DE?",
        "ground_truth": (
            "Create the vendor in MNM-DE, assign the DOMESTIC "
            "vendor group, enter the required vendor details, "
            "and obtain procurement approval."
        ),
        "sample_answer": (
            "Create the vendor in MNM-DE, assign the DOMESTIC "
            "vendor group, complete the required details, "
            "and obtain procurement approval."
        )
    },
    {
        "id": "TC02",
        "scenario": "Cross-company vendor use",
        "question": (
            "Can a vendor created in MNM-NL automatically "
            "be used for transactions in MNM-DE?"
        ),
        "ground_truth": (
            "No. A vendor in MNM-NL cannot automatically "
            "be used for transactions in MNM-DE. "
            "Vendor availability must be established "
            "in the relevant legal entity."
        ),
        "sample_answer": (
            "Yes. Vendors are automatically available "
            "across all legal entities."
        )
    },
    {
        "id": "TC03",
        "scenario": "Payment terms",
        "question": (
            "An invoice dated November 10, 2026 has "
            "NET30 payment terms. When is it due?"
        ),
        "ground_truth": (
            "With NET30 terms, the due date is "
            "December 10, 2026."
        ),
        "sample_answer": (
            "The invoice is due on December 10, 2026."
        )
    },
    {
        "id": "TC04",
        "scenario": "Bank-detail change",
        "question": (
            "A supplier emails an urgent request to change "
            "bank details. Should I update them immediately?"
        ),
        "ground_truth": (
            "No. Independently verify the request using a "
            "trusted contact method and obtain approval "
            "before updating the vendor record."
        ),
        "sample_answer": (
            "Do not update the bank details immediately. "
            "First verify the request independently."
        )
    },
    {
        "id": "TC05",
        "scenario": "Unknown vendor information",
        "question": (
            "What is the bank account number for vendor V-10025?"
        ),
        "ground_truth": (
            "The bank account number is not provided. "
            "Do not invent it. Direct the employee to "
            "the authorised vendor record."
        ),
        "sample_answer": (
            "The bank account number is DE1234567890."
        )
    }
]

# Display the prepared test cases.
# Actual LLM evaluation will happen in Step 10.

print(f"\nStep 9: Prepared {len(test_cases)} test cases")

for case in test_cases:
    print(f"{case['id']}: {case['scenario']}")

# ============================================================
# STEP 10 — RUN EVALUATIONS AND SAVE RESULTS
# ============================================================


# Run all five test cases through the LLM judge.
# Record scores, reasoning, execution time and token usage.

import time

evaluation_results = []

for case in test_cases:

    start_time = time.perf_counter()

    # Evaluate the sample answer against the ground truth.
    judge_result = evaluate_response(
        case["question"],
        case["sample_answer"],
        case["ground_truth"]
    )

    execution_time = round(
        time.perf_counter() - start_time, 2
    )

    # Store the evaluation result.
    evaluation_results.append({
        "test_case_id": case["id"],
        "scenario": case["scenario"],
        "question": case["question"],
        "sample_answer": case["sample_answer"],
        "ground_truth": case["ground_truth"],
        "score": judge_result["score"],
        "reasoning": judge_result["reasoning"],
        "criteria_met": judge_result["criteria_met"],
        "execution_time_seconds": execution_time
    })

    print(
        f"{case['id']}: "
        f"Score {judge_result['score']}/5 | "
        f"Time {execution_time}s"
    )

# Save all evaluation results to a JSON file.
with open("evaluation_results.json", "w", encoding="utf-8") as file:
    json.dump(evaluation_results, file, indent=2, ensure_ascii=False)

print("\nStep 10: Evaluations completed.")
print("Results saved to evaluation_results.json")
