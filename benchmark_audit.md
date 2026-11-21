# Benchmark Audit & Client Scenario

## Step 1 — Client Scenario (Option A: Financial Services)
**Meridian Community Bank**, a mid-sized regional retail bank, wants to automate the drafting of personalized **adverse action (loan rejection, counteroffer, and incomplete-application) letters** from structured underwriting outputs for consumer auto, personal, and home improvement loans. The letters must be **factually accurate, empathetic, and strictly compliant** with US federal fair-lending statutes—specifically the **Equal Credit Opportunity Act (ECOA / Regulation B)** and the **Fair Credit Reporting Act (FCRA)**. The client's primary concerns are factual hallucinations (inventing credit bureaus, scores, or denial reasons), omission of mandatory statutory disclosures (such as the 60-day free credit report notice), unauthorized commitments of future loan approval, and leakage of protected-class characteristics (such as age, marital/widowed status, or retirement/pension status) from raw underwriter notes.

---

## Step 2 — Existing Benchmark Evaluation Cards

### Card 1: IFEval (Instruction-Following Evaluation)

* **Benchmark Name:** IFEval (Instruction-Following Evaluation for Large Language Models)
* **Year:** 2023
* **Source:** Zhou et al., Google Research — [https://arxiv.org/abs/2311.07911](https://arxiv.org/abs/2311.07911) (featured on the Hugging Face Open LLM Leaderboard v2)

**Why it seemed relevant:**
Adverse action notices must satisfy strict structural, inclusion, and exclusion rules—such as naming the exact credit bureau, stating up to four principal denial reasons, including a 60-day credit report disclosure, and omitting prohibited terms. IFEval evaluates whether an LLM faithfully obeys explicit verifiable formatting, keyword-inclusion, and keyword-avoidance constraints in free-form generation.

**Contamination risk:**
* [ ] Low - Model likely not trained on this data
* [x] Medium - Some overlap possible
* [ ] High - Model definitely saw this during training
* **Explanation:** Although IFEval's programmatic verifier scripts check synthetic constraint combinations rather than memorized answer keys, the 541 base prompt templates have been publicly hosted on Hugging Face and GitHub since late 2023 and frequently appear in post-training instruction-tuning mixtures.

**Saturation risk:**
* [ ] Low - Benchmark is challenging
* [ ] Medium - Some models perform well
* [x] High - Many models achieve near-perfect scores
* **Explanation:** Current frontier and mid-sized instruction-tuned models routinely achieve 85%–92%+ strict prompt-level accuracy on IFEval, leaving little headroom to distinguish subtle compliance failures in high-stakes financial communications.

**Format:**
* [ ] Multiple Choice
* [x] Free-form text
* [ ] Code generation
* [ ] Other: Free-form text scored via deterministic programmatic constraint verifiers (regex, keyword counts, formatting checks)

**Verdict:**
* [ ] Use it as-is
* [x] Adapt it (explain how)
* [ ] Reject it (explain why)
* **Explanation:** IFEval's generic prompts (e.g., "write a poem without the letter 'e'") do not test banking compliance or empathetic tone, so it cannot be used as-is. However, we **adapt its deterministic verifier architecture** by building custom regex and keyword-presence/absence checks for ECOA/FCRA disclosures and protected-class redaction inside our evaluation pipeline.

---

### Card 2: FinQA

* **Benchmark Name:** FinQA: A Dataset of Numerical Reasoning over Financial Data
* **Year:** 2021
* **Source:** Chen et al., EMNLP 2021 — [https://arxiv.org/abs/2109.00122](https://arxiv.org/abs/2109.00122) / [https://github.com/czyssrs/FinQA](https://github.com/czyssrs/FinQA)

**Why it seemed relevant:**
Because our client operates in financial services and loan adverse action letters must accurately cite financial figures—such as debt-to-income (DTI) ratios, credit utilization percentages, APRs, and credit scores—a dedicated financial-domain benchmark appeared directly aligned with banking accuracy.

**Contamination risk:**
* [ ] Low - Model likely not trained on this data
* [ ] Medium - Some overlap possible
* [x] High - Model definitely saw this during training
* **Explanation:** Released in 2021 and constructed from public S&P 500 SEC 10-K filings, FinQA has been widely ingested into open financial corpora, leaderboard evaluations, and instruction-tuning datasets for several years.

**Saturation risk:**
* [ ] Low - Benchmark is challenging
* [x] Medium - Some models perform well
* [ ] High - Many models achieve near-perfect scores
* **Explanation:** Modern frontier LLMs using chain-of-thought reasoning achieve ~75%–82% execution accuracy on FinQA (approaching the human expert baseline of ~91%), though multi-step table arithmetic still presents moderate difficulty.

**Format:**
* [ ] Multiple Choice
* [ ] Free-form text
* [ ] Code generation
* [x] Other: Numerical question answering / DSL program generation over financial tables and earnings text

**Verdict:**
* [ ] Use it as-is
* [ ] Adapt it (explain how)
* [x] Reject it (explain why)
* **Explanation:** FinQA measures multi-step corporate accounting arithmetic (e.g., year-over-year EBITDA margins from 10-K filings), whereas our loan-letter workflow receives pre-computed underwriting metrics (e.g., `DTI: 48%`) and requires closed-context faithfulness, ECOA/FCRA legal disclosures, and empathetic customer communication.

---

### Card 3: TruthfulQA

* **Benchmark Name:** TruthfulQA: Measuring How Models Mimic Human Falsehoods
* **Year:** 2022
* **Source:** Lin et al., ACL 2022 — [https://arxiv.org/abs/2109.07958](https://arxiv.org/abs/2109.07958) / [https://github.com/sylinrl/TruthfulQA](https://github.com/sylinrl/TruthfulQA)

**Why it seemed relevant:**
Preventing factual hallucinations—such as fabricating credit bureau names, inventing false statutory timelines, or misstating denial reasons—is a top priority for Meridian Community Bank, making a benchmark explicitly designed to measure truthfulness and hallucination resistance seem highly relevant.

**Contamination risk:**
* [ ] Low - Model likely not trained on this data
* [ ] Medium - Some overlap possible
* [x] High - Model definitely saw this during training
* **Explanation:** TruthfulQA is one of the most heavily cited safety benchmarks in LLM literature and has been included in virtually every major evaluation suite since 2022, resulting in extensive direct and paraphrased exposure in pretraining and alignment data.

**Saturation risk:**
* [ ] Low - Benchmark is challenging
* [ ] Medium - Some models perform well
* [x] High - Many models achieve near-perfect scores
* **Explanation:** Contemporary RLHF-aligned models routinely score 80%–92%+ on TruthfulQA (often outperforming human baselines due to memorized trivia patterns), making it poorly discriminative for enterprise deployment.

**Format:**
* [x] Multiple Choice
* [x] Free-form text
* [ ] Code generation
* [ ] Other: Short-answer adversarial trivia questions paired with MC1/MC2 multiple-choice variants

**Verdict:**
* [ ] Use it as-is
* [ ] Adapt it (explain how)
* [x] Reject it (explain why)
* **Explanation:** TruthfulQA tests *parametric world-knowledge truthfulness* against common internet myths (e.g., health superstitions or historical misconceptions), not *contextual faithfulness* to a private customer underwriting record. High scores on TruthfulQA do not prevent an LLM from hallucinating an external credit bureau when none was pulled.