# Reflection

## 1. What would change if the client's data was in French?
Most benchmarks, including IFEval, LegalBench and BBQ, are English-first. Translated versions lose nuance, may carry translation errors, and can still be contaminated because the originals were in the training data. I would therefore build the test set from real French-language letters and applicant records, written or checked by native speakers, and adapt the rule-based checks: French keywords for the rejection reason, the right complaint body for the market (e.g. a French banking ombudsman instead of Kifid), and a language check.

New challenges: models and LLM judges are generally weaker at judging tone, register and readability outside English. Politeness conventions also differ (vous, formal closings), so an English-trained judge may misjudge what "empathetic" means. To verify quality, I would calibrate the judge on French reference letters scored by native-speaking compliance staff and keep human review on a larger sample than in English.

## 2. "Is this model AGI-level?"
I would answer that this evaluation cannot tell, and that the question does not have a clear meaning yet. "AGI" has no agreed definition or test; it usually refers to broad, human-level ability across almost all tasks. My evaluation measured one narrow task, rejection letters, on five cases.

Answering the question would require evaluations across many domains, novel problems the model has not seen, long-term autonomy and real-world reliability, and even then experts would disagree on the threshold. I would redirect the client to the question that matters for their decision: is the model good enough, safely, for this task, under these conditions? For that I can give an evidence-based answer, with caveats about sample size, contamination and model version changes.

## 3. What could I not evaluate without a human?
Whether a letter is legally sufficient and genuinely fair to a real customer. My own run showed why: the judge marked a correct letter as failing and missed that it implied the customer's file was incomplete, which is a subtle but real compliance and fairness issue. Rule-based checks only find what they are told to look for, and an LLM judge shares the blind spots and biases of the model it evaluates.

In practice, I would have a compliance officer review a random sample of letters (e.g. 5%) plus every case where rule checks and judge disagree, and use their scores to recalibrate the judge over time.
