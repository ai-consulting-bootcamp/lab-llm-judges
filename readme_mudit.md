# Repository Map

This file explains what each file in the lab contains and how the files relate to one another.
It is the detailed companion to the restored [`README.md`](./README.md), which stays brief and lab-oriented.

## Main Lab Artifacts

- [`instructions.md`](./instructions.md)
  - The source lab brief.
  - Defines the scenario options, required templates, success criteria, and implementation steps.
  - All other deliverables are built to satisfy the requirements in this file.

- [`rubric.md`](./rubric.md)
  - The grading reference used by the reviewer.
  - The content in the deliverables is designed to align with the rubric categories and success criteria.

- [`benchmark_audit.md`](./benchmark_audit.md)
  - Contains the 3 benchmark evaluation cards for the retail scenario.
  - This is the output of Step 2 and feeds the evaluation strategy in `evaluation_design.md`.

- [`evaluation_design.md`](./evaluation_design.md)
  - Contains the 5 retail evaluation prompt cards, the judge prompt, the bias analysis, and the calibration strategy.
  - This is the design input for the Python implementation in `llm_judge_evaluation.py`.

- [`evaluation_memo.md`](./evaluation_memo.md)
  - The client-facing memo summarizing the imagined evaluation results.
  - It is written from the same retail scenario and evaluation logic used in the design and implementation files.

- [`reflection.md`](./reflection.md)
  - Answers the three reflection questions from the lab.
  - It is conceptually connected to the evaluation design because it discusses language, AGI claims, and human judgment limits.

- [`llm_judge_evaluation.py`](./llm_judge_evaluation.py)
  - The runnable Python evaluation script.
  - Implements the judge, test cases, scoring logic, metrics collection, and JSON export.
  - Uses the retail policy assumptions and judge rubric from `evaluation_design.md`.

- [`evaluation_results.json`](./evaluation_results.json)
  - The output artifact created by running `llm_judge_evaluation.py`.
  - Contains per-case results plus aggregate summary metrics.

- [`implementation_summary.md`](./implementation_summary.md)
  - A short summary of what the Python implementation does and what it produced.
  - Sits between the code and the report artifacts by describing the implemented evaluation flow.

## Supporting Files

- [`.gitignore`](./.gitignore)
  - Ignores local secrets, caches, and virtual environment folders.
  - Keeps the repository clean while allowing the lab deliverables to be committed.

- [`requirements.txt`](./requirements.txt)
  - Lists the Python dependencies needed to run the evaluator.
  - Supports the implementation in `llm_judge_evaluation.py`.

- [`README.md`](./README.md)
  - Short usage guide for the lab repository.
  - Tells a reader how to install dependencies and run the evaluator.
  - This file is intentionally brief; the detailed file map lives here in `readme_mudit.md`.

## How The Files Connect

1. `instructions.md` defines the lab requirements.
2. `rubric.md` defines how the submission will be judged.
3. `benchmark_audit.md` and `evaluation_design.md` satisfy the written design portion of the lab.
4. `evaluation_design.md` provides the judge structure used by `llm_judge_evaluation.py`.
5. `llm_judge_evaluation.py` generates `evaluation_results.json`.
6. `evaluation_results.json` provides the results narrative for `evaluation_memo.md` and `implementation_summary.md`.
7. `reflection.md` documents the conceptual tradeoffs behind the evaluation choices.

In short, the flow is:

`instructions.md` -> `benchmark_audit.md` + `evaluation_design.md` -> `llm_judge_evaluation.py` -> `evaluation_results.json` -> `evaluation_memo.md` and `implementation_summary.md`
