# Benchmark audit

## 1. IFEval

**Benchmark Name:** Instruction-Following Evaluation (IFEval)
**Year:** 2023
**Source:** [Zhou et al., Instruction-Following Evaluation for Large Language Models](https://arxiv.org/abs/2311.07911)

**Why it seemed relevant:** IFEval tests around 500 prompts using 25 types of verifiable instructions. This fits MIRA's need to check explicit constraints such as required sections, palette terms, exclusions, and frame count.

**Contamination risk:** Medium
**Explanation:** The prompts, code, and data are public, which increases contamination exposure, but this does not prove that any particular model trained on them.

**Saturation risk:** Medium
**Explanation:** Strong instruction-tuned models may handle many mechanical constraints well, reducing discrimination on simple items. More complex preference conflicts can still expose failures.

**Format:** Other — free-form responses scored with rule-based checks.
**Verdict:** Adapt
**Explanation:** Reuse the idea of objectively verifiable constraints, but add MIRA-specific human and LLM review for creative fidelity.

## 2. MT-Bench

**Benchmark Name:** MT-Bench
**Year:** 2023
**Source:** [Zheng et al., Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685)

**Why it seemed relevant:** MT-Bench uses open-ended, multi-turn questions and an LLM judge. Its approach is relevant to scoring coherence, usefulness, and instruction adherence where exact answers do not exist.

**Contamination risk:** High
**Explanation:** Questions and evaluation code have been publicly available and widely reused. That raises exposure risk without proving training-set inclusion for a specific model.

**Saturation risk:** Medium
**Explanation:** Modern assistants may perform strongly on familiar general-chat tasks. The benchmark may therefore separate MIRA-specific creative-direction failures less effectively than a custom set.

**Format:** Free-form.
**Verdict:** Adapt
**Explanation:** Use a pointwise rubric and structured judge output, while addressing documented position, verbosity, and self-preference biases through calibration and human review.

## 3. MMLU-Pro

**Benchmark Name:** MMLU-Pro
**Year:** 2024
**Source:** [Wang et al., MMLU-Pro](https://arxiv.org/abs/2406.01574)

**Why it seemed relevant:** MMLU-Pro offers more challenging, reasoning-focused questions with ten answer options across multiple domains. It can indicate structured reasoning ability that may support consistent planning.

**Contamination risk:** Medium
**Explanation:** It is public and partly builds on the older MMLU ecosystem, increasing possible exposure. Its newer and revised items reduce but do not remove this concern.

**Saturation risk:** Low
**Explanation:** The authors designed it to be harder and more discriminative than MMLU. This rating may change as model performance improves.

**Format:** Multiple Choice.
**Verdict:** Reject for direct MIRA scoring
**Explanation:** It tests academic knowledge and reasoning rather than whether a campaign respects a person's visual choices. It is useful background evidence, not a valid proxy for MIRA quality.

## Why MIRA needs a custom evaluation

General benchmarks do not represent MIRA's central contract: direct answers and visual choices must override inference, unsupported preferences must not be invented, and five creative frames must form one coherent campaign. A custom evaluation can combine deterministic checks for explicit constraints with rubric-based review of specificity and coherence. Even then, the five-case set is a proof of concept: it is too small for statistically strong model comparisons and remains vulnerable to prompt variance and judge bias.
