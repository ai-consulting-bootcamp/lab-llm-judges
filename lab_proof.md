# Lab proof: LLMs grading LLMs, with receipts

**Author:** Elif Yurdakul · Ironhack W7D4 · Scenario: AI-drafted loan decline letters for Kranich Direktbank AG (fictional, Berlin)

## 1. Workflow (code)

```
data/test_cases.json (5 case files + ground truth + rule checks)
        │
        ▼
llm_judge_evaluation.py
  [1] calibrate judge ── known-good letter (expect ≥4) / known-bad letter (expect ≤2)
  [2] for each model (gpt-4o-mini, gpt-5.4-mini) × case:
        generate letter ──► rule checks (required / forbidden terms, ≤250 words)
                       └──► LLM judge ×3 (gpt-5.4-mini, JSON: score, reasoning, 4 criteria)
        PASS = rules pass AND mean score ≥ 4 AND 4/4 criteria
  [3] metrics: scores, consistency, time, tokens, cost ──► evaluation_results.json + results_chart.png
```

| Deliverable | File |
|---|---|
| Benchmark audit (Step 2) | [`benchmark_audit.md`](benchmark_audit.md) |
| 5 prompt cards, judge prompt, bias + calibration (Steps 1, 3, 4) | [`evaluation_design.md`](evaluation_design.md) |
| Client memo (Step 5) | [`evaluation_memo.md`](evaluation_memo.md) |
| Reflection (Step 6) | [`reflection.md`](reflection.md) |
| Code (Steps 7–11) | [`llm_judge_evaluation.py`](llm_judge_evaluation.py) · [`data/test_cases.json`](data/test_cases.json) |
| Results: final (judge v2) | [`evaluation_results.json`](evaluation_results.json) · [`results_chart.png`](results_chart.png) |
| Results: first run (judge v1) | [`results/evaluation_results_judge_v1.json`](results/evaluation_results_judge_v1.json) · [`results/results_chart_judge_v1.png`](results/results_chart_judge_v1.png) |
| Implementation summary | [`implementation_summary.md`](implementation_summary.md) |

Commands used:
```bash
python llm_judge_evaluation.py                                              # run 1: generate + judge (v1)
python llm_judge_evaluation.py --rejudge results/evaluation_results_judge_v1.json   # run 2: same letters, judge v2
```

## 2. One run: input → evidence → output (TC5, the hallucination trap)

**Input** (case file; the decline reason is missing on purpose):
```
reference: KD-2026-0438 · applicant: Leon Wagner · product: Personal loan · amount_eur: 12,000
decision: Declined · decision_process: Credit officer decision · main_reason: [not recorded]
```
**Ground truth:** do NOT invent a reason. Insert `[MISSING: …]` and flag the letter for staff.

**Output 1: gpt-5.4-mini** (shortened)
> "…we cannot approve your application for the above loan amount. The main reason for this decision is: **[MISSING: main reason for the decline]**. You may request an explanation of the assessment, share your point of view, and ask for a member of staff to review the decision. … *Note to staff: Main reason for the decline is missing from the case file and must be inserted before sending.*"

**Output 2: gpt-4o-mini** (shortened)
> "Unfortunately, **we are unable to provide the specific reason for this decision as it was not recorded in our system.** … If you have concerns about your credit history, you may wish to check your records with relevant credit bureaus directly."

**Evidence:**

| Letter | Rule checks | Judge v1 scores | Judge v2 scores | Final verdict |
|---|---|---|---|---|
| gpt-5.4-mini | PASS | 2, 3, 2 → FAIL ❌ *(judge mistake)* | **5, 4, 4 → PASS** | Correct behaviour |
| gpt-4o-mini | FAIL: `[MISSING` absent; "credit history" present | 2, 2, 2 → FAIL | **2, 2, 2 → FAIL** | Real failure |

What the judge said:
- **v1, gpt-5.4-mini:** "it leaves a placeholder for a missing reason and even includes an internal note to staff, which should not be sent to the applicant."
- **v2, gpt-5.4-mini:** "it correctly avoids inventing a reason by marking the missing main reason for staff review."
- **v2, gpt-4o-mini:** "the draft wrongly tells the applicant only that the reason was 'not recorded' instead of flagging the missing reason for staff with a placeholder."

**Final output (whole run, judge v2):**

| | gpt-4o-mini | gpt-5.4-mini |
|---|---|---|
| Pass rate | 4 of 5 (80%) | **5 of 5 (100%)** |
| Average judge score | 4.2 | 4.87 |
| Generation time per letter | 5.95 s | 1.16 s |
| Cost per 1,000 letters | $0.25 | $1.19 |

Calibration: known-good 5/5/5, known-bad 1/1/1. Judge consistency: 100% / 80%.
Totals for both runs: 82 API calls, about 111k tokens, about **$0.15**.

## 3. Failure / limitation I hit

**My first judge failed its own calibration test.** It scored the known-good letter 2, 2, 5. Its reasoning showed two design errors in *my* prompt:
1. "Never reveal internal thresholds" didn't say *which* thresholds are internal. So the judge punished the customer-facing affordability limit, and randomly punished the €10,000 policy in TC3.
2. The judge's rules contradicted the generator's rules on how to handle missing information, so it failed gpt-5.4-mini for doing exactly what it was told.

**The fix:** judge prompt v2 adds four clarifications (see the `JUDGE_PROMPT` "Important clarifications" block). I then **re-judged the same letters** (`--rejudge`), so the judge was the only thing that changed.

**Limitation that remains:** v2 was fixed using the same two reference letters it is calibrated on, so it could be over-fitted to them. A fresh, human-scored calibration set of about 30 letters is the next step. The judge is also one of the models it judges (self-preference risk), and 5 cases means each letter moves a pass rate by 20 points.
