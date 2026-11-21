# LLMs grading LLMs, with receipts · Ayhan Demir
Ironhack AI Consulting & Integration Bootcamp, Week 7 lab. **Reviewers: start with [lab_proof.md](lab_proof.md).**

## Scenario
Option C, Retail. Kleinanzeigen (fictional engagement) wants a customer-service chatbot for buyers who pay with "Sicher bezahlen": returns (buyer-protection claims on a marketplace), questions about items, and complaints, answered only from the official policy, calmly and in the customer's language. Main risks: invented fees or refund rules, false refund promises, the wrong tone and the wrong language.

## Approach
1. Audited 3 public benchmarks (τ-bench retail, IFEval, CoCoNot) for relevance, contamination and saturation.
2. Designed 5 custom prompts, based on Bitext retail intents (Hugging Face) and rewritten for Kleinanzeigen, with an answer key from the Kleinanzeigen help page.
3. Wrote an LLM-as-judge prompt (task, criteria, reasoning steps, JSON output, score anchors) with a bias analysis and a calibration strategy.
4. Ran it in Python with the OpenAI SDK: gpt-4o-mini as chatbot and judge, plus Extension 1 (gpt-5.4-mini as second chatbot), Extension 3 (calibration on 10 known-quality replies) and Extension 4 (gpt-5.4-mini as bigger judge).
5. Wrote the client memo from the real results, and a reflection.

## File map
| File | What it is |
|---|---|
| `lab_proof.md` | Entry point: one run from input to output, deliverables, a limitation |
| `benchmark_audit.md` | Step 1 scenario and Step 2: three benchmark evaluation cards |
| `evaluation_design.md` | Steps 3-4: policy sheet, five prompt cards, judge prompt, bias analysis, calibration strategy |
| `evaluation_memo.md` | Step 5: one-page client memo, numbers from the run |
| `reflection.md` | Step 6: three reflection questions |
| `llm_judge_evaluation.ipynb` | Steps 7-11 and Extensions 1, 3, 4; also writes every document above |
| `evaluation_results.json` | All replies, judge outputs, rule checks, time, tokens, cost and aggregates |
| `implementation_summary.md` | What was built and the key findings |
| `score_chart.png` | Judge score per test case |

## How to run
1. Python 3.12 and VS Code with the Jupyter extension.
2. Create `.env` in this folder with `OPENAI_API_KEY=your_key` (listed in `.gitignore`).
3. Open `llm_judge_evaluation.ipynb` and run the cells top to bottom. The notebook installs its packages (`openai`, `langchain`, `langchain-openai`, `python-dotenv`, `datasets`, `pandas`, `matplotlib`).
4. Estimated API cost: under $0.05. Each milestone has an undo cell; backups go to `_backup/` (listed in `.gitignore`).
