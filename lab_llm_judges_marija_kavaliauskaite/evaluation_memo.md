# Evaluation memo

**TO:** MIRA Product Team
**FROM:** Marija Kavaliauskaite
**DATE:** 2026-08-21
**SUBJECT:** LLM Evaluation Results — MIRA AI Creative Director

## Executive Summary

The completed proof-of-concept evaluation measured whether MIRA follows direct creative instructions, preserves supplied preferences, avoids unsupported assumptions, and produces a specific, coherent campaign direction. All 5 cases completed with 0 failures, producing an average score of **4.2/5**. The strongest areas were user-input precedence and five-frame campaign consistency at **5/5** each. Hallucination resistance was the weakest case at **3/5**, while explicit visual preference adherence and specificity/usefulness each scored **4/5**.

## Methodology

The custom MIRA benchmark contains five prompts covering explicit visual preference adherence, user-input precedence, five-frame campaign consistency, hallucination resistance, and practical specificity. The evaluated model and judge default to `gpt-4o-mini`. Each generated answer is scored from 1–5 against instruction adherence, preference fidelity, campaign consistency, specificity, and absence of unsupported assumptions. The judge must return structured JSON with concise reasoning and a Boolean flag for every criterion.

Rules can also check expected frame count, named sections, required palette terms, and explicit exclusions. Because they cannot decide whether a campaign genuinely feels coherent or distinctive, human review remains part of calibration and final quality review.

## Results

The executed evaluation achieved an average score of **4.2/5**, with a minimum of **3/5** and a maximum of **5/5**. User-input precedence and five-frame campaign consistency were the strongest cases at **5/5**, showing that the model honored an explicit choice over conflicting background context and maintained a coherent direction across a multi-frame campaign. Explicit visual preference adherence and specificity/usefulness both scored **4/5**. Hallucination resistance was weakest at **3/5** because the answer introduced unconfirmed tone and visual choices despite being asked to keep unknown details explicit.

All **5 of 5 cases completed with 0 failures**. Total runtime was **48.051 seconds** (9.61 seconds per case on average). Generation and judging used **8,421 total tokens**: 5,167 input tokens and 3,254 output tokens. Exact cost is unavailable because pricing was intentionally not hardcoded.

## Caveats & Limitations

N=5 is a severely underpowered proof of concept. No statistical significance is claimed, and the results cannot support strong model comparison or production conclusions. Scores may vary across generations, while an LLM judge may favour verbosity, polished English, familiar model-family style, or its own creative assumptions. The benchmark covers selected MIRA risks, not every user, language, content type, or failure mode. Reproducibility also depends on API model versions and provider behaviour.

## Recommendation

Under these conditions, the completed run demonstrates that the harness is suitable for diagnostic evaluation, not a production selection decision. Before comparing models or prompts, calibrate the judge against weak, medium, and strong MIRA examples reviewed by humans, add targeted hallucination-resistance cases, and expand the dataset.

## Additional Metrics

The harness records latency and tokens for both generation and judging. Exact cost is unavailable because pricing was intentionally not hardcoded. Unnecessary repeated model calls also imply avoidable compute demand, but tokens, latency, and cost are operational proxies rather than direct environmental measurements.
