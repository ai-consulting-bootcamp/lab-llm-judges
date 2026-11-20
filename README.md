# lab_llm_judges_nicolo — LLMs Grading LLMs, with Receipts

## Scenario
NordHome, a fictional mid-sized online home-goods retailer, wants an LLM chatbot to handle first-line customer service: return and refund requests, product questions, and complaints. It must apply the return policy exactly, answer product questions only from catalogue data, and stay polite and calm with angry customers. The main risks are made-up policy terms or product facts, the wrong tone with upset customers, and failing to pass sensitive cases (safety issues, legal threats) to a human.

## Approach
1. **Benchmark audit:** reviewed IFEval, TruthfulQA and τ-bench retail for relevance, contamination and saturation. None answers "does the bot follow *our* policy?", so I built a custom evaluation.
2. **Evaluation design:** 5 test prompts from easy to critical, each with a ground truth and verification method, plus an LLM-as-judge prompt with a 1–5 scale, bias analysis and calibration plan.
3. **Implementation:** gpt-4o-mini answers the 5 prompts as the NordHome chatbot. A second gpt-4o-mini call grades each reply against its expected answer. Time, tokens and cost are recorded.
4. **Reporting:** client memo with caveats, reflection, and a proof page.

**Result:** average 4.2/5. Routine cases scored 5/5, but the safety case failed (1/5). Judge cost $0.0011 for 5 cases.

## File map

| File | Purpose |
|---|---|
| `lab_proof.md` | **Entry point for the reviewer**: one full run, evidence, results, failure |
| `benchmark_audit.md` | Step 2: 3 benchmark evaluation cards |
| `evaluation_design.md` | Steps 3–4: 5 prompt cards, judge prompt, bias analysis, calibration |
| `evaluation_memo.md` | Step 5: 1-page client memo |
| `reflection.md` | Step 6: answers to the 3 reflection questions |
| `llm_judge_evaluation.ipynb` | Steps 7–11: Python code |
| `evaluation_results.json` | Output of the evaluation run |
| `implementation_summary.md` | What I built and key findings |

## How to run

1. Install packages:
   ```bash
   pip install openai langchain langchain-openai python-dotenv
   ```
2. Create a `.env` file in this folder with your key (it is excluded by `.gitignore`):
   ```
   OPENAI_API_KEY=your_key_here
   ```
3. Open `llm_judge_evaluation.ipynb` and run the cells from top to bottom. Results are saved to `evaluation_results.json`.

Model: `gpt-4o-mini`. A full run costs well under $0.01.
