# W7D5_LAB_LLMs grading LLMs—with receipts
- Week 7 / Day 5
- Student: Andreas Papachristophorou
- Course: AI Consulting & Integration 2026-07
- Date: 2026-08-21
---

# Step 2: Benchmark Audit 

## Benchmark 1

**Benchmark name:** MEDIQA-Sum 2023

**Year:** 2023

**Source:** Overview of the MEDIQA-Sum Task at ImageCLEF 2023
[Link_1](https://www.microsoft.com/en-us/research/publication/overview-of-the-mediqa-sum-task-at-imageclef-2023-summarization-and-classification-of-doctor-patient-conversations/?lang=fr-ca)

**Why relevant:** It evaluates whether a model can identify relevant clinical topics and generate section-level or full clinical notes from medical conversations. This directly tests completeness, correct medical wording, and whether critical facts make it into a summary.

**Contamination risk:** **High.** The benchmark and its task data have been publicly available since 2023, so current general-purpose models may have encountered related material during training.

**Saturation risk:** **Medium.** Results for generation tasks remain well below perfect lexical-match scores, but overlap metrics such as ROUGE do not reliably detect every clinically dangerous omission or hallucination.

**Format:** Free-form text generation.

**Verdict:** **Adapt it.** Use it for the general task, but add hospital-specific checks for allergies, medications, dosages, diagnoses, and negations such as “no penicillin allergy.”

## Benchmark 2

**Benchmark name:** MIMIC-IV-BHC: A dataset and benchmark for hospital course summarization with adapted large language models

**Year:** 2024 (Mar 9, 2024)

**Source:** Aali et al., arXiv:2403.05720; later published in JAMIA.
[Link_2](https://huggingface.co/papers/2403.05720)


**Why relevant:** This benchmark evaluates LLMs that generate brief hospital course summaries from clinical notes. It compares healthcare-adapted and general-purpose models, so it is highly relevant to assessing whether an LLM can create accurate, complete hospital-record summaries while handling clinical language.

**Contamination risk:** **Medium.** The benchmark paper and associated research are public, so some models or fine-tuning datasets may have been exposed to descriptions, methods, or related clinical summarization examples. However, the underlying MIMIC-IV-BHC dataset is restricted-access, which reduces—though does not eliminate—the chance that benchmark records were included directly in a general model’s training data.

**Saturation risk:** **Medium.** Several capable models have been evaluated on this task and can produce strong summaries, but performance is not near-perfect or consistent across models and long clinical records remain challenging. Automated scores can also miss unsafe errors, such as omitted allergies or invented clinical facts, so clinician review is still necessary.

**Format:** free-form text generation

**Verdict:** **Adapt it.** because it is highly relevant but focuses on brief hospital-course summaries from discharge-related notes rather than every type of patient record. 


## Benchmark 3

**Benchmark name:** MedHELM

**Year:** 2025 (May)

**Source:** Stanford CRFM MedHELM; Holistic Evaluation of Large Language Models for Medical Tasks.
[Link_3-1]https://crfm.stanford.edu/helm/medhelm/v1.0.0/
[Link_3-2]https://arxiv.org/abs/2505.23802

**Why relevant:** MedHELM evaluates LLMs on healthcare tasks that reflect clinical work, including clinical-note generation and patient-record summarization. Unlike a single narrow benchmark, it measures multiple dimensions relevant to the hospital scenario, such as factual accuracy, completeness, writing quality, and performance across different clinical workflows.

**Contamination risk:** **Low.** Although MedHELM publishes its methodology and model results, much of its evaluation suite uses private or gated-access clinical datasets. Its current suite contains 35 benchmarks: 14 private, 7 gated-access, and 14 public. Because private and gated patient-record data are much less likely to appear in public model-training data, the risk of models memorising the exact evaluation examples is reduced.

**Saturation risk:** **Low.** Results vary significantly between models and across healthcare tasks, and no model performs near-perfectly across the benchmark suite. The continued difficulty and performance spread mean MedHELM can still distinguish strengths and weaknesses among models.

**Format:** Mixed formats, including free-form clinical text generation, structured outputs, and some question-answering tasks.

**Verdict:** **Adapt it.** Use MedHELM’s clinical-note-generation and patient-record-summarisation tasks as the foundation, but add the hospital’s safety-critical checks: allergies, medication names and dosages, diagnoses, key test results, and negated information. These explicit checks make the evaluation better matched to the intended workflow and help detect dangerous omissions that a broad quality score could miss.