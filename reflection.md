# TenderAI Evaluation Reflection

## Question 1 — What would change if the client's data was in French?

If the client's data was primarily in French, the evaluation would need to include French-language test cases rather than assuming that English benchmark performance transfers directly to French. The custom benchmark should be built from representative French tender documents, terminology, requirements, and company evidence. Some English benchmarks could still provide general information about model capability, but they would not be sufficient to establish French-language performance for the client's specific workflow.

Additional challenges could include differences in legal and business terminology, translation ambiguity, and differences in how requirements are expressed in French procurement documents. Evaluation should therefore test whether the model preserves the meaning of requirements and evidence rather than simply checking whether the French text is grammatically correct. Quality could be verified using French-speaking human reviewers, bilingual reference answers, rule-based checks where possible, and an LLM judge that has been explicitly calibrated on French examples.

For a production system, I would recommend creating a dedicated French evaluation set rather than translating an English benchmark mechanically. The test set should reflect the actual language, terminology, document structure, and business context that the client expects the system to handle.

---

## Question 2 — The client asks: "Is this model AGI-level?"

I would not treat a single benchmark or this TenderAI evaluation as evidence that a model is "AGI-level." AGI is not a single standardized technical score, and the term can refer to different ideas about general intelligence, adaptability, reasoning, autonomy, and performance across many domains. A model can perform extremely well on a particular benchmark while still having important limitations outside that benchmark.

I would explain to the client that our evaluation answers a narrower and more useful business question: whether the model performs reliably for the TenderAI task under defined conditions. A broader claim about general intelligence would require evaluations across many capabilities and environments, including reasoning, knowledge, planning, instruction following, tool use, robustness, adaptation, and potentially long-horizon tasks. Even then, I would avoid claiming that benchmark results alone prove AGI.

My recommendation would therefore be to focus the decision on the client's actual business objective. Instead of asking whether the model is "AGI-level," we should ask whether it meets the required reliability, accuracy, safety, latency, and cost thresholds for the intended workflow.

---

## Question 3 — What is the one thing you could not evaluate without a human?

One important aspect that cannot be fully evaluated without humans is whether a generated tender response is genuinely appropriate for the client's business and professional context. A rule-based evaluator can check objective facts and formatting, while an LLM judge can assess many semantic qualities, but neither guarantees that the response reflects the client's strategic priorities, professional standards, or acceptable level of business risk.

For example, a response could be factually grounded and well written but still be inappropriate because it emphasizes the wrong evidence, uses a tone that the client would not accept, or presents a borderline claim too confidently. These judgments can depend on organizational context and professional experience that may not be fully represented in the evaluation prompt.

In practice, I would include human evaluation for a sample of cases, particularly high-risk or ambiguous cases. Human reviewers could score relevance, business appropriateness, and risk while the automated evaluator handles repetitive checks. The human scores could then be compared with the LLM judge's scores to identify disagreements and improve calibration. This creates a hybrid evaluation system rather than assuming that automation can replace human judgment completely.
