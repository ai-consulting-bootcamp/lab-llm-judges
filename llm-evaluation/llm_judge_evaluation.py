import os
import json
import time

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# 1. SET UP OPENAI
# ============================================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY was not found. Check your .env file."
    )

client = OpenAI(api_key=api_key)

print("OpenAI client initialized successfully.")


# ============================================================
# 2. LLM-AS-JUDGE PROMPT
# ============================================================

JUDGE_PROMPT = """
You are evaluating an AI-generated summary of a patient's medical record.

Your task is to determine whether the summary is sufficiently accurate,
complete, and clinically safe for use by a physician taking over the
patient's care.

Evaluation Criteria:

1. Factual Accuracy:
The summary must accurately represent the source record. It must not
invent diagnoses, treatments, medication changes, test results, or
clinical events.

2. Critical Information Completeness:
The summary should preserve clinically important information, especially
diagnoses, abnormal laboratory results, treatments, medication changes,
and follow-up requirements.

3. Clinical Safety:
The summary must preserve information whose omission or alteration could
affect patient care. Medication instructions, abnormal results,
treatment changes, allergies, and follow-up requirements should receive
particular attention.

Scoring:

5 = Excellent: Accurate, complete, and clinically safe.
4 = Good: Minor issue that does not affect clinical interpretation or safety.
3 = Acceptable with concerns: Some relevant information is missing or imprecise.
2 = Poor: Important information is missing or incorrectly represented.
1 = Unsafe: Major factual errors or safety-critical omissions.

Reasoning Steps:

Step 1: Compare the generated summary against the original patient record.

Step 2: Identify important omissions or inaccuracies.

Step 3: Identify unsupported or contradictory claims.

Step 4: Determine whether any errors could affect clinical decision-making
or patient safety.

Return ONLY valid JSON in this format:

{
  "score": 1,
  "reasoning": "Brief explanation",
  "criteria_met": {
    "criterion_1": true,
    "criterion_2": true,
    "criterion_3": true
  }
}
"""


# ============================================================
# 3. EVALUATION FUNCTION
# ============================================================

def evaluate_response(original_prompt, model_response):

    judge_input = f"""
{JUDGE_PROMPT}

ORIGINAL TASK AND PATIENT RECORD:
{original_prompt}

CANDIDATE MODEL RESPONSE:
{model_response}
"""

    judge_response = client.responses.create(
        model="gpt-4o-mini",
        input=judge_input,
        text={
            "format": {
                "type": "json_schema",
                "name": "evaluation_result",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "score": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 5
                        },
                        "reasoning": {
                            "type": "string"
                        },
                        "criteria_met": {
                            "type": "object",
                            "properties": {
                                "criterion_1": {
                                    "type": "boolean"
                                },
                                "criterion_2": {
                                    "type": "boolean"
                                },
                                "criterion_3": {
                                    "type": "boolean"
                                }
                            },
                            "required": [
                                "criterion_1",
                                "criterion_2",
                                "criterion_3"
                            ],
                            "additionalProperties": False
                        }
                    },
                    "required": [
                        "score",
                        "reasoning",
                        "criteria_met"
                    ],
                    "additionalProperties": False
                }
            }
        }
    )

    result = json.loads(judge_response.output_text)

    return result


# ============================================================
# 4. TEST DATASET
# ============================================================

test_cases = [

    # --------------------------------------------------------
    # TEST 1 — ACCURACY
    # --------------------------------------------------------

    {
        "id": "test_01_accuracy",

        "prompt": """
Summarize the following patient record for a physician taking over
the patient's care.

Patient record:
A 67-year-old man with hypertension and type 2 diabetes was admitted
with three days of worsening shortness of breath and fever. Chest X-ray
showed right lower-lobe pneumonia. He was treated with IV ceftriaxone
and azithromycin and supplemental oxygen. Blood cultures were negative.
His oxygen requirement resolved by hospital day 3. He was transitioned
to oral amoxicillin-clavulanate and discharged home on hospital day 4.
Follow-up with his primary-care physician was recommended within one week.
""",

        "response": """
The patient is a 67-year-old man with hypertension and type 2 diabetes
who was admitted with pneumonia causing shortness of breath and fever.
Chest X-ray confirmed right lower-lobe pneumonia. He was treated with
IV ceftriaxone, azithromycin, and supplemental oxygen, with resolution
of his oxygen requirement. He was transitioned to oral
amoxicillin-clavulanate and discharged home on hospital day 4 with
primary-care follow-up recommended within one week.
"""
    },


    # --------------------------------------------------------
    # TEST 2 — COMPLETENESS
    # --------------------------------------------------------

    {
        "id": "test_02_completeness",

        "prompt": """
Summarize the following patient's hospital course for a physician
taking over the patient's care. Prioritize information that could
affect immediate clinical decisions.

Patient record:
A 74-year-old woman was admitted after a fall. CT head showed no acute
intracranial hemorrhage. Imaging revealed a left femoral neck fracture.
She underwent surgical fixation on hospital day 2. Her home warfarin
was held on admission because of an elevated INR of 4.2. Vitamin K was
administered. Her INR decreased to 1.4 before surgery. Warfarin was
restarted after surgery. She developed postoperative acute blood-loss
anemia with hemoglobin falling from 11.8 g/dL to 7.9 g/dL and received
one unit of packed red blood cells. At discharge, hemoglobin was 9.1 g/dL.
""",

        "response": """
The patient was admitted after a fall and found to have a left femoral
neck fracture. She underwent surgical fixation and was discharged after
recovering from the procedure. Her anticoagulation was managed during
the hospitalization, and she received treatment for postoperative anemia.
"""
    },


    # --------------------------------------------------------
    # TEST 3 — SAFETY
    # --------------------------------------------------------

    {
        "id": "test_03_safety",

        "prompt": """
Produce a concise discharge summary from the following record. Prioritize
information that could cause patient harm if omitted or incorrectly
summarized.

Patient record:
An 81-year-old patient with chronic kidney disease and heart failure
was admitted with worsening lower-extremity edema. Creatinine increased
from a baseline of 1.4 mg/dL to 2.1 mg/dL during admission. The patient
received IV furosemide with improvement in edema. Because of worsening
renal function, the ACE inhibitor was held during hospitalization.
At discharge, creatinine had improved to 1.7 mg/dL. The discharge
medication list explicitly states that the ACE inhibitor should remain
held pending outpatient renal function testing. Follow-up blood testing
was recommended within 3 days.
""",

        "response": """
The patient with chronic kidney disease and heart failure was admitted
with worsening edema and treated with IV furosemide. Renal function
improved during the admission. The ACE inhibitor was held because of
worsening renal function and should remain held after discharge pending
follow-up blood testing within 3 days.
"""
    },


    # --------------------------------------------------------
    # TEST 4 — MEDICAL TERMINOLOGY
    # --------------------------------------------------------

    {
        "id": "test_04_terminology",

        "prompt": """
Summarize this patient record for a physician. Preserve important
medical terminology and clinically significant findings.

Patient record:
A 59-year-old woman with a history of atrial fibrillation and
hyperlipidemia presented with sudden-onset right-sided weakness and
expressive aphasia. CT head showed no intracranial hemorrhage.
CTA demonstrated a left middle cerebral artery occlusion. She received
intravenous thrombolysis followed by mechanical thrombectomy with
successful reperfusion. MRI subsequently demonstrated a small left
MCA territory infarct. Neurology recommended continuation of
anticoagulation for atrial fibrillation after the appropriate
post-stroke interval.
""",

        "response": """
A 59-year-old woman with an irregular heartbeat and high cholesterol
developed sudden weakness on the right side and difficulty speaking.
Brain imaging showed a blockage in a blood vessel supplying the brain.
She received clot-busting medication and a procedure to remove the
clot. Further imaging showed a small stroke. Her doctors recommended
continuing blood-thinning medication.
"""
    },


    # --------------------------------------------------------
    # TEST 5 — SAFETY-CRITICAL OMISSION
    # --------------------------------------------------------

    {
        "id": "test_05_safety_critical",

        "prompt": """
Create a concise summary for a physician reviewing the patient's
discharge record. Do not omit information that could affect immediate
patient safety.

Patient record:
A 45-year-old woman was admitted with pyelonephritis and treated with
IV antibiotics. Urine culture grew an ESBL-producing E. coli resistant
to ceftriaxone but susceptible to ertapenem. Antibiotics were changed
to ertapenem. She improved clinically and was discharged with a
7-day course of oral antibiotics according to the infectious disease
team's recommendations. She has a documented severe penicillin allergy
with a previous episode of anaphylaxis.
""",

        "response": """
A 45-year-old woman was hospitalized with a kidney infection and treated
with antibiotics. She improved clinically and was discharged to complete
a 7-day course of antibiotics. Follow-up with her physician was
recommended.
"""
    }
]


# ============================================================
# 5. RUN EVALUATION
# ============================================================

results = []

for test_case in test_cases:

    print(f"\nEvaluating {test_case['id']}...")

    start_time = time.perf_counter()

    result = evaluate_response(
        test_case["prompt"],
        test_case["response"]
    )

    elapsed_time = time.perf_counter() - start_time

    results.append({
        "id": test_case["id"],
        "score": result["score"],
        "reasoning": result["reasoning"],
        "criteria_met": result["criteria_met"],
        "time_seconds": round(elapsed_time, 3)
    })

    print(json.dumps(result, indent=2))
    print(f"Time: {elapsed_time:.3f} seconds")


# ============================================================
# 6. CALCULATE SUMMARY METRICS
# ============================================================

scores = [result["score"] for result in results]
times = [result["time_seconds"] for result in results]

criterion_counts = {
    "criterion_1_factual_accuracy": 0,
    "criterion_2_completeness": 0,
    "criterion_3_clinical_safety": 0
}

for result in results:

    if result["criteria_met"]["criterion_1"]:
        criterion_counts["criterion_1_factual_accuracy"] += 1

    if result["criteria_met"]["criterion_2"]:
        criterion_counts["criterion_2_completeness"] += 1

    if result["criteria_met"]["criterion_3"]:
        criterion_counts["criterion_3_clinical_safety"] += 1


summary = {
    "number_of_tests": len(results),
    "average_score": round(sum(scores) / len(scores), 2),
    "minimum_score": min(scores),
    "maximum_score": max(scores),
    "total_time_seconds": round(sum(times), 3),
    "average_time_seconds": round(sum(times) / len(times), 3),
    "criteria_met_counts": criterion_counts
}


# ============================================================
# 7. SAVE RESULTS
# ============================================================

final_results = {
    "test_cases": results,
    "summary": summary
}

with open("results.json", "w") as f:
    json.dump(final_results, f, indent=2)


# ============================================================
# 8. PRINT SUMMARY
# ============================================================

print("\n========================================")
print("EVALUATION SUMMARY")
print("========================================")

print(json.dumps(summary, indent=2))

print("\nResults saved to results.json")