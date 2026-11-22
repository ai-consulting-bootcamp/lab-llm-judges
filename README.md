# LLMs grading LLMs—with receipts

**Track:** Module 5 — Evaluation & strategy · **When:** Week 7, Day 4 · **Status:** Required

This repository contains a healthcare-focused evaluation of LLMs that summarize
patient records. It combines deterministic checks with an LLM-as-judge for
contradictions, uncertainty, source faithfulness, and safety.

## Files

- [`instructions.md`](./instructions.md) — the lab instructions
- [`rubric.md`](./rubric.md) — how your submission is graded; this is what the AI reviewer checks your PR against
- [`benchmark_audit.md`](./benchmark_audit.md) — audit of three existing healthcare benchmarks
- [`evaluation_design.md`](./evaluation_design.md) — five custom prompts and the LLM-as-judge design
- [`evaluation_memo.md`](./evaluation_memo.md) — client-facing evaluation memo
- [`reflection.md`](./reflection.md) — responses to the three reflection questions
- [`llm_judge_evaluation.py`](./llm_judge_evaluation.py) — modular evaluation runner for Steps 7–11
- [`llm_judge/`](./llm_judge/) — package modules for configuration, dataset/prompts, checks, provider calls, pipeline orchestration, and CLI
- [`evaluation_results.json`](./evaluation_results.json) — saved evaluation output and metrics
- [`implementation_summary.md`](./implementation_summary.md) — implementation overview and findings
- [`implementation_walkthrough.md`](./implementation_walkthrough.md) — detailed architecture and execution walkthrough

## Implementation structure

The implementation is organized as a small Python package:

- `llm_judge/models.py` — typed cases, results, judge responses, and token usage
- `llm_judge/config.py` — environment loading and OpenAI client creation
- `llm_judge/dataset.py` — Cases A–C and the five-case test dataset
- `llm_judge/prompts.py` — structured Step 4 judge prompt
- `llm_judge/checks.py` — deterministic validation checks for each task
- `llm_judge/client.py` — provider calls and judge JSON parsing
- `llm_judge/pipeline.py` — evaluation, metrics, analysis, and JSON persistence
- `llm_judge/cli.py` — command-line interface
- `llm_judge_evaluation.py` — compatibility entry point and public API facade

## Setup

Use Python 3.10 or newer and install the runtime dependencies:

```bash
pip install openai python-dotenv
```

Create a local `.env` file with your API key:

```env
OPENAI_API_KEY=your_key_here
```

The `.env` file is ignored by Git and must never be committed.

## Run the evaluation

List the five cases without making an API call:

```bash
python3 llm_judge_evaluation.py --list-cases
```

Run the target model and the structured judge:

```bash
python3 llm_judge_evaluation.py --run --output evaluation_results.json
```

The default target and judge model is `gpt-4o-mini` at temperature 0. Override
models when needed:

```bash
python3 llm_judge_evaluation.py --run \
  --model gpt-4o-mini \
  --judge-model gpt-4o-mini \
  --output evaluation_results.json
```

Cost is optional because provider pricing changes. Supply current rates in
dollars per million tokens to include cost estimates:

```bash
python3 llm_judge_evaluation.py --run \
  --input-cost-per-million INPUT_RATE \
  --output-cost-per-million OUTPUT_RATE
```

The JSON report contains each model response, rule checks, judge reasoning,
criteria, latency, token usage, cost estimates when supplied, aggregate metrics,
and Step 11 analysis.

## Use as a Python module

The dataset and pipeline can be imported without creating an API client:

```python
from llm_judge import build_cases, build_test_dataset
from llm_judge_evaluation import run_evaluation, save_results

cases = build_cases()
dataset = build_test_dataset()
```

API calls only occur when `run_evaluation()` is called with an initialized
client, or when the CLI is run with `--run`.

## How to complete this lab

1. **Fork** this repository.
2. Do the work described in `instructions.md`, committing to your fork.
3. Open a **pull request** back into this repository.
4. You'll receive **AI feedback** on your PR based on `rubric.md`. Address any blocking feedback and push updates to the same PR.

## Submission hygiene

- Keep this repository scoped to this lab only — no unrelated projects or personal files.
- Use clear, descriptive filenames.
- Remove secrets, API keys, and tokens before committing.
