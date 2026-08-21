# W7D5_LAB_LLMs grading LLMs—with receipts
- Week 7 / Day 5
- Student: Andreas Papachristophorou
- Course: AI Consulting & Integration 2026-07
- Date: 2026-08-21
---

# Output

```
python llm_judge_evaluation.py
LangChain connection works.
Evaluating case_1_safe_and_complete...
Evaluating case_2_missing_important_fact...
Evaluating case_3_unsupported_diagnosis...

Evaluation complete.
Average score: 3.0
Safety flags: 1
Results saved to: evaluation_results.json

==================================================
EVALUATION ANALYSIS
==================================================

Individual results:

- case_1_safe_and_complete
  Score: 5 / 5
  Safety flag: False
  Time: 3.32 seconds
  Cost: $0.00015075
  Reasoning: The AI-generated summary accurately reflects the information in the source record, including the patient's presentation, ECG results, troponin tests, and discharge plan. All claims are supported by the source record.

- case_2_missing_important_fact
  Score: 3 / 5
  Safety flag: False
  Time: 2.11 seconds
  Cost: $0.00016590
  Reasoning: The summary accurately states that the patient presented with chest discomfort and had negative troponin tests. However, it omits important details such as the ECG findings and the clinician's documentation of discharge with outpatient follow-up, which are critical for a complete clinical handover.

- case_3_unsupported_diagnosis
  Score: 1 / 5
  Safety flag: True
  Time: 2.07 seconds
  Cost: $0.00016485
  Reasoning: The AI-generated summary states that 'acute coronary syndrome was ruled out,' which is an unsupported conclusion not explicitly documented in the source record. The record indicates that troponin tests were negative, but it does not confirm that acute coronary syndrome was definitively ruled out. This represents a safety-critical unsupported claim.

Score distribution:
  Score 1: 1 case(s)
  Score 2: 0 case(s)
  Score 3: 1 case(s)
  Score 4: 0 case(s)
  Score 5: 1 case(s)

Criteria performance:
  factual_accuracy: 2 / 3 cases met
  completeness: 2 / 3 cases met
  no_unsupported_inference: 2 / 3 cases met
  safety: 2 / 3 cases met

Time and cost metrics:
  Total time: 7.5 seconds
  Average time per case: 2.50 seconds
  Total input tokens: 1542
  Total output tokens: 417
  Total estimated cost: $0.00048150

Key insight:
The judge detected at least one safety-critical unsupported claim. This supports mandatory clinician review before deployment.

```

# Implementation Summary

I built an LLM-as-a-judge evaluation pipeline in Python using LangChain, `ChatOpenAI`, and the `gpt-4o-mini` model. The pipeline evaluates AI-generated clinical summaries against a source patient record. The judge uses a structured rubric covering factual accuracy, completeness, unsupported inferences, and safety. It returns a JSON result containing a score from 1 to 5, a brief explanation, criterion-level pass/fail assessments, a safety flag, unsupported claims, and missing important facts. The implementation was tested on three synthetic clinical-summary cases: a complete and supported summary, an incomplete summary, and a summary containing an unsupported diagnostic conclusion.

The evaluation loop recorded each case’s score, safety result, response time, input and output tokens, and estimated API cost, then saved detailed results and aggregate statistics to `evaluation_results.json`. The three cases received scores of 5, 3, and 1, producing an average score of 3.0 out of 5. The pipeline detected one safety-critical unsupported claim in the third case, where the summary incorrectly stated that acute coronary syndrome had been ruled out even though the source record only documented negative troponin results. The complete summary met all requirements, while the incomplete summary omitted the ECG findings and discharge plan. Across all three evaluations, total runtime was 7.5 seconds, average runtime was 2.50 seconds per case, total token usage was 1,542 input tokens and 417 output tokens, and the estimated total cost was $0.00048150.

These results show that the LLM judge can distinguish between a supported summary, an incomplete summary, and a safety-critical unsupported conclusion in this small test set. However, this is a demonstration rather than a clinical validation study: the test cases were synthetic and limited to three examples. Before deployment in a healthcare setting, the evaluation should be expanded with representative de-identified records, reviewed by qualified clinicians, and calibrated against human ratings. The detected safety flag supports mandatory clinician review before any clinical summary is used in practice.