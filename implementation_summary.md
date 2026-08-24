# Implementation Summary

I implemented a small retail evaluation package that follows the lab structure end to end: benchmark audit, custom prompt design, judge prompt design, client memo, reflection, and a Python evaluation runner. The Python script is centered on a retail support rubric with four criteria: helpfulness, tone, policy adherence, and resolution quality.

The evaluator supports an OpenAI-backed judge when an API key is available and falls back to a deterministic offline scoring mode when it is not. That let me generate a reproducible `evaluation_results.json` in this environment while still keeping the live API path in place for a real run. I used a compact test set of five retail support examples so the pipeline stays inexpensive and easy to inspect.

The main output pattern is intentionally structured: each case records the prompt, sample response, judge reasoning, criterion flags, timing, and a lightweight cost field. This makes it straightforward to compare cases, review failure modes, and swap in a live model later without changing the reporting format.

