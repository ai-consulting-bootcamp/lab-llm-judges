## Retail chatbot evaluation

The lab evaluates a fictional online retailer’s chatbot on returns, product questions, and complaints. The Python script calls GPT-4o mini through LangChain and combines a reference-based LLM judge with exact routing-label checks.

- [`benchmark_audit.md`](./benchmark_audit.md) — client scenario and three public benchmark reviews
- [`evaluation_design.md`](./evaluation_design.md) — five test cases and the judge design
- [`evaluation_memo.md`](./evaluation_memo.md) — client memo based on simulated results
- [`reflection.md`](./reflection.md) — language coverage, AGI, and human judgment
- [`llm_judge_evaluation.py`](./llm_judge_evaluation.py) and [`requirements.txt`](./requirements.txt) — evaluation code and dependencies
- [`evaluation_results.json`](./evaluation_results.json) and [`implementation_summary.md`](./implementation_summary.md) — live-run details and analysis

Run from the project directory in PowerShell. Set `OPENAI_API_KEY` in the environment or in the local `.env` file before running the last command. It sends ten API requests and replaces `evaluation_results.json` with the new run.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe .\llm_judge_evaluation.py --evaluate
```
