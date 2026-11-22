# Evaluation Memo

**To:** Chief Medical Information Officer, [Hospital]  
**From:** AI Evaluation Consultant  
**Date:** November 22, 2026  
**Subject:** LLM evaluation for discharge-record summarization

## Executive summary

We evaluated five safety-focused tasks covering completeness, abstention, medication reconciliation, contradiction handling, and prompt-injection resistance. The recorded run evaluated five cases successfully; rule-based checks passed 2/5 cases, with an average rule score of 0.7655. The one LLM-judge case received score 1, so the tested configuration is not ready for unsupervised clinical use.

## Methodology

The design adapts the benchmark audit’s healthcare scenario and uses synthetic Cases A–C. Case A is a clean discharge record, Case B adds the NKDA versus penicillin-anaphylaxis contradiction, and Case C adds an instruction-injection string. The evaluation combines deterministic checks for critical facts, medication values, abstention, uncertainty, negation, and unsafe approval language with the structured LLM judge for contradiction handling.

The Python runner uses `gpt-4o-mini` by default, temperature 0, and records each response, rule result, judge reasoning, latency, token counts, and optional cost. Published benchmarks informed the design but were not treated as production evidence because of contamination, saturation, and task-mismatch concerns.

## Results

The recorded five-case run completed all cases. Target-model latency totaled 23.27 seconds, averaging 4.65 seconds per case. Target usage was 2,862 tokens; the judge used 1,628 tokens and took 4.44 seconds. The rule-based pass rate was 40%. The judge’s score of 1 indicates a critical failure on the contradiction/uncertainty case, which should be treated as a safety signal even though the sample is very small.

## Caveats and recommendation

These results are directional, not a clinical safety guarantee. Five synthetic cases cannot represent real specialties, note formats, languages, long records, or EHR integration. The judge is an approximation of clinician review and may share model blind spots. Cost was not estimated in the recorded run because current provider rates were not supplied.

Under these conditions, for this task, I recommend only a clinician-supervised pilot with every summary reviewed before use. Confidence is high that autonomous deployment is inappropriate and low that this sample estimates production error rates. Expand the held-out set, have clinicians label critical failures, and rerun calibration before comparing models or permitting workflow integration.
