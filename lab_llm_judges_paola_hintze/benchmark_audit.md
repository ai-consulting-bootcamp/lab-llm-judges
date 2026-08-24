# Benchmark Audit

## Client scenario

A fictional social-impact consultancy wants an LLM assistant to turn short client briefs into evidence-grounded recommendations for nonprofit and entrepreneurship-program leaders. The output must preserve supplied facts, separate evidence from inference, follow explicit format constraints, and use a clear, constructive consulting tone. The most important failures are fabricated evidence, unsupported certainty, omitted constraints, and recommendations that could mislead resource-allocation decisions.

## Benchmark Evaluation Card 1 — TruthfulQA

**Benchmark name:** TruthfulQA  
**Year:** 2021 (paper; published at ACL 2022)  
**Source:** Lin, Hilton & Evans, [TruthfulQA: Measuring How Models Mimic Human Falsehoods](https://arxiv.org/abs/2109.07958); [official repository](https://github.com/sylinrl/TruthfulQA)

**Why it seemed relevant:** TruthfulQA tests whether a model repeats plausible misconceptions rather than giving truthful answers. That is relevant because polished but false statements can be more harmful than obvious errors when presented as evidence for a recommendation.

**Contamination risk:** **High.** The complete set of 817 questions and reference answers has been public since 2021 and is widely mirrored and used in leaderboards. A current foundation model may have encountered the items or discussions of them, so a high score is not clean evidence of production truthfulness.

**Saturation risk:** **Medium.** The original paper reported a substantial gap from human performance, but modern models and instruction tuning have improved. The adversarial misconceptions remain useful, yet the benchmark does not directly test faithfulness to a private client brief.

**Format:** Multiple choice and free-form generation.

**Verdict:** **Adapt it.** Preserve the adversarial idea—tempting but unsupported claims—but replace public trivia with held-out, synthetic client briefs. Score every material claim for entailment by the brief and reward an explicit “not provided” response.

## Benchmark Evaluation Card 2 — IFEval

**Benchmark name:** Instruction-Following Evaluation (IFEval)  
**Year:** 2023  
**Source:** Zhou et al., [Instruction-Following Evaluation for Large Language Models](https://arxiv.org/abs/2311.07911); [official Google Research implementation](https://github.com/google-research/google-research/tree/master/instruction_following_eval)

**Why it seemed relevant:** Client deliverables often impose observable constraints such as word limits, headings, required caveats, or a fixed number of recommendations. IFEval evaluates compliance with such verifiable instructions and therefore covers an important part of operational reliability.

**Contamination risk:** **High.** Prompts and checking code are public, the benchmark is widely reported, and its roughly 500 prompts have been available since 2023. Exact-item exposure is plausible for current models.

**Saturation risk:** **Medium.** Objective constraints remain compositional and can still reveal failures, but many modern instruction-tuned models are optimized on similar tasks. Passing a keyword or length check says nothing about factual quality.

**Format:** Free-form text with deterministic instruction-level and prompt-level checks.

**Verdict:** **Adapt it.** Generate confidential variants combining consulting constraints: exactly three recommendations, evidence labels, a stated uncertainty, and a prohibited claim. Retain deterministic checks but pair them with source-faithfulness and human usefulness review.

## Benchmark Evaluation Card 3 — RAGTruth

**Benchmark name:** RAGTruth  
**Year:** 2024  
**Source:** Wu et al., [RAGTruth: A Hallucination Corpus for Developing Trustworthy Retrieval-Augmented Language Models](https://arxiv.org/abs/2401.00396); [official repository](https://github.com/ParticleMedia/RAGTruth)

**Why it seemed relevant:** The proposed assistant is grounded in a supplied brief, so faithfulness to context is closer to the real risk than open-domain accuracy. RAGTruth contains nearly 18,000 naturally generated RAG responses with case- and word-level human annotations across question answering, data-to-text, and summarization.

**Contamination risk:** **Medium.** The dataset and annotations are public and may be present in training or evaluation-tuning corpora, but its scale, response diversity, and span-level annotations reduce the likelihood that every item has been memorized.

**Saturation risk:** **Low to medium.** Detecting subtle unsupported spans remains difficult, although progress on hallucination detectors and possible annotation omissions can inflate apparent performance. Domain transfer to social-impact consulting is also uncertain.

**Format:** Free-form RAG outputs with case labels and word-level hallucination spans.

**Verdict:** **Adapt it.** Reuse its entailment-oriented annotation approach on held-out social-impact briefs, separating contradictory claims, unverifiable additions, and harmless stylistic elaboration. Double-annotate high-impact claims and adjudicate disagreement with a domain-capable human.

## Audit conclusion

No public benchmark is sufficient as a procurement gate. TruthfulQA probes misleading plausibility, IFEval probes observable compliance, and RAGTruth is closest to source faithfulness; all three should inform a custom, private test set. The acceptance decision should rest on held-out client-like cases, deterministic critical-failure checks, calibrated judging, and targeted human review rather than a single leaderboard score.

