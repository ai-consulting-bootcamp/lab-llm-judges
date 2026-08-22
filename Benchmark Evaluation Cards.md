Benchmark Name: TrialGPT-Matching criterion-level evaluation

Year: 2024

Source:
Nature Communications:
https://www.nature.com/articles/s41467-024-53081-z

NIH/NLM TrialGPT project:
https://www.ncbi.nlm.nih.gov/research/trialgpt/about/

repository
https://github.com/ncbi-nlp/TrialGPT?utm_source=chatgpt.com

### Why it seemed relevant:
TrialGPT-Matching evaluates patient eligibility against clinical-trial criteria on a
criterion-by-criterion basis. For each criterion, the system produces an eligibility
classification, an explanation, and identifies supporting sentences from the patient
record. This is closely aligned with our Clinical Trial Eligibility Screening Assistant,
which must classify criteria and provide evidence from the patient record.

Contamination risk:

[ ] Low

[x] Medium

[ ] High

Explanation:
The TrialGPT paper, code, methodology, and associated datasets are publicly available.
Therefore, newer LLMs could potentially have been exposed to the paper, repository, or
related benchmark material during training. However, we do not have evidence that a
specific model was trained on the exact evaluation examples, so contamination cannot
be assumed to be high.

### Saturation risk:
[ ] Low

[x] Medium

[ ] High

Explanation:
TrialGPT-Matching achieved 87.3% criterion-level eligibility accuracy, compared with
approximately 88.7–90.0% for the human experts in the study. This suggests that the
task is challenging but that strong models already perform relatively well. Performance
is therefore not saturated, but the benchmark may become less discriminative as newer
models improve.

### Format:
[ ] Multiple Choice

[ ] Free-form text

[ ] Code generation

[x] Other: criterion-level classification with evidence and free-text explanation

### Verdict:

[ ] Use it as-is

[x] Adapt it

[ ] Reject it

Explanation:
The benchmark is highly relevant, but its labels do not exactly match our intended
output. TrialGPT uses different labels for inclusion and exclusion criteria, including
"Included", "Not included", "Excluded", "Not excluded", "Not enough information",
and "Not applicable". We would simplify this into MET, NOT MET, and UNKNOWN and
retain the requirement to identify supporting evidence from the patient record.

---
---

Benchmark Name: TREC 2022 Clinical Trials Track

Year: 2022

Source:
TREC Clinical Trials Track:
https://www.trec-cds.org/2022.html

NIST TREC data page:
https://trec.nist.gov/data/trials2022.html

https://trec.nist.gov/pubs/trec31/papers/Overview_trials.pdf

Why it seemed relevant:
The benchmark evaluates patient-to-clinical-trial matching. The input is a synthetic
free-text patient description resembling an EHR admission note, and systems must retrieve
clinical trials that are suitable for that patient. Trial inclusion and exclusion criteria
are central to determining relevance, so the benchmark tests many of the same reasoning
challenges as our Clinical Trial Eligibility Screening Assistant.

### Contamination risk:
[ ] Low

[x] Medium

[ ] High

Explanation:
The benchmark topics, relevance judgments, task description, and results have been publicly
available since 2022. Therefore, newer models may have been exposed to the benchmark or
related material during training. However, there is no evidence that a specific model has
seen the exact patient-trial pairs, so high contamination cannot be assumed.

### Saturation risk:
[x] Low

[ ] Medium

[ ] High

Explanation:
The benchmark remains a challenging information-retrieval task involving a large trial
collection, complex eligibility criteria, and semantic differences between patient records
and trial descriptions. Published TREC results show substantial room for improvement rather
than near-perfect performance, so saturation appears low.

### Format:
[ ] Multiple Choice

[ ] Free-form text

[ ] Code generation

[x] Other: information retrieval / ranking with graded relevance labels
    (Eligible, Excluded, Not Relevant)

### Verdict:
[ ] Use it as-is

[x] Adapt it

[ ] Reject it

Explanation:
The benchmark is highly relevant to the overall clinical-trial matching problem, but it
does not directly evaluate criterion-level eligibility classification. Its main task is to
rank trials for a patient, whereas our system receives a patient record and a specific
trial's criteria and evaluates each criterion individually. We could therefore reuse or
adapt patient cases, trial criteria, and eligibility judgments, but would need to create
criterion-level reference labels such as MET, NOT MET, and UNKNOWN.

---
---

Benchmark Name: SIGIR 2016 Patient–Clinical Trial Matching Collection

Year: 2016

https://ielab.io/publications/koopman-2016-matching.html

https://bevankoopman.github.io/papers/sigir2016_clinicaltrials_collection.pdf

https://researchdata.edu.au/a-test-collection-clinical-trials/664508



### Source:
Koopman, B. & Zuccon, G. (2016).
A Test Collection for Matching Patients to Clinical Trials.
39th International ACM SIGIR Conference on Research and Development
in Information Retrieval.

### Why it seemed relevant:
The benchmark was created specifically to evaluate systems that match patients
to potentially suitable clinical trials. It contains patient case reports,
clinical trial records, and relevance assessments made by medical professionals.
This relates directly to our Clinical Trial Eligibility Screening Assistant
because both tasks require interpreting patient information in relation to
clinical-trial eligibility.

### Contamination risk:
[ ] Low

[ ] Medium

[x] High

Explanation:
The benchmark has been publicly available since 2016 and has been reused in
subsequent patient–trial matching research, including later LLM studies.
Modern models may therefore have been exposed to the paper, patient cases,
trial records, or derived benchmark examples during training. Exact exposure
for any specific model cannot be confirmed.

### Saturation risk:
[ ] Low

[x] Medium

[ ] High

Explanation:
The benchmark is old and has been used extensively in subsequent retrieval and
matching research, so newer approaches may perform substantially better than
the systems originally evaluated on it. However, patient–trial matching remains
a non-trivial task and the benchmark does not appear to be universally solved,
so high saturation would be difficult to justify.

### Format:
[ ] Multiple Choice

[ ] Free-form text

[ ] Code generation

[x] Other: information retrieval / patient-to-trial relevance ranking

### Verdict:
[ ] Use it as-is

[x] Adapt it

[ ] Reject it

Explanation:
The collection is valuable because it provides medically assessed patient–trial
pairs and realistic patient case descriptions. However, its relevance labels
reflect whether a medical assessor would refer the patient to a trial rather
than whether each individual eligibility criterion is MET, NOT MET, or UNKNOWN.
For our use case, the patient cases and trial information could therefore be
reused or adapted, but new criterion-level ground-truth labels would be needed.