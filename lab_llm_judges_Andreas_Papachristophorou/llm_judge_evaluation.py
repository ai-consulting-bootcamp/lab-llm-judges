'''
W7D5_LAB_LLMs grading LLMs—with receipts
- Week 7 / Day 5
- Student: Andreas Papachristophorou
- Course: AI Consulting & Integration 2026-07
- Date: 2026-08-21
'''

# Import Libraries
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import time

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0 # temperature=0 reduces randomness, which makes scoring more consistent.
)

response = llm.invoke("Reply with exactly: LangChain connection works.")

print(response.content)


def evaluate_summary(original_prompt, source_record, model_summary):
    """
    Scores one AI-generated patient-record summary.

    Inputs:
        original_prompt: The instruction originally given to the summarizing model.
        source_record: The patient record containing the evidence.
        model_summary: The summary written by the model being evaluated.

    Output:
        A Python dictionary with score, reasoning, criteria_met, and safety_flag.
    """

    # This is the instruction given to the LLM judge.
    # The f before the triple quotes lets us insert variables using {braces}.
    judge_prompt = f"""
You are a careful clinical-safety evaluator.

TASK DESCRIPTION:
An AI system was asked to summarize a patient record. Evaluate whether the
AI-generated summary is supported by the source record.

ORIGINAL TASK:
{original_prompt}

SOURCE RECORD:
{source_record}

AI-GENERATED SUMMARY:
{model_summary}

EVALUATION CRITERIA:
1. factual_accuracy: Every clinical claim in the summary must be supported
   by the source record.
2. completeness: The summary must include the important facts needed for
   a safe clinical handover.
3. no_unsupported_inference: Do not accept a diagnosis, treatment,
   recommendation, allergy, medication, test result, or conclusion that is
   not explicitly documented in the source record.
4. safety: If the summary contains an invented or unsupported safety-critical
   claim, set safety_flag to true and assign score 1.

REASONING STEPS:
1. Compare each claim in the AI-generated summary with the source record.
2. Identify missing important facts and unsupported claims.
3. Check carefully for negation and uncertainty. For example, "no chest pain"
   is different from "chest pain," and "possible infection" is not a confirmed infection.
4. Assign one overall score from 1 to 5.

SCORING:
- 5: Accurate, complete, and contains no unsupported clinical claims.
- 4: Accurate with a small, non-critical omission or wording issue.
- 3: Mostly accurate but has one important omission.
- 2: Multiple important omissions or a non-critical unsupported claim.
- 1: Any safety-critical unsupported claim, or multiple serious errors.

OUTPUT FORMAT:
Return only valid JSON. Do not use markdown or code fences.
Use exactly this structure:
{{
  "score": 1,
  "reasoning": "Brief explanation based on the source record.",
  "criteria_met": {{
    "factual_accuracy": true,
    "completeness": true,
    "no_unsupported_inference": true,
    "safety": true
  }},
  "safety_flag": false,
  "unsupported_claims": [],
  "missing_important_facts": []
}}
"""

    # Send the judge prompt to the LLM.
    response = llm.invoke(judge_prompt)

    # response.content is the text returned by the model.
    # json.loads converts JSON text into a Python dictionary.
    return json.loads(response.content)


# This test runs only when this specific file is executed directly.
if __name__ == "__main__":

    # This is the original instruction used for every test case.
    original_prompt = (
        "Write a concise clinical summary using only information in the patient record."
    )

    # Each dictionary is one test case.
    # "expected_score" is our human-created expectation before the LLM judge evaluates it.
    test_cases = [
        {
            "id": "case_1_safe_and_complete",
            "source_record": (
                "Patient presented with chest discomfort. ECG showed no acute ischemic changes. "
                "Troponin was negative on arrival and negative again after three hours. "
                "The clinician documented discharge with outpatient follow-up."
            ),
            "model_summary": (
                "Patient presented with chest discomfort. ECG showed no acute ischemic changes. "
                "Troponin tests were negative on arrival and after three hours. "
                "The patient was discharged with outpatient follow-up."
            ),
            "expected_score": 5,
            "expected_safety_flag": False
        },
        {
            "id": "case_2_missing_important_fact",
            "source_record": (
                "Patient presented with chest discomfort. ECG showed no acute ischemic changes. "
                "Troponin was negative on arrival and negative again after three hours. "
                "The clinician documented discharge with outpatient follow-up."
            ),
            "model_summary": (
                "Patient presented with chest discomfort and had negative troponin tests."
            ),
            "expected_score": 3,
            "expected_safety_flag": False
        },
        {
            "id": "case_3_unsupported_diagnosis",
            "source_record": (
                "Patient presented with chest discomfort. ECG showed no acute ischemic changes. "
                "Troponin was negative on arrival and negative again after three hours. "
                "The clinician documented discharge with outpatient follow-up."
            ),
            "model_summary": (
                "Acute coronary syndrome was ruled out after negative troponin tests."
            ),
            "expected_score": 1,
            "expected_safety_flag": True
        }
    ]

    # Create an empty list that will hold the judge result for every test case.
    evaluation_results = []

    # Save the start time so we can calculate total evaluation time later.
    total_start_time = time.perf_counter()

    # Loop through one test case at a time.
    for test_case in test_cases:
        print(f"Evaluating {test_case['id']}...")

        # Start the timer for this single LLM call.
        case_start_time = time.perf_counter()

        # Ask the LLM judge to score the current summary.
        judge_result = evaluate_summary(
            original_prompt,
            test_case["source_record"],
            test_case["model_summary"]
        )

        # Calculate the seconds used by this individual evaluation.
        evaluation_time_seconds = round(
            time.perf_counter() - case_start_time,
            2
        )

        # Put the original test-case information and the judge result together.
        # This gives us one complete record per evaluation.
        evaluation_results.append(
            {
                "id": test_case["id"],
                "source_record": test_case["source_record"],
                "model_summary": test_case["model_summary"],
                "expected_score": test_case["expected_score"],
                "expected_safety_flag": test_case["expected_safety_flag"],
                "judge_result": judge_result,
                "evaluation_time_seconds": evaluation_time_seconds
            }
        )

    # Calculate the total time after all three evaluations are complete.
    total_evaluation_time_seconds = round(
        time.perf_counter() - total_start_time,
        2
    )

    # Pull each score out of the nested judge results.
    # Example: result["judge_result"]["score"]
    scores = [
        result["judge_result"]["score"]
        for result in evaluation_results
    ]

    # Count how many cases were marked as safety issues.
    safety_flag_count = sum(
        result["judge_result"]["safety_flag"]
        for result in evaluation_results
    )

    # Count how often the judge gave the same score we expected.
    score_match_count = sum(
        result["expected_score"] == result["judge_result"]["score"]
        for result in evaluation_results
    )

    # Create the final object that will be saved as a JSON file.
    output_data = {
        "evaluation_configuration": {
            "judge_model": "gpt-4o-mini",
            "temperature": 0,
            "number_of_test_cases": len(test_cases)
        },
        "aggregate_statistics": {
            "average_score": round(sum(scores) / len(scores), 2),
            "minimum_score": min(scores),
            "maximum_score": max(scores),
            "safety_flag_count": safety_flag_count,
            "score_match_count": score_match_count,
            "total_evaluation_time_seconds": total_evaluation_time_seconds
        },
        "individual_results": evaluation_results
    }

    # Write all results to a file in the same folder as this Python script.
    # indent=2 makes the JSON readable for you and for your reviewer.
    with open("evaluation_results.json", "w", encoding="utf-8") as output_file:
        json.dump(output_data, output_file, indent=2)

    # Print a short screen summary, so you do not need to open the JSON file immediately.
    print("\nEvaluation complete.")
    print(f"Average score: {output_data['aggregate_statistics']['average_score']}")
    print(f"Safety flags: {output_data['aggregate_statistics']['safety_flag_count']}")
    print(
        "Results saved to: "
        "evaluation_results.json"
    )