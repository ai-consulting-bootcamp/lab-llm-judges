# Implementation Summary

The Python implementation is an offline-capable LLM-as-judge pipeline for the retail customer-service scenario. It contains five test cases, representative assistant responses, a structured judge rubric, deterministic checks for policy and tool-call conditions, timing, token estimates, and JSON output. Running the script without arguments produces a reproducible demonstration result; running with `--live` uses the OpenAI API if `OPENAI_API_KEY` is available.

The demonstration run produced an average score of 4.6/5.0 across five cases. This is not a claim about a deployed model: the responses are illustrative, the dataset is intentionally small, and the offline judge is a transparent fallback. The next consultant step would be to replace the sample responses with real candidate-model outputs, expand the private test set, and calibrate the judge against human labels.

## Run

```bash
python llm_judge_evaluation.py
python llm_judge_evaluation.py --live --model gpt-4o-mini
```

The live command requires the `openai` package and an `OPENAI_API_KEY` environment variable. Do not commit the API key or a `.env` file.
