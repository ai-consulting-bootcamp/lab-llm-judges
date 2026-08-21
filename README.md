# Lab | Week 7 | Day 5 | LLMs grading LLMs—with receipts
## John Adams

#### Your chosen scenario

John (the "client") wants a RAG-backed chatbot that stands in for an initial coffee chat with recruiters and hiring managers, answering questions about his work history, skills, and projects, then booking a call or sending a message. The bot is a direct stand-in for his personal brand, so hallucinated experience, off-script tone, or misstated facts don't just look like a bug, they can misrepresent him to a recruiter.

#### Brief overview of your approach

- Audited 3 existing benchmarks (IFBench, BFCL, SimpleQA Verified) against the scenario, rejecting SimpleQA Verified since it tests memorized knowledge, not RAG retrieval.
- Designed 5 custom evaluation prompts, tied to real observed issues from testing the actual chatbot (retrieval misses, internal data leakage), plus a control question with no known trap.
- Built a full LLM-as-judge prompt for the brand tone prompt, with bias analysis and a calibration strategy.
- Wrote a client memo and 3 reflection questions.
- Implemented and ran the judge in a Jupyter notebook, using real `gpt-4o-mini` API calls, not simulated output.

#### Files

- `benchmark_audit.md`, Step 2, 3 benchmark evaluation cards
- `evaluation_design.md`, Steps 1, 3, 4: scenario, 5 evaluation prompts, judge design with bias and calibration analysis
- `evaluation_memo.md`, Step 5: 1-page client memo
- `reflection.md`, Step 6: 3 reflection questions
- `llm_judge_evaluation.ipynb`, Steps 7-11: setup, judge implementation, test dataset, evaluation run, results analysis
- `evaluation_results.json`, saved output from the notebook run
- `implementation_summary.md`, 2-3 paragraph summary of what was built and key findings

#### How to run your code

1. Install dependencies: `pip install openai python-dotenv`
2. Add your own `OPENAI_API_KEY` to a `.env` file in this folder (not committed, see `.gitignore`)
3. Run `llm_judge_evaluation.ipynb` top to bottom
4. Results save to `evaluation_results.json`
