# TenderAI LLM-as-Judge Evaluation — Implementation Summary

## What We Built

We implemented a small LLM-as-Judge evaluation pipeline for TenderAI, a Retrieval-Augmented Generation (RAG) system designed to assess tender requirements using company evidence. The evaluator uses `gpt-4o-mini` as the judge and evaluates candidate responses against four criteria: evidence grounding, correctness of the compliance judgment, hallucination avoidance, and explanation quality.

The evaluation uses five deliberately designed test cases covering evidence sufficiency, evidence-based project identification, multi-document reasoning, instruction following, and contradictory evidence. The Python pipeline sends each test case to the judge, parses the structured JSON response, records evaluation time and token usage, calculates aggregate results, and saves the complete evaluation output to `evaluation_results.json`.

## Key Findings

The evaluation produced an average score of 3.60/5 across five test cases. The strongest results were observed on straightforward evidence-grounding and project-identification tasks, with T1 and T2 receiving 5/5. Lower scores occurred on multi-document reasoning (T3: 3/5), instruction following (T4: 3/5), and contradictory evidence (T5: 2/5).

The contradictory-evidence test is particularly important for TenderAI. The candidate response accepted a 120 MW figure from one document while ignoring a conflicting 48 MW figure from another document. The judge correctly identified this as a problem. In a production tender system, conflicting evidence should be flagged for verification rather than resolved by simply selecting the more favorable claim.

## Performance Metrics

- Test cases evaluated: 5
- Average score: 3.60/5
- Minimum score: 2/5
- Maximum score: 5/5
- Total evaluation time: 11.086 seconds
- Total input tokens: 1,658
- Total output tokens: 497
- Total tokens: 2,155

These results are based on a small evaluation set and should not be interpreted as a production accuracy estimate. The purpose of this exercise was to validate the evaluation methodology and identify potential failure modes.

## Limitations

The test dataset contains only five manually designed cases, so the results cannot establish broad model performance. LLM-as-Judge evaluations can also be affected by judge variability, prompt design, and evaluator bias. Additional examples, calibration cases, repeated runs, and human evaluation would be required before using the score as evidence for production readiness.

The evaluation also tests pre-written candidate responses rather than measuring the complete TenderAI generation pipeline. Future work should evaluate actual model-generated responses and compare automated judge scores with human assessments.