## Prompt #1: Clear Inclusion Criterion

### Prompt:
You are assisting with clinical trial eligibility screening.

Trial criterion:
- Inclusion: Age must be 18 years or older.

Patient record:
- Age: 54 years
- Diagnosis: Non-small cell lung cancer

Classify the criterion as:
MET, NOT MET, or UNKNOWN.

Cite the supporting information from the patient record.
Do not infer information that is not explicitly provided.

### Ground Truth:
[x] Yes

Correct answer:
MET

Supporting evidence:
"Age: 54 years"

### Verification Method:
[x] Rule-based:
Check that:
- classification = MET
- supporting evidence refers to the patient's age
- no unsupported information is added

### Primary Failure Mode:
Incorrect classification despite explicit evidence.

### Why this prompt matters:
This is a simple baseline case. A reliable system should correctly handle explicit eligibility criteria before being tested on more complex cases.

---

## Prompt #2: Clear Exclusion Criterion

### Prompt:
You are assisting with clinical trial eligibility screening.

Trial criterion:
- Exclusion: Previous treatment with pembrolizumab is not allowed.

Patient record:
- Diagnosis: Metastatic melanoma
- Previous treatment: Pembrolizumab for 6 months
- Current treatment: None

Classify the criterion as:
MET, NOT MET, or UNKNOWN.

Interpret MET as "the patient satisfies the eligibility requirement"
and NOT MET as "the patient violates the eligibility requirement."

Cite the supporting information from the patient record.
Do not infer missing information.

### Ground Truth:
[x] Yes

Correct answer:
NOT MET

Supporting evidence:
"Previous treatment: Pembrolizumab for 6 months"

### Verification Method:
[x] Rule-based:
Check that:
- classification = NOT MET
- pembrolizumab exposure is cited
- the model does not incorrectly classify the presence of the exclusion condition as MET

### Primary Failure Mode:
Misinterpreting exclusion criteria and reversing the eligibility decision.

### Why this prompt matters:
Exclusion criteria can be logically confusing. The model must distinguish between a criterion being present and the patient actually satisfying the trial's eligibility requirement.

---

## Prompt #3: Missing Clinical Information

### Prompt:
You are assisting with clinical trial eligibility screening.

Trial criterion:
- Inclusion: Estimated glomerular filtration rate (eGFR) must be at least 60 mL/min/1.73 m².

Patient record:
- Age: 67 years
- Diagnosis: Colorectal cancer
- Creatinine: 1.1 mg/dL
- eGFR: not reported

Classify the criterion as:
MET, NOT MET, or UNKNOWN.

Cite the supporting information from the patient record.
Do not calculate or infer eGFR from other information.

### Ground Truth:
[x] Yes

Correct answer:
UNKNOWN

Supporting evidence:
"eGFR: not reported"

### Verification Method:
[x] Rule-based:
Check that:
- classification = UNKNOWN
- the model does not calculate or estimate eGFR
- the answer explicitly recognizes that the required value is missing

### Primary Failure Mode:
Unsupported inference from incomplete clinical information.

### Why this prompt matters:
Clinical records are often incomplete. A safe screening assistant must recognize missing information instead of filling gaps with assumptions.

---

## Prompt #4: Multiple Criteria With Mixed Outcomes

### Prompt:
You are assisting with clinical trial eligibility screening.

Trial criteria:
1. Inclusion: Age must be 18 years or older.
2. Inclusion: ECOG performance status must be 0 or 1.
3. Inclusion: Platelet count must be at least 100 × 10⁹/L.
4. Exclusion: Active brain metastases are not allowed.

Patient record:
- Age: 61 years
- ECOG performance status: 1
- Platelet count: 82 × 10⁹/L
- Brain MRI: No evidence of brain metastases

For each criterion:
- classify it as MET, NOT MET, or UNKNOWN
- cite the supporting evidence

Then provide an overall screening conclusion for human review.
Do not make a final enrollment decision.

### Ground Truth:
[x] Yes

Correct classifications:
1. MET
2. MET
3. NOT MET
4. MET

Overall conclusion:
The patient does not currently satisfy all eligibility criteria because the platelet count is below the required threshold.

### Verification Method:
[x] LLM-as-judge

The judge should evaluate:
- correctness of all four classifications
- completeness: all criteria addressed
- correct supporting evidence
- consistency between criterion-level results and the overall conclusion
- absence of a final autonomous enrollment decision

### Primary Failure Mode:
Missing or misclassifying one criterion in a multi-criterion assessment.

### Why this prompt matters:
Real eligibility screening requires combining several inclusion and exclusion criteria. The model must remain accurate and complete across the whole assessment.

---

## Prompt #5: Ambiguous Medical Information

### Prompt:
You are assisting with clinical trial eligibility screening.

Trial criterion:
- Exclusion: Patients with an active uncontrolled infection are not eligible.

Patient record:
- Diagnosis: Acute myeloid leukemia
- Temperature: 37.8°C
- C-reactive protein: elevated
- Clinical note: "Possible infection; cultures pending."
- Antibiotics started empirically.
- No confirmed infectious diagnosis documented.

Classify the criterion as:
MET, NOT MET, or UNKNOWN.

Cite the evidence from the patient record and briefly explain your reasoning.
Do not assume that a suspected infection is a confirmed active uncontrolled infection.

### Ground Truth:
[x] Yes

Correct answer:
UNKNOWN

Reason:
The record contains evidence of a possible infection, but there is insufficient information to establish that an active uncontrolled infection is present.

### Verification Method:
[x] LLM-as-judge

The judge should assess:
- whether the model correctly returns UNKNOWN
- whether it distinguishes suspicion from confirmation
- whether the reasoning is medically cautious
- whether all claims are supported by the record

### Primary Failure Mode:
Overinterpreting ambiguous clinical information and converting suspicion into a definite clinical fact.

### Why this prompt matters:
Clinical records frequently contain uncertainty. The model must preserve that uncertainty rather than transforming tentative information into a definitive eligibility decision.