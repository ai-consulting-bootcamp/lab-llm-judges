**TO:** NordHome Customer Care Leadership
**FROM:** Nicolò
**DATE:** 20 November 2026
**SUBJECT:** LLM Evaluation Results – Customer Service Chatbot

**EXECUTIVE SUMMARY**
We tested whether gpt-4o-mini can handle NordHome's first-line customer service within your return policy. It handled routine returns, policy refusals and an angry complaint well, but failed the one safety case we tested. Under these conditions, it is not ready to run without human oversight.

**METHODOLOGY**
Public benchmarks (IFEval, TruthfulQA, τ-bench retail) were reviewed and used only for context: they are either saturated, likely seen in training, or don't test your specific policy. We therefore built a custom test of 5 realistic customer messages, from easy to critical: a standard return, a used-mattress return (not allowed), a product question with missing information, an angry damaged-delivery complaint, and a safety incident with a legal threat.

The chatbot (gpt-4o-mini, with your policy and catalogue as instructions) answered each message. A second gpt-4o-mini instance acted as judge, scoring each reply 1–5 against a written correct answer on three criteria: tone, policy accuracy, and no invented promises. Settings were fixed (temperature 0) and each case was run once.

**RESULTS**
Average score was 4.2/5. Four of five replies scored 5/5. The bot applied the policy correctly, refused the used mattress politely, said "I don't know" on warranty rather than inventing one, and declined extra compensation to the angry customer without sounding defensive. No reply invented a promise.

The safety case failed (1/5). When a customer reported that a lamp burned their child, the bot handed over to a human, but did not tell the customer to stop using the lamp and showed no concern. In a real incident this is the most damaging possible failure.

**CAVEATS & LIMITATIONS**
Five cases cannot show reliability: a single run means a different day could give different scores. The same model wrote and graded the replies, which can inflate scores, and the judge was not calibrated against human ratings. It also did not apply its own scoring scale exactly on the safety case. We tested English only, a short fictional policy, and one model. These results describe this set-up, not production performance.

**RECOMMENDATION**
Under these conditions, for this task, we recommend a limited pilot: let the bot draft replies for returns and product questions, with an agent approving them before sending. Safety, injury and legal messages should be routed directly to a human, not handled by the bot. Before wider rollout, we recommend fixing the escalation instructions, testing 50–100 real anonymised tickets, and calibrating the judge with your team's ratings. Confidence: moderate for routine cases, low for edge cases.

**ADDITIONAL METRICS**
Grading took about 2 seconds per reply and cost $0.0011 for all five (about $0.22 per 1,000 graded conversations at current gpt-4o-mini prices; chatbot replies are billed separately). At this cost, automated grading of every conversation is affordable. The real cost driver is the human review needed for the cases the bot cannot be trusted with. Energy use was not measured. Using a small model keeps it low, but it should be tracked once volumes grow.
