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

    # The original instruction given to the summarization model.
    test_original_prompt = (
        "Write a concise clinical summary using only information in the patient record."
    )

    # The source record is the evidence the judge must use.
    test_source_record = (
        "Patient presented with chest discomfort. ECG showed no acute ischemic changes. "
        "Troponin was negative on arrival and negative again after three hours. "
        "The clinician documented discharge with outpatient follow-up."
    )

    # This intentionally unsafe summary tests whether the judge catches
    # an unsupported diagnostic conclusion.
    test_model_summary = (
        "The patient had acute coronary syndrome ruled out after negative troponin tests."
    )

    # Call the function and store its dictionary result.
    result = evaluate_summary(
        test_original_prompt,
        test_source_record,
        test_model_summary
    )

    # Print the result in an easy-to-read, indented JSON format.
    print(json.dumps(result, indent=2))