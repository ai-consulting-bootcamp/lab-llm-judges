# Evaluation memo

**TO:** Head of Retail Credit, Spree Bank AG
**FROM:** Murat Comez, AI Consulting
**DATE:** 26 November 2026
**SUBJECT:** LLM Evaluation Results - Automated Loan Rejection Letters

## Executive summary
We tested whether `gpt-6-luna` can draft loan rejection letters that are accurate, compliant and clear enough for a credit officer to approve with light editing. Under these test conditions the model averaged **4.2/5** on our rubric and passed all hard compliance checks in **100%** of cases. It is suitable for a supervised pilot.

## Methodology
Public benchmarks did not fit this task: IFEval is saturated and generic, FinanceBench tests analyst Q&A rather than customer letters, and TruthfulQA is general knowledge with high contamination risk (see `benchmark_audit.md`). We therefore built a custom 5-case test set covering the main risks: a standard rejection, a missing reason code (hallucination trap), discriminatory information in internal notes (compliance trap), an emotional applicant (tone) and strict format rules.

Each letter was scored in two independent ways: deterministic rule checks (required and forbidden content, word limit) and an LLM judge (`gpt-4o-mini`) using a rubric for reason accuracy, compliance and tone, with score anchors from 1 (harmful) to 5 (send after quick review). One model was tested.

## Results
Mean judge score 4.2/5 (range 3-5). Criteria met: reason accuracy 100%, compliance 100%, tone/clarity 60%; rule pass rate 100%.

Cases needing attention: P5. The weakest was P5 (Format constraints (length, reference, no jargon)), where the judge noted: "The letter correctly states the reason for rejection but uses the term 'debt-to-income ratio' instead of explaining it in plain words, which does not fully meet the clarity requirement. All compliance criteria are met, and the tone is respectful, but the use of jargon affects the overall clarity."

## Caveats and limitations
These results cover 5 synthetic cases from one run. They show behaviour on our test set, not a guarantee for all applicants. The judge is an LLM from the same family as the generator and may share its blind spots; it has not yet been calibrated against credit officers' ratings. Results can vary between runs and model versions, and we did not test German-language letters, which production would require.

## Recommendation
Under these conditions and for this task, we recommend a supervised pilot in which every letter is reviewed by a credit officer before sending, with the rule checks as a hard gate. Confidence: **low to moderate**, because the test set is small. Next step: 50+ cases including German letters, and calibration of the judge against human ratings.

## Additional metrics
The full evaluation (5 letters plus 5 judge calls) took 23.4 s, about 4.7 s per case, and used 5633 tokens, about **$0.00148** at gpt-4o-mini list prices. At this cost per letter, generation cost is negligible next to officer review time. Energy use per letter is small, but it scales with volume and with any switch to larger models.
