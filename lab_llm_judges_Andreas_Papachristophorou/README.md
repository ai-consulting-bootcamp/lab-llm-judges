# W7D5_LAB_LLMs grading LLMs—with receipts
- Week 7 / Day 5
- Student: Andreas Papachristophorou
- Course: AI Consulting & Integration 2026-07
- Date: 2026-08-21
---

## Your chosen scenario

Option B: Healthcare

- A hospital wants to summarize patient records
- Requirements: Must preserve critical medical information
- Key concerns: Accuracy, completeness, medical terminology

> A hospital wants to use an LLM to create concise summaries of patient records so that clinicians can review important information more efficiently. The summaries must accurately preserve diagnoses, medications, allergies, test results, and changes in a patient’s condition while using correct medical terminology. The main risks are omitting critical information, inventing facts, confusing medications or dosages, and producing a summary that could lead to an unsafe clinical decision.

## Project Overview

This project implements an LLM-as-a-judge evaluation pipeline for a healthcare use case. The scenario evaluates whether AI-generated patient-record summaries are accurate, complete, supported by the source record, and safe for clinical handover.

The implementation uses Python, LangChain, OpenAI's `gpt-4o-mini` model, and a structured JSON evaluation format. The evaluator scores each model-generated summary from 1 to 5 and checks factual accuracy, completeness, unsupported inferences, and safety-critical errors.

## Key Findings

The evaluation was run on three synthetic clinical-summary test cases:

- A safe and complete summary received a score of 5 out of 5.
- A summary missing important ECG and discharge information received a score of 3 out of 5.
- A summary with an unsupported diagnostic conclusion received a score of 1 out of 5 and triggered a safety flag.

The average score across the three cases was 3.0 out of 5. One safety-critical unsupported claim was detected. This supports the recommendation that clinical summaries should receive qualified clinician review before they are used in practice.

## Project Structure

```text
W7D5_LAB_LLMs_grading_LLMs-with_receipts/
│
├── .vscode/                         # VS Code workspace settings
├── lab_llm_judges_Andreas_Papachristophorou/
│   ├── benchmark_audit.md            # Review of three relevant LLM benchmarks
│   ├── evaluation_design.md          # Five evaluation prompts and LLM-judge design
│   ├── evaluation_memo.md            # Client-facing evaluation memo
│   ├── evaluation_results.json       # Detailed results, tokens, time, and cost metrics
│   ├── implementation_summary.md     # Brief description of the implementation and findings
│   ├── llm_judge_evaluation.py       # Python LLM-as-a-judge evaluation pipeline
│   ├── README.md                     # Project documentation and instructions
│   ├── reflection.md                 # Reflection on evaluation design challenges
│   └── requirements.txt              # Required Python packages
│
├── .env                              # OpenAI API key; not committed to GitHub
├── .gitignore                        # Files excluded from Git tracking, including .env
├── instructions.md                   # Lab instructions
├── README.md                         # This file
└── rubric.md                         # Lab assessment criteria
```

## Setup

1. Open a terminal in the project folder.

2. Move into the implementation folder:

```bash
cd lab_llm_judges_Andreas_Papachristophorou
```

3. Install the required packages:

```bash
python -m pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your OpenAI API key:

```text
OPENAI_API_KEY=your_api_key_here
```

Do not upload or commit the `.env` file because it contains a private API key.

## Run the Evaluation

From inside the `lab_llm_judges_Andreas_Papachristophorou` folder, run:

```bash
python llm_judge_evaluation.py
```

The script evaluates three test summaries and prints:

- Individual scores and judge reasoning
- Safety flags and rubric criteria performance
- Score distribution
- Evaluation time
- Input and output token usage
- Estimated API cost

The script also creates or overwrites:

```text
evaluation_results.json
```

## Limitations

This project is a small demonstration using three synthetic examples. Its results do not establish clinical safety or real-world performance. A production evaluation would require a larger set of representative, de-identified records, clinician-defined reference standards, human review, and calibration of the LLM judge against clinical expert ratings.
