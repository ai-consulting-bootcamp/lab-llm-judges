# W7D5_LAB_LLMs grading LLMs—with receipts
- Week 7 / Day 5
- Student: Andreas Papachristophorou
- Course: AI Consulting & Integration 2026-07
- Date: 2026-08-21
---

# Step 6: Reflection

### 1. If the data were French
If the hospital’s patient records were in French, I would build a French-language evaluation set rather than simply translating the English prompts. Medical terms, abbreviations, negation, and the usual structure of clinical notes can differ between languages and healthcare systems. For example, the judge would need to recognise French negative phrases and distinguish them from a confirmed diagnosis.

I would use French-speaking clinicians to create and label realistic test cases, including summaries with correct clinical facts, missing information, and unsupported claims. The LLM-as-judge should be tested against these clinician labels, especially for equivalently worded phrases and French medical abbreviations. Human review would remain essential for safety-critical or ambiguous cases.

### 2. Is the model AGI-level?
I would explain that "Artificial General Intelligence (AGI) - level" is not a clear or useful conclusion from this evaluation. This project measures a narrow task: summarising synthetic patient records while preserving accuracy, completeness, and safety. A high score would show that the model performs well under these specific test conditions, not that it has general intelligence or reliable understanding across all domains.

Assessing a broad claim such as AGI would require many evaluations across different tasks, languages, situations, and time periods, including reasoning, adaptation to new tasks, factual reliability, safety, and performance under uncertainty. Even then, benchmark scores alone would not settle the question because models may be exposed to benchmark-like data during training and can behave unpredictably outside the test set.

### 3. What requires a human?
The most important aspect that cannot be evaluated fully without a human is clinical usefulness and safety in context. A summary may be factually accurate but still fail to highlight the most urgent information for the next clinician. Deciding what matters most can depend on a patient’s history, local clinical workflow, and professional judgment.

Rule-based checks can find missing keywords, while an LLM-as-judge can compare the summary to the record. However, both can miss subtle medical implications, accept a plausible but unsafe inference, or reproduce the same misunderstanding. In practice, clinicians should review all pilot summaries, investigate safety flags, label disagreement cases, and use those examples to improve both the summarisation prompt and the evaluation rubric.