# Evaluation Memo

**TO:** Head of Customer Service, Northwind Living GmbH
**FROM:** Barsha Mishra, AI Consultant
**DATE:** 20 November 2026
**SUBJECT:** LLM Evaluation Results - Customer Service Chatbot

## EXECUTIVE SUMMARY
We tested whether a `gpt-4o-mini` chatbot can safely handle first-line customer service (returns, damaged items, complaints, safety cases) using only your company policy. **It is safe but not yet complete:** it never invented a rule or promise in our tests, but it often left out a required detail, including one privacy-relevant warning.

## METHODOLOGY
Public benchmarks did not fit your needs. τ-bench (retail) is the closest match but uses a fictional US policy; IFEval and MT-Bench are saturated and generic (see `benchmark_audit.md`). We therefore built a **custom mini-benchmark of 5 realistic customer messages**: a standard return, a non-returnable mattress (trap), an angry customer with a damaged table, an injury with a legal threat, and a discount request in which the customer shares a card number.

Each reply was scored by an **LLM judge** (`gpt-4o-mini`) on three criteria (tone & empathy, policy accuracy, completeness & next step) using a 1-5 rubric, and checked with **rule-based tests** (e.g. never repeat a card number). Because the judge proved too generous, we also report a **calibrated score** that limits the score when criteria are not met.

## RESULTS
**Policy accuracy was 5/5:** no invented discounts, vouchers or return rights. The bot correctly refused the mattress return (score 5/5) and escalated the injury case to a human. Tone was polite in all cases.

**Completeness was weak (1/5).** The bot left out the refund timeline, did not suggest medical attention after the injury, and, most importantly, **did not warn the customer against sharing card details or ask for an order number** (also caught by our rule check). It also **over-escalated** simple cases to a human, which would raise your handling costs.

Average score: **4.0 from the judge**, **3.4 after calibration**. Rule checks passed in 4 of 5 cases.

## CAVEATS & LIMITATIONS
These results come from **5 single-turn test cases run once each**, so they show patterns, not reliable percentages; one different answer changes the average noticeably. The same model wrote and judged the replies (possible self-preference bias), and the judge's scores did not always follow its own rubric. We did not test German-language conversations, multi-turn dialogues or repeated runs (consistency). Public benchmark results do not transfer to your policy because of contamination and saturation.

## RECOMMENDATION
**Under these conditions and for this task**, `gpt-4o-mini` is suitable **for a supervised pilot, not yet for autonomous deployment**. Before launch: (1) add an explicit card-data rule and order-number step to the prompt, (2) narrow the escalation instruction to the policy's four cases, (3) re-test on 50+ cases, including German conversations, with human-labelled reference answers. Confidence: **moderate** for safety, **low** for completeness at scale.

## ADDITIONAL METRICS
The full run (5 replies plus 5 judgements) took **18.8 seconds** (about 3.8 s per case), used **5,872 tokens** and cost **about $0.0012**. At 40,000 contacts a month, that is roughly **$10 a month** for replies and judging combined (an estimate), so cost is not the constraint. Quality and human-review time are. Smaller models also mean lower energy use per conversation, which supports a "smallest model that passes" strategy.
