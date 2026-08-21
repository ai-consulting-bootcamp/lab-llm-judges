TO: Management Board & Compliance Officer, German Consumer Lending Operations
FROM: Lead AI Systems & Regulatory Evaluation Consultant
DATE: August 21, 2026
SUBJECT: LLM Evaluation Results — Automated Credit Rejection Notice (Kreditabsage) Generator

## EXECUTIVE SUMMARY
We evaluated a candidate LLM's ability to draft consumer-facing credit rejection notices (Kreditabsagen) against five compliance-critical scenarios: SCHUFA/budget data mapping, Art. 22(3) GDPR disclosure, AGG non-discrimination, formal-register tone, and prompt injection resistance. No existing public benchmark verifies German consumer-lending disclosure compliance directly, so we built a custom evaluation (see benchmark_audit.md). On the five scenarios tested, the model produced no observed compliance violations, though this sample is too small to support a general compliance guarantee.

## METHODOLOGY
We built five custom scenario prompts covering the primary failure modes from scoping: factual hallucination, missing statutory disclosures, discriminatory reasoning, tone/register violations, and prompt-injection overrides (full prompts in `evaluation_design.md`). Each scenario was scored by a rule-based check plus a structured LLM-as-judge evaluator run at temperature 0, requiring extraction of causal rejection language before scoring, with a hard cap of 1/5 if any demographic attribute was used causally.

We tested one candidate model (`gpt-4o-mini`) as both generator and, in a separate call, judge. This is a single-model pilot; a model-vs-model comparison was out of scope this phase.

## RESULTS
On rule-based checks, 5/5 scenarios matched expected content (correct figures, required GDPR disclosure phrases, absence of the injected approval language). On LLM-judged criteria, the model passed all AGG non-discrimination and formal-register checks; the one recurring deduction was stylistic — output leaned toward rigid legal phrasing over warmer customer-relationship language. We report compliance-critical checks (AGG, GDPR, injection resistance) as pass/fail rather than an averaged score, since a failure there should not be offset by strong performance elsewhere.

## CAVEATS & LIMITATIONS
These results come from one example per scenario, evaluated once, by a judge that is the same model that generated the letters — a self-judging setup that may share the generator's blind spots. Our custom prompts avoid the contamination and saturation risks identified in public benchmarks like FinQA and IFEval (see benchmark_audit.md), but introduce a new limitation: we have not tested reproducibility across paraphrased inputs or repeated runs, so results may not generalize beyond the exact wording tested. The judge's connector-based discrimination rule may also miss coded or connotative allusions to protected attributes that a human reviewer would catch.

## RECOMMENDATION
Under these specific test conditions, for this narrow scenario set, results are consistent with compliant behavior — we do not yet have grounds for a high-confidence compliance claim at deployment scale. We recommend a staged pilot with an expanded, human-labeled test set and mandatory human-in-the-loop review for all rejection notices until that larger evaluation is complete.

## ADDITIONAL METRICS
Precise latency, token, and cost figures require running the Part 2 implementation and will be reported once that pipeline runs. Based on published gpt-4o-mini pricing, we project roughly $0.0001-0.0002 per notice with sub-2-second latency — negligible at expected volume, and low enough that environmental/compute cost is not a limiting factor versus the human-review overhead needed until compliance behavior is validated at scale.