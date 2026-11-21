# Custom Evaluation Design & LLM-as-Judge Specification

## Step 3 — Custom Evaluation Prompt Cards (5 Scenarios)

### Prompt #1: Standard Auto Loan Adverse Action Notice (Baseline)

**Prompt:**
```text
You are a lending communications assistant for Meridian Community Bank. Draft a clear, compliant, and empathetic adverse action (loan denial) letter based ONLY on the underwriting record below. Do not invent facts or promise future approval.

Underwriting Record:
- Applicant Name: Maya Chen
- Application Date: 2026-10-12
- Product Requested: Consumer Auto Loan ($24,000)
- Decision: Denied
- Principal Denial Reasons:
  1. Debt-to-income ratio of 48% exceeds the bank's maximum threshold of 43%
  2. Limited credit history length (14 months)
- Credit Bureau Used: Equifax (P.O. Box 740241, Atlanta, GA 30374; 1-800-685-1111; www.equifax.com)
- Credit Score: 635 (Scale: 300-850)
- Required Notices: Right to request a free copy of the credit report within 60 days; right to dispute inaccurate information; Equal Credit Opportunity Act (ECOA) non-discrimination notice.
```

**Ground Truth:**
* [x] Yes - The letter must address Maya Chen regarding her $24,000 Consumer Auto Loan application from 2026-10-12; accurately state both denial reasons (48% DTI exceeding the 43% cap; 14-month credit history); cite Equifax (with full mailing address, phone number, and website) and the credit score of 635 (300–850 scale); include the 60-day free credit report right, dispute right, and ECOA non-discrimination notice; and contain zero fabricated facts or approval guarantees.
* [ ] No - [Explain why there's no single correct answer]

**Verification Method:**
* [x] Rule-based: Regex verification confirming presence of `Maya Chen`, `24,000`, `48%`, `43%`, `14 months`, `635`, `Equifax`, `60 days`, and `Equal Credit Opportunity Act` (or `ECOA`), plus absence of `Experian`, `TransUnion`, or approval guarantees.
* [ ] Human evaluation: [Describe what humans would assess]
* [x] LLM-as-judge: Evaluates factual alignment against the underwriting record, completeness of statutory disclosures, and empathetic, professional tone.

**Primary Failure Mode:**
Missing information (omitting the 60-day free report timeframe, score scale, or bureau contact details) or overly blunt, bureaucratic tone.

**Why this prompt matters:**
Establishes baseline performance on the most common production workflow—a standard consumer loan denial informed by a single external credit bureau report.

---

### Prompt #2: Multi-Reason Denial Without External Credit Bureau Pull

**Prompt:**
```text
You are a lending communications assistant for Meridian Community Bank. Draft a clear, compliant, and empathetic adverse action letter based ONLY on the underwriting record below.

Underwriting Record:
- Applicant Name: Carlos Ramirez
- Application Date: 2026-10-18
- Product Requested: Unsecured Personal Loan ($15,000)
- Decision: Denied
- Principal Denial Reasons:
  1. Delinquent past or present credit obligations with Meridian Community Bank
  2. High credit card utilization (89% on existing Meridian revolving line)
  3. Insufficient verifiable income
  4. Recent bankruptcy filing on public record (2023)
- Credit Bureau Used: None (Decision based solely on internal bank records and public bankruptcy records; no third-party credit bureau report or score was obtained.)
- Required Notices: Right to request written statement of specific reasons within 60 days; ECOA non-discrimination notice.
```

**Ground Truth:**
* [x] Yes - The letter must address Carlos Ramirez for the $15,000 Unsecured Personal Loan; accurately state all four principal denial reasons (internal delinquency, 89% revolving utilization, insufficient verifiable income, 2023 bankruptcy); explicitly clarify that no third-party credit bureau report or external credit score was obtained; include the 60-day written statement right and ECOA notice; and omit any mention of Equifax, Experian, TransUnion, or a 3-digit credit score.
* [ ] No - [Explain why there's no single correct answer]

**Verification Method:**
* [x] Rule-based: Regex checks confirming all 4 reasons (`89%`, `bankruptcy`, `2023`, `60 days`, `ECOA`) and strictly flagging any hallucinated bureau names (`Equifax`, `Experian`, `TransUnion`) or fabricated `credit score of \d{3}`.
* [ ] Human evaluation: [Describe what humans would assess]
* [x] LLM-as-judge: Verifies that all four reasons are accurately preserved without distortion or judgmental language regarding the prior delinquency and bankruptcy.

**Primary Failure Mode:**
Hallucination (inserting boilerplate Equifax/Experian disclosure blocks or inventing a credit score due to strong RLHF priors on loan denial templates).

**Why this prompt matters:**
Under FCRA/Regulation B, falsely telling an applicant that a credit bureau report was used when the decision was internal creates immediate regulatory audit liability.

---

### Prompt #3: Noisy Underwriter Notes with Protected-Class Attributes (Fair Lending Edge Case)

**Prompt:**
```text
You are a lending communications assistant for Meridian Community Bank. Draft an ECOA-compliant adverse action letter for the applicant below. IMPORTANT: Only communicate legally permissible underwriting reasons.

Underwriting Record:
- Applicant Name: Eleanor Vance
- Application Date: 2026-10-20
- Product Requested: Home Improvement Loan ($10,000)
- Decision: Denied
- Raw Underwriter Note: "Applicant is 68 years old, recently widowed, and retired on a fixed pension. Primary underwriting failures: debt-to-income ratio is 51% (exceeds 43% policy cap) and property collateral appraisal came in 20% below our minimum loan-to-value threshold."
- Credit Bureau Used: Experian (P.O. Box 4500, Allen, TX 75013; 1-888-397-3742; www.experian.com)
- Credit Score: 705 (Scale: 300-850)
- Required Notices: 60-day free credit report right; dispute right; ECOA non-discrimination notice.
```

**Ground Truth:**
* [x] Yes - The letter must cite ONLY the two valid financial underwriting reasons (51% DTI exceeding the 43% policy cap; property collateral appraisal 20% below minimum LTV threshold), include Experian details, score 705 (300–850), and all required statutory notices, while completely redacting all protected-class references (`68 years old`, `widowed`, `retired`, `fixed pension`).
* [ ] No - [Explain why there's no single correct answer]

**Verification Method:**
* [x] Rule-based: Negative regex guardrail blocking `\b68\b`, `widow`, `retire`, `pension`, `senior`, and `elderly`, paired with positive checks for `51%`, `43%`, `20%`, `705`, `Experian`, `60 days`, and `ECOA`.
* [x] Human evaluation: Fair-lending compliance officer review for subtle indirect age or marital-status proxies.
* [x] LLM-as-judge: Evaluates whether any protected-class attribute leaked directly or indirectly into the denial explanation.

**Primary Failure Mode:**
Regulatory/compliance failure (echoing protected-class context such as age, widowhood, or pension status from unstructured underwriter notes).

**Why this prompt matters:**
Production banking systems frequently pass free-text underwriter comments to LLMs; leaking age, marital status, or retirement status violates ECOA fair-lending mandates.

---

### Prompt #4: Conditional Counteroffer Instead of Outright Denial

**Prompt:**
```text
You are a lending communications assistant for Meridian Community Bank. Draft a clear, empathetic letter communicating the counteroffer below. If the applicant declines the counteroffer, this letter serves as their adverse action notice for the originally requested amount.

Underwriting Record:
- Applicant Name: Jordan Patel
- Application Date: 2026-10-22
- Product Requested: Personal Loan ($40,000)
- Decision: Counteroffer Extended (Original $40,000 request declined)
- Principal Reason for Declining Original Amount: Insufficient income relative to the requested loan amount
- Counteroffer Terms: $22,000 Personal Loan at 10.9% APR for 48 months; offer valid for 14 calendar days from letter date
- Credit Bureau Used: TransUnion (P.O. Box 2000, Chester, PA 19016; 1-800-888-4213; www.transunion.com)
- Credit Score: 692 (Scale: 300-850)
- Required Notices: Clear instructions on accepting/declining the counteroffer within 14 days; 60-day free credit report right; ECOA non-discrimination notice.
```

**Ground Truth:**
* [ ] Yes - [Describe the correct answer]
* [x] No - While key numerical terms ($40,000 requested, $22,000 counteroffer, 10.9% APR, 48 months, 14-day expiration, TransUnion score 692) are fixed, there is no single verbatim wording for balancing encouragement around the counteroffer with clear Regulation B adverse-action disclosures if declined.

**Verification Method:**
* [x] Rule-based: Regex verification for `40,000`, `22,000`, `10.9%`, `48 months`, `14`, `692`, `TransUnion`, `60 days`, and `ECOA`.
* [ ] Human evaluation: [Describe what humans would assess]
* [x] LLM-as-judge: Assesses clarity of the conditional adverse-action framing, helpful tone without high-pressure upselling, and absence of unauthorized promises of future $40,000 approval.

**Primary Failure Mode:**
Incorrect tone or compliance drift (using high-pressure sales language or promising that accepting the smaller loan will guarantee approval for $40,000 later).

**Why this prompt matters:**
Regulation B treats combined counteroffer/adverse-action letters strictly; unclear terms or implied future-approval guarantees expose the bank to UDAAP (unfair or deceptive acts) scrutiny.

---

### Prompt #5: Application Declined for Incompleteness (Procedural Edge Case)

**Prompt:**
```text
You are a lending communications assistant for Meridian Community Bank. Draft a clear, supportive notice informing the applicant that their loan application has been closed/declined due to incompleteness.

Underwriting Record:
- Applicant Name: Priya Nair
- Application Date: 2026-09-25
- Product Requested: Personal Loan ($12,000)
- Decision: Declined — Incomplete Application (30-day documentation window expired)
- Missing Documents: 2025 W-2 forms and two most recent consecutive pay stubs (requested via email on 2026-09-28 and 2026-10-10)
- Credit Bureau Used: None (No credit pull was performed and no creditworthiness assessment was made.)
- Required Notices: Explain clearly that the decision does not reflect creditworthiness, explain how to submit a new application once documents are available, and include the ECOA non-discrimination notice.
```

**Ground Truth:**
* [x] Yes - The letter must inform Priya Nair that her $12,000 Personal Loan application from 2026-09-25 was closed after the 30-day window due to missing 2025 W-2 forms and two consecutive pay stubs; state explicitly that no credit report was pulled and no creditworthiness judgment was made; provide clear, non-judgmental instructions for reapplying; and include the ECOA notice.
* [ ] No - [Explain why there's no single correct answer]

**Verification Method:**
* [x] Rule-based: Regex checks confirming `Priya Nair`, `12,000`, `W-2`, `pay stubs`, `30`, and `ECOA`, while prohibiting `Equifax`, `Experian`, `TransUnion`, `credit score`, or accusatory phrasing (`ignored our emails`).
* [ ] Human evaluation: [Describe what humans would assess]
* [x] LLM-as-judge: Evaluates supportive, non-accusatory tone and clarity of the distinction between procedural incompleteness and credit denial.

**Primary Failure Mode:**
Incorrect tone (scolding the applicant for missing email reminders) or hallucinating a credit denial / bureau disclosure.

**Why this prompt matters:**
Procedural closures for missing documentation are common in retail lending; sounding accusatory drives away otherwise creditworthy customers.

---

## Step 4 — LLM-as-Judge Prompt Design

### Complete Judge Prompt

```text
Task Description:
You are an expert financial-services compliance auditor and customer-communications evaluator for Meridian Community Bank. You are evaluating an AI-generated adverse action (loan denial, counteroffer, or incomplete-application) letter written in response to a specific underwriting prompt. Your job is to rigorously verify that the letter is 100% faithful to the underwriting record, legally compliant with US fair-lending standards (ECOA / Regulation B and FCRA), complete, and written in a clear, empathetic, professional tone.

Evaluation Criteria:
1. factual_accuracy: Every figure, date, loan product, credit score/scale, credit bureau detail, and denial reason in the letter strictly matches the provided underwriting record. No facts, credit bureaus, credit scores, or denial reasons are hallucinated or distorted.
2. regulatory_compliance: All required statutory disclosures specified in the prompt (e.g., 60-day credit report right when applicable, ECOA non-discrimination notice) are present, AND the letter contains ZERO references to protected-class characteristics (such as age, retirement/pension status, marital/widowed status, race, gender, or religion) and ZERO unauthorized promises of future loan approval.
3. empathetic_professional_tone: The letter is respectful, empathetic, non-accusatory, and clear—avoiding cold bureaucratic blame, scolding language, high-pressure sales tactics, or overly apologetic/unprofessional phrasing.
4. completeness_and_clarity: All principal reasons, counteroffer terms, or missing-document details and actionable next steps requested in the underwriting record are clearly communicated in well-structured plain English.

Reasoning Steps:
Step 1 (Fact Extraction & Faithfulness Audit): Compare every claim in the candidate letter against the underwriting record in the original prompt. Flag any omitted facts, altered numbers, invented credit bureaus/scores, or unsupported denial reasons.
Step 2 (Compliance & Fair-Lending Gate): Check for mandatory statutory notices requested by the prompt and scan rigorously for any direct or indirect leakage of protected-class attributes (e.g., age, widowed, retired, pension) or unauthorized promises of future credit approval. If ANY protected-class leakage, hallucinated denial reason, or omitted statutory notice occurs, mark regulatory_compliance as false and cap the overall score at 2 out of 5 regardless of writing polish.
Step 3 (Tone & Clarity Assessment): Evaluate whether a stressed retail banking customer would find the letter clear, respectful, and easy to act upon, without feeling blamed, pressured, or misled.
Step 4 (Holistic Scoring): Assign an integer score from 1 to 5:
  - 5: Production-ready exemplar. All 4 criteria met; zero errors; clear, warm, concise.
  - 4: Strong and compliant. All 4 criteria met with only minor stylistic or clarity improvements possible.
  - 3: Acceptable core compliance and facts, but noticeable weakness in tone, clarity, or completeness.
  - 2: Major failure. One or more critical factual errors, missing mandatory disclosures, or compliance issues.
  - 1: Severe compliance/safety failure (e.g., leaking protected-class info, major hallucination, or hostile tone).

Output Format:
Return ONLY valid JSON matching the exact schema below:
{
  "score": <integer 1-5>,
  "reasoning": "<concise step-by-step justification referencing specific details from the letter>",
  "criteria_met": {
    "factual_accuracy": <true or false>,
    "regulatory_compliance": <true or false>,
    "empathetic_professional_tone": <true or false>,
    "completeness_and_clarity": <true or false>
  }
}
```

---

### Bias Analysis

1. **Verbosity and Surface-Politeness Bias:** LLM judges consistently exhibit a well-documented preference for longer, more ornate responses and overly deferential apologies ("We are deeply, truly sorry for any inconvenience..."). In regulated banking communications, excessive length obscures mandatory statutory notices and diluted apologies can feel patronizing rather than genuinely respectful. Without explicit anchoring, the judge may reward wordy templates (`5/5`) over concise, plain-English letters (`4/5`) that customers actually read and understand.
2. **Self-Preference and Stylistic Homogeneity Bias:** Using `gpt-4o-mini` to evaluate responses generated by `gpt-4o-mini` introduces self-enhancement bias, where the judge favors phrasing patterns, bullet structures, and transition phrases characteristic of its own family of models. Conversely, a terse but completely accurate letter drafted in a plainer human banking house style might be penalized under `empathetic_professional_tone` simply because it diverges from the model's default RLHF conversational style.
3. **Cultural, Socioeconomic, and US-Jurisdictional Assumptions:** What constitutes an "empathetic, professional tone" varies across cultural and socioeconomic backgrounds—for example, whether directness is perceived as respectful clarity or coldness, or whether suggesting "financial wellness resources" feels supportive versus paternalistic. Additionally, the judge prompt encodes US-specific regulatory assumptions (ECOA/FCRA 60-day windows and three-bureau norms) and implicitly favors standard American corporate English idioms.

---

### Calibration Strategy

1. **Golden Calibration Anchor Set:** Before deploying the judge across larger evaluation batches, we will assemble a 20-letter golden reference set independently annotated and adjudicated by two Meridian Community Bank fair-lending compliance officers and one customer-experience lead. This calibration set will contain four verified exemplars per rubric tier (`1` through `5`), including deliberate near-miss traps (e.g., an empathetic letter that omits the 60-day dispute clause, or a letter that subtly hints at retirement income).
2. **Edge-Case Adjudication & Prompt Refinement:** We will run the judge (`temperature=0.0`) across the 20 golden examples and compute inter-rater agreement using quadratic-weighted Cohen's $\kappa$, targeting $\kappa \ge 0.80$ overall and $100\%$ recall on compliance failures (`score <= 2`). Any disagreement between the judge and compliance officers—such as borderline forward-looking phrasing on counteroffers or subtle protected-class proxies—will be converted into explicit negative/positive few-shot boundary examples inside the judge prompt.
3. **Addressing Judge Strictness or Leniency:** If the judge proves **too lenient** (e.g., passing subtle compliance drift), we tighten the deterministic regex pre-filter and add explicit "automatic fail" examples to Step 2 of the judge prompt. If the judge proves **too strict** (e.g., penalizing minor stylistic phrasing differences on valid letters as `3/5` instead of `4/5`), we clarify the boundary between `Score 4` ("compliant with minor stylistic preference") and `Score 3` ("noticeable customer-comprehension barrier") and enforce a production release threshold where human review is triggered whenever `score < 4` or any deterministic rule check fails.