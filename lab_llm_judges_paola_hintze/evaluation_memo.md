# Evaluation Memo

**TO:** Executive Team, Northstar Social Impact Consulting  
**FROM:** Paola Hintze  
**DATE:** 24 August 2026  
**SUBJECT:** LLM Evaluation Results — Evidence-Grounded Consulting Recommendations

## Executive summary

We evaluated whether a small language model can convert social-impact briefs into useful recommendations without inventing evidence. Across five cases, the calibration run averaged **3.6/5**; three met the proposed threshold of 4, while one unsupported-outcome response triggered the critical-failure rule. The result supports a human-reviewed drafting pilot—not autonomous client delivery.

## Methodology

The design drew on TruthfulQA for adversarial plausibility, IFEval for instruction compliance, and RAGTruth for context faithfulness. Because these public benchmarks are imperfect proxies, the mini-benchmark used five client-like briefs covering missing outcomes, inconsistent arithmetic, causal confounding, unavailable demographic breakdowns, and implementation constraints.

Fixed candidate answers isolated judge behavior. The rubric assessed source faithfulness, instruction compliance, usefulness, and uncertainty/tone on a 1–5 anchored scale. A factual fabrication capped the score at 2. The committed result is a transparent calibration replay; live mode uses `gpt-4o-mini`, structured output, token accounting, elapsed time, and cost estimation.

## Results

Scores were **5, 2, 4, 3, and 4** (mean 3.6; median 4; range 2–5). Four responses avoided critical failure, and 15 of 20 criterion decisions were positive (75%). The weakest asserted a 70% placement rate although no employment outcomes existed; the judge correctly applied the cap.

The demographic case abstained correctly but omitted sample-size and privacy safeguards. The implementation plan respected the no-new-CRM constraint, but needed baselined success measures. Thus the rubric distinguished factual safety from writing quality.

## Caveats and limitations

Five synthetic cases cannot represent all domains, languages, sensitive attributes, or attacks. Public benchmark contamination and saturation limit generalization. LLM judges may share provider/style biases with candidates and vary across runs. The replay demonstrates pipeline logic but does not replace fresh API runs or blinded human comparison.

## Recommendation

**Under these conditions, for evidence-bounded first drafts, proceed with a controlled pilot with medium confidence.** Require human approval, block fabricated figures and unsupported subgroup/causal claims, and review any score below 4. Do not use the system for final funding, eligibility, or safeguarding decisions. Expand to at least 50 representative cases before production.

## Additional metrics

Replay incurred no API cost; live mode records tokens and latency. At the documented rates used in code ($0.15/M input; $0.60/M output), the five-case run should cost below one cent, but reporting must use API values. Measure review time and rework alongside cost; tokens alone cannot establish environmental impact without provider energy and carbon data.
