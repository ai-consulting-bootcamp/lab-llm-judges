# TenderAI Evaluation Design

## 1. Evaluation Strategy

The evaluation is designed for a TenderAI-style Retrieval-Augmented Generation (RAG) assistant that analyzes tender requirements using a company knowledge base.

The evaluation focuses on five capabilities that are important for production use:

1. Evidence sufficiency
2. Evidence extraction
3. Multi-document reasoning
4. Instruction following
5. Contradictory evidence handling

The goal is not simply to measure whether the model produces fluent answers. The evaluation measures whether the model produces answers that are supported by the available evidence and appropriate for a professional tender-analysis workflow.

---

# Prompt 1 — Evidence Sufficiency

## Prompt

A tender requirement states:

> "Demonstrate experience delivering offshore wind projects with a capacity greater than 100 MW."

The retrieved company evidence contains the following project references:

* NorthWind Farm — 48 MW
* SunVale Solar Park — 35 MW
* Coastal Wind Extension — 22 MW

Based only on the provided evidence, assess whether the company can demonstrate experience with an offshore wind project greater than 100 MW.

Do not introduce information that is not contained in the evidence.

## Ground Truth

**Yes.**

The provided evidence does not demonstrate experience with an offshore wind project greater than 100 MW.

The appropriate conclusion is **INSUFFICIENT**.

The model should not invent or infer the existence of a qualifying project.

## Verification Method

**Rule-based + LLM-as-judge**

Rule-based checks can identify whether the response contains an unsupported qualifying project or incorrectly claims that the requirement is fully supported.

An LLM judge can evaluate whether the conclusion is properly supported by the evidence and whether the response avoids unsupported claims.

## Primary Failure Mode

**Hallucination / unsupported claim**

## Why This Prompt Matters

A tender assistant must be able to recognize when the knowledge base does not contain sufficient evidence. Incorrectly claiming that a company has completed a qualifying project could create commercial and compliance risks.

---

# Prompt 2 — Evidence-Based Project Identification

## Prompt

Using only the provided company evidence, identify the project references that are relevant to a renewable-energy experience requirement.

For each relevant project, provide:

* Project name
* Technology
* Capacity

Do not add information that is not contained in the evidence.

## Ground Truth

The expected information must match the source documents.

Known synthetic examples include:

* NorthWind Farm — Wind — 48 MW
* SunVale Solar Park — Solar — 35 MW
* Coastal Wind Extension — Wind — 22 MW

The evaluator should treat the source documents as the authoritative ground truth.

## Verification Method

**Rule-based + LLM-as-judge**

Project names, technologies, and capacities can be compared against the source data using exact or normalized matching.

An LLM judge can evaluate whether the response accurately represents the evidence without introducing unsupported information.

## Primary Failure Mode

**Incorrect information extraction / hallucination**

## Why This Prompt Matters

Correct retrieval does not automatically guarantee a correct final answer. The model may retrieve the correct document but incorrectly extract, combine, or transform the information.

---

# Prompt 3 — Multi-Document Reasoning

## Prompt

You are assessing a tender requirement that asks the company to demonstrate:

* relevant quality certifications,
* renewable-energy project experience, and
* engineering/procurement support experience.

Use only the provided evidence from the company knowledge base.

Summarize:

1. Which parts of the requirement are supported.
2. What evidence supports each part.
3. Which parts remain unsupported or require additional evidence.

Do not assume that information not present in the evidence is true.

## Ground Truth

The ground truth is based on the individual source documents.

For example:

* The company has ISO 9001 certification.
* The company has renewable-energy project references.
* The company has engineering and procurement support capabilities.

The evaluation should verify whether the model correctly connects each requirement to the appropriate evidence and identifies any missing evidence.

## Verification Method

**LLM-as-judge**

A judge evaluates whether the response:

* correctly identifies the supported requirements,
* connects claims to the correct evidence,
* identifies gaps,
* avoids unsupported assumptions.

## Primary Failure Mode

**Missing information / incomplete reasoning**

## Why This Prompt Matters

Real tender analysis often requires combining information from several documents. A system that only works when all evidence appears in one document will have limited usefulness in a real consulting workflow.

---

# Prompt 4 — Instruction Following

## Prompt

Assess the tender requirement using exactly these four sections:

STATUS

EVIDENCE

GAP

RECOMMENDATION

Do not add any other sections.

Use only the provided evidence when making the assessment.

## Ground Truth

**Yes.**

The expected response structure is explicitly defined.

The response must contain:

1. STATUS
2. EVIDENCE
3. GAP
4. RECOMMENDATION

No additional sections should be introduced.

The content within those sections must still be evidence-based.

## Verification Method

**Rule-based**

A program can check whether:

* STATUS exists.
* EVIDENCE exists.
* GAP exists.
* RECOMMENDATION exists.
* Unexpected sections have not been added.

A secondary semantic evaluation can verify that the content of the sections is appropriate.

## Primary Failure Mode

**Instruction-following failure**

## Why This Prompt Matters

In a production workflow, structured output may be consumed by another application or automation step. Failure to follow the required format can therefore cause downstream workflow failures even when the underlying reasoning is correct.

---

# Prompt 5 — Contradictory Evidence

## Prompt

Two company documents contain conflicting information about the same project:

**Document A:**

> Project X — 48 MW

**Document B:**

> Project X — 120 MW

The tender requirement asks the company to demonstrate experience with a project greater than 100 MW.

Assess whether the company can currently claim that Project X satisfies the requirement.

Identify the conflict and explain what should happen before making the claim.

Do not choose one version without acknowledging the contradiction.

## Ground Truth

**The company should not make the claim without verification.**

The two documents contain contradictory capacity information.

The correct response should:

1. Identify the contradiction.
2. Avoid treating either value as definitively correct.
3. Recommend verification of the authoritative source before using Project X as evidence for the tender requirement.

## Verification Method

**LLM-as-judge**

The judge evaluates whether the model identifies the contradiction, avoids making an unsupported claim, and recommends appropriate verification.

## Primary Failure Mode

**False claim / failure to handle contradictory evidence**

## Why This Prompt Matters

Enterprise knowledge bases can contain outdated, duplicated, or contradictory information. A reliable AI system should detect uncertainty rather than silently selecting the information that produces the most favorable answer.

---

# 2. LLM-as-Judge Design

## Selected Evaluation

The LLM-as-judge will evaluate **Prompt 1 — Evidence Sufficiency**.

This evaluation is particularly important because hallucination and unsupported claims are major risks in tender analysis.

---

## Task Description

The original model is asked to determine whether a tender requirement is supported by the retrieved company evidence.

The model must assess the evidence provided and determine whether the company can demonstrate experience with an offshore wind project greater than 100 MW.

The provided evidence contains project capacities of 48 MW, 35 MW, and 22 MW.

The judge must determine whether the model's response is supported by this evidence.

---

## Evaluation Criteria

### Criterion 1 — Evidence Grounding

The response must base its conclusion only on the evidence provided.

### Criterion 2 — Correct Compliance Judgment

The response should conclude that the requirement is insufficiently supported because none of the listed projects exceeds 100 MW.

### Criterion 3 — Hallucination Avoidance

The response must not invent a project, capacity, customer, or other evidence that is not present in the supplied information.

### Criterion 4 — Explanation Quality

The response should clearly explain why the evidence is insufficient rather than providing an unsupported conclusion.

---

## Reasoning Steps

The judge should evaluate the response in the following order:

### Step 1 — Identify the evidence

Determine what project capacities are actually present in the supplied evidence.

### Step 2 — Compare the evidence with the requirement

Check whether any supplied project demonstrates capacity greater than 100 MW.

### Step 3 — Check for unsupported claims

Determine whether the model introduced information that was not contained in the evidence.

### Step 4 — Evaluate the final conclusion

Determine whether the model correctly concluded that the evidence is insufficient.

---

## Output Format

The judge should return structured JSON:

```json
{
  "score": 1,
  "reasoning": "The response correctly identifies that none of the supplied projects exceeds 100 MW and does not introduce unsupported evidence.",
  "criteria_met": {
    "evidence_grounding": true,
    "correct_compliance_judgment": true,
    "hallucination_avoidance": true,
    "explanation_quality": true
  }
}
```

### Score Scale

| Score | Meaning                                                                    |
| ----- | -------------------------------------------------------------------------- |
| 1     | Very poor — incorrect conclusion and/or major unsupported claims           |
| 2     | Poor — significant problems but some relevant reasoning                    |
| 3     | Acceptable — partially correct but with weaknesses                         |
| 4     | Good — correct and well-supported with minor weaknesses                    |
| 5     | Excellent — fully correct, grounded, clear, and free of unsupported claims |

---

# 3. Judge Bias Analysis

An LLM-as-judge can introduce its own biases and should therefore not be treated as an objective source of truth.

### Hidden Biases

The judge may prefer certain writing styles, such as highly detailed or formal responses, even when a shorter response is factually correct. It may also favor a particular language style or terminology. Since TenderAI may eventually operate in multilingual environments, language-specific preferences could influence scoring.

The judge could also be overly impressed by fluent or confident responses. A polished response may appear better than a concise response even when the polished response contains unsupported claims. The evaluation therefore needs explicit criteria that prioritize evidence grounding over writing style.

### Domain Bias

The judge may have its own assumptions about engineering, procurement, renewable energy, or tender processes. To reduce this problem, the judge should be instructed to rely only on the supplied task, evidence, and evaluation criteria rather than external knowledge.

---

# 4. Judge Calibration Strategy

Before using the judge on production-like test cases, it should be calibrated using examples with known quality levels.

At minimum, calibration should include:

* one clearly correct response,
* one response that incorrectly claims sufficient evidence,
* one response containing a hallucinated project,
* one partially correct response,
* one response that correctly identifies insufficient evidence but provides a weak explanation.

These examples establish score anchors and help determine whether the judge is too strict or too lenient.

If the judge consistently gives high scores to hallucinated responses, the rubric should be strengthened around evidence grounding and unsupported claims. If it penalizes correct concise answers too heavily, the rubric should be adjusted so that style is not rewarded over factual correctness.

The calibration examples should remain separate from the final test set where possible. This reduces the risk that the evaluator is simply learning the expected answers instead of providing an independent assessment.

---

# 5. Evaluation Principles

The evaluation follows five principles:

1. **Grounding over fluency** — factual support is more important than writing style.
2. **Evidence before assumptions** — the model should not rely on information outside the supplied evidence when the task requires evidence-grounded analysis.
3. **Explicit uncertainty** — insufficient or contradictory evidence should be reported rather than hidden.
4. **Multiple evaluation methods** — rule-based checks are preferred when objective verification is possible, while LLM-as-judge is used for more semantic criteria.
5. **Human oversight** — automated evaluation should support, not completely replace, human review for high-impact tender decisions.
