# LLMs grading LLMs—with receipts

**Track:** Module 5 — Evaluation & strategy · **When:** Week 7, Day 4 · **Status:** Required

This repository contains the completed submission for the lab described in
[`instructions.md`](./instructions.md), graded against [`rubric.md`](./rubric.md).

## Scenario

**Option C — Retail:** A retailer wants an LLM-based customer service chatbot that
handles returns, product questions, and complaints. The key concerns are helpfulness,
tone, and resolution rate — especially for frustrated customers reporting repeated
delivery/damage failures. The full evaluation focuses on one high-stakes case: a
customer whose order has arrived late three times and damaged this time, who is
considering never shopping there again. The chatbot must de-escalate, acknowledge the
pattern of failures (not just today's issue), and offer a concrete, policy-consistent
resolution (full refund or replacement, no time limit beyond 90 days for damaged items).

## Approach

1. **Audited 3 existing benchmarks** (MultiWOZ, ABCD, EchoMind) against the scenario
   and rejected all three — none score tone/empathy, and two are structurally
   dialogue-state-tracking or policy-action benchmarks rather than quality judges.
   This motivated building a custom evaluation instead of reusing an off-the-shelf one.
2. **Designed 5 custom evaluation prompts** covering a basic policy lookup, a
   conditional edge case, an ambiguous multi-intent request, an adversarial
   policy-bending attempt, and a tone-sensitive complaint — mixing rule-based and
   LLM-as-judge verification depending on whether the prompt has a single correct
   answer.
3. **Built a complete LLM-as-judge prompt** for the tone-sensitive complaint case
   (task description, 3 evaluation criteria, reasoning steps, structured JSON output),
   with a written bias analysis and calibration strategy.
4. **Implemented and ran the judge in Python** (`gpt-4o-mini` via the OpenAI API) against
   4 hand-crafted response variants, collecting score, reasoning, criteria pass/fail,
   time, and cost per case.
5. **Wrote a client-facing evaluation memo and reflection** covering results, caveats,
   a hedged recommendation, and three open evaluation-design questions (non-English
   data, "is this AGI-level?", what needs a human).

## Files

| File | What it is |
|---|---|
| [`README.md`](./README.md) | This file — scenario, approach, and file map. |
| [`instructions.md`](./instructions.md) | The lab instructions (progress checkboxes marked as completed below). |
| [`rubric.md`](./rubric.md) | Grading rubric the AI reviewer checks this PR against. |
| [`benchmark_audit.md`](./benchmark_audit.md) | Step 2 — 3 benchmark evaluation cards (MultiWOZ, ABCD, EchoMind) with contamination/saturation/verdict. |
| [`evaluation_design.md`](./evaluation_design.md) | Steps 3–4 — 5 custom evaluation prompt cards + the full LLM-as-judge prompt, bias analysis, and calibration strategy. |
| [`evaluation_memo.md`](./evaluation_memo.md) | Step 5 — 1-page client memo: methodology, results, caveats, hedged recommendation, cost/time metrics. |
| [`reflection.md`](./reflection.md) | Step 6 — written answers to the 3 reflection questions. |
| [`llm_judge_evaluation.py`](./llm_judge_evaluation.py) | Steps 7–11 — the working LLM-as-judge implementation (OpenAI API, `gpt-4o-mini`). |
| [`evaluation_results.json`](./evaluation_results.json) | Output of running `llm_judge_evaluation.py`: per-case scores/reasoning/criteria plus aggregate stats. |
| [`implementation_summary.md`](./implementation_summary.md) | 2–3 paragraph summary of what was built and the key findings. |

## How to run the code

```bash
# 1. Install dependencies
pip install openai python-dotenv

# 2. Add your OpenAI API key to a .env file (already git-ignored)
echo "OPENAI_API_KEY=your_key_here" > .env

# 3. Run the evaluation
python llm_judge_evaluation.py
```

This runs the judge (`gpt-4o-mini`) against the 4 test cases defined in
`llm_judge_evaluation.py`, prints per-case scores and a summary to the console, and
overwrites `evaluation_results.json` with the latest run.

## How to complete this lab

1. **Fork** this repository.
2. Do the work described in `instructions.md`, committing to your fork.
3. Open a **pull request** back into this repository.
4. You'll receive **AI feedback** on your PR based on `rubric.md`. Address any blocking feedback and push updates to the same PR.

## Submission hygiene

- Keep this repository scoped to this lab only — no unrelated projects or personal files.
- Use clear, descriptive filenames.
- Remove secrets, API keys, and tokens before committing (`.env` is git-ignored).
