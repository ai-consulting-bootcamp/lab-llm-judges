# Northline Home Retail Support Evaluation

Northline Home is a fictional online retailer evaluating an assistant that drafts customer support replies about returns, product compatibility, missing parcels, and complaints. This submission combines deterministic checks for structured outcomes, refund amounts, and reply length with an independent LLM judge for accuracy, completeness, policy safety, and customer experience.

## Files

- `benchmark_audit.md` ? critique of three public benchmarks and their fit for this use case.
- `evaluation_design.md` ? five custom cases, ground truth, verification methods, judge rubric, bias analysis, and calibration plan.
- `llm_judge_evaluation.py`, `test_cases.json`, `judge_prompt.txt` ? executable evaluation and its inputs.
- `evaluation_results.json` ? saved API run with case-level replies, checks, judge evidence, usage, timing, and aggregate metrics.
- `evaluation_memo.md` ? client-facing interpretation of the measured results and limitations.
- `implementation_summary.md` ? implementation details, findings, and case breakdown.
- `reflection.md` ? responses to the three reflection questions.
- `requirements.txt` ? Python dependencies.

## Run

Use Python 3.10 or later. Install dependencies with `python -m pip install -r requirements.txt`. Set `OPENAI_API_KEY` in the environment or create a local `.env` file containing that variable; the secret file is excluded from this submission. From this folder, run:

```text
python .\llm_judge_evaluation.py --env-file .\.env
```

The evaluation uses `gpt-4o-mini` for candidate replies and `gpt-5.4-mini` for judging. It writes `evaluation_results.json`, `evaluation_memo.md`, and `implementation_summary.md` in this folder.
