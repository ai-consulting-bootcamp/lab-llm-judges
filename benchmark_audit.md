# Step 2 — Benchmark Audit

**Client:** MNM AG (fictional)  
**Use case:** Dynamics 365 Finance & Operations Vendor Management AI Assistant  
**Objective:** Assess public benchmarks for testing factual correctness, instruction following, and the reliability of LLM-as-a-judge evaluations.

## Benchmark 1 — EKRAG (2025)

**Benchmark name:** Enterprise-Knowledge RAG (EKRAG)  
**Year:** 2025  
**Source:** Yu et al., *EKRAG: Benchmark RAG for Enterprise Knowledge Question Answering* (KnowledgeNLP 2025). https://aclanthology.org/2025.knowledgenlp-1.13/

**Why it seemed relevant:**  
EKRAG examines enterprise question answering over corporate documents, including whether generated answers are correct, relevant, and faithful to the supplied information. This closely matches MNM AG's need to answer vendor-creation, payment-term, and legal-entity questions using approved company reference material.

**Contamination risk:** **Medium (estimated)**  
The benchmark draws on publicly accessible corporate documents, and the published evaluation is accessible to model developers. Training overlap is possible; we have no evidence that a particular model encountered the exact questions.

**Saturation risk:** **Low–Medium (estimated)**  
Enterprise questions requiring retrieval and synthesis remain challenging, but difficulty depends on the model and task. No claim of a measured saturation rate is made here.

**Format:** **Other — document-grounded, free-form question answering**, with supporting corporate documents and evaluation of retrieval and answer quality.

**Verdict:** **Adapt it.**  
Create original MNM AG questions with fictional policy excerpts as evidence. Assess whether the assistant's answers are correct, relevant, and supported by those excerpts; do not reuse public benchmark questions as the main test set.

## Benchmark 2 — IFBench (2025)

**Benchmark name:** IFBench — *Generalizing Verifiable Instruction Following*  
**Year:** 2025  
**Source:** Pyatkin et al., *Generalizing Verifiable Instruction Following* (NeurIPS 2025). https://proceedings.neurips.cc/paper_files/paper/2025/hash/46499a0622ecf568b72d17b61e45dbd5-Abstract-Datasets_and_Benchmarks_Track.html

**Why it seemed relevant:**  
IFBench tests whether models can follow unfamiliar, precisely checkable instructions rather than only familiar benchmark constraints. MNM AG's assistant must respect instructions such as identifying the relevant legal entity, following a required response format, and stating when information is unavailable.

**Contamination risk:** **Low–Medium (estimated)**  
Its newer, out-of-domain constraints were designed to test generalization, potentially reducing dependence on familiar tasks. Nevertheless, the benchmark is public, and exact model training exposure cannot be verified.

**Saturation risk:** **Low–Medium (estimated)**  
The benchmark was developed to challenge models on new constraints, making complete saturation less likely than on older, repeatedly tested instructions. This is a qualitative judgment, not a measured score for our target model.

**Format:** **Free-form text with automatically verifiable instruction constraints** (including a multi-turn variant).

**Verdict:** **Adapt it.**  
Develop MNM AG-specific constraints, such as responding in a fixed structure, avoiding unsupported bank-account details, and explicitly distinguishing MNM-DE from MNM-NL. Verify objective constraints using simple Python checks where possible.

## Benchmark 3 — GroUSE (2025)

**Benchmark name:** GroUSE — *Grounded QA Unitary Scoring of Evaluators*  
**Year:** 2025  
**Source:** Muller et al., *GroUSE: A Benchmark to Evaluate Evaluators in Grounded Question Answering* (COLING 2025). https://aclanthology.org/2025.coling-main.304/

**Why it seemed relevant:**  
GroUSE evaluates the **evaluators themselves**: whether an LLM judge detects different failure modes in answers supposedly grounded in source material. This is particularly relevant because the lab requires us to build an LLM-as-a-judge, not merely to score a chatbot's answers.

**Contamination risk:** **Medium (estimated)**  
Its published unit tests could appear in training or tuning data. We cannot establish exposure for a specific judge model, so the risk is a cautious estimate rather than a confirmed finding.

**Saturation risk:** **Low–Medium (estimated)**  
The research shows that automated judges can miss important failure modes. Some strong models may perform well, but there is no basis here to claim that the benchmark is universally saturated.

**Format:** **Other — structured meta-evaluation unit tests** of judge decisions on grounded question-answering failure modes.

**Verdict:** **Adapt it.**  
Create a small set of MNM AG answers with deliberately planted errors, such as an invented vendor bank account, an unsupported payment term, or a legal-entity mix-up. Check whether our LLM judge identifies these errors and gives appropriately lower scores.

## Overall Recommendation

**Adapt all three benchmarks rather than using their public questions unchanged.** They cover complementary evaluation needs:

- **EKRAG:** Is the answer correct and grounded in company evidence?
- **IFBench:** Does the assistant follow explicit instructions and constraints?
- **GroUSE:** Can the LLM judge reliably detect faulty or unsupported answers?

For Step 3, build **five original, fictional MNM AG evaluation prompts** with documented ground truth and verification methods. Keep their policy facts within the supplied synthetic reference material. This improves task relevance and reduces reliance on potentially contaminated public test items, but does **not** prove zero contamination.

**Limitations:** Contamination and saturation assessments above are qualitative, not empirical findings. The 2025 publication dates do not guarantee that the benchmarks are absent from any model's training data. No benchmark scores or client-model evaluations have yet been run.
