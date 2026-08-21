# LLMs Grading LLMs — Retail Chatbot Evaluation Lab

This repository contains the completed deliverables for the **LLMs grading LLMs—with receipts** lab.

## Scenario

The client is a fictional online retailer evaluating an LLM customer-service chatbot. The chatbot must answer product questions, explain return eligibility, handle complaints, escalate safety issues, and call approved support tools without fabricating actions.

## File map

| File | Purpose |
|---|---|
| `benchmark_audit.md` | Audit of MMLU, MT-Bench, and BFCL, including contamination/saturation risks and recommendations. |
| `evaluation_design.md` | Five custom evaluation prompt cards, verification methods, failure modes, complete judge prompt, bias analysis, and calibration plan. |
| `evaluation_memo.md` | Approximately one-page client memo with illustrative results and professional caveats. |
| `reflection.md` | Responses to the three reflection questions. |
| `llm_judge_evaluation.py` | Offline-capable Python evaluation pipeline with optional OpenAI live mode. |
| `evaluation_results.json` | Results from the reproducible offline demonstration run. |
| `implementation_summary.md` | Implementation explanation, findings, limitations, and run instructions. |

## How to run

Offline demonstration, no API key required:

```bash
python llm_judge_evaluation.py
```

Live API mode:

```bash
pip install openai
export OPENAI_API_KEY="your_key_here"
python llm_judge_evaluation.py --live --model gpt-4o-mini
```

Never commit API keys or `.env` files. The offline results are deliberately labelled as a demonstration; they are not evidence that a production model has passed the client’s acceptance criteria.

## External references

- MMLU paper: https://arxiv.org/abs/2009.03300
- MT-Bench paper: https://arxiv.org/abs/2306.05685
- BFCL paper: https://proceedings.mlr.press/v267/patil25a.html
- Stanford HELM: https://crfm.stanford.edu/helm/

### Offline and Online Tests done successfully