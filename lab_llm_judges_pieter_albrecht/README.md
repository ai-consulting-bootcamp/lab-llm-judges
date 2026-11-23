# Lab: LLMs Grading LLMs, with Receipts

**Author:** Pieter Albrecht · Ironhack AI Consulting & Integration Bootcamp

> **Reviewer entry point:** [`lab_proof.md`](./lab_proof.md)

## Scenario
A Dutch retail bank wants to use an LLM to draft rejection letters for consumer loan applications, generated from the applicant's file and the credit decision. Letters must state the actual reason for rejection, explain how to appeal or file a complaint, and be clear and empathetic. The main risks are the model inventing or misstating the reason, leaving out required information, and using a cold or discriminatory tone.

## Approach
1. **Benchmark audit:** reviewed IFEval, LegalBench and BBQ for relevance, contamination and saturation. None fits the use case, which justifies a custom evaluation.
2. **Custom evaluation design:** 5 test prompts covering a standard case, tone, hallucination, bias and Dutch-language output, each with ground truth, a verification method and a failure mode.
3. **LLM-as-judge:** a judge prompt with task description, 4 criteria, reasoning steps, score anchors and JSON output, plus bias analysis and calibration strategy.
4. **Implementation:** a Python pipeline that generates letters with gpt-4o-mini, verifies them with rule-based checks and an LLM judge (3 runs per case), and tracks score, time, tokens and cost.
5. **Reporting:** a client memo with hedged recommendations, plus reflection.

**Key result:** average judge score 4.4/5; rules and judge agreed on 4/5 cases. On the missing-reason case the judge contradicted its own reasoning and failed a correct letter. Full run cost: $0.0049.

## How to run
```bash
pip install openai python-dotenv matplotlib
echo "OPENAI_API_KEY=your_key_here" > .env   # never commit this file
python llm_judge_evaluation.py
```
Outputs: `evaluation_results.json`, `score_chart.png` and a printed report.

## File map
| File | Purpose |
| --- | --- |
| `lab_proof.md` | Entry point: code, one run with input, evidence, output, failure |
| `benchmark_audit.md` | Step 2: three benchmark evaluation cards |
| `evaluation_design.md` | Steps 3–4: five prompt cards, judge prompt, bias analysis, calibration |
| `evaluation_memo.md` | Step 5: one-page client memo |
| `reflection.md` | Step 6: answers to the three reflection questions |
| `llm_judge_evaluation.py` | Steps 7–11: evaluation pipeline |
| `evaluation_results.json` | Raw results and summary metrics |
| `score_chart.png` | Judge scores and criteria met per case |
| `implementation_summary.md` | What was built and key findings |
