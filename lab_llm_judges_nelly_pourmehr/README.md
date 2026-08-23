# LLM Judges with Receipts - SaaS Support Chatbot Evaluation

## Scenario
A SaaS company wants an AI chatbot that answers feature questions and helps customers troubleshoot the product. Main risks: hallucinating features that don't exist, wrong tone under frustration, incomplete troubleshooting, false claims about account access, and guessing at vague requests.

## Approach
1. Audited 3 existing benchmarks (TauBench, IFEval, GAIA) for relevance, contamination, and saturation. Rejected IFEval as saturated.
2. Designed 5 custom evaluation prompts, each targeting a specific failure mode.
3. Built one full LLM-as-judge prompt, targeting the multi-cause troubleshooting prompt, with bias analysis and calibration notes.
4. Wrote a client memo and reflection on evaluation design tradeoffs.
5. Implemented the judge in Python (OpenAI API, gpt-4o-mini), ran it on all 5 test cases, and saved results with cost and time metrics.

## Files
- `benchmark_audit.md` - 3 benchmark evaluation cards
- `evaluation_design.md` - 5 evaluation prompts, full judge prompt, bias analysis, calibration strategy
- `evaluation_memo.md` - 1-page client memo
- `reflection.md` - answers to 3 reflection questions
- `llm_judge_evaluation.py` - judge function, test dataset, evaluation runner
- `evaluation_results.json` - full results, individual and aggregate
- `implementation_summary.md` - summary of what was built and key findings

## How to run
1. `conda activate My_class_repo_conda`
2. `pip install openai python-dotenv`
3. Add your key to `.env`: `OPENAI_API_KEY=your_key_here`
4. `python llm_judge_evaluation.py`