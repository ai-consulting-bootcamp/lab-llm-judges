Clinical Trial Eligibility Screening Assistant

A pharmaceutical company is evaluating an LLM-based decision-support tool to assist clinical trial recruitment teams. The system receives a short patient record together with a trial's inclusion and exclusion criteria. For each criterion, it must classify the available evidence as MET, NOT MET, or UNKNOWN, cite the supporting information from the patient record, and produce an overall eligibility assessment for review by a clinical research professional. The system must never infer missing clinical information or make the final enrollment decision. The evaluation will focus on criterion-level accuracy, completeness, unsupported inference, and correct handling of missing information.

design limitation: UNKNOWN currently mixes at least two situations: missing information and criterion not applicable

---
---

## banchmarks

1. TrialGPT Criterion-Level Matching — strongest fit

TrialGPT is the closest match to use case. Its matching component evaluates a patient against trial eligibility criteria criterion by criterion, generates an explanation, identifies the relevant sentence in the patient note, and assigns an eligibility label. That is extremely close to desired MET / NOT MET / UNKNOWN + evidence output. In its published evaluation, TrialGPT used physician annotations for 1,015 patient-criterion pairs and reported 87.3% criterion-level accuracy.

links:
TrialGPT project — NIH/NLM
TrialGPT paper — Nature Communications
TrialGPT code and data — GitHub

Initial verdict: probably adapt, not use exactly as-is. It is directly relevant, but its label taxonomy is slightly different from ours and it evaluates a larger end-to-end trial-matching framework.


2. TREC Clinical Trials 2022 — very relevant, but broader

The TREC Clinical Trials benchmark gives the system a synthetic patient description and asks it to identify suitable trials from ClinicalTrials.gov. Trials are judged as eligible, excluded, or not relevant, and the inclusion/exclusion criteria are central to the task. The 2022 track continued the 2021 setup with new patient topics.

links:
TREC Clinical Trials 2022 official page
NIST TREC 2022 dataset
TREC 2022 data, topics and qrels

Initial verdict: adapt. It is excellent for patient–trial matching, but it evaluates mainly retrieval/ranking at trial level, whereas your assistant evaluates individual eligibility criteria. That limitation is useful to discuss in your benchmark critique.

3. SIGIR 2016 Patient–Clinical Trial Matching Collection — useful historical benchmark

This benchmark contains a large clinical-trial corpus and 60 patient case reports, with medical professionals judging whether a patient would likely be referred to a trial. It was specifically created to evaluate patient-to-clinical-trial matching.

links:
SIGIR 2016 benchmark description and paper
Original benchmark paper PDF

Initial verdict: probably adapt or reject, depending on how strict we want to be. It is highly relevant conceptually, but it is older, small in terms of patient cases, and focuses on trial-level relevance/referral rather than criterion-level reasoning.

---
---

