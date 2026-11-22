# Benchmark audit

The client is Northline Home, a fictional online retailer. It wants an assistant that drafts clear customer replies about returns, product questions and complaints. A suitable reply must follow the policy record, explain the next step, and avoid invented actions or compensation promises.

## 1. τ-bench Retail

| Field | Assessment |
| --- | --- |
| Benchmark and year | τ-bench Retail, 2024 |
| Source | [Yao et al., paper](https://arxiv.org/abs/2406.12045) and [official repository with Retail results](https://github.com/sierra-research/tau-bench) |
| Relevance | Retail conversations test how an assistant interprets store policy while interacting with a customer and a simulated order system. That is a close proxy for missing parcels, returns, and escalation, especially when decisions depend on order state. |
| Contamination risk | **Medium.** The published code, tasks, and policy examples are available for training or tuning. Exposure of the specific model snapshots to the test set cannot be verified from public availability alone. |
| Saturation risk | **Low in the published comparison.** The repository's Claude 3.5 Sonnet October 2024 Retail baseline scores 69.2% on pass¹ and 46.2% on pass⁴. Repeated success is substantially below the ceiling in that comparison. This evidence is historical and does not establish the standing of current models. |
| Format | Other. Multi-turn simulated customer conversations with tool use and final database-state comparison. |
| Verdict | **Adapt.** Borrow policy-grounded scenarios and a check on the resulting decision. Use Northline's own policy and assess the quality of the drafted explanation separately. Live tool execution is outside this evaluation's scope. |

## 2. IFEval

| Field | Assessment |
| --- | --- |
| Benchmark and year | Instruction-Following Evaluation for Large Language Models (IFEval), 2023 |
| Source | [Zhou et al., paper](https://arxiv.org/abs/2311.07911) and [Google Gemma 3 model card](https://ai.google.dev/gemma/docs/core/model_card_3) |
| Relevance | A retail drafting assistant needs to obey concrete requirements such as a length limit and a prescribed outcome field. IFEval's verifiable constraints provide a model for turning those requirements into reproducible checks. |
| Contamination risk | **Medium.** The evaluation prompts and checking code are public. Familiar instruction formats or direct prompt reuse could inflate results. The exact training exposure of either evaluated model is unknown. |
| Saturation risk | **Medium.** Google's Gemma 3 card reports zero-shot scores of 88.9–90.4 for its 4B, 12B and 27B instruction-tuned variants, with scores clustered toward the top of the scale. That evidence suggests reduced separation among stronger variants under that setup rather than a confirmed ceiling across all models. |
| Format | Free-form generation with deterministic instruction checks and prompt-level and instruction-level accuracy. |
| Verdict | **Adapt.** Use exact checks for the structured outcome and refund amount, plus an explicit length constraint. Grounding, empathy and next-step quality require case-specific review. |

## 3. Berkeley Function-Calling Leaderboard

| Field | Assessment |
| --- | --- |
| Benchmark and year | Berkeley Function-Calling Leaderboard (BFCL), first released in 2024. The formal paper appeared in 2025. |
| Source | [Initial Berkeley release](https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html), [ICML paper](https://proceedings.mlr.press/v267/patil25a.html) and [version 4 leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html) |
| Relevance | The ability to choose a structured action and supply the right arguments becomes relevant if the assistant eventually looks up an order or starts an escalation. Relevance detection is especially useful when a required parameter is missing or no appropriate tool applies. |
| Contamination risk | **Medium.** Public examples and scoring code make overlap plausible. The versioned leaderboard includes several evaluation settings, but publication alone cannot establish exposure for the tested model. |
| Saturation risk | **Medium and slice-dependent.** The version 4 table dated April 12, 2026 lists 95.5% for the top-ranked row on the non-live simple slice, versus 77.47% overall. Easier calls appear close to a ceiling in that row, while broader evaluation still exposes errors. |
| Format | Other. Structured function selection and arguments across single-turn and multi-turn scenarios, with AST-based checks and additional evaluation tracks. |
| Verdict | **Reject as-is.** The current assistant drafts replies and has no tools. BFCL would become useful in a separate integration test when support workflows can actually modify order state. |

