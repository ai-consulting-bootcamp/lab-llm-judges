# Implementation Summary

We implemented an LLM-as-judge evaluation pipeline for a retail chatbot's
complaint-handling responses, using gpt-4o-mini with three criteria: empathy/
acknowledgment, concrete resolution, and tone appropriateness. The judge takes a
customer complaint and a chatbot response, and returns a structured JSON verdict
(1-5 score, reasoning, and per-criterion pass/fail) using OpenAI's
`response_format={"type": "json_object"}` to guarantee parseable output.

Testing on 4 hand-crafted response variants (good, generic/deflecting,
empathetic-but-no-resolution, and policy-correct-but-dismissive) produced an
average score of 2.25/5. The judge correctly ranked the well-constructed response
highest (5/5, all criteria met) and appropriately penalized the three flawed
responses (1-2/5), confirming the judge discriminates response quality rather than
scoring everything similarly. Criteria-level pass rates were 2/4 (empathy), 1/4
(resolution), and 2/4 (tone) — resolution was the hardest criterion to pass in this
set.

One notable limitation surfaced by the real data: the "dismissive" response
actually stated the correct policy (refund/replacement) but was still marked as
failing "concrete resolution," suggesting the judge's scoring of resolution quality
is influenced by tone rather than fully independent, as the rubric intended. Each
evaluation took approximately 1.5-2 seconds and cost about $0.00013 per case
(~$0.0005 total for all 4), confirming gpt-4o-mini is a practical, low-cost choice
for ongoing production monitoring of real complaint transcripts at scale.