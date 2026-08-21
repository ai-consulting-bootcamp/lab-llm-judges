# Troubleshooting Notes

How this implementation addresses each issue raised in the lab's Tips &
Troubleshooting section.

## JSON parsing errors in judge responses
- The judge call uses `response_format={"type": "json_object"}` to force
  valid JSON output (`llm_judge_evaluation.py`, `judge_response()`).
- The parse is wrapped in `try/except json.JSONDecodeError`; on failure the
  raw text is preserved inside the result (`reasoning` field) instead of
  crashing the run, so one bad response doesn't lose the rest of the batch.

## Inconsistent judge scores
- The judge is called at `temperature=0` specifically to minimize run-to-run
  variance (the assistant-generation call keeps `temperature=0.7`, since some
  natural variation there is expected and realistic).
- Known limitation: this run used a single pass per case, not repeated runs.
  For a production decision, each case should be run 3+ times and averaged —
  noted as a follow-up in `evaluation_memo.md`.

## High API costs
- `gpt-4o-mini` is used for both generation and judging.
- The pipeline tracks and reports token usage and estimated cost per call and
  in aggregate (`estimate_cost()`), so cost is visible rather than assumed.
- The test set is intentionally small (5 cases) during development, per the
  lab's own guidance; the real run cost ~$0.001 total for all 5 cases.

## Judge is too strict/lenient
- The judge prompt includes explicit score anchors (5 = fully meets all
  criteria; 3 = partial/uneven; 1 = fails most criteria) rather than a bare
  1-5 scale with no reference points.
- Calibration strategy (reference examples, handling ambiguous middle cases)
  is documented in `evaluation_design.md` under Bias Analysis.
- Concrete finding from the real run: the judge's binary criteria were marked
  "true" on two cases it still scored 4/5, meaning the checklist alone
  under-differentiates response quality relative to the judge's own written
  reasoning. Fix direction: tighten the `coaching_stance` criterion to
  distinguish a question that merely invites reflection from one that also
  moves the conversation toward a concrete next step.
