# Reflection

## 1. What would change if the data were in French?

I would not simply translate the English benchmark. French clinical abbreviations, medication names, units, date formats, and discharge-note conventions need a native test set created with French-speaking clinicians. I would look for French biomedical benchmarks for candidate screening, but rely primarily on de-identified records from the client.

The judge and checklist would need French calibration. Bilingual clinicians should label a gold set, and the evaluation should measure both French quality and the gap from English performance. GDPR, health-data hosting, and model-provider restrictions would also affect which APIs could be used. Back-translation could be a diagnostic tool, but not a substitute for native review.

## 2. Is this model AGI-level?

There is no agreed operational definition of AGI, so this evaluation cannot answer that question. Broadly, AGI would imply strong performance across many tasks, including novel problems and longer-horizon learning or action. A good score on clinical summarization measures one narrow capability under one prompt and data distribution.

I would redirect the client to the decision that matters: whether the model is safe and useful for this workflow. Answering an AGI question would require a broad, contamination-resistant evaluation of generalization, autonomy, learning, and robustness. Even excellent results here would not support claims about general intelligence.

## 3. What cannot be evaluated without a human?

Clinical significance cannot be fully evaluated without a human. A missing routine detail may be harmless while a missing medication hold could create serious risk; that distinction depends on patient context and local clinical practice. Rules can only check anticipated fields, and an LLM judge can share the system’s blind spots.

In practice, two clinicians should independently review a stratified sample, adjudicate disagreements, review every judge-flagged critical failure, and audit a random sample of passes. Their labels should calibrate the judge and continue after deployment through periodic sampling.
