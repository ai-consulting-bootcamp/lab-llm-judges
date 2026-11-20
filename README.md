# LLM-as-Judge Evaluation Lab: Northwind Living Customer Service Chatbot

**Author:** Barsha Mishra

## Scenario
**Northwind Living** (fictional) is a German online retailer for furniture and home goods. It wants an LLM chatbot as the first line of customer service for returns, delivery, product questions and complaints. The chatbot must follow the company policy exactly, stay calm with upset customers, and hand over to a human for legal threats, safety issues or requests outside the policy. The main failure modes are hallucinated policies, wrong tone, missing escalation and mishandled personal data.

## Approach
1. **Benchmark audit:** reviewed τ-bench (retail), IFEval and MT-Bench for relevance, contamination and saturation. None fits the client's own policy, so I built a custom mini-benchmark.
2. **Evaluation design:** 5 test prompts (standard return, non-returnable mattress trap, angry customer, injury plus legal threat, discount and card-number privacy case), each with ground truth, verification method and failure mode, plus a full LLM-as-judge prompt with bias analysis and calibration strategy.
3. **Implementation:** `gpt-4o-mini` chatbot → `gpt-4o-mini` judge (JSON, 1-5 score, 3 criteria) + rule-based regex checks → metrics (score, criteria, time, tokens, cost) → `evaluation_results.json`.
4. **Calibration extra:** the judge gave scores of 4 when its own criteria were not met, so a calibrated score caps the score by the number of criteria met (average 4.0 → 3.4).
5. **Reporting:** a 1-page client memo and a reflection.

## How to run
1. Create a `.env` file (not committed): `OPENAI_API_KEY=your_key_here`
2. Install the packages: `pip install openai python-dotenv`
3. Open `llm_judge_evaluation.ipynb` and run all cells top to bottom. A full run costs less than $0.01 with `gpt-4o-mini`.

## File map
| File | What it is |
|---|---|
| `benchmark_audit.md` | 3 benchmark evaluation cards (τ-bench, IFEval, MT-Bench) with verdicts |
| `evaluation_design.md` | Company policy, 5 evaluation prompt cards, the full LLM-as-judge prompt, bias analysis and calibration strategy |
| `llm_judge_evaluation.ipynb` | Python implementation: setup, judge, test cases, run, metrics, analysis, calibrated score |
| `evaluation_results.json` | Results per case (reply, scores, reasoning, criteria, rules, time, tokens, cost) and summary statistics |
| `implementation_summary.md` | What I built and the key findings |
| `evaluation_memo.md` | 1-page memo to the client with results, caveats and recommendation |
| `reflection.md` | Answers to the 3 reflection questions |
| `.gitignore` | Keeps `.env` (API key) out of the repo |
