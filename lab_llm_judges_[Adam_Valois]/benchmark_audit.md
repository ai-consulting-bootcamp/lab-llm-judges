# Client Scenario and Bechmark Audit

## Scenario

- A hospital wants to summarize patient records
- Requirements: Must preserve critical medical information
- Key concerns: Accuracy, completeness, medical terminology

## Benchmark 1

**Benchmark Name:** MIMIC-IV-BHC — Brief Hospital Course Summarization Benchmark
**Year:** 2024/2025
**Source:** Aali et al., *A dataset and benchmark for hospital course summarization with adapted large language models*, Journal of the American Medical Informatics Association. [Paper](https://doi.org/10.1093/jamia/ocae312?utm_source=chatgpt.com)

**Why it seemed relevant:**
This benchmark directly evaluates LLMs generating brief hospital-course summaries from clinical notes, making it highly relevant to a hospital summarization system. It evaluates both automated summarization metrics and clinician judgments, including aspects such as comprehensiveness, factual correctness, conciseness, and fluency.

**Contamination risk:**
[ ] Low - Model likely not trained on this data
[x] Medium - Some overlap possible
[ ] High - Model definitely saw this during training

**Explanation:** The benchmark was published recently, but it is derived from MIMIC-IV clinical data, which has been publicly available for years. Some models may therefore have encountered related MIMIC data during training. The benchmark itself is newer, making complete contamination less certain.

**Saturation risk:**
[x] Low - Benchmark is challenging
[ ] Medium - Some models perform well
[ ] High - Many models achieve near-perfect scores

**Explanation:** The benchmark evaluates long clinical inputs and requires models to synthesize medically meaningful summaries. The authors also found differences between automated metrics and clinician preferences, suggesting that the task is not saturated by simple lexical similarity.

**Format:**
[ ] Multiple Choice
[x] Free-form text
[ ] Code generation
[ ] Other: __________

**Verdict:**
[ ] Use it as-is
[x] Adapt it (explain how)
[ ] Reject it (explain why)

**Adaptation:** Use the benchmark's hospital-course summarization task but add explicit evaluation for preservation of critical information, particularly diagnoses, medications/dosages, procedures, allergies, adverse events, and follow-up instructions.

## Benchmark 2

**Benchmark Name:** A Meta-Evaluation of Faithfulness Metrics for Long-Form Hospital-Course Summarization
**Year:** 2023
**Source:** Adams, Zuckerman & Elhadad, *A Meta-Evaluation of Faithfulness Metrics for Long-Form Hospital-Course Summarization*, Proceedings of Machine Learning for Healthcare. [Paper](https://proceedings.mlr.press/v219/adams23a.html?utm_source=chatgpt.com)

**Why it seemed relevant:**
This benchmark is particularly relevant because it focuses on whether generated hospital summaries faithfully represent the source medical records. Human annotators identify incorrect, missing, and unsupported clinical information, including errors involving diagnoses, medications, procedures, treatments, dosages, and dates.

**Contamination risk:**
[ ] Low - Model likely not trained on this data
[x] Medium - Some overlap possible
[ ] High - Model definitely saw this during training

**Explanation:** The benchmark was published in 2023 and uses clinical data derived from hospital admissions. Some underlying clinical data may have been available to models during training, although contamination of the specific benchmark evaluation set cannot be assumed.

**Saturation risk:**
[x] Low - Benchmark is challenging
[ ] Medium - Some models perform well
[ ] High - Many models achieve near-perfect scores

**Explanation:** Clinical faithfulness is difficult because a summary can be fluent and plausible while still omitting important information or introducing incorrect details. The benchmark specifically identifies errors such as incorrect dosages, dates, symptoms, and hallucinated information.

**Format:**
[ ] Multiple Choice
[x] Free-form text
[ ] Code generation
[x] Other: Human annotation of clinical summary errors

**Verdict:**
[ ] Use it as-is
[x] Adapt it (explain how)
[ ] Reject it (explain why)

**Adaptation:** Adapt the error categories into a hospital-specific evaluation rubric. Give greater weight to safety-critical omissions or errors, such as allergies, medication changes, diagnoses, procedures, and abnormal test results, rather than treating every error equally.

## Benchmark 3

**Benchmark Name:** MedNLI — A Natural Language Inference Dataset for the Clinical Domain
**Year:** 2019
**Source:** Shivade, *MedNLI - A Natural Language Inference Dataset For The Clinical Domain*, PhysioNet. [Dataset](https://doi.org/10.13026/C2RS98?utm_source=chatgpt.com)

**Why it seemed relevant:**
MedNLI evaluates whether clinical statements are supported or contradicted by information in a patient's medical record. This is relevant to the scenario because a summary must not introduce medical claims that are unsupported by the original record.

**Contamination risk:**
[ ] Low - Model likely not trained on this data
[ ] Medium - Some overlap possible
[x] High - Model definitely saw this during training

**Explanation:** MedNLI was released in 2019 and is based on the widely used MIMIC-III clinical dataset. Because both the dataset and benchmark have been publicly available for several years, training-data overlap is a significant concern for modern LLMs.

**Saturation risk:**
[ ] Low - Benchmark is challenging
[x] Medium - Some models perform well
[ ] High - Many models achieve near-perfect scores

**Explanation:** Modern LLMs have strong general clinical-language and inference capabilities, so performance may be relatively high. More importantly, MedNLI tests clinical inference rather than the actual summarization task.

**Format:**
[x] Multiple Choice
[ ] Free-form text
[ ] Code generation
[ ] Other: Clinical natural language inference

**Verdict:**
[ ] Use it as-is
[x] Adapt it (explain how)
[ ] Reject it (explain why)

**Adaptation:** Use MedNLI-style tests as a secondary evaluation: extract important claims from generated summaries and test whether each claim is supported by the patient's source record. This would turn the benchmark into a targeted hallucination and factual-consistency test for the summarization system.
