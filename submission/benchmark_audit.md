# Benchmark Audit

## Scenario
A Tier-1 automotive supplier's procurement team wants to use an LLM to generate
should-cost negotiation-prep summaries from RFQ and cost-breakdown data,
extending the should-cost benchmarking engine built in Project 3. Requirements:
numerically accurate cost figures, clear identification of cost drivers,
professional tone suitable for supplier negotiation prep. Key concerns:
hallucinated cost figures, missing critical cost drivers, and overconfident
recommendations that could weaken a buyer's negotiating position.

## Benchmark 1: FinQA
- **Year:** 2021
- **Source:** Chen et al., "FinQA: A Dataset of Numerical Reasoning over
  Financial Data" (arXiv:2109.00122)
- **Why it seemed relevant:** Numerical reasoning over financial data,
  structurally close to extracting numbers from a cost breakdown and
  reasoning over them correctly.
- **Contamination risk:** High -- a 2021 dataset almost certainly folded
  into pretraining corpora for any current-generation model.
- **Saturation risk:** Medium -- newer, harder benchmarks exist specifically
  because older ones like FinQA show ceiling performance from current models.
- **Format:** Free-form numerical answer with reasoning chain.
- **Verdict:** Reject as a scoring benchmark; borrow its query structure
  (extract -> compute -> answer) as a template for custom prompt design.

## Benchmark 2: FinanceBench
- **Year:** 2023
- **Source:** Islam et al., "FinanceBench: A New Benchmark for Financial
  Question Answering" (arXiv:2311.11944)
- **Why it seemed relevant:** Tests retrieval, interpretation, and reasoning
  over real financial filings, with a diagnostic focus on accuracy, evidence
  citation, and hallucination resistance -- the core risk in our scenario is
  the model inventing cost figures not grounded in the actual RFQ input.
- **Contamination risk:** Medium -- 2023 release, built on real filings not
  easily memorized verbatim.
- **Saturation risk:** Low-medium -- models still show meaningful hallucination
  and refusal-rate failures on this benchmark.
- **Format:** Free-form QA with evidence-grounding requirement.
- **Verdict:** Adapt -- useful supporting evidence on hallucination/grounding
  risk, but not a direct fit since it targets SEC-filing QA rather than
  negotiation-prep summarization.

## Benchmark 3: Vectara Hallucination Leaderboard (HHEM)
- **Year:** Ongoing, refreshed November 2025
- **Source:** Vectara HHEM leaderboard
- **Why it seemed relevant:** Directly measures how often a summary contains
  claims unsupported by its source document -- the exact failure mode this
  scenario cares about (a negotiation memo stating a cost figure not in the
  RFQ data).
- **Contamination risk:** Low -- the leaderboard was refreshed with a harder,
  longer-document dataset in November 2025 specifically to guard against
  gaming.
- **Saturation risk:** High for top-tier models, but real gaps remain for
  smaller/cheaper models (under ~7B parameters) -- directly relevant since
  our target deployment model is gpt-4o-mini, a cost-optimized tier.
- **Format:** Automated faithfulness scoring (source vs. summary).
- **Verdict:** Use as-is for directional calibration on the mini-tier model
  actually planned for deployment.
