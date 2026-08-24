# LLMs grading LLMs—with receipts

**Track:** Module 5 — Evaluation & strategy · **When:** Week 7, Day 4 · **Status:** Required

This repository contains everything you need for this lab.

## Scenario

A retailer wants an AI customer service chatbot that handles returns, product questions, and complaints. The chatbot must be helpful, use the right tone, and resolve issues correctly. The main risks are giving wrong return or refund policy information, sounding rude or dismissive, and failing to escalate cases it cannot handle on its own.

## Files

- [`instructions.md`](./instructions.md) — the lab instructions
- [`rubric.md`](./rubric.md) — how your submission is graded; this is what the AI reviewer checks your PR against
- `benchmark_audit.md`: 3 existing benchmarks evaluated for fit with this scenario
- `evaluation_design.md`: 5 custom evaluation prompts, plus one full LLM-as-judge prompt with bias and calibration analysis
- `evaluation_memo.md`: 1-page memo to the client with results and recommendation
- `reflection.md`: answers to the 3 reflection questions
- `llm_judge_evaluation.ipynb`: Jupyter notebook implementation of the judge, run on a small test set
- `evaluation_results.json`: output of running the judge (scores, reasoning, time, tokens, cost)
- `implementation_summary.md`: short summary of what the code does and what it found

## How to run the code

1. Create a `.env` file in this folder with `OPENAI_API_KEY=your_key_here`.
2. Install dependencies: `pip install openai python-dotenv`.
3. Open `llm_judge_evaluation.ipynb` and run all cells in order.
4. Results are saved to `evaluation_results.json`, and a summary is printed at the end of the notebook.

## How to complete this lab

1. **Fork** this repository.
2. Do the work described in `instructions.md`, committing to your fork.
3. Open a **pull request** back into this repository.
4. You'll receive **AI feedback** on your PR based on `rubric.md`. Address any blocking feedback and push updates to the same PR.

## Submission hygiene

- Keep this repository scoped to this lab only — no unrelated projects or personal files.
- Use clear, descriptive filenames.
- Remove secrets, API keys, and tokens before committing.
