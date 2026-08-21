# LLMs Grading LLMs — With Receipts

## Scenario
An AI coaching assistant for employees: helping them define personal/
professional development goals and improve performance in their current role.
Requirements: goals must be specific, measurable, and derived from what the
employee actually said; the assistant must keep a supportive, non-judgmental
coaching tone; it must recognize when a topic falls outside coaching scope
(e.g. mental health, HR/legal issues) and redirect appropriately. Main
concerns: generic advice, overstepping into therapy territory, and sycophantic
responses that validate instead of coach.

## Overview of approach
1. **Benchmark audit** (`benchmark_audit.md`) — evaluated MT-Bench,
   EmpatheticDialogues, and MMLU for fit; rejected all three as insufficient
   for coaching-specific behavior, kept MT-Bench's judging methodology as a
   reference.
2. **Evaluation design** (`evaluation_design.md`) — 5 custom prompts covering
   the coaching moments most likely to reveal quality gaps (vague goals,
   emotionally loaded/borderline scope, unmeasurable goals, resistance to the
   coaching process, and accountability follow-up), plus a full LLM-as-judge
   prompt with bias analysis and calibration strategy.
3. **Evaluation memo** (`evaluation_memo.md`) — 1-page client-facing summary
   with appropriate hedging and caveats.
4. **Reflection** (`reflection.md`) — answers on French-language adaptation,
   the "is this AGI-level" question, and what requires human evaluation.
5. **Implementation** (`llm_judge_evaluation.py`) — runs the 5 prompts through
   gpt-4o-mini (the coaching assistant), then judges each response with a
   generalized version of the Step 4 judge rubric (specificity-seeking,
   coaching stance, tone). Saves results + metrics to
   `evaluation_results.json`.

## File map
- `benchmark_audit.md` — 3 benchmark evaluation cards
- `evaluation_design.md` — 5 evaluation prompts + judge prompt + bias/calibration analysis
- `evaluation_memo.md` — 1-page client memo
- `reflection.md` — 3 reflection questions
- `test_dataset.py` — explicit test dataset (prompt, ground truth, expected criteria per case)
- `llm_judge_evaluation.py` — evaluation pipeline (generation + judging), imports `test_dataset.py`
- `evaluation_results.json` — output of the pipeline (generated on run)
- `implementation_summary.md` — summary of what was built and key findings
- `troubleshooting_notes.md` — how each lab-guide troubleshooting issue was addressed
- `requirements.txt` — Python dependencies
- `.env.example` — template for the required `OPENAI_API_KEY`

## How to run
```bash
pip install -r requirements.txt
cp .env.example .env   # then add your real OPENAI_API_KEY
python llm_judge_evaluation.py
```
This prints a per-case and aggregate summary to the console and writes full
results to `evaluation_results.json`.