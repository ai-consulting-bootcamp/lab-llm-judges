# Evaluation Memo

**TO:** Clinical Development Leadership  
**FROM:** Nevena Zujko  
**DATE:** 22 August 2026  
**SUBJECT:** LLM Evaluation Results – Clinical Trial Eligibility Screening Assistant

## EXECUTIVE SUMMARY

We evaluated `gpt-4o-mini` as a decision-support model for clinical trial eligibility screening, focusing on criterion-level accuracy, completeness, evidence grounding, appropriate handling of missing or ambiguous information, and preservation of the human decision boundary. Under the tested conditions, the model achieved an average judge score of **5.0/5 across five test cases**, with all defined evaluation criteria satisfied.

## METHODOLOGY

The evaluation design was informed by three existing clinical trial matching benchmarks: **TrialGPT**, the **TREC 2022 Clinical Trials Track**, and the **SIGIR 2016 Patient–Clinical Trial Matching Collection**. These benchmarks were useful for understanding patient–trial matching tasks, but none directly matched the required criterion-level output format; therefore, a custom evaluation was used for execution.

The custom dataset contained five synthetic clinical cases covering: a clear inclusion criterion, exclusion logic, missing clinical information, multiple simultaneous criteria, and ambiguous clinical evidence. `gpt-4o-mini` generated the eligibility assessments. A separate `gpt-4.1-mini` LLM-as-judge evaluated each response against predefined ground truth using five criteria: criterion-level accuracy, completeness, evidence grounding, overall consistency, and adherence to the decision-support boundary. The judge returned structured scores from 1–5 with reasoning and criterion-level pass/fail assessments.

## RESULTS

All five cases received a score of **5/5**, giving an average score of **5.0/5** and a score range of **5–5**. All five evaluation criteria achieved a **100% pass rate** across the test set.

Notably, the model correctly interpreted an exclusion criterion, returned `UNKNOWN` rather than inferring an unreported eGFR, correctly evaluated four simultaneous eligibility criteria, and preserved uncertainty when an infection was suspected but not confirmed. No unsupported clinical information or autonomous final enrollment decisions were identified by the judge.

## CAVEATS & LIMITATIONS

These results do **not** demonstrate that the model is universally reliable for clinical trial screening. The dataset contains only five synthetic and relatively controlled examples, so the absence of failures limits our ability to identify harder failure modes or estimate real-world error rates. The evaluation also relies on an LLM judge, which may introduce its own reasoning, verbosity, or domain-assumption biases.

The external benchmarks reviewed are public and may have some contamination or saturation risk. In addition, TREC and SIGIR primarily assess patient-to-trial retrieval or relevance rather than the exact criterion-level task evaluated here.

## RECOMMENDATION

**Under these conditions and for this specific task**, `gpt-4o-mini` shows promising performance as a clinical trial eligibility **decision-support** tool. Confidence is **moderate for the tested scenarios but low-to-moderate for generalization to real clinical data**. Before deployment, evaluation should be expanded with larger, more difficult, real-world or expert-reviewed cases and human validation of ambiguous examples. Final eligibility and enrollment decisions should remain with qualified clinical professionals.

## ADDITIONAL METRICS

The complete evaluation required **22.95 seconds**, consumed **5,579 tokens**, and had an estimated API cost of **$0.002796**. Environmental impact was not directly measured; token consumption and execution volume can serve only as limited operational proxies.