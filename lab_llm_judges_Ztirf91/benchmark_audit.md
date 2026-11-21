# Benchmark audit — Retail customer support

## Client scenario

A fictional online retailer wants a chatbot to answer questions about returns and products and respond to complaints. It must ground answers in the retailer’s policy and catalog, explain the next step clearly, and escalate cases when critical information is missing. The main risks are promising refunds without authorization, inventing product facts, and mishandling a complaint.

The saturation ratings below are qualitative judgments based on published evidence. Public availability creates an exposure risk. Actual training-set overlap is unknown for the candidate models.

## τ-bench Retail text — listed as τ²-bench by Sierra

**Relevance.** The retail text tasks examine whether a support agent can follow store policy and complete transactions in simulated conversations. The March 2026 release corrected ambiguous tasks and incorrect expected actions in existing domains, which matters when a bad reference can penalize a correct response.

**Contamination risk — Medium.** The retail tasks are public and build on earlier public tasks and policies. The updated release date alone cannot establish whether a candidate model has seen overlapping cases.

**Saturation risk — Medium (provisional).** This is a mature public task family, and performance may cluster on familiar workflows. The audit has no matched current-model results for the corrected retail tasks, so it cannot establish how well they separate our candidates.

**Format.** Simulated multi-turn text conversations with tool calls and programmatic outcome checks.

**Leaderboard.** In Sierra’s interface, select τ²-bench and then Retail. Sierra’s GPT-5.2 (high) submission reports 81.58% pass¹ and 51.75% pass⁴ for Retail. The same submission also contains Banking results, so use the Retail block when citing it. These scores describe one published setup. Confirm the task version before comparing runs.

**Verdict — Adapt.** Write fresh cases against the fictional retailer’s policy and verify the proposed disposition against explicit references. Verify the final order state if the retailer later connects the bot to transaction tools.

[Sierra Research, τ³-bench release and retail task corrections](https://sierra.ai/uk/blog/bench-advancing-agent-benchmarking-to-knowledge-and-voice)

[Sierra leaderboard](https://taubench.com/) · [Sierra’s GPT-5.2 submission](https://raw.githubusercontent.com/sierra-research/tau2-bench/main/web/leaderboard/public/submissions/gpt-5-2_sierra_2026-02-26/submission.json)

## IFBench (2025)

**Relevance.** IFBench extends IFEval with 58 new verifiable constraints and tests whether models generalize to unfamiliar instructions. A retailer similarly needs its chatbot to follow its own output requirements, such as formatting an escalation label for a routing system.

**Contamination risk — Medium.** IFBench’s tasks and verification code are public. Its original holdout design measures generalization relative to the older instruction inventory. Exposure for models trained after publication is unknown.

**Saturation risk — Low based on the original study.** The authors found substantial gaps on the new constraints for models that did well on familiar ones. This evidence is historical and does not establish current saturation.

**Format.** Free-form text generation scored by deterministic constraint verifiers.

**Verdict — Adapt.** Use programmatic checks for retailer-specific output constraints. Add reference-based checks for policy decisions and product facts.

[IFBench paper](https://openreview.net/pdf?id=yfYgwjj5F8) · [AllenAI code and data](https://github.com/allenai/IFBench)

## MT-Bench (2023)

**Relevance.** The multi-turn format resembles a support chat in which information arrives over several messages. The study also describes judge biases that matter when assessing complaint responses, including a preference for longer answers.

**Contamination risk — Medium.** The questions and associated judgments are public. Later models could have seen items or examples of how they are scored.

**Saturation risk — Medium.** A published comparison reported 9.26 out of 10 for one GPT-4 snapshot, suggesting limited headroom for some models under that evaluation setup. A single high score provides limited evidence about saturation across models.

**Format.** Open-ended multi-turn chat responses assessed by a judge model.

**Verdict — Reject as a client acceptance test.** General chat ratings provide insufficient evidence about applying this retailer’s policies or making support handoffs. Use the study’s judge-bias findings when designing the custom rubric.

[Zheng et al., MT-Bench](https://arxiv.org/abs/2306.05685) · [DeepSeek LLM, Table 8](https://arxiv.org/pdf/2401.02954)
