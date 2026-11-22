# LLMs grading LLMs—with receipts

**Track:** Module 5 — Evaluation & strategy · **When:** Week 7, Day 4 · **Status:** Required

This repository contains everything you need for this lab.

## Files

- [`instructions.md`](./instructions.md) — the lab instructions
- [`rubric.md`](./rubric.md) — how your submission is graded; this is what the AI reviewer checks your PR against

## How to complete this lab

1. **Fork** this repository.
2. Do the work described in `instructions.md`, committing to your fork.
3. Open a **pull request** back into this repository.
4. You'll receive **AI feedback** on your PR based on `rubric.md`. Address any blocking feedback and push updates to the same PR.

## Submission hygiene

- Keep this repository scoped to this lab only — no unrelated projects or personal files.
- Use clear, descriptive filenames.
- Remove secrets, API keys, and tokens before committing.


## Completed Lab — MNM AG LLM Evaluation

### Project Overview
This lab implements an LLM-as-a-Judge evaluation system using Python and OpenAI's `gpt-4o-mini`.

The fictional client, MNM AG, uses a Dynamics 365 Finance & Operations assistant to answer vendor-management questions across its German and Dutch legal entities.

### Implementation
- Evaluated three benchmarks: EKRAG, IFBench and GroUSE.
- Designed five evaluation test cases.
- Implemented an LLM judge with a 1–5 scoring rubric.
- Evaluated accuracy, policy compliance, safety and groundedness.
- Recorded evaluation scores, reasoning and execution times.

### Evaluation Results

| Test Case | Scenario | Score |
|---|---|---|
| TC01 | New vendor creation | 4/5 |
| TC02 | Cross-company vendor use | 1/5 |
| TC03 | NET30 payment terms | 5/5 |
| TC04 | Bank-detail change | 4/5 |
| TC05 | Unknown vendor information | 1/5 |

Average score: **3.0/5**

### How to Run

1. Install the dependencies:

   `pip install openai python-dotenv`

2. Create a `.env` file containing your own `OPENAI_API_KEY`.

3. Run:

   `python llm_judge_evaluation.py`

4. Review the generated `evaluation_results.json`.

### Deliverables
- `benchmark_audit.md` — Benchmark selection and analysis
- `evaluation_design.md` — Evaluation cards and judge design
- `evaluation_memo.md` — Client-facing evaluation memo
- `reflection.md` — Lab reflections
- `llm_judge_evaluation.py` — Python implementation
- `evaluation_results.json` — Actual evaluation results
- `implementation_summary.md` — Implementation findings and limitations

### Limitations
The evaluation uses five fictional test cases and one LLM judge. Results are preliminary and require human review before production use.

The `.env` file is excluded from Git to protect API credentials.
