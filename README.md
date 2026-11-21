# Meridian Community Bank — LLM Evaluation & LLM-as-Judge Lab

This submission evaluates whether an LLM can draft accurate, empathetic, and compliant adverse-action letters for consumer lending. The test suite covers auto-loan denials, internal-record denials, protected-class leakage, counteroffers, and incomplete applications.

## Deliverables

- [`benchmark_audit.md`](./benchmark_audit.md) — audit of IFEval, FinQA, and TruthfulQA.
- [`evaluation_design.md`](./evaluation_design.md) — five custom prompts, judge rubric, bias analysis, and calibration plan.
- [`evaluation_memo.md`](./evaluation_memo.md) — client-facing evaluation memo.
- [`reflection.md`](./reflection.md) — reflections on localization, AGI claims, and human review.
- [`llm_judge_evaluation.py`](./llm_judge_evaluation.py) — standalone OpenAI pipeline with offline mock mode.
- [`llm_judge_evaluation.ipynb`](./llm_judge_evaluation.ipynb) — notebook version with visualizations.
- [`evaluation_results.json`](./evaluation_results.json) — structured results from the checked-in offline simulation.
- [`implementation_summary.md`](./implementation_summary.md) — implementation and findings summary.
- [`requirements.txt`](./requirements.txt) — Python dependencies.

The lab instructions and grading rubric remain available in [`instructions.md`](./instructions.md) and [`rubric.md`](./rubric.md).

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

For live OpenAI evaluation, create a `.env` file containing `OPENAI_API_KEY=...`. Never commit that file.

## Run

Run deterministic offline verification without API usage:

```bash
python llm_judge_evaluation.py --mock --output evaluation_results.json
```

Run the live candidate-generation and judge pipeline:

```bash
python llm_judge_evaluation.py --output evaluation_results.json
```

The live run requires an API key and incurs API cost. The checked-in results are explicitly marked `mock_offline_simulation`; they demonstrate pipeline behavior and must not be interpreted as independent evidence of live model quality.

To use the notebook, launch `llm_judge_evaluation.ipynb` after installing the dependencies and selecting the project environment.
