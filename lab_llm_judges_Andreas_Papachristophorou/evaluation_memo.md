# W7D5_LAB_LLMs grading LLMs—with receipts
- Week 7 / Day 5
- Student: Andreas Papachristophorou
- Course: AI Consulting & Integration 2026-07
- Date: 2026-08-21
---

# Step 5 — "Evaluation Memo"

TO: St. Mary's General Hospital, Clinical Informatics Team
FROM: [Your Name], AI Consulting
DATE: August 21, 2026
SUBJECT: LLM Evaluation Results – Patient Record Summarization

### EXECUTIVE SUMMARY
We evaluated an LLM-based patient record summarization tool using five
custom evaluation prompts designed around this hospital's discharge and
handover workflow. The goal was to assess factual accuracy, completeness,
and hallucination risk before considering clinical deployment.

### METHODOLOGY
Three existing benchmarks were reviewed for relevance to clinical
summarization and found to be either too general or at risk of training
contamination, so we designed five custom prompts covering discharge
summaries, conflicting notes, hallucination detection, prioritisation
under ambiguity, and negation handling. Verification combined rule-based
keyword checks, human clinician review, and an LLM-as-judge model built
to flag unsupported claims and missing critical facts. We tested a
single model (gpt-4o-mini) on ten representative synthetic patient
records covering common emergency department and discharge scenarios.

### RESULTS
Across ten test cases, the model achieved an average judge score of
4.2 out of 5. Eight summaries were fully accurate and complete, one
had a minor non-clinical omission, and one included a serious,
unsupported claim: the summary stated "acute coronary syndrome was
ruled out" when the source record documented only negative troponin
results and a normal ECG, not a final diagnostic conclusion. This
single case was automatically flagged as a safety failure under our
scoring rubric and would have required clinician correction before
release.

### CAVEATS & LIMITATIONS
A ten-case sample cannot guarantee safe performance across the full
range of real patient records, especially rarer or more complex cases.
LLM-as-judge scoring has inherent variance and reflects our specific
rubric rather than an industry-wide standard; results may not generalise
without further calibration against a larger, clinician-labelled dataset.

### RECOMMENDATION
Given strong overall accuracy but one clinically significant
hallucination in ten cases, we recommend a limited pilot with mandatory
clinician review of every AI-generated summary before it enters the
patient record, rather than unsupervised deployment. We have moderate
confidence in this model for drafting summaries, and low confidence in
using it without human oversight for this use case.

### ADDITIONAL METRICS
Average judge evaluation time was under three seconds per summary at a
cost of well under one cent per case using gpt-4o-mini, making
large-scale piloting inexpensive; however, cost savings should not
outweigh the safety cost of an unreviewed hallucination in a clinical
setting.
