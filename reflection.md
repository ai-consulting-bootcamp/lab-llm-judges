# Reflection — three evaluation design challenges

## 1. How would the design change if the client's data were French?

First, I would create evidence packs from authorized French-language registry extracts and corporate documents. The tasks would use native business and legal vocabulary, original dates and numeric conventions, plus reference answers reviewed by francophone subject-matter experts. I would not treat a translation into English as the only ground truth: mistranslating a legal status, corporate form or qualified statement can itself introduce an error.

Second, I would score the generated report in French and cross-check exact entities, citations, amounts and dates with deterministic rules where possible. A bilingual reviewer would adjudicate borderline cases and determine whether the judge penalizes natural French phrasing. We would test French prompt injection and cross-lingual evidence retrieval separately; a model that reads French fluently may still conflate legal concepts or silently translate away uncertainty.

## 2. The client asks: "Is this model AGI-level?" What do you say?

"AGI-level" has no agreed operational threshold for this procurement decision. A five-case company-research evaluation can show whether the model succeeds on specific input types, not whether it is generally intelligent or reliable across unrelated tasks. Claiming AGI based on high benchmark scores would confuse general capability with fitness for a compliance workflow.

I would ask the client which decisions depend on that label, then propose task-specific acceptance criteria: supported factual accuracy, severe-error rate, robust abstention, resilience to malicious sources, cost, latency and reproducibility across fresh private samples. Broader generality could be explored with multiple unseen tasks and environments, but the practical decision remains whether this exact workflow is safe and useful under human supervision.

## 3. What is one thing a human must evaluate, and why?

A qualified reviewer must decide whether a due-diligence narrative is **appropriate to issue to a client**. This includes whether the disclosed uncertainty is legally and commercially sufficient for a specific transaction, whether the evidence needs an authoritative update and whether a missing ownership fact should block the report. A model judge can flag risks but cannot accept professional accountability or make those contextual judgments reliably.

In practice, a lawyer or trained compliance analyst would review all high-severity cases and a random sample of routine reports, annotate precise failure categories and escalate disagreements between rule checks and the judge. Their adjudications would become a private calibration set. Automated scores would support triage and quality monitoring, not replace sign-off for consequential conclusions.
