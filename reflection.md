# Reflection — NordHome Chatbot Evaluation

## Question 1: What would change if the client's data was in French?

I would not rely on machine-translated benchmarks, because translation adds its own errors. Instead, I would write the test prompts directly in French with a native speaker, using real phrasing from NordHome's French tickets: "tu" vs. "vous", regional expressions, typos, and French-English mixing.

The rule-based checks would need rewriting ("6,95 €", "5 à 7 jours ouvrés"), and politeness norms differ: "tu" with an unknown customer can come across as rude. The LLM judge is also likely less reliable in French, so I would calibrate it again with replies scored by a French-speaking customer-care agent.

## Question 2: Your client asks "is this model AGI-level?" — how do you respond?

I would say this evaluation can't answer that, and it isn't the right question for their decision. "AGI" has no agreed definition or test. We measured something narrow: how one model handles five NordHome situations, under one policy, at one point in time.

I would bring the discussion back to what matters: does the bot follow the policy, avoid inventing facts, and always escalate safety cases? Even a perfect score would mean "fit for this task, under these conditions". Thinking of it as "AGI-level" could lead the client to give it too much freedom, such as approving refunds alone.

## Question 3: What is the one thing you could not evaluate without a human?

Whether a reply is safe to send in a legal or safety situation, like the lamp that burned a child. A rule can check the escalation phrase and an LLM judge can check tone, but neither can reliably judge whether a sentence could be read as admitting fault, or whether it feels right to a worried parent. That depends on legal context and company risk appetite, and a mistake is very costly.

In practice, a customer-care lead (and legal, for the first version) would review every escalation reply during testing. In production, all safety and legal conversations would go straight to a human, and a weekly human spot-check of other conversations would catch what automated checks miss.
