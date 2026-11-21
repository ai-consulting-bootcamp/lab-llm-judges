# Benchmark audit — CompanyScope evidence-grounded reports

**Date:** 21 November 2026
**Context:** A fictional legal/compliance team's CompanyScope-style company-research assistant prepares short due-diligence notes from retrieved registry entries, annual accounts, and news snippets. Requirements: correct legal-entity matching, current facts, arithmetic, citation support, honest uncertainty, and resistance to instructions embedded in external material. The client is not asking the model to make a final legal or sanctions decision.

**Interpretation of risks:** Contamination and saturation levels below are *risk assessments*, not verified claims about any model's training data or current score. Public release increases possible contamination but does not prove a model trained on a benchmark. Different benchmark subsets have different difficulty; without a current head-to-head run, saturation cannot be established quantitatively.

## Card 1 — FinanceBench (2023)

**Source:** Islam et al., *FinanceBench: A New Benchmark for Financial Question Answering* (2023): https://arxiv.org/abs/2311.11944

**Why relevant:** Open-book questions grounded in public-company filings test whether a model derives financial answers from evidence rather than inventing numbers. CompanyScope's accounts module similarly needs current figures, units, arithmetic, and document traceability. FinanceBench is narrower than our overall due-diligence workflow.

- **Contamination risk: Medium.** The benchmark and public examples have been available since 2023, making overlap plausible. We do **not** know whether a particular deployed model saw them during training. Prefer private, recent or freshly constructed tests for launch decisions.
- **Saturation risk: Low–medium (qualitative).** Some question types may be easier for frontier models; the original paper nevertheless found substantial failures in evaluated 2023 systems. Historic results cannot substitute for current model testing.
- **Format:** Free-form financial questions, reference answers and evidence spans; may require numeric calculation.
- **Verdict: Adapt.** Use source-grounded numeric and temporal cases, but replace original issuers/filings with permissioned client documents. Grade currency, years, arithmetic, and citation entailment separately; do not port public benchmark scores into a performance claim.
- **What it misses:** Legal entity name collisions, malicious retrieved text, unknown beneficial ownership, German registry formats.

## Card 2 — RAGBench (2024)

**Source:** Friel, Belyi & Sanyal, *RAGBench: Explainable Benchmark for Retrieval-Augmented Generation Systems* (2024): https://arxiv.org/abs/2407.11005
**Dataset:** https://huggingface.co/datasets/rungalileo/ragbench

**Why relevant:** RAGBench focuses on whether generated answers are supported by retrieved context and provides explainable evaluation signals. CompanyScope similarly combines external evidence and model-generated summaries, creating a failure path from irrelevant retrieval to unsupported confident reporting.

- **Contamination risk: Medium.** A large published dataset and derivative examples can enter model-development pipelines. We cannot establish training overlap for the selected model, and some benchmark examples may be less exposed than others.
- **Saturation risk: Medium/unknown.** It spans varied RAG tasks and domains, so averaging hides hard cases. Report results by subset instead of treating a high global score as proof of trustworthy company due diligence.
- **Format:** Context, query, generated answer, and annotated/explainable RAG evaluation labels; free-form language.
- **Verdict: Adapt.** Retain evidence faithfulness and response adequacy as evaluation dimensions. Create small, client-specific examples where supporting IDs and contradictions are manually verified. Use deterministic checks for numeric fields, not only a second language model.
- **What it misses:** Register-specific authoritative source priority, actual sanctions-screening processes, legal sign-off.

## Card 3 — LegalBench (2023)

**Source:** Guha et al., *LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models* (NeurIPS 2023): https://papers.neurips.cc/paper_files/paper/2023/hash/89e44582fd28ddfea1ea4dcb0ebbf4b0-Abstract-Datasets_and_Benchmarks.html
**Project:** https://hazyresearch.stanford.edu/legalbench/

**Why relevant:** Company-research reports may contain legal/compliance language where unsupported conclusions are dangerous. LegalBench's legal reasoning and extraction tasks provide a useful taxonomy for distinguishing fact extraction from legal interpretation.

- **Contamination risk: Medium–high (potential only).** The 2023 public benchmark has substantial visibility, yet no direct proof of model exposure is available. Treat apparent benchmark familiarity as one threat to generalization.
- **Saturation risk: Medium/heterogeneous.** Some extraction/classification tasks can be easier than nuanced reasoning. A single aggregate benchmark score would conceal whether the model overstates conclusions on unsupported evidence.
- **Format:** Mixed task formats: classification, extraction, entailment and generation depending on subtask.
- **Verdict: Adapt selectively.** Borrow reasoning and calibrated-uncertainty principles; build local registry/ownership/sanctions-evidence examples rather than claiming LegalBench measures a live due-diligence decision.
- **What it misses:** Freshness of a retrieved corporate record, citations to a specific registry entry, prompt injection via a third-party web page.

## Decision and deployment relevance

None of these public benchmarks alone is an adequate acceptance test. The five **original, fictional** cases in `test_cases.json` cover identity, freshness, arithmetic, abstention, and prompt injection. They illustrate the harness; a real client pilot needs a larger private sample, reference adjudication by a domain expert, sampling of real report failures, and repeated judge calibration. No benchmark authors' quantitative results are presented as our model's results.
