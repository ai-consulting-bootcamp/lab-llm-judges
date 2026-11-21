# Reflection · Kleinanzeigen buyer-support chatbot

**Author:** Ayhan Demir · **Date:** 2026-11-20

## 1. What would change if the client's data was in French?
Most public benchmarks are English-first. τ-bench 2.0 ships six languages (English, Spanish, Portuguese, Hindi, Chinese, Korean) but not French, and IFEval and CoCoNot are English only. I would translate my own test prompts, have a native speaker fix them, and add French rule checks: reply language, euro formatting such as "5,00 €", and the formal "vous".

New challenges: translated prompts sound unnatural, the policy itself must exist in French, and models and judges are usually weaker outside English, so the judge could be harsher or more lenient on French replies. To verify quality, I would calibrate the judge separately on French reference replies and check it against a French-speaking agent on a sample, instead of trusting the English calibration.

## 2. "Is this model AGI-level?"
"AGI-level" has no agreed definition, and the target keeps moving: once a human-level score is reached, the definition tends to change. What I can say is much narrower: on five Kleinanzeigen buyer questions, under these conditions, the model scored what the memo reports. That says nothing about general intelligence.

Answering the question would need broad evaluations across reasoning, knowledge, tool use and novel problems (for example ARC-AGI-3), and even those only show performance on their own tasks. I would bring the conversation back to the business question: is it reliable enough for this support task, at what cost, and with which guardrails?

## 3. The one thing I could not evaluate without a human
Whether a reply actually resolves the situation for this customer: whether an angry buyer who lost 250 € feels taken seriously and trusts the next steps. The judge can check facts against the policy, and rules can check language and length, but neither knows how the message lands with a real person. The judge's idea of "empathetic" is itself an assumption (see the bias analysis).

In practice, Kleinanzeigen team leads would label a weekly sample of real replies PASS or FAIL with a short reason. I would compare those labels with the judge (agreement, recall of bad replies), and every disagreement would become a new calibration example. Customer signals such as reopen rate or satisfaction scores would complement these labels, not replace them.
