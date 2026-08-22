# LLM-as-Judge Evaluation Lab

## Overview

This project implements an end-to-end evaluation workflow for an LLM-based **Clinical Trial Eligibility Screening Assistant**.

The goal is to evaluate whether an LLM can reliably assess clinical trial eligibility criteria using only information explicitly provided in a patient record. The project combines benchmark review, custom evaluation design, an LLM-as-judge, automated metric collection, and result analysis.

---

## Scenario

The system receives:

- a short patient record
- clinical trial inclusion and exclusion criteria

For each criterion, the assistant must classify the available evidence as:

- `MET`
- `NOT MET`
- `UNKNOWN`

The assistant must also cite supporting evidence from the patient record.

For cases with multiple criteria, it may provide an overall screening conclusion for review by a clinical research professional.

The system must:

- use only information explicitly provided in the patient record
- avoid inferring missing clinical information
- avoid inventing patient information
- preserve uncertainty when information is incomplete or ambiguous
- not make the final enrollment decision

The intended use is **clinical decision support**, not autonomous patient enrollment.

---

## Evaluation Approach

The project follows three main stages:

1. Review existing benchmarks relevant to clinical trial matching.
2. Design a custom evaluation tailored to criterion-level eligibility screening.
3. Implement and run an LLM-as-judge evaluation using the OpenAI API.

### Benchmark Review

Three existing benchmarks were reviewed:

- **TrialGPT-Matching**
- **TREC 2022 Clinical Trials Track**
- **SIGIR 2016 Patient–Clinical Trial Matching Collection**

These benchmarks are relevant because they evaluate different aspects of patient-to-clinical-trial matching.

However, none of them directly matches the required output format of this project. In particular, TREC and SIGIR primarily focus on patient-to-trial retrieval or relevance, while this project requires a criterion-by-criterion classification.

Therefore, the benchmarks were used as references and a custom evaluation dataset was created.

---

## Custom Test Dataset

The evaluation dataset contains five synthetic clinical trial screening cases designed to cover different types of reasoning:

1. **Clear inclusion criterion**  
   Tests whether the model correctly identifies an explicitly satisfied requirement.

2. **Exclusion criterion**  
   Tests whether the model correctly interprets exclusion logic.

3. **Missing clinical information**  
   Tests whether the model returns `UNKNOWN` instead of inferring missing values.

4. **Multiple criteria**  
   Tests completeness and consistency across several inclusion and exclusion criteria.

5. **Ambiguous clinical information**  
   Tests whether the model preserves uncertainty instead of converting suspected information into confirmed information.

Each test case contains:

- the original prompt
- patient information
- trial criteria
- predefined ground truth
- expected evaluation criteria

---

## Models

### Model Being Evaluated

`gpt-4o-mini`

This model generates the clinical trial eligibility screening responses.

### Judge Model

`gpt-4.1-mini`

A different model is used as the judge to reduce the limitation of having the tested model evaluate its own responses.

---

## LLM-as-Judge Design

The judge compares each generated response with the predefined ground truth.

Each response is evaluated across five dimensions:

### 1. Criterion-Level Accuracy

Are the `MET`, `NOT MET`, and `UNKNOWN` classifications correct?

### 2. Completeness

Did the model address every requested eligibility criterion?

### 3. Evidence Grounding

Are classifications and explanations supported by information explicitly present in the patient record?

### 4. Overall Consistency

Is the overall screening conclusion consistent with the individual criterion-level classifications?

### 5. Decision Boundary

Does the model remain a decision-support tool rather than making an autonomous final enrollment decision?

The judge assigns an overall score from **1 to 5**:

- `5` — fully correct, complete, grounded, and appropriately cautious
- `4` — mostly correct with a minor issue
- `3` — partially correct with a meaningful omission or inconsistency
- `2` — multiple important errors or unsupported conclusions
- `1` — fundamentally incorrect, misleading, or unsafe

The judge returns structured JSON containing:

- overall score
- reasoning
- pass/fail assessment for each evaluation criterion

---

## Implementation

The evaluation is implemented using the **OpenAI API directly**, without LangChain.

The main evaluation script performs the following workflow:

```text
Clinical trial prompt
        ↓
gpt-4o-mini
        ↓
Candidate response
        ↓
Ground truth + evaluation rubric
        ↓
gpt-4.1-mini judge
        ↓
Score + reasoning + criteria assessment
        ↓
Metrics
        ↓
evaluation_results.json
```







Run the evaluation:     python llm_judge_evaluation.py

saves the results to:   evaluation_results.json

Analyze the results:    python analyze_results.py

generates:              score_distribution.png and criteria_pass_rates.png

project files:

benchmark_audit.md  
evaluation_design.md  
evaluation_memo.md  
reflection.md  
llm_judge_evaluation.py  
analyze_results.py  
evaluation_results.json  
implementation_summary.md  
score_distribution.png  
criteria_pass_rates.png  
README.md  

Key Limitation

The evaluation dataset contains only five synthetic and relatively controlled examples. Although the model achieved full scores on all cases, the dataset is too small to establish robust real-world performance. A stronger evaluation would include a larger set of difficult and ambiguous cases, expert-reviewed ground truth, and human validation of the LLM judge.