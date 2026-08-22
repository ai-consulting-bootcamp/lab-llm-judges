# Reflection

## Question 1: What would change in your evaluation design if your client's data was in French?

If the patient records and trial criteria were in French, I would adapt the evaluation so that both the test data and the reference answers were written and reviewed in French. I would also check whether the selected benchmark data are available in French or whether translated or newly created examples are needed. Translation alone may not be sufficient because medical terminology, abbreviations, and phrasing can differ across languages and healthcare systems.

Quality verification would need additional attention. Rule-based checks could still work for structured outputs such as MET, NOT MET, and UNKNOWN, but the medical reasoning and evidence citations should ideally be reviewed by a French-speaking clinical expert. I would also test whether the LLM-as-judge behaves consistently in French and compare its judgments with human review on a small calibration set.

## Question 2: Your client asks “is this model AGI-level?” — how do you respond?

I would explain that our evaluation cannot determine whether a model is “AGI-level.” The evaluation is designed to measure performance on one specific task: clinical trial eligibility screening. Strong performance would show that the model performs well on this defined use case under the tested conditions, not that it has general intelligence.

To make broader claims about general intelligence, the model would need to be evaluated across many different capabilities and domains, such as reasoning, planning, knowledge transfer, language understanding, coding, and unfamiliar problem solving. Even then, there is no universally accepted benchmark or threshold that definitively establishes AGI, so any such conclusion would require substantial caveats.

## Question 3: What is the one thing you could not evaluate without a human, and why?

The most important aspect I would not rely on an automated evaluator alone to assess is whether the model's handling of ambiguous clinical information is appropriate in a real clinical context. An LLM judge can check consistency, grounding, and adherence to a rubric, but it may share similar reasoning errors or medical assumptions with the model being evaluated.

I would therefore include human evaluation by a clinical research or medical expert for a sample of difficult and ambiguous cases. Their judgments could be compared with the LLM judge to identify disagreements, improve the evaluation rubric, and calibrate the automated evaluator before using it more broadly.