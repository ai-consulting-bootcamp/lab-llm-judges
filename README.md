# LAB | LLMs grading LLMs - with receipts

**Scenario:** Spree Bank AG (fictional German retail bank) wants an LLM to draft loan rejection letters that a credit officer reviews before sending. The letters must give the real reason only, stay compliant (no protected characteristics, no promise of approval, contact and review option included) and be clear and respectful.

**Approach:** I audited 3 public benchmarks (IFEval, FinanceBench, TruthfulQA), and none fits as-is. I then designed a custom 5-case benchmark with two traps (a missing reason code and discriminatory internal notes). Each letter is verified twice: rule-based regex checks act as a hard gate, and an LLM-as-judge rubric (1-5, with criteria flags) grades quality. Time, tokens and cost are tracked.

Start with **[lab_proof.md](lab_proof.md)**.

## How to run
```
pip install -r requirements.txt
cp .env.example .env      # add OPENAI_API_KEY
python llm_judge_evaluation.py
```

## File map
| File | Purpose |
|---|---|
| `lab_proof.md` | Reviewer entry point: workflow, one run with evidence, results, failure/limitation |
| `benchmark_audit.md` | Scenario + 3 benchmark evaluation cards (Step 1-2) |
| `evaluation_design.md` | 5 prompt cards, judge prompt, bias analysis, calibration (Step 3-4) |
| `evaluation_memo.md` | 1-page client memo (Step 5) |
| `reflection.md` | 3 reflection questions (Step 6) |
| `llm_judge_evaluation.py` | Implementation (Step 7-11) |
| `evaluation_results.json` | Raw per-case results and aggregate metrics |
| `implementation_summary.md` | What I built and key findings |
