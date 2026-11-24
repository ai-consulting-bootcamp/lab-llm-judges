# ShopCo — LLM Judge Evaluation

This lab evaluates fictional ShopCo customer support replies.
It uses five custom cases and an LLM judge with three criteria:
accuracy, completeness, and tone.

Start with [lab_proof.md](lab_proof.md) for the example run,
evidence, main results, and limitations.

## Main Findings

Sandra accepted 4 of 5 replies after AI-assisted review.
The judge accepted 2 of 5 and matched 3 of 5 human verdicts.
Some judge explanations included incorrect claims.

The results support keeping human review.
They do not establish production reliability.

## File Map

| File | Purpose |
|---|---|
| `lab_proof.md` | Main entry point and evidence |
| `benchmark_audit.md` | Review of three public benchmarks |
| `evaluation_design.md` | Policy, five cases, judge prompt, biases, and calibration plan |
| `llm_judge_evaluation.ipynb` | Python implementation and recorded outputs |
| `generated_responses.json` | Five generated replies and generation metrics |
| `human_review.json` | Human-reviewed labels for the generated replies |
| `calibration_v1_results.json` | Original calibration results and API records |
| `calibration_v2_results.json` | Calibration after the prompt adjustment |
| `evaluation_results.json` | Main judge results, API inputs, and aggregate metrics |
| `implementation_summary.md` | Implementation and findings |
| `evaluation_memo.md` | Client report |
| `reflection.md` | Answers to the reflection questions |
| `requirements.txt` | Main Python dependencies |
| `.env.example` | Environment variable template without secrets |
| `.gitignore` | Excludes local secrets and temporary files |

## Environment

Recorded environment:
- Python 3.11.17
- openai 3.26.1
- python-dotenv 1.2.4
- VS Code with Jupyter support

The response model and judge were requested as `gpt-4o-mini`.
The API returned `gpt-4o-mini-2024-07-18`.

## Setup

1. Open the lab folder in VS Code.
2. Select a Python 3.11 environment for the notebook.
3. Install the dependencies:

   python -m pip install -r requirements.txt

4. Copy `.env.example` to `.env`.
5. Set your own `OPENAI_API_KEY` locally.
6. Never commit `.env` or print the API key.

## Reviewing the Submitted Run

Read the saved notebook outputs and JSON files.
No API key or new API calls are needed to inspect these results.

The main run used judge prompt `shopco-v2`.
The earlier calibration files preserve both prompt versions.

## Running a New Experiment

The notebook records an interactive experiment.
Read the cells before executing them.

Some cells make paid API calls. Existing response and result
files are reused, and evidence-saving cells prevent overwrites.

To run a fresh experiment, use a separate copy of the lab folder
without the generated JSON files. Keep the submitted evidence
unchanged. The v1 calibration requires the v1 prompt saved in
`calibration_v1_results.json`; the current design contains v2.

Do not expect identical outputs or metrics on a new run.
Model availability, behaviour, and prices can change.

## Scope and Limitations

This is a fictional, English-language experiment with five cases.
Human labels were reviewed with AI assistance.
Generation and judging used the same model.
Energy use and carbon emissions were not measured.