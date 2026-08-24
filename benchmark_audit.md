# Benchmark Audit - Retail Customer Service Chatbot

## Scenario Context
The client wants a retail customer service chatbot that can handle returns, product questions, and complaints while staying helpful, calm, and policy-aware. The main risks are hallucinating policies, sounding defensive or robotic, and failing to resolve the issue with a concrete next step.

## Benchmark 1

Benchmark Name: MultiWOZ 2.4
Year: 2022
Source: https://paperswithcode.com/paper/multiwoz-2-4-a-multi-domain-task-oriented

Why it seemed relevant:
MultiWOZ is a multi-turn task-oriented dialogue benchmark, which makes it a close structural match for retail support conversations. The chatbot has to track context, ask for missing details, and complete a user goal over several turns, which mirrors returns, complaints, and product questions.

Contamination risk:
[ ] Low - Model likely not trained on this data
[x] Medium - Some overlap possible
[ ] High - Model definitely saw this during training
Explanation: MultiWOZ is public, widely reused, and appears in many dialogue training corpora and benchmark discussions. A modern model may have seen the dataset or very similar dialog patterns, so the benchmark is useful but not cleanly held out.

Saturation risk:
[ ] Low - Benchmark is challenging
[x] Medium - Some models perform well
[ ] High - Many models achieve near-perfect scores
Explanation: MultiWOZ remains non-trivial because dialogue state tracking and multi-turn completion are still error-prone, but strong systems have narrowed the gap enough that it is not highly discriminative by itself.

Format:
[ ] Multiple Choice
[ ] Free-form text
[ ] Code generation
[x] Other: Multi-turn task-oriented dialogue with state tracking and response generation

Verdict:
[ ] Use it as-is
[x] Adapt it (explain how)
[ ] Reject it (explain why)
Explanation: Adapt it into a small retail dialogue subset or use it only for multi-turn completion and slot-handling subtests, because the original domains are travel-oriented rather than retail support.

## Benchmark 2

Benchmark Name: IFEval
Year: 2023
Source: https://paperswithcode.com/dataset/ifeval

Why it seemed relevant:
IFEval measures instruction following with explicit, verifiable constraints. That is directly relevant to retail support, where the assistant should obey format constraints, tone constraints, and policy instructions such as asking for an order number before escalating.

Contamination risk:
[ ] Low - Model likely not trained on this data
[ ] Medium - Some overlap possible
[x] High - Model definitely saw this during training
Explanation: Instruction-following prompts are highly likely to appear in public data, benchmark discussions, and alignment training material. Even if the exact dataset is not memorized, the pattern is familiar enough that contamination risk is materially high.

Saturation risk:
[ ] Low - Benchmark is challenging
[x] Medium - Some models perform well
[ ] High - Many models achieve near-perfect scores
Explanation: Many current models do well on simple instruction-following checks, so the benchmark can saturate on basic constraints. It is still useful as a compliance filter, but it will not fully separate strong retail assistants from average ones.

Format:
[ ] Multiple Choice
[x] Free-form text
[ ] Code generation
[ ] Other: Structured free-form text with explicit instruction checks

Verdict:
[ ] Use it as-is
[x] Adapt it (explain how)
[ ] Reject it (explain why)
Explanation: Use the instruction-following structure as a sub-benchmark for retail-specific constraints such as "be concise", "do not invent policy", and "include a clear next action". That keeps the useful verification style while making the task domain-specific.

## Benchmark 3

Benchmark Name: TruthfulQA
Year: 2022
Source: https://crfm.stanford.edu/helm/classic/v0.3.0/?group=truthful_qa

Why it seemed relevant:
TruthfulQA is relevant because a retail chatbot must answer product and policy questions without hallucinating facts. A wrong return policy, invented warranty, or fabricated product compatibility claim would be a real customer-service failure.

Contamination risk:
[ ] Low - Model likely not trained on this data
[x] Medium - Some overlap possible
[ ] High - Model definitely saw this during training
Explanation: Truthfulness benchmarks are widely discussed and often reused in training or evaluation contexts. The exact benchmark questions may not be memorized, but the benchmark family is well known enough that contamination is a realistic concern.

Saturation risk:
[ ] Low - Benchmark is challenging
[x] Medium - Some models perform well
[ ] High - Many models achieve near-perfect scores
Explanation: The benchmark is still discriminative because models continue to hallucinate on tricky factual questions, but performance has improved enough that the easiest examples no longer reveal much.

Format:
[ ] Multiple Choice
[x] Free-form text
[ ] Code generation
[ ] Other: Free-form factual QA with truthfulness scoring

Verdict:
[ ] Use it as-is
[x] Adapt it (explain how)
[ ] Reject it (explain why)
Explanation: Reframe it around retail policy and product-knowledge questions so the benchmark directly measures hallucination risk in customer support instead of general trivia truthfulness.
