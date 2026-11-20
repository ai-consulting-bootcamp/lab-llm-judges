# Reflection

## 1. What would change if the client's data were in French?
I could not rely on English benchmarks. I would look for French or multilingual versions (some benchmarks have translated subsets) and, more importantly, rewrite my own test cases **natively in French**, not machine-translated, because real customers use idioms, informal register (tu/vous) and typos. Policy terms such as "retour gratuit" or "délai de rétractation" must be checked against the French version of the policy and French consumer law, which may differ from Germany's.

New challenges: the LLM judge may be **less reliable at judging tone in French**, and politeness norms differ (formal *vous*, longer courtesy phrases). My regex rule checks would also need French patterns. To verify quality, I would have **native French-speaking customer service staff** label a calibration set and compare the judge's scores with theirs before trusting it.

## 2. The client asks: "Is this model AGI-level?"
I would answer that this is the wrong question for their decision, and that **nothing in our evaluation can answer it**. "AGI" has no agreed definition or test; it usually means human-level ability across almost all tasks. We tested **one narrow task** (5 customer service cases) under controlled conditions.

What we *can* say is how well the model handles **their** task: safe on policy, weaker on completeness. To even discuss general capability, you would need broad, hard and uncontaminated evaluations across many domains (reasoning, planning, tool use, long tasks, novel problems), and even then experts disagree. My caveat would be: "Under these conditions, for this task, the model performs at a level suitable for a supervised pilot. That says nothing about general intelligence."

## 3. One thing I could not evaluate without a human, and why
**Whether an upset customer actually feels respected and calmed down.** Tone and empathy are subjective and culture-dependent. The judge can check whether an apology is present, but not whether it sounds sincere to a real German customer, or whether a direct, factual answer would be appreciated more than a warm one. Rule-based checks can only find words; an LLM judge has its own style and cultural biases, and it was too lenient in our run.

In practice I would combine both: have customer service staff **score a sample of replies each week** (especially complaints and all safety cases), use those labels to **calibrate the judge**, and track real outcomes such as customer satisfaction scores, repeat contacts and escalation rates after launch.
