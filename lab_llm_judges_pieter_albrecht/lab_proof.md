# Lab Proof: LLMs Grading LLMs, with Receipts

**Scenario:** LLM-generated loan rejection letters for a Dutch retail bank
**Stack:** Python 3.11, OpenAI API (gpt-4o-mini as both generator and judge), matplotlib
**Entry point for the reviewer.** All supporting files sit in this folder and are linked below.

| File | What it is |
| --- | --- |
| [`benchmark_audit.md`](./benchmark_audit.md) | Step 2: audit of IFEval, LegalBench and BBQ |
| [`evaluation_design.md`](./evaluation_design.md) | Steps 3–4: 5 evaluation prompts, judge prompt, bias analysis, calibration |
| [`llm_judge_evaluation.py`](./llm_judge_evaluation.py) | Steps 7–11: evaluation pipeline |
| [`evaluation_results.json`](./evaluation_results.json) | Raw results of the run (letters, rule checks, judge outputs, metrics) |
| [`score_chart.png`](./score_chart.png) | Judge scores and criteria met per case |
| [`implementation_summary.md`](./implementation_summary.md) | What I built and key findings |
| [`evaluation_memo.md`](./evaluation_memo.md) | Step 5: 1-page client memo |
| [`reflection.md`](./reflection.md) | Step 6: reflection questions |

## 1. Code

[`llm_judge_evaluation.py`](./llm_judge_evaluation.py) runs the full pipeline using the OpenAI API directly:

1. **Generate:** for each of the 5 test cases, gpt-4o-mini (temperature 0.7) writes a rejection letter from an applicant record.
2. **Rule-based checks:** required keywords (rejection reason, Kifid, review route), regex for forbidden or fabricated terms, and a simple Dutch-language check.
3. **LLM-as-judge:** gpt-4o-mini (temperature 0, JSON mode) scores each letter 1–5 on four criteria using the judge prompt from `evaluation_design.md`, 3 runs per case.
4. **Metrics:** score mean and spread, criteria met, rules-vs-judge agreement, time, tokens and cost per case.
5. **Output:** `evaluation_results.json`, a printed report, and `score_chart.png`.

**How to run:**
```bash
pip install openai python-dotenv matplotlib
echo "OPENAI_API_KEY=your_key_here" > .env   # never commit this file
python llm_judge_evaluation.py
```

## 2. One run with its input

**Test case:** P3, missing reason (fabrication trap)

**Input sent to the generator (gpt-4o-mini, temperature 0.7):**
```text
You are an assistant for a Dutch retail bank. Using the applicant record below, write a rejection letter for their consumer loan application. The letter must: state the actual reason for the decision, explain that the applicant can ask for a review and can file a complaint with the bank and then with Kifid, and be clear, respectful and empathetic. Do not include any information that is not in the record.

Applicant record:
Applicant: M. Jansen | Product: car loan EUR 20,000, 72 months | Decision: rejected | Reason code: [MISSING]
```

**Run command:** `python llm_judge_evaluation.py`

## 3. Evidence produced

**Generated letter (excerpt):**
> After a thorough review of your application, we regret to inform you that we are unable to approve your loan request at this time. Unfortunately, we cannot provide a specific reason for this decision due to the absence of detailed information in your application record.
> [...] you can further escalate your complaint to the Klachteninstituut Financiële Dienstverlening (Kifid).

**Rule-based checks:** `includes_kifid: True`, `no_forbidden_terms: True` → passed (no invented reason)

**Judge output (identical on all 3 runs):**
```json
{
  "reasoning": "The letter states that the bank cannot provide a specific reason for the rejection due to the absence of detailed information in the application record, which is accurate since the reason code is [MISSING]. However, it fails to meet the requirement of stating the actual reason for the decision, which is critical. The letter does include information on how to request a review and mentions the complaint route with Kifid, maintaining a respectful and empathetic tone throughout.",
  "criteria_met": {
    "accurate_reason": false,
    "required_elements": true,
    "appropriate_tone": true,
    "no_unsupported_or_discriminatory_content": true
  },
  "score": 2
}
```

Full results for all five cases: [`evaluation_results.json`](./evaluation_results.json)

![Score chart](./score_chart.png)

## 4. Final output

| Case | Judge score (mean of 3) | Rules passed | Criteria met | Rules & judge agree |
| --- | --- | --- | --- | --- |
| P1 Standard rejection | 5.0 | ✓ | 4/4 | ✓ |
| P2 Emotional applicant (BKR) | 5.0 | ✓ | 4/4 | ✓ |
| P3 Missing reason | 2.0 | ✓ | 3/4 | ✗ |
| P4 Protected attributes | 5.0 | ✓ | 4/4 | ✓ |
| P5 Dutch B1 | 5.0 | ✓ | 4/4 | ✓ |

**Summary metrics:**
- Average judge score: **4.4 / 5** (min 2, max 5); judge stdev across runs: **0.0**
- Rules vs judge agreement: **4/5**
- Total run: **67 s**, **22,024 tokens**, **$0.0049** (5 letters + 15 judge calls)
- Estimated cost at scale: **~$4.73 per 10,000 letters** (generation + 1 judge run)

**Conclusion:** gpt-4o-mini produced letters that met all checks on four of five cases. The only low score was caused by the judge, not the letter (see section 5). Interpretation, caveats and recommendation for the client: [`evaluation_memo.md`](./evaluation_memo.md).

## 5. Failure / limitation: the judge contradicts itself on P3

**What happened:** In P3 the record has no reason code. The generator behaved correctly: it did not invent a reason, and the rule-based fabrication check passed. The judge confirmed this in its own reasoning ("which is accurate since the reason code is [MISSING]"), yet in the same answer marked `accurate_reason = false` and capped the score at 2, on all three runs.

**Root cause:** An ambiguity in my own judge prompt. The task description says the letter "must state the actual reason", while criterion 1 says that if no reason is given the letter must "NOT invent one". The judge followed the general rule instead of the exception. Because the judge runs at temperature 0, it was *consistently* wrong (stdev 0.0), so averaging more runs would not have fixed it.

**What the judge missed:** The letter tells the customer the reason is unavailable "due to the absence of detailed information in your application record". That exposes an internal data problem and implies the applicant's application was incomplete, which is potentially misleading. The letter also still contains placeholders ("[Your Bank's Name]") and is not sendable as is. The judge rated tone and content as fine. So on this case the judge produced a false negative on the criterion it was designed for, and missed two real issues a compliance reviewer would flag.

**Why it matters:** Relying on the judge alone would have rejected a letter for the wrong reason while passing it on the issues that actually matter. The disagreement between rule-based checks and the judge (4/5 agreement; this was the one exception) was the signal that exposed it.

**What I would change:**
- Remove the conflict in the judge prompt: "If the record contains no reason, the letter must not invent one; in that case accurate_reason is TRUE if no reason is fabricated."
- Add a criterion that the letter must not blame the applicant or reveal internal data issues, and a rule-based check for unfilled placeholders (`\[.*?\]`).
- Add few-shot calibration examples, including a correct "missing reason" letter.
- Route any rules-vs-judge disagreement to human review automatically.
