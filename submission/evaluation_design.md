# Evaluation Design

## 5 Custom Evaluation Prompts

### Prompt 1: Basic Cost Driver Summary (baseline accuracy case)
- **Prompt:** Given this should-cost breakdown for a stamped bracket
  [material: $2.10/unit, labor: $1.85/unit, overhead: $0.95/unit,
  freight: $0.40/unit, total should-cost: $5.30/unit vs. supplier quote:
  $6.75/unit], write a 3-sentence negotiation-prep summary identifying the
  top cost driver and the gap to target.
- **Ground truth:** Yes -- material is the largest line item ($2.10); gap is
  $1.45/unit (27% over should-cost).
- **Verification:** Rule-based -- check correct driver and gap within
  rounding tolerance.
- **Primary failure mode:** Hallucination (inventing a driver or figure not
  in the input).
- **Why it matters:** Floor test -- arithmetic and driver-ranking accuracy
  on clean data.

### Prompt 2: Missing Data Edge Case
- **Prompt:** Given this should-cost breakdown where freight cost is
  missing/unknown [material: $2.10, labor: $1.85, overhead: $0.95,
  freight: N/A, supplier quote: $6.75], write a negotiation-prep summary.
- **Ground truth:** No single answer, but correct *behavior* exists: flag
  the missing data, avoid computing a false total.
- **Verification:** LLM-as-judge.
- **Primary failure mode:** Silent gap-filling / fabricated totals -- the
  single most dangerous failure mode for this use case.
- **Why it matters:** Real RFQ data is rarely fully clean; a fabricated
  total is indistinguishable from a real one to the buyer.

### Prompt 3: Cost Driver Ranking Under Ambiguity
- **Prompt:** Given a should-cost breakdown with two closely-priced
  components [tooling amortization: $1.42/unit, material: $1.38/unit,
  labor: $1.10/unit], identify and justify the primary cost driver for
  negotiation focus.
- **Ground truth:** Yes -- tooling amortization is marginally higher, but a
  good answer notes the closeness rather than overstating certainty.
- **Verification:** LLM-as-judge (correctness + calibrated hedging).
- **Primary failure mode:** Overconfidence on a razor-thin margin.
- **Why it matters:** Tests confidence calibration, not just correctness.

### Prompt 4: Tone and Professional Framing
- **Prompt:** Rewrite this raw analyst note into negotiation-ready language:
  "Supplier is charging way too much for labor, basically robbing us, need
  to hammer them on this."
- **Ground truth:** No single answer -- subjective quality.
- **Verification:** LLM-as-judge (tone, retained factual claim).
- **Primary failure mode:** Under- or over-correcting tone.
- **Why it matters:** Distinct skill from numerical accuracy; shows up
  constantly in real deliverables.

### Prompt 5: Multi-Currency Freight Complexity (stress test)
- **Prompt:** Given a should-cost calc where material is priced in EUR
  (EUR 1.85, converted at 1.08 USD/EUR), labor in USD ($1.90), and freight
  quoted in a mixed incoterm (FOB Shanghai, buyer pays freight separately at
  $0.55/unit), write a summary of total landed cost per unit in USD and flag
  any assumptions made.
- **Ground truth:** Yes -- total is approximately $4.45/unit; a correct
  answer flags the FOB/freight-responsibility assumption.
- **Verification:** Rule-based (arithmetic tolerance) + LLM-as-judge
  (assumption-flagging).
- **Primary failure mode:** Silent currency/unit conversion errors, or
  failing to surface the incoterm assumption.
- **Why it matters:** The most realistic hard case; mirrors the currency and
  freight modules built in the Project 3 should-cost engine.

## LLM-as-Judge Prompt (final, generalized version)

The judge was initially designed narrowly around Prompt 2 (assuming freight
was always the missing field), then generalized after testing revealed it
was misapplying missing-data criteria to prompts with complete data. See
`llm_judge_evaluation.py` for the final `JUDGE_SYSTEM_PROMPT` implementation,
which:

1. First determines from the *original prompt* which fields were actually
   provided vs. missing/ambiguous (rather than assuming a fixed scenario).
2. Applies Gap Acknowledgment, No Fabricated Totals, and Actionable Despite
   Gap criteria conditionally based on that determination.
3. Returns structured JSON: score (0-1), reasoning, and per-criterion
   true/false.

## Bias Analysis

The most significant predicted (and later confirmed) bias is a
**verbosity/hedging bias**: the judge tends to reward responses that hedge
explicitly and visibly, because "I notice X is missing" is an easy pattern
to detect, while penalizing responses that are correct but unhedged. This
was borne out directly in testing: Prompt 5's response was arithmetically
correct and used all provided data correctly, yet was scored 0.5 because it
didn't explicitly narrate the EUR-to-USD conversion mechanics -- an
expectation never stated in the judge's own rubric. This matters for a
negotiation-memo use case specifically, since terse, confident, correct
writing is often *more* professional, not less.

A secondary risk is **domain-fluency bias**: the judge is itself a
general-purpose LLM with no grounding in should-cost materiality thresholds
(e.g., freight is often a small percentage of landed cost on some commodity
types, larger on others), so it may over- or under-penalize a gap depending
on a component's real-world significance, which it has no way to assess.

## Calibration Strategy

Calibration would use 2-3 few-shot reference examples embedded directly in
the judge prompt: one clear pass, one clear failure (silent fabrication),
and one deliberately implicit-but-correct case (handles the gap correctly
without an explicit "flag" sentence) -- directly targeting the verbosity
bias observed above. For edge cases, the judge would be run multiple times
at temperature 0 (or with prompt-phrasing variants); persistent disagreement
across runs would be treated as a signal that the underlying response is
genuinely ambiguous and warrants human review rather than a forced score.
If the judge trends too strict, criterion 2 (No Fabricated Totals) would be
loosened to accept clearly-labeled estimates rather than requiring literal
refusal to state any number.
