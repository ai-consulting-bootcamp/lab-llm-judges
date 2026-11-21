# Evaluation Memo

**TO:** Head of Customer Support, Kleinanzeigen (lab scenario, fictional engagement)
**FROM:** Ayhan Demir
**DATE:** 2026-11-20
**SUBJECT:** LLM Evaluation Results - Kleinanzeigen buyer-support chatbot

## Executive Summary
We measured whether a low-cost model can answer "Sicher bezahlen" buyer questions correctly, calmly and in the customer's language. On 5 test messages, gpt-4o-mini scored 4.6/5 on average and gpt-5.4-mini 4.6/5, graded by an LLM judge checked against 10 replies of known quality.

## Methodology
We audited three public benchmarks (τ-bench retail, IFEval, CoCoNot); none covers a German marketplace policy, so we built a custom test of 5 customer messages: a not-as-described return, an item question the bot cannot answer, an angry scam complaint, an unshipped item and a fee question in German. The answer keys come from the Kleinanzeigen help page (checked 2026-11-20).

Each reply got rule-based checks (language, at most 150 words, required facts such as the 5,00 € fee) and an LLM judge score (gpt-4o-mini, temperature 0) from 1 to 5 on policy accuracy, resolution, and tone and language; 4 or more counts as PASS.

Both chatbots (gpt-4o-mini, gpt-5.4-mini) used the same system prompt, once each.

## Results
gpt-4o-mini: average 4.6/5 (min 3, max 5), 4/5 replies PASS, 17/18 rule checks passed. gpt-5.4-mini: average 4.6/5, 5/5 PASS, 18/18 rule checks passed. Replies not in the customer's language: 0/5 for gpt-4o-mini, 0/5 for gpt-5.4-mini.

Weakest case for gpt-4o-mini: "Fee question in German" (3/5). Judge's reason, shortened: "The chatbot's reply accurately states the service fee as 5 EUR and confirms that the buyer is responsible for this fee,..." Most-missed criterion: policy_accuracy (not met in 1 of 5 cases).

Judge check on the 10 known-quality replies: gpt-4o-mini matched the level exactly in 60%, within one point in 100%, and caught 83% of the bad replies; gpt-5.4-mini scored 90%, 100% and 100%.

## Caveats & Limitations
Five prompts with one run each make this a smoke test: a gap of less than one point could be noise. An OpenAI judge grades OpenAI models (self-preference risk), and the calibration levels were set by the evaluator, not by Kleinanzeigen agents. gpt-4o-mini shuts down on 14 January 2027 and the policy can change, so results may not be reproducible. Public benchmarks carry contamination and saturation risk, and none covers German. Only single messages were tested, without tools or multi-turn conversations.

## Recommendation
Under these conditions, for this task, the two models performed about the same (gap +0.0 points), so keep the cheaper gpt-4o-mini. The bigger judge (gpt-5.4-mini) was not clearly better on the known levels, so gpt-4o-mini stays the judge. Confidence: low (small sample). Before launch: test at least 50 real, anonymised tickets (after a GDPR review) and check the judge against team-lead labels.

## Additional Metrics
The main test plus the model comparison used 17,189 tokens and cost $0.0067. Judging costs about $0.21 per 1,000 replies with gpt-4o-mini versus $1.29 with gpt-5.4-mini (1.7 s versus 1.37 s per reply). Energy was not measured; tokens and time are the proxies.
