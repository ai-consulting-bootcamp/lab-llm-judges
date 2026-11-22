# Lab Proof — LLMs Grading LLMs with Receipts

## Scenario and scope

This lab evaluates answers from a fictional Dynamics 365 Finance & Operations vendor-management assistant for MNM AG, covering the MNM-DE and MNM-NL legal entities. All company policies and vendor details in the test cases are fictional.

## Design evidence (Steps 1–6)

- Selected the MNM AG vendor-management use case.
- Reviewed EKRAG, IFBench and GroUSE in `benchmark_audit.md`.
- Prepared five evaluation cards and a 1–5 LLM-judge rubric in `evaluation_design.md`.
- Documented a client-facing evaluation approach in `evaluation_memo.md` and reflections in `reflection.md`.

## Implementation evidence (Steps 7–10)

- Created `llm_judge_evaluation.py` using Python, the OpenAI API and `gpt-4o-mini`.
- Loaded the API key from a local `.env` file and configured `.gitignore` to exclude it.
- Implemented a judge returning JSON with `score`, `reasoning` and `criteria_met` (accuracy, policy compliance, safety and groundedness).
- Successfully tested the judge on the supplier bank-detail-change scenario (score: 5/5).
- Prepared and executed five fictional test cases. Results were written to `evaluation_results.json`.

| Case | Scenario | Judge score | Execution time |
|---|---|---:|---:|
| TC01 | New vendor creation | 4/5 | 1.64 s |
| TC02 | Cross-company vendor use | 1/5 | 1.16 s |
| TC03 | NET30 payment terms | 5/5 | 1.17 s |
| TC04 | Bank-detail change | 4/5 | 1.81 s |
| TC05 | Unknown vendor bank account | 1/5 | 1.30 s |

**Observed average:** 3.0/5 across five cases; total recorded execution time: 7.08 seconds. These are actual outputs from one run, not predicted scores.

## Analysis evidence (Step 11)

`implementation_summary.md` documents the implementation, findings and limitations. The judge assigned low scores to incorrect and fabricated answers, but the 4/5 score for TC04 warrants human review because the sample answer omitted the approval requirement. Five synthetic cases are insufficient to establish production reliability.

## Submission files

- `README.md`
- `benchmark_audit.md`
- `evaluation_design.md`
- `evaluation_memo.md`
- `reflection.md`
- `llm_judge_evaluation.py`
- `evaluation_results.json`
- `implementation_summary.md`
- `lab_proof.md`

**Security:** `.env` contains the local API credential and must not be committed. Git ignore verification returned `.gitignore:1:.env .env`.

**Limitations:** No production MNM AG data or live Dynamics 365 environment was used. Token usage and API cost were not recorded in this run.
