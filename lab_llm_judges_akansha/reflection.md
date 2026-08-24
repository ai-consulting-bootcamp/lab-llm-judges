# Reflection

## Question 1: If the client's data were in French

Our current design would need real rework, not just translation. The benchmark audit process itself would change: FinQA and LegalBench are English/US-centric, and IFEval's constraint phrasing is unlikely to transfer directly, so we'd need to check whether French-specific legal-reasoning or numerical benchmarks exist, or accept that we're building custom prompts from scratch even for the audit stage.

**New challenges:** French consumer-credit law (Code de la consommation) has different disclosure requirements than German AGG/DSGVO, so the ground truth itself changes, not just the language. Formality register also differs from German "Sie" — French uses "vous" but doesn't have as sharp a formal/informal split in professional writing, so our rule-based "informal pronoun" check wouldn't map cleanly.

For quality verification, we would not trust our own or the judge's French output without a native/fluent reviewer calibrating the judge first, the same way we'd insist on for German — we would specifically test whether the judge model's French discrimination-detection is as reliable as its German detection before trusting it, since that's not guaranteed to transfer.

## Question 2: "Is this model AGI-level?"

I'd push back on the premise first: "AGI-level" has no agreed technical definition, and nothing we tested measures it — our evaluation checks whether the model can competently draft compliant rejection notices, which is a narrow, answerable question, not a claim about general intelligence.

Answering their actual underlying question ("can we trust this model broadly?") and determining if a model is "AGI-level" for this domain would require testing autonomous multi-step legal reasoning, zero-shot adaptation to novel statutory amendments, and adversarial resilience against unseen prompt injections. Crucially, I would caution the client that benchmark performance indicates statistical alignment on training data, not genuine cognitive agency or liability-free operational reliability.

I'd caveat clearly that passing our evaluation says nothing about capability outside consumer-lending correspondence, and redirect to the decision that matters: does it reliably do this specific job well enough to deploy, with human review in place.

## Question 3: What requires a human

Whether a rejection letter would actually land as respectful and non-discriminatory to a real, specific customer — not just whether it passes our rubric — is the thing I'd least trust to full automation. Coded or connotative discriminatory language, exactly the gap we flagged in the judge's bias analysis, is where LLM-as-judge is weakest, because it inherits the same blind spots as the generator and can be fooled by fluent, policy-shaped text that still lands badly.

In practice, I'd use human legal/compliance review as a mandatory gate for any letter the judge scores as failing a compliance-critical criterion, plus a periodic random-sample audit even on passing letters, tracking human/judge agreement over time so we know when the judge's calibration needs revisiting rather than assuming it holds indefinitely.
