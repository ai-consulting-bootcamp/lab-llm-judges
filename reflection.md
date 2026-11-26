# Reflection

## 1. What would change if the client's data was in French?

Most public benchmarks would become even less useful. IFEval, TruthfulQA and FinanceBench are English-first, and translated versions lose cultural context and add translation errors that the model then gets blamed for. I would build the test set natively in French from real (anonymised) letter templates and reason codes rather than translate the English one. The regex layer would need to be rewritten completely, not translated: forbidden-term lists for protected characteristics have to cover French grammar (gender and plural forms, e.g. "âgé/âgée/âgés") and French legal wording, and required patterns change too (e.g. "taux d'endettement" instead of "debt-to-income").

New challenges: the judge's English bias gets stronger. It may grade French politeness formulas ("Nous vous prions d'agréer…") as stiff, or fail to notice wrong register, such as "tu" instead of "vous". Model quality also varies more by language, so a model that is fine in English may make grammar or terminology errors in French. Verification would rely more on native-speaker review: a French-speaking credit officer rates a sample, the judge is calibrated against those ratings, and the judge prompt itself is written and tested in French.

## 2. "Is this model AGI-level?"

I would say that this is not a question this evaluation can answer, and that it is not the decision they need to make. "AGI-level" has no agreed definition or test. It usually means human-level performance across almost all cognitive tasks, while we tested one narrow task with 5 cases. A model can write excellent rejection letters and still fail at basic planning, arithmetic or anything outside its training distribution.

To say anything about general capability you would need broad, uncontaminated, regularly refreshed evaluations across reasoning, knowledge, planning, tool use and long-horizon tasks, plus comparison with human experts. Even then, experts disagree on what would count. The caveat I would put in writing: our results mean "under these conditions, this model performs well enough on this task for supervised use", nothing more. The useful version of their question is "can we trust it with this process, and with what controls?", and that is what the evaluation answers.

## 3. The one thing I could not evaluate without a human

Whether the letter is fair and appropriate for this specific person. The rules can check that no protected word appears, and the judge can check tone against a rubric. Neither can judge whether, for an applicant who wrote about medical bills for her father, the letter strikes the right balance between honesty and compassion, or whether a reason is legally sufficient under the bank's actual obligations. That takes contextual judgment, accountability and knowledge of what customers and regulators actually react to. An LLM judge has none of these, and it shares the blind spots of the model it is grading.

In practice I would keep a credit officer as the final reviewer of every letter during the pilot, have officers rate a random sample each week on the same rubric, and use those ratings to recalibrate the judge and expand the test set. Disagreements between officer and judge are the cases most worth adding to the benchmark.
