# LLMs grading LLMs—with receipts — Paola Hintze

This submission evaluates an LLM used by a fictional social-impact consultancy to draft evidence-grounded recommendations from a supplied client brief. The assistant must preserve the source facts, distinguish evidence from recommendations, follow the requested format, use an appropriate consulting tone, and abstain when the brief does not support a claim.

The evaluation combines three benchmark audits, five production-like prompt cards, a calibrated LLM-as-judge rubric, deterministic safety checks, and a reproducible Python pipeline. Candidate answers are fixed fixtures so that model judging—not answer generation—is the variable under test.

## Submission map

All student deliverables are in [`lab_llm_judges_paola_hintze/`](./lab_llm_judges_paola_hintze/):

- [`benchmark_audit.md`](./lab_llm_judges_paola_hintze/benchmark_audit.md) — three benchmark evaluation cards.
- [`evaluation_design.md`](./lab_llm_judges_paola_hintze/evaluation_design.md) — five prompt cards, full judge prompt, bias analysis, and calibration plan.
- [`evaluation_memo.md`](./lab_llm_judges_paola_hintze/evaluation_memo.md) — client-facing evaluation memo.
- [`reflection.md`](./lab_llm_judges_paola_hintze/reflection.md) — responses to the three reflection questions.
- [`llm_judge_evaluation.py`](./lab_llm_judges_paola_hintze/llm_judge_evaluation.py) — OpenAI Responses API evaluation pipeline with structured output, replay mode, metrics, and validation.
- [`evaluation_results.json`](./lab_llm_judges_paola_hintze/evaluation_results.json) — reproducible calibration-replay results for five cases.
- [`implementation_summary.md`](./lab_llm_judges_paola_hintze/implementation_summary.md) — implementation choices, results, and limitations.
- [`requirements.txt`](./lab_llm_judges_paola_hintze/requirements.txt) — Python dependency.

The original [`instructions.md`](./instructions.md) and [`rubric.md`](./rubric.md) remain at repository root for traceability.

## Run the evaluation

```bash
cd lab_llm_judges_paola_hintze
python -m venv .venv
source .venv/bin/activate  # Windows Git Bash: source .venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env
# Add your OPENAI_API_KEY to .env; never commit it.
python llm_judge_evaluation.py --mode live --output evaluation_results_live.json
```

To reproduce the committed calibration result without an API key:

```bash
python llm_judge_evaluation.py --mode replay --output evaluation_results.json
```

Replay mode is explicitly labelled and does not claim API token usage or paid cost. Live mode uses `gpt-4o-mini`, captures API-reported token usage, measures wall-clock time, estimates cost from documented rates, and writes an auditable JSON record.
