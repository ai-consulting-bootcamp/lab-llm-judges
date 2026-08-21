# LLM-as-Judge Evaluation Lab -- Should-Cost Negotiation-Prep Summarization

## Scenario
A Tier-1 automotive supplier's procurement team wants to use an LLM to
generate should-cost negotiation-prep summaries from RFQ and cost-breakdown
data, extending the should-cost benchmarking engine from Project 3. Key
concerns: hallucinated cost figures, missing critical cost drivers, and
overconfident recommendations.

## Approach
1. Audited 3 existing financial LLM benchmarks (FinQA, FinanceBench, Vectara
   HHEM) for relevance, contamination, and saturation risk against this
   scenario -- see `benchmark_audit.md`.
2. Designed 5 custom evaluation prompts covering baseline accuracy, missing
   data, ambiguous ranking, tone, and multi-currency complexity, plus a full
   LLM-as-judge prompt with bias and calibration analysis -- see
   `evaluation_design.md`.
3. Wrote a client-facing evaluation memo with results and caveats -- see
   `evaluation_memo.md`.
4. Answered 3 reflection questions on evaluation design challenges -- see
   `reflection.md`.
5. Implemented and ran the evaluation in Python -- see
   `llm_judge_evaluation.py`, `evaluation_results.json`, and
   `implementation_summary.md`.

## File Map
- `benchmark_audit.md` -- 3 benchmark evaluation cards
- `evaluation_design.md` -- 5 custom eval prompts + full judge prompt + bias/calibration analysis
- `evaluation_memo.md` -- 1-page client memo with real results
- `reflection.md` -- 3 reflection question responses
- `llm_judge_evaluation.py` -- working evaluation pipeline (generation + LLM-as-judge)
- `evaluation_results.json` -- raw results from the evaluation run
- `implementation_summary.md` -- summary of what was built and key findings

## How to Run
1. Activate the `bootcamp-env` conda environment.
2. Create a `.env` file with `OPENAI_API_KEY=your_key_here`.
3. Run: `python llm_judge_evaluation.py`
4. Results are written to `evaluation_results.json`; aggregate stats print
   to console.
