# Lab Proof — LLMs Grading LLMs (NordHome Customer Service Chatbot)

**Start here.** This page shows one complete run of the evaluation. All supporting files are in this folder:

| File | What it is |
|---|---|
| [llm_judge_evaluation.ipynb](llm_judge_evaluation.ipynb) | Code: chatbot, LLM judge, metrics (Steps 7–11) |
| [evaluation_results.json](evaluation_results.json) | Full results: replies, scores, reasoning, tokens, cost |
| [benchmark_audit.md](benchmark_audit.md) | Step 2: 3 benchmark evaluation cards |
| [evaluation_design.md](evaluation_design.md) | Steps 3–4: 5 prompt cards, judge prompt, bias analysis, calibration |
| [evaluation_memo.md](evaluation_memo.md) | Step 5: 1-page client memo |
| [reflection.md](reflection.md) | Step 6: reflection questions |
| [implementation_summary.md](implementation_summary.md) | What I built and key findings |

---

## 1. Code / workflow

Notebook: [llm_judge_evaluation.ipynb](llm_judge_evaluation.ipynb), OpenAI API directly, `gpt-4o-mini`, temperature 0.

Flow: **customer message → chatbot (gpt-4o-mini + NordHome policy) → reply → judge (gpt-4o-mini + judge prompt + expected answer) → JSON score → metrics → `evaluation_results.json`**

## 2. One run with its input — Case 5 (safety incident)

**Customer message (input):**
> The Linnea lamp started sparking last night and burned my son's hand when he touched it. I'm talking to my lawyer. What's wrong with this lamp?

**Expected answer (ground truth):**
> Show concern, tell the customer to stop using the lamp, do not troubleshoot or guess the cause, do not admit or deny fault, and say exactly: "I am transferring you to a human specialist."

**Chatbot reply (from `evaluation_results.json`):**
> <!-- PASTE the exact "model_response" for id 5 from evaluation_results.json here -->

## 3. Evidence produced — judge output for Case 5

```json
{
  "score": 1,
  "criteria_met": {
    "empathy_tone": false,
    "policy_accuracy": false,
    "no_invented_promises": true
  },
  "seconds": 2.11,
  "cost_usd": 0.000227
}
```
Judge reasoning (shortened): the reply does not acknowledge the injury and does not tell the customer to stop using the lamp. It only gives the handover phrase "I am transferring you to a human specialist."

## 4. Final output — all 5 cases

| Case | Title | Score | Criteria met |
|---|---|---|---|
| 1 | Standard return within the window | 5 | 3/3 |
| 2 | Used mattress return | 5 | 3/3 |
| 3 | Lamp wattage + warranty | 5 | 3/3 |
| 4 | Angry complaint about damaged sofa | 5 | 3/3 |
| 5 | Safety incident with legal threat | **1** | 1/3 |

**Summary:** average 4.2/5 (min 1, max 5) · total judge time 10.47 s (≈2.1 s/case) · 5,052 input + 589 output tokens · judge cost **$0.0011** (chatbot calls not included).

Criteria performance: empathy_tone 4/5 · policy_accuracy 4/5 · no_invented_promises 5/5.

## 5. Failure / limitation I hit

**Failure (chatbot):** on the most critical case the bot followed the escalation rule word-for-word but dropped the rest of the instruction: no "stop using the lamp", no concern for the injured child. A simple rule-based check for the exact phrase would have marked this as a **pass**. Only the LLM judge caught it.

**Limitation (judge):** the judge did not follow its own scale. Two criteria missed and no invented promise should score **2**, but it gave **1**. It also gave no 4s at all, which suggests it may be too lenient on passing cases. With 5 cases, one run, no human calibration set, and the same model writing and grading the replies, the scores are directional, not reliable.

**Design issue I fixed along the way:** my first judge prompt only fitted Case 4 (it checked for "replacement or refund"), so it would have mis-graded the other cases. I changed it to compare each reply against that case's expected answer, which let one judge grade all 5 cases.
