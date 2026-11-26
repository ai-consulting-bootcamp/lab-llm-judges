# Benchmark audit

**Client scenario (Option A, Financial Services):** Spree Bank AG (fictional), a German retail bank, wants an LLM to draft loan rejection letters that a credit officer reviews before sending. Each letter must state the real reason for the decision, stay compliant (no invented reasons, no protected characteristics such as age or family status as a reason, no promise of later approval, a pointer to contact and human review) and read as clear and respectful. The main failure modes are hallucinated reasons, discriminatory wording, ignored format rules and a cold or legalistic tone.

---

## Card 1: IFEval (Instruction-Following Eval)

- **Year:** 2023
- **Source:** Zhou et al., "Instruction-Following Evaluation for Large Language Models", arXiv:2311.07911

**Why it seemed relevant:** Rejection letters come with hard format rules: word limits, a mandatory reference number, required sections and banned jargon. IFEval measures exactly this kind of "verifiable instruction" and checks it with code rather than an LLM, which is what a compliance team wants.

**Contamination risk:** Medium. The prompts have been public since 2023 and are widely used in model reports, so newer models have likely seen them or close variants. The instruction types (e.g. "answer in under N words") are generic enough that memorisation helps less than with fact questions.

**Saturation risk:** High. Frontier models report scores in the high 80s to 90s, so it no longer separates strong models well.

**Format:** Free-form text with rule-based checks.

**Verdict:** **Adapt.** Reuse the method (rule-based verifiable constraints), not the dataset: write bank-specific constraints (reference number present, ≤150 words, no "DTI"/"LTV" jargon, no forbidden phrases) and check them with regex in `llm_judge_evaluation.py`.

---

## Card 2: FinanceBench

- **Year:** 2023
- **Source:** Islam et al., "FinanceBench: A New Benchmark for Financial Question Answering", arXiv:2311.11944 (Patronus AI)

**Why it seemed relevant:** It is a finance-domain benchmark that tests whether a model answers financial questions faithfully from source documents, which looks close to "explain a credit decision correctly".

**Contamination risk:** Medium-High. The questions are built on public company filings (10-K/10-Q) that are part of common web training data, and a public sample of the benchmark is available.

**Saturation risk:** Low-Medium. Open-book numerical reasoning over long filings is still hard, especially without good retrieval.

**Format:** Free-form question answering over documents.

**Verdict:** **Reject.** It measures analyst-style numerical QA over corporate filings, not customer communication. A high FinanceBench score says nothing about tone, compliance wording or whether a letter invents a rejection reason.

---

## Card 3: TruthfulQA

- **Year:** 2021
- **Source:** Lin, Hilton, Evans, "TruthfulQA: Measuring How Models Mimic Human Falsehoods", arXiv:2109.07958

**Why it seemed relevant:** The biggest risk in a rejection letter is a confident but false statement (an invented reason, a wrong right or a wrong deadline). TruthfulQA was built to measure whether models repeat plausible falsehoods.

**Contamination risk:** High. It has been public since 2021, is heavily discussed and has been used in many training and evaluation pipelines.

**Saturation risk:** Medium-High. Modern instruction-tuned models score far above the original baselines, and part of that gain reflects exposure to the benchmark itself.

**Format:** Multiple choice and free-form generation.

**Verdict:** **Reject as-is, keep the idea.** Its questions are general-knowledge misconceptions, not bank decisions. The useful idea is the "trap" design: I built my own hallucination trap (a case where no reason code is given, see P2 in `evaluation_design.md`) to test whether the model invents a reason.

---

**Conclusion:** None of the three public benchmarks can be used as-is for this client. IFEval's method is reused, and the evaluation itself is a custom 5-case benchmark scored by rules plus an LLM judge.
