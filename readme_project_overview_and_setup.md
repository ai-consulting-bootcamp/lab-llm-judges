# Meridian Community Bank — LLM Evaluation & LLM-as-Judge Lab

## Chosen Client Scenario (Option A: Financial Services)
**Meridian Community Bank** wants to automate the drafting of **adverse action (loan rejection, counteroffer, and incomplete-application) letters** for retail consumer lending (auto, personal, and home improvement loans) directly from structured underwriting records. The letters must be **factually accurate, empathetic, and fully compliant** with US federal fair-lending laws—specifically the **Equal Credit Opportunity Act (ECOA / Regulation B)** and the **Fair Credit Reporting Act (FCRA)**. The primary risks and failure modes include hallucinated credit bureaus or denial reasons, omitted statutory disclosures (such as the 60-day free credit report notice), unauthorized promises of future loan approval, and leakage of protected-class attributes (e.g., age, marital/widowed status, retirement/pension income) from raw underwriter notes.

## Overview of Evaluation Approach
1. **Benchmark Audit (`benchmark_audit.md`):** Audited three public LLM benchmarks (**IFEval**, **FinQA**, and **TruthfulQA**) for domain relevance, training-data contamination, and score saturation. Rejected FinQA and TruthfulQA due to task mismatch and heavy saturation/contamination, and adapted IFEval's deterministic constraint-verification methodology to enforce mandatory statutory disclosures and prohibited-term guardrails.
2. **Custom Mini-Benchmark & LLM-as-Judge Design (`evaluation_design.md`):** Built 5 realistic adverse-action evaluation prompts spanning standard denials, internal-only denials without credit bureau pulls, noisy underwriter notes containing protected-class attributes, conditional counteroffers, and incomplete-application closures. Designed a 4-criterion compliance-gated LLM-as-judge prompt (`factual_accuracy`, `regulatory_compliance`, `empathetic_professional_tone`, `completeness_and_clarity`) paired with a bias analysis and human calibration plan.
3. **Executive Client Reporting & Critical Reflection (`evaluation_memo.md`, `reflection.md`):** Authored a 1-page client evaluation memo with hedged recommendations, operational metrics, and methodological caveats, alongside reflections on French-language localization, AGI framing, and human-in-the-loop necessity.
4. **Python Implementation & Telemetry (`llm_judge_evaluation.py`, `llm_judge_evaluation.ipynb`, `evaluation_results.json`):** Implemented an automated evaluation pipeline using `gpt-4o-mini` (`temperature=0.0`, JSON structured output) combined with deterministic regex guardrails, tracking per-case scores, criteria pass rates, latency, token usage, and estimated USD cost.

## Repository File Structure

| File | Lab Deliverable | Description |
| :--- | :--- | :--- |
| `README.md` | Repository Map | Client scenario, evaluation overview, file directory map, and setup instructions. |
| `benchmark_audit.md` | Part 1, Steps 1–2 | Client scenario definition and 3 structured benchmark evaluation cards (`IFEval`, `FinQA`, `TruthfulQA`). |
| `evaluation_design.md` | Part 1, Steps 3–4 | 5 custom evaluation prompt cards, full LLM-as-judge prompt, bias analysis, and calibration strategy. |
| `evaluation_memo.md` | Part 1, Step 5 | 1-page executive evaluation memo to Meridian Community Bank leadership with hedged recommendations. |
| `reflection.md` | Part 1, Step 6 | Written reflections on French localization, "AGI-level" client questions, and human-only judgment. |
| `llm_judge_evaluation.py` | Part 2, Steps 7–11 | Standalone Python script running candidate generation, LLM-as-judge scoring, rule checks, and reporting. |
| `llm_judge_evaluation.ipynb` | Part 2, Steps 7–11 | Interactive Jupyter Notebook version of the evaluation pipeline with `matplotlib` score visualizations. |
| `evaluation_results.json` | Part 2, Step 10 | Structured JSON output containing aggregate statistics, token/cost metrics, and per-case judge reasoning. |
| `implementation_summary.md` | Part 2, Step 11 | 3-paragraph summary of the Python implementation, key findings, and operational telemetry. |
| `requirements.txt` | Environment Setup | Python package dependencies (`openai`, `langchain`, `langchain-openai`, `python-dotenv`, `matplotlib`). |

## How to Run the Code

### 1. Create a Local Folder & Install Dependencies
Place all downloaded files into a folder named `lab_llm_judges_[your_name]`, then install the dependencies:

```bash
pip install -r requirements.txt
```

### 2. Configure Your OpenAI API Key (Keep Out of Git!)
Create a `.env` file in your project root and add `.env` to a `.gitignore` file so secrets are never committed to GitHub:

```bash
echo "OPENAI_API_KEY=your_actual_openai_api_key_here" > .env
printf ".env\n__pycache__/\n.ipynb_checkpoints/\n" > .gitignore
```

### 3. Run the Evaluation Pipeline
- **Live OpenAI API mode (`gpt-4o-mini`):**
  ```bash
  python llm_judge_evaluation.py
  ```
- **Offline verification mode (no API key or spend required):**
  ```bash
  python llm_judge_evaluation.py --mock
  ```
- **Jupyter Notebook mode:**
  ```bash
  jupyter notebook llm_judge_evaluation.ipynb
  ```