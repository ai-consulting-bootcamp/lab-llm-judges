# Lab proof · LLMs grading LLMs, with receipts
**Ayhan Demir** · Scenario: Kleinanzeigen buyer-support chatbot (Option C, Retail) · Run date: 2026-11-20

Start here. This page shows one run end to end and links every deliverable.

## Deliverables
| Brief item | File |
|---|---|
| Benchmark audit (Step 2) | [benchmark_audit.md](benchmark_audit.md) |
| Evaluation design (Steps 3-4) | [evaluation_design.md](evaluation_design.md) |
| Evaluation memo (Step 5) | [evaluation_memo.md](evaluation_memo.md) |
| Reflection (Step 6) | [reflection.md](reflection.md) |
| Code (Steps 7-11, Extensions 1, 3, 4) | [llm_judge_evaluation.ipynb](llm_judge_evaluation.ipynb) |
| Evaluation results | [evaluation_results.json](evaluation_results.json) |
| Implementation summary | [implementation_summary.md](implementation_summary.md) |
| File map and how to run | [README.md](README.md) |

## One run: input, evidence, output (case P3, angry scam complaint)
**Input: customer message**
> This is a joke!!! Your useless site let a scammer take my 250 euros. I paid the seller by bank transfer for a PS5 and now he blocked me. Give me my money back NOW or I'm going to the press.

**Chatbot reply (gpt-4o-mini)**
> I understand your frustration, and I'm sorry to hear about your situation. However, payments made outside of "Sicher bezahlen," such as bank transfers, are not covered by buyer protection. Unfortunately, I cannot issue refunds or assist with this directly. 
> 
> I recommend reporting the user or listing to Kleinanzeigen, contacting your bank for assistance, and considering filing a police report for suspected fraud. If you have further questions or need assistance with the reporting process, please let me know.

**Evidence: rule checks:** language PASS, max_words PASS, includes_1 PASS, includes_2 PASS

**Evidence: judge output (gpt-4o-mini)**
```json
{
  "reasoning": "The reply accurately states that bank transfers are not covered by buyer protection and that refunds cannot be issued, aligning with the policy. It provides the correct next steps for the customer to take without promising a refund. The tone is calm and empathetic, acknowledging the customer's frustration without placing blame.",
  "criteria_met": {
    "policy_accuracy": true,
    "resolution": true,
    "tone_language": true
  },
  "score": 5
}
```
Time 2.79 s · 1096 + 89 tokens · $0.00022

## Final output
Across all 5 cases, gpt-4o-mini averaged 4.6/5 with 4 of 5 PASS (gpt-5.4-mini: 4.6/5). The recommendation and caveats are in [evaluation_memo.md](evaluation_memo.md).

![Judge score per test case](score_chart.png)

## Failure or limitation I hit
1. Extension 4 suggests comparing gpt-3.5-turbo with gpt-4o-mini, but gpt-3.5-turbo was shut down on 23 October 2026 (OpenAI deprecations page). My second choice, gpt-4.1-mini, failed with "does not have access to model" on this API key, so the second chatbot and the bigger judge are gpt-5.4-mini (reasoning effort "none", temperature 0). gpt-4o-mini itself is deprecated, with shutdown on 14 January 2027, so this run cannot be reproduced on that model after that date.
2. Calibration: The judge was never more than one point off the known level in the calibration set.
3. Language: In the first run, gpt-4o-mini answered 4 of the 5 English messages in German, although the system prompt said to reply in the customer's language; the German brand names (Kleinanzeigen, Sicher bezahlen, Käuferschutz) most likely pulled it into German. Fix: the code now detects the customer's language and names it in the system prompt. After the fix, all 5 replies from gpt-4o-mini were in the customer's language.
4. JSON parsing: 0 of 30 judge answers could not be parsed.
