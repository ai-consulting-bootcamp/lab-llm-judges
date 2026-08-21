# Implementation Summary

Built a working LLM-as-judge evaluation pipeline in `llm_judge_evaluation.py`
using the OpenAI API directly (gpt-4o-mini for both generation and judging).
The pipeline generates a model response for each of 5 custom should-cost
negotiation-prep prompts, scores each response against a structured judge
prompt (task description, evaluation criteria, reasoning steps, JSON output
format), and writes individual and aggregate results to
`evaluation_results.json`.

The most significant finding came from a design flaw caught mid-implementation:
the first version of the judge prompt was written narrowly around a single
scenario (missing freight data) and, when reused across all 5 test cases, it
incorrectly penalized responses where no data was actually missing --
producing a misleadingly low initial average score (0.7, with a 0.3 minimum)
that reflected judge misapplication rather than model failure. The judge was
generalized to first determine which fields were actually present or missing
from the original prompt before applying its criteria, rather than assuming
a fixed scenario. Re-running after the fix raised the average to 0.8 and
correctly discriminated between a genuine model failure (Prompt 2, where the
model silently derived a freight figure from data marked missing) and a
judge-side false negative (Prompt 5, where the model's arithmetic was fully
correct but the judge penalized it for not narrating its currency-conversion
steps) -- exactly the verbosity/hedging bias predicted in the Step 4 bias
analysis, now confirmed empirically rather than just theorized.

One limitation worth flagging: response generation runs at temperature 0.7
to simulate realistic production variance, which means re-running the suite
regenerates different responses each time. This conflates "did the judge
change" with "did the generated response change" across runs, and a cleaner
follow-up would fix a set of generated responses once and re-run only the
judge against them when iterating on judge design.
