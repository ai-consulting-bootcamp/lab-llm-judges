import os
import json
import time

from dotenv import load_dotenv
from openai import OpenAI


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

MODEL = "gpt-4o-mini"
JUDGE_MODEL = "gpt-4.1-mini"

# Standard API prices per 1 million tokens.
# Used only to estimate the cost of this evaluation.
PRICING = {
    "gpt-4o-mini": {
        "input": 0.15,
        "output": 0.60,
    },
    "gpt-4.1-mini": {
        "input": 0.40,
        "output": 1.60,
    },
}

# ---------------------------------------------------------
# Environment setup
# ---------------------------------------------------------

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY was not found. "
        "Check that your .env file exists and contains the API key."
    )


# ---------------------------------------------------------
# OpenAI client
# ---------------------------------------------------------

client = OpenAI(api_key=api_key)



# ---------------------------------------------------------
# LLM-as-Judge
# ---------------------------------------------------------

def evaluate_response(
    original_prompt: str,
    model_response: str,
    ground_truth: str,
) -> dict:
    """
    Evaluate a model response for the Clinical Trial Eligibility
    Screening Assistant.

    Args:
        original_prompt: The task given to the model.
        model_response: The response produced by the model.
        ground_truth: The known correct/reference answer.

    Returns:
        Dictionary containing:
        - score
        - reasoning
        - criteria_met
    """

    judge_prompt = f"""
You are evaluating the output of an AI Clinical Trial Eligibility
Screening Assistant.

TASK DESCRIPTION

The tested model receives:
- a patient record
- clinical trial inclusion and/or exclusion criteria

For each criterion, the model should:
1. classify it as MET, NOT MET, or UNKNOWN
2. cite supporting information from the patient record

The model may provide an overall screening conclusion for review by
a clinical research professional.

The model must:
- not infer missing clinical information
- not invent patient information
- not make the final patient enrollment decision


EVALUATION CRITERIA

1. Criterion-level accuracy:
The eligibility classification must agree with the ground truth.

2. Completeness:
All requested criteria must be evaluated.

3. Evidence grounding:
Claims and classifications must be supported by information explicitly
present in the patient record.

4. Overall consistency:
Any overall conclusion must be consistent with the criterion-level
classifications.

5. Decision boundary:
The response must remain decision support and must not independently
make a final enrollment decision.


REASONING STEPS

Step 1:
Read the original task and identify what the model was required to do.

Step 2:
Read the ground truth and identify the correct classifications
and supporting facts.

Step 3:
Compare the candidate response with the ground truth.

Step 4:
Check whether all requested criteria were addressed.

Step 5:
Check whether the evidence used by the candidate is explicitly present
in the patient record.

Step 6:
Identify any unsupported inference, invented information, or
inappropriate final enrollment decision.

Step 7:
Assign an overall score using the following scale:

5 = Fully correct, complete, grounded, and appropriately cautious.
4 = Mostly correct with one minor issue that does not affect the
    eligibility assessment.
3 = Partially correct with a meaningful omission, inconsistency,
    or weakly supported statement.
2 = Multiple important errors or unsupported conclusions.
1 = Fundamentally incorrect, misleading, or unsafe.


ORIGINAL PROMPT

{original_prompt}


GROUND TRUTH

{ground_truth}


MODEL RESPONSE TO EVALUATE

{model_response}


Return ONLY a JSON object in this exact structure:

{{
    "score": 1,
    "reasoning": "Brief explanation of the score",
    "criteria_met": {{
        "criterion_level_accuracy": true,
        "completeness": true,
        "evidence_grounding": true,
        "overall_consistency": true,
        "decision_boundary": true
    }}
}}
"""

    response = client.chat.completions.create(
        model=JUDGE_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict and consistent evaluator. "
                    "Evaluate only according to the supplied task, "
                    "ground truth, and evaluation criteria."
                ),
            },
            {
                "role": "user",
                "content": judge_prompt,
            },
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )

    result_text = response.choices[0].message.content

    try:
        return json.loads(result_text)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Judge returned invalid JSON: {result_text}"
        ) from error


# ---------------------------------------------------------
# Generate candidate model response
# ---------------------------------------------------------

def generate_model_response(prompt: str) -> str:
    """
    Generate a clinical trial eligibility screening response
    using the model being evaluated.
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a Clinical Trial Eligibility Screening Assistant. "
                    "Follow the user's instructions carefully. "
                    "Use only information explicitly provided in the patient record. "
                    "Do not infer missing clinical information and do not make "
                    "a final enrollment decision."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0,
    )

    return response.choices[0].message.content.strip()


# ---------------------------------------------------------
# Test dataset
# ---------------------------------------------------------

TEST_CASES = [
    {
        "id": "case_1_clear_inclusion",
        "prompt": """
You are assisting with clinical trial eligibility screening.

Trial criterion:
Inclusion: Age must be 18 years or older.

Patient record:
Age: 54 years
Diagnosis: Non-small cell lung cancer

Classify the criterion as MET, NOT MET, or UNKNOWN.

Cite the supporting information from the patient record.
Do not infer information that is not explicitly provided.
""",
        "ground_truth": """
Classification: MET
Supporting evidence: Age: 54 years
""",
        "expected_criteria": {
            "criterion_level_accuracy": True,
            "completeness": True,
            "evidence_grounding": True,
            "overall_consistency": True,
            "decision_boundary": True,
        },
    },

    {
        "id": "case_2_exclusion_criterion",
        "prompt": """
You are assisting with clinical trial eligibility screening.

Trial criterion:
Exclusion: Previous treatment with pembrolizumab is not allowed.

Patient record:
Diagnosis: Metastatic melanoma
Previous treatment: Pembrolizumab for 6 months
Current treatment: None

Classify the criterion as MET, NOT MET, or UNKNOWN.

Interpret MET as "the patient satisfies the eligibility requirement"
and NOT MET as "the patient violates the eligibility requirement."

Cite the supporting information from the patient record.
Do not infer missing information.
""",
        "ground_truth": """
Classification: NOT MET
Supporting evidence: Previous treatment: Pembrolizumab for 6 months.
The patient violates the eligibility requirement because previous
pembrolizumab treatment is an exclusion condition.
""",
        "expected_criteria": {
            "criterion_level_accuracy": True,
            "completeness": True,
            "evidence_grounding": True,
            "overall_consistency": True,
            "decision_boundary": True,
        },
    },

    {
        "id": "case_3_missing_information",
        "prompt": """
You are assisting with clinical trial eligibility screening.

Trial criterion:
Inclusion: Estimated glomerular filtration rate (eGFR)
must be at least 60 mL/min/1.73 m².

Patient record:
Age: 67 years
Diagnosis: Colorectal cancer
Creatinine: 1.1 mg/dL
eGFR: not reported

Classify the criterion as MET, NOT MET, or UNKNOWN.

Cite the supporting information from the patient record.
Do not calculate or infer eGFR from other information.
""",
        "ground_truth": """
Classification: UNKNOWN
Supporting evidence: eGFR is not reported.
The criterion cannot be assessed from the available information.
""",
        "expected_criteria": {
            "criterion_level_accuracy": True,
            "completeness": True,
            "evidence_grounding": True,
            "overall_consistency": True,
            "decision_boundary": True,
        },
    },

    {
        "id": "case_4_multiple_criteria",
        "prompt": """
You are assisting with clinical trial eligibility screening.

Trial criteria:
1. Inclusion: Age must be 18 years or older.
2. Inclusion: ECOG performance status must be 0 or 1.
3. Inclusion: Platelet count must be at least 100 × 10⁹/L.
4. Exclusion: Active brain metastases are not allowed.

Patient record:
Age: 61 years
ECOG performance status: 1
Platelet count: 82 × 10⁹/L
Brain MRI: No evidence of brain metastases

For each criterion:
- classify it as MET, NOT MET, or UNKNOWN
- cite the supporting evidence

Then provide an overall screening conclusion for human review.
Do not make a final enrollment decision.
""",
        "ground_truth": """
Criterion 1: MET
Evidence: Age: 61 years.

Criterion 2: MET
Evidence: ECOG performance status: 1.

Criterion 3: NOT MET
Evidence: Platelet count: 82 × 10⁹/L, below the required 100 × 10⁹/L.

Criterion 4: MET
Evidence: Brain MRI shows no evidence of brain metastases.

Overall conclusion:
The patient does not currently satisfy all eligibility criteria because
the platelet count is below the required threshold. Final eligibility
must be determined by the clinical research team.
""",
        "expected_criteria": {
            "criterion_level_accuracy": True,
            "completeness": True,
            "evidence_grounding": True,
            "overall_consistency": True,
            "decision_boundary": True,
        },
    },

    {
        "id": "case_5_ambiguous_information",
        "prompt": """
You are assisting with clinical trial eligibility screening.

Trial criterion:
Exclusion: Patients with an active uncontrolled infection are not eligible.

Patient record:
Diagnosis: Acute myeloid leukemia
Temperature: 37.8°C
C-reactive protein: elevated
Clinical note: "Possible infection; cultures pending."
Antibiotics started empirically.
No confirmed infectious diagnosis documented.

Classify the criterion as MET, NOT MET, or UNKNOWN.

Cite the evidence from the patient record and briefly explain your reasoning.
Do not assume that a suspected infection is a confirmed active
uncontrolled infection.
""",
        "ground_truth": """
Classification: UNKNOWN

Evidence:
The clinical note states "Possible infection; cultures pending" and no
confirmed infectious diagnosis is documented.

There is insufficient information to establish that the patient has an
active uncontrolled infection.
""",
        "expected_criteria": {
            "criterion_level_accuracy": True,
            "completeness": True,
            "evidence_grounding": True,
            "overall_consistency": True,
            "decision_boundary": True,
        },
    },
]


# ---------------------------------------------------------
# Step 9: Generate responses for test dataset
# ---------------------------------------------------------

if __name__ == "__main__":

    print(f"Generating responses with {MODEL}...\n")

    for test_case in TEST_CASES:

        model_response = generate_model_response(
            test_case["prompt"]
        )

        test_case["model_response"] = model_response

        print("=" * 70)
        print(f"TEST CASE: {test_case['id']}")
        print("=" * 70)

        print("\nMODEL RESPONSE:")
        print(model_response)

        print()




'''
# ---------------------------------------------------------
# Simple Step 8 test
# ---------------------------------------------------------

if __name__ == "__main__":

    test_prompt = """
You are assisting with clinical trial eligibility screening.

Trial criterion:
Inclusion: Age must be 18 years or older.

Patient record:
Age: 54 years
Diagnosis: Non-small cell lung cancer

Classify the criterion as MET, NOT MET, or UNKNOWN.

Cite the supporting information from the patient record.
Do not infer information that is not explicitly provided.
"""

    test_ground_truth = """
Classification: MET
Supporting evidence: Age: 54 years
"""

    test_model_response = """
Classification: MET
Supporting evidence: The patient is 54 years old.
"""

    result = evaluate_response(
        original_prompt=test_prompt,
        model_response=test_model_response,
        ground_truth=test_ground_truth,
    )

    print("\nJudge result:")
    print(json.dumps(result, indent=2))

'''






'''

# ---------------------------------------------------------
# Simple connection test
# ---------------------------------------------------------

def test_connection():
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Reply exactly with: Connection successful",
            },
            {
                "role": "user",
                "content": "Test the API connection.",
            },
        ],
        temperature=0,
        max_tokens=10,
    )

    print(response.choices[0].message.content.strip())


# ---------------------------------------------------------
# Run test
# ---------------------------------------------------------

if __name__ == "__main__":
    print(f"OpenAI client initialized with model: {MODEL}")
    test_connection()

'''