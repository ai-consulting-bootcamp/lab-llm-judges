# LLM-as-Judge Design

## Task Description

The model is assisting with clinical trial eligibility screening.

It receives:
- a patient record
- a set of clinical trial inclusion and exclusion criteria

For each criterion, the model must:
1. classify it as MET, NOT MET, or UNKNOWN
2. cite supporting information from the patient record

The model must then provide an overall screening conclusion for review by a clinical research professional.

The model must not infer missing clinical information and must not make the final enrollment decision.

---

## Evaluation Criteria

1. Criterion-level accuracy:
Each eligibility criterion must be classified correctly as MET, NOT MET, or UNKNOWN according to the patient record and reference answer.

2. Completeness:
All trial criteria must be evaluated. No criterion may be omitted.

3. Evidence grounding:
Each classification must be supported by information explicitly present in the patient record. The response must not introduce unsupported facts or assumptions.

4. Overall consistency:
The overall screening conclusion must be consistent with the individual criterion-level classifications.

5. Decision boundary:
The response must remain a decision-support assessment and must not independently make the final patient enrollment decision.

---

## Reasoning Steps

Step 1:
Compare each criterion with the corresponding information in the patient record.

Step 2:
Compare the model's classification for each criterion against the reference classification.

Step 3:
Check whether every criterion has been evaluated and supported with appropriate evidence from the patient record.

Step 4:
Identify any unsupported inference, invented information, or interpretation that goes beyond the supplied record.

Step 5:
Check whether the overall conclusion logically follows from the criterion-level results.

Step 6:
Check that the model does not make an autonomous final enrollment decision.

Step 7:
Assign an overall score based on the criteria below.

Score anchors:
5 = Fully correct, complete, grounded, and appropriately cautious.

4 = Mostly correct with one minor issue that does not affect the eligibility assessment.

3 = Partially correct but contains a meaningful omission, inconsistency, or weakly supported 
statement.

2 = Multiple important errors or unsupported conclusions.

1 = Fundamentally incorrect, misleading, or unsafe assessment.

---

## Output Format

{
  "score": 1-5,
  "reasoning": "Brief explanation of the score",
  "criteria_met": {
    "criterion_level_accuracy": true,
    "completeness": true,
    "evidence_grounding": true,
    "overall_consistency": true,
    "decision_boundary": true
  }
}

---
---

### Hidden biases

The judge itself can introduce bias. For example, it may prefer a particular writing style even though style is not part of our task, or penalize a concise answer compared with a longer one even when both are equally correct. It may also rely on its own medical knowledge and “correct” the reference answer instead of evaluating only against the supplied patient record and trial criteria.

There is also a domain-specific risk: the judge may interpret ambiguous clinical language more confidently than a human expert would. For example, it could treat “possible infection” as confirmed infection. We therefore need to explicitly instruct the judge to evaluate grounding and uncertainty preservation, not general medical plausibility.

### Calibration strategy

We should calibrate the judge using a small set of known examples before using it on the full evaluation. I would prepare at least three reference responses: one clearly excellent response, one partially correct response, and one clearly poor response. We then check whether the judge gives approximately the expected scores, such as 5, 3, and 1.

We should also include edge cases, especially missing information and ambiguous clinical wording. If the judge is consistently too strict or too lenient, we adjust the scoring anchors or add examples showing what each score should mean. 