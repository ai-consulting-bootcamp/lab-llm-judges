# CompanyScope — LLMs grading LLMs (with receipts)

**Ironhack AI Consulting & Integration | 21 November 2026 | Lab implementation**

This repository addresses the lab using **a fictional CompanyScope-style company-research use case**: an assistant drafts sourced corporate notes from registry extracts, annual accounts and news. It must avoid false entity matches, outdated facts, arithmetic mistakes, imagined ownership and malicious instructions hidden in retrieved documents. The five case records are invented for safe testing; they are **not** actual CompanyScope production queries.

## Start here

[`lab_proof.md`](lab_proof.md) provides one reproducible run, the input and output, observed errors, evidence, caveats, and a reviewer checklist. **Honesty note:** The committed `evaluation_results.json` is a true local *offline fixture-rule check*, not a run of OpenAI models. You need an API key and `--mode live` to satisfy the practical live LLM-as-judge execution requirement.

## File map

| File | Purpose |
| --- | --- |
| [`lab_proof.md`](lab_proof.md) | Reviewer entry point: exact command, input, evidence, final output, limitation. |
| [`benchmark_audit.md`](benchmark_audit.md) | Three complete public-benchmark audit cards with risks, format and verdict. |
| [`evaluation_design.md`](evaluation_design.md) | Five evaluation prompt cards, full judge rubric, bias analysis and calibration. |
| [`test_cases.json`](test_cases.json) | Full source/evidence packs, tasks, reference answers and simple validation rules. |
| [`fixture_responses.json`](fixture_responses.json) | Handcrafted good/bad candidate answers for smoke testing; not API responses. |
| [`llm_judge_evaluation.py`](llm_judge_evaluation.py) | Executable offline validation and live OpenAI generation + LLM judge. |
| [`evaluation_results.json`](evaluation_results.json) | Actual offline-run JSON: 3/5 fixture rule checks pass; API fields null. |
| `evaluation_results_live.json` and `live_run_summary.md` | **Created after your live run**; per-case judged scores, metrics, reasons, and a reviewer-readable run record. |
| [`evaluation_memo.md`](evaluation_memo.md) | Client memo with measured offline results and explicit limitations. |
| [`reflection.md`](reflection.md) | Responses about French data, "AGI-level" and the human's role. |
| [`implementation_summary.md`](implementation_summary.md) | Summary of architecture, result, and limitations. |
| [`tests/test_evaluation.py`](tests/test_evaluation.py) | Standard-library unit tests for checker and JSON judge validation. |
| [`requirements.txt`](requirements.txt), [`.env.example`](.env.example), [`.gitignore`](.gitignore) | Dependencies, private configuration example and secret protection. |

## Setup (Mac Terminal)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
# Edit .env locally to contain your real OPENAI_API_KEY; never commit it.
```

Run a zero-cost reproduction of the supplied fixture check:

```bash
python3 llm_judge_evaluation.py --mode offline
python3 -m unittest discover -s tests -v
```

Run **real model generation and independent LLM-as-judge calls** (uses paid API credits):

```bash
python3 llm_judge_evaluation.py --mode live --candidate-source generated
```

For quicker **judge-only calibration** on five known quality levels, without generating new responses:

```bash
python3 llm_judge_evaluation.py --mode live --candidate-source fixtures
```

The live script defaults to `gpt-4o-mini` for both roles. Outputs are `evaluation_results_live.json` plus `live_run_summary.md` (automatically generated, with real input/output/score/usage evidence). To choose models: `--target-model MODEL --judge-model MODEL`. Cost estimates use rates **$0.15 input / $0.60 output per million tokens** as verified on the OpenAI `gpt-4o-mini` model page on 2026-11-21; rates can change. For a different model or price, adjust `--input-price` and `--output-price` (one shared pair; if using differently priced target and judge models, the cost estimate will not be correct, so use identical models for the cost demo or amend pricing). API calls will cost money, even when estimates are tiny. No live results are committed until actually produced.

## Scope and use limits

The public benchmarks are **research context**, not claimed scores for this application. Our five fictional tests exercise a grading pipeline, not the full retrieval stack; they are not a valid accuracy confidence interval. Client deployment requires a larger private expert-annotated set, routine human review of material facts, reliable provenance and repeatability checks. An LLM judge complements but cannot replace independent verification of legal/compliance claims.

**References:** [FinanceBench](https://arxiv.org/abs/2311.11944), [RAGBench](https://arxiv.org/abs/2407.11005), [LegalBench](https://papers.neurips.cc/paper_files/paper/2023/hash/89e44582fd28ddfea1ea4dcb0ebbf4b0-Abstract-Datasets_and_Benchmarks.html), [OpenAI API](https://developers.openai.com/api/docs/guides/structured-outputs), [GPT-4o mini model pricing](https://developers.openai.com/api/docs/models/gpt-4o-mini).
