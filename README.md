# Northline Home retail support evaluation

Northline Home is a fictional retailer testing an assistant that drafts replies about returns, product compatibility, missing parcels, and complaints. The evaluation combines exact checks of structured fields with a separate LLM judge for factual accuracy, completeness, policy safety, and customer experience.

| File | Purpose |
| --- | --- |
| `benchmark_audit.md` | Three public benchmark assessments and their relevance to Northline |
| `evaluation_design.md` | Five prompt cards, judge rubric, bias analysis, and calibration strategy |
| `test_cases.json`, `judge_prompt.txt` | The executable cases and judge rubric |
| `llm_judge_evaluation.py`, `requirements.txt` | Evaluation entry point and pinned dependencies |
| `evaluation_results.json` | Run export with replies, judge evidence, usage, timing, and aggregate metrics |
| `evaluation_memo.md` | One-page client memo generated from the run |
| `implementation_summary.md` | Implementation overview, findings, and per-case breakdown generated from the run |
| `reflection.md` | Reflections on French evaluation, general capability, and human review |

## Reproduction

The entry point uses Python 3.10 or later and the OpenAI Responses API. The API key comes from the environment or the repository-root `.env`. A full run makes five generation calls, five grading calls, and two calibration calls. The JSON export and Markdown reports are written after all cases complete.

From the folder containing the evaluation script:

```text
python -m pip install -r requirements.txt
python llm_judge_evaluation.py
```

Price estimates use the published standard per-token rates for [GPT-4o mini](https://developers.openai.com/api/docs/models/gpt-4o-mini) and [GPT-5.4 mini](https://developers.openai.com/api/docs/models/gpt-5.4-mini).

## Submission package

The completed deliverables and their reproduction inputs are collected in [`lab_llm_judges_sergii_rostovskyi/`](./lab_llm_judges_sergii_rostovskyi/). The package README describes its contents and run command.
