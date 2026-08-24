# Implementation Summary

The Python pipeline evaluates five fixed candidate responses against an anchored consulting rubric. In live mode it sends the original prompt, reference facts, constraints, and candidate answer to OpenAI's Responses API using `gpt-4o-mini` and a strict JSON Schema. Each result records criterion scores, pass/fail decisions, critical failures, unsupported claims, reasoning, elapsed time, API-reported token usage, and estimated cost. The script validates every returned record, applies a defensive local cap when critical failure is true, calculates aggregate statistics, and writes the complete run configuration and pricing assumptions to JSON. Fixed candidates make judge behavior the experimental variable and allow direct reruns.

The committed `evaluation_results.json` is a **calibration replay**, not a claimed paid API call. This distinction is included in both the file and README because no API credential is stored in the repository. The replay contains five previously reviewed structured judgments and runs through the same validation and aggregation code, producing scores of 5, 2, 4, 3, and 4 (mean 3.6; median 4), with one critical unsupported-outcome failure and 15/20 criteria met. Replay token and cost fields are `null`/zero because the API did not report usage for that run; live mode captures those values directly.

The main finding is that average quality alone is unsafe: one polished answer fabricated a placement rate and therefore failed even though other cases were usable. A production gate should combine the judge with deterministic checks, require review below score 4, and treat any fabricated metric, demographic claim, or causal overstatement as a blocker. Before deployment, I would add at least 50 representative cases, run repeated judgments, and compare the judge against two independent human reviewers with special attention to false negatives on critical failures.

## Reproduction

```bash
python llm_judge_evaluation.py --mode replay --output evaluation_results.json
```

For a live run, install dependencies, place `OPENAI_API_KEY` in an uncommitted `.env`, and run:

```bash
python llm_judge_evaluation.py --mode live --output evaluation_results_live.json
```

The implementation uses Structured Outputs because schema adherence is stronger than basic JSON mode. Pricing constants are explicit configuration values and should be checked against the current official pricing page before any client cost projection.
