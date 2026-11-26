# Reflection (Step 6)

## 1. What would change if the client's data was in French?

The legal content would not change, because the AI Act and the GDPR are the same in every EU language, but the evaluation would. Our reference answers would have to be rewritten in French using the official French legal terms ("système d'IA à haut risque", "analyse d'impact relative à la protection des données"). Translating them automatically risks introducing the very errors we are trying to detect. English benchmarks would be even less useful than they already are.

New challenges: the judge might prefer English-style phrasing or penalise correct French terms it knows less well, and models are generally less accurate in languages with less training data. National guidance also differs (the French CNIL publishes its own recommendations). To verify quality, we would ask a French-speaking legal reviewer to grade a sample and compare her grades with the judge's, and we would add rule-based checks for the key French terms.

## 2. "Is this model AGI-level?"

I would answer that the question cannot be answered with this evaluation, and that it is not the question that matters for the project. "AGI" has no agreed definition or test; it usually means broad human-level ability across almost any task. We measured one narrow task: answering 5 SME questions on two EU laws.

What we can say is: for this task, under these conditions, the model agreed with our reference answers in 5 out of 5 cases, with one minor gap and one error the judge missed. Answering the AGI question would need evaluations across many domains, novel problems, long tasks and real-world outcomes, and even then experts would disagree. I would redirect the client to the questions that drive the decision: is it accurate enough, safe enough and cheap enough for this use, with human review?

## 3. What could not be evaluated without a human?

Whether an answer is legally correct in a situation the reference does not cover. Both the LLM judge and rule-based checks compare the answer with a reference; when the assistant adds something new (like the Article 50 duty in P4), only someone with legal knowledge can say whether it is right, partly right or harmful. Responsibility also matters: if a client acts on the advice, a person must be accountable for it.

In practice, a person with legal training reviews every answer the judge scores 4 or lower, plus a random 20 % of the 5s. She records whether she agrees with the judge, and every disagreement becomes a new reference example to improve the judge.
