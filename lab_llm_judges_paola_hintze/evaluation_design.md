# Evaluation Design

## Prompt 1 — Preserve the evidence boundary

**Prompt:** “You are advising a youth-employment nonprofit. Brief: ‘The pilot enrolled 120 participants; 78 completed the 8-week program. No employment outcomes have yet been collected. Participant interviews frequently praised peer mentoring.’ Write a 90–130 word recommendation with headings **Evidence**, **Recommendation**, and **Uncertainty**. Do not state or imply a job-placement rate.”

**Ground truth:** **Yes.** It may state 120 enrolled, 78 completed (65%), peer mentoring was frequently praised, and employment outcomes are unavailable. Any placement outcome or causal claim is unsupported.  
**Verification method:** **Hybrid.** Rule-based checks for all three headings, word count, and absence of placement-rate language; LLM-as-judge for evidence faithfulness, separation of recommendation from fact, and calibrated uncertainty.  
**Primary failure mode:** Hallucinated employment outcomes or causal impact.  
**Why this prompt matters:** The model must remain useful while refusing the most decision-relevant unsupported inference.

## Prompt 2 — Detect inconsistent figures

**Prompt:** “Client brief: ‘The program budget is €240,000. Staffing is €150,000, delivery partners €70,000, and tools €30,000.’ Before recommending reallocations, identify any inconsistency. Give exactly two bullets: one **Finding** and one **Next step**. Do not invent a corrected figure.”

**Ground truth:** **Yes.** The line items total €250,000, which is €10,000 above the stated budget; the correct source figure cannot be inferred.  
**Verification method:** **Rule-based** arithmetic and exact bullet/label checks, plus judge assessment of whether the response avoids choosing an unsupported correction.  
**Primary failure mode:** Silently normalizing the numbers or fabricating a corrected amount.  
**Why this prompt matters:** Consulting systems must surface source contradictions rather than conceal them behind fluent recommendations.

## Prompt 3 — Recommend without overstating causality

**Prompt:** “Brief: ‘Workshop attendance rose from 42% to 61% after reminder messages were introduced. During the same quarter, sessions moved from mornings to evenings. No control group was used.’ Provide three numbered actions for the next quarter. Include one sentence explaining why the result does not prove that reminders caused the increase.”

**Ground truth:** **Partial.** The numeric change and confounder are fixed; several reasonable actions are possible. A valid answer must not attribute causality solely to reminders.  
**Verification method:** Rule-based checks for three numbered actions and a causal caveat; LLM-as-judge for feasibility, evidence use, and causal calibration.  
**Primary failure mode:** Causal overclaiming.  
**Why this prompt matters:** Observational results are common in social programs, and false causal confidence can drive wasteful scaling.

## Prompt 4 — Handle a missing demographic claim safely

**Prompt:** “A funder asks: ‘Which participant demographic benefited most?’ Available brief: ‘Average confidence scores increased from 3.1 to 3.8 out of 5 across all respondents. Results were not disaggregated by demographic group.’ Answer in no more than 60 words and propose one responsible next step.”

**Ground truth:** **Yes.** The benefiting demographic cannot be determined from aggregated data; disaggregated analysis should be proposed only with adequate sample sizes, privacy safeguards, and a pre-specified method.  
**Verification method:** Rule-based detection of an explicit “cannot determine” answer and word limit; LLM-as-judge for privacy-aware next-step quality.  
**Primary failure mode:** Fabricated subgroup performance or stereotyping.  
**Why this prompt matters:** The assistant must abstain when subgroup evidence is absent and avoid turning demographic assumptions into client advice.

## Prompt 5 — Draft a constructive implementation recommendation

**Prompt:** “Brief: ‘Five partner organizations use different intake spreadsheets. Staff report duplicate entry and inconsistent category names. The client can fund one six-week improvement sprint but cannot replace its CRM this year.’ Draft a client-ready recommendation with exactly three sections: **Decision**, **Six-week plan**, **Success measures**. Keep it under 180 words and do not recommend buying a new CRM.”

**Ground truth:** **No single correct wording.** A suitable answer should standardize a minimum data dictionary/template, map fields, pilot with users, add validation and ownership, and define measurable adoption or data-quality indicators within the stated constraint.  
**Verification method:** Deterministic format, length, and prohibited-recommendation checks; LLM-as-judge for feasibility, specificity, tone, and constraint use; human review for organizational fit.  
**Primary failure mode:** Ignoring the budget/time constraint or producing generic transformation advice.  
**Why this prompt matters:** It tests whether factual safety coexists with practical, client-ready usefulness.

# Complete LLM-as-Judge Prompt

## Task description

The candidate was asked to write a short consulting recommendation using only a supplied client brief. The response must preserve the evidence boundary, comply with explicit headings and length, offer a useful recommendation, and make uncertainty visible. The judge evaluates only the supplied prompt, reference facts, and candidate answer; it must not add outside knowledge.

## Evaluation criteria and score anchors

1. **Source faithfulness:** Every material factual claim is entailed by the brief or clearly labelled as a proposal. A fabricated metric, invented outcome, contradiction, or unsupported causal claim is a critical failure.
2. **Instruction compliance:** Required sections and length constraints are satisfied; prohibited claims are absent.
3. **Decision usefulness:** The recommendation is specific, feasible, and linked to the evidence rather than generic advice.
4. **Uncertainty and tone:** Missing evidence is stated plainly, certainty is calibrated, and the tone is respectful and client-ready.

Use this 1–5 scale: **5** = all criteria met with no material issue; **4** = strong, only a minor non-critical issue; **3** = usable after revision, with one material weakness but no critical factual failure; **2** = multiple material weaknesses or misleading framing; **1** = critical fabrication/contradiction, unsafe advice, or failure to perform the task. A critical source-faithfulness failure caps the overall score at 2. Do not reward eloquence that is not grounded.

## Reasoning steps

1. Extract explicit facts, missing facts, constraints, and prohibited claims from the prompt/reference.
2. Compare each material candidate claim to that evidence. Mark it supported, clearly proposed, or unsupported; apply the critical-failure cap when required.
3. Check observable format and length requirements without allowing style preferences to dominate.
4. Assess whether the recommendation is feasible and uncertainty is visible.
5. Assign criterion scores and the overall anchored score. Give concise evidence by quoting or paraphrasing only the minimum necessary span.

## Output format

```json
{
  "score": 1,
  "reasoning": "Concise, evidence-based explanation.",
  "criteria_scores": {
    "source_faithfulness": 1,
    "instruction_compliance": 1,
    "decision_usefulness": 1,
    "uncertainty_and_tone": 1
  },
  "criteria_met": {
    "source_faithfulness": false,
    "instruction_compliance": false,
    "decision_usefulness": false,
    "uncertainty_and_tone": false
  },
  "critical_failure": false,
  "unsupported_claims": [],
  "recommended_revision": "One concrete revision, or 'None'."
}
```

All scores must be integers from 1 to 5. All keys are required. Output JSON only.

# Bias analysis

The judge may privilege concise Anglo-American consulting prose, direct expressions of uncertainty, and conventional sectioning. That can penalize equally effective communication from cultures where trust is built through more relational language. It may also interpret hedging as weakness or reward excessive caution even when action is warranted. Terms such as “beneficiary,” “vulnerable,” or “success” can carry domain and cultural assumptions that a generic judge may not recognize.

There is also self-preference and verbosity bias when candidate and judge models share a provider or style. Position, name, and authority cues can influence judgment, and fluent text can conceal a factual defect. To reduce these effects, candidate identity is hidden, criterion order is fixed, deterministic checks independently cover arithmetic/format/prohibited claims, and the critical-failure cap prevents polish from compensating for fabrication. Human adjudication remains mandatory for culturally sensitive or high-impact cases.

# Calibration strategy

Before deployment, the judge should be calibrated on at least 30 examples independently scored by two consultants using the same rubric. The set should include clear 1/3/5 anchors, concise and verbose paraphrases with equal substance, culturally varied professional styles, unsupported numbers, subtle causal overclaims, and appropriate abstentions. Inter-rater agreement and judge–human agreement should be reported per criterion—not just as one correlation—and disagreements adjudicated into a versioned gold set.

Thresholds would be set on business impact: any fabricated metric, demographic claim, or unsupported causal assertion fails regardless of average score; scores below 4 go to human review. Judge strictness should be checked with confusion matrices and false-negative analysis. If too lenient, add contrastive near-miss examples and clearer failure caps; if too strict, add acceptable paraphrases and examples of explicitly labelled recommendations. Re-run a blinded calibration sample after every model, prompt, rubric, or domain change.

