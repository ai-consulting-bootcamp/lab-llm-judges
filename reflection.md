# Reflection

## 1. What would change if the client’s data was in French?

I would add French-language examples to the private benchmark rather than assuming that an English benchmark score transfers. The test set should cover French customer-service vocabulary, formal and informal address, regional phrasing, accents, and policy terms that may not translate literally. I would also test code-switching, spelling mistakes, and messages written by non-native speakers.

Verification would combine deterministic checks for product and policy facts with French-speaking human reviewers for tone, politeness, and clarity. The judge prompt should explicitly say that natural French may use different sentence length and politeness conventions than English. I would calibrate the judge with French reference examples and compare its scores with bilingual reviewers. A translated English test set could be useful for comparison, but it should not replace native or client-authored French cases.

## 2. How would I respond to “Is this model AGI-level?”

I would explain that “AGI-level” is not a single operational metric. It could mean broad knowledge, transfer to new tasks, autonomy, robustness, long-horizon planning, or human-level performance across many domains. Our retail evaluation measures a narrow business workflow, so it cannot establish or disprove AGI.

I would redirect the conversation to decision-relevant evidence: success on unseen retail cases, safety and policy compliance, tool reliability, multilingual performance, robustness to adversarial inputs, latency, cost, and human escalation quality. I would state the scope clearly: “Under these conditions, for this task, this model meets or does not meet the agreed acceptance criteria.” That answer is more useful and less likely to turn a marketing label into an unsupported technical claim.

## 3. What could not be evaluated without a human?

The hardest item to evaluate without a human is whether a response shows appropriate empathy in a sensitive complaint while still being concise and culturally natural. Rule-based checks can detect banned promises or missing fields, and an LLM judge can provide a scalable signal, but neither guarantees that a real customer would feel understood or respected.

I would use human review for a stratified sample of complaints, safety cases, and judge disagreements. Reviewers would score empathy, clarity, fairness, and whether the suggested next step feels realistic. I would measure agreement between reviewers and the automated judge, investigate systematic disagreements, and keep human review in the release process for high-risk categories.
