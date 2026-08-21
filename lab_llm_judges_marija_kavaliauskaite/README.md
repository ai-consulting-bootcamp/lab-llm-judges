# LLMs Grading LLMs — MIRA Evaluation

## Scenario

MIRA is an AI Creative Director that turns user-provided brand context, visual preferences, creative answers, and reference material into a coherent editorial campaign direction. This proof-of-concept evaluation checks instruction following, preference fidelity, campaign consistency, specificity, context preservation, and resistance to unsupported assumptions.

## Repository structure

- `benchmark_audit.md` — audit of IFEval, MT-Bench, and MMLU-Pro.
- `evaluation_design.md` — five MIRA prompts, judge rubric, bias analysis, calibration, and statistical limitations.
- `llm_judge_evaluation.py` — runnable five-case generation and judging harness.
- `evaluation_results.json` — real per-case and aggregate results from the completed evaluation.
- `evaluation_memo.md` — client memo reporting the completed evaluation and its limitations.
- `reflection.md` — responses on French data, AGI claims, and human creative review.
- `implementation_summary.md` — implementation and current execution status.
- `requirements.txt` — Python dependencies.
- `.env.example` — placeholder for the required environment variable; contains no secret.
- `.gitignore` — excludes local secrets, virtual environments, and Python cache files.

## Evaluation approach

The lab adapts ideas from three public benchmarks into five custom MIRA cases. The script first generates one response per case with `gpt-4o-mini`, then uses a structured LLM judge to score it from 1–5 against five criteria. The completed run evaluated all **5 cases with 0 failures**, achieved an average score of **4.2/5**, took **48.051 seconds**, and used **8,421 total tokens**. Exact cost remains unavailable because pricing was intentionally not hardcoded. Rule-based checks and human review are recommended alongside the automated judge.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:

```text
OPENAI_API_KEY=your_api_key_here
```

Run:

```bash
python3 llm_judge_evaluation.py
```

## Outputs

The executed `evaluation_results.json` contains per-case prompts, generated responses, scores, reasoning, criterion flags, elapsed time, token usage, errors, and aggregate statistics. The harness records a failed case without crashing the remaining evaluation, although this run completed with no failures.

## Limitations

Five cases are severely underpowered and cannot establish statistical significance, broad production quality, or the best model. LLM judges can show position, length, self-preference, language, and style bias. Reliable decisions require a larger representative dataset, repeated runs, calibrated human labels, model/version metadata, and human creative review.
