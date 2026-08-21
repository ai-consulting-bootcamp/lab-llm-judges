## Step 5, Evaluation Memo

TO:      Head of Retail Credit Operations, Nordbank
FROM:    Gordan Skopljak, External Evaluation Consultant
DATE:    21st AUG 2026
SUBJECT: LLM Evaluation Results, Automated Loan Rejection Letters

EXECUTIVE SUMMARY

We built and tested an evaluation system for rejection letters drafted from
your structured decision records. Rather than testing a live drafting
model, we ran the evaluation against five fixed sample letters chosen to
carry specific faults, so we could confirm the system detects known
defects. It correctly passed the three clean letters and caught both
planted faults: one letter that referenced a credit bureau not used in the
decision, and one that invented a decline reason for a record where the
reason field was empty. We recommend a supervised pilot, not unsupervised
deployment.

METHODOLOGY

Public benchmarks were audited first and rejected as a basis for this decision. The widely cited general-capability tests measure multiple choice knowledge, not regulated document generation, and their published scores are difficult to separate from training data contamination. A strong public score would not have told you whether a letter is safe to send.

We therefore built a custom evaluation of five test cases drawn from your own decision record format. Two are verified by code, checking that the correct reason appears, that no other reason appears, that the manual review right and the bureau reference are present where required, and that the letter stays under 300 words. Two are scored by a second language model acting as a judge, assessing tone against a fixed rubric. One case supplies a deliberately incomplete record to test whether the model flags the gap or invents a reason to fill it.

This round tested the evaluation system itself, not a live drafting model.
The five letters were fixed samples, hand-written to carry specific faults,
so we could verify the system detects known defects rather than confounding
drafting quality with evaluation quality. The tone judge ran on gpt-4o-mini
at temperature 0. A production evaluation would add a drafting model and
generate letters live; that is the natural next step.

RESULTS

Deterministic checks are the reliable part of these findings. All three
clean letters passed the full gate: correct reason present, no forbidden
reason, bureau reference matching the record, manual review right stated,
under 300 words. The two fault letters failed the gate as intended, one for
referencing a bureau the record said was not used, one for stating an
income reason the record did not contain. The incomplete-record case is the
one to watch: the letter invented a plausible income reason for an empty
reason field, and only the deterministic gate caught it. A model that
invents a plausible reason when a field is empty is not usable at any
volume, because the failure is invisible to the reviewing officer.

Tone scores averaged 4.2 out of 5. The judge scored the one deliberately
condescending letter a 2, correctly, and rated the compliance-fault letters
highly on tone because their wording was in fact courteous. This is the
intended division of labour: the judge assesses tone and the gate assesses
fact, and a high tone score on the incomplete-record letter is exactly why
tone scores must never be read on their own. Treat these numbers as
directional only.

CAVEATS AND LIMITATIONS

We cannot certify compliance. Our checks confirm that specific required elements are present; whether the resulting letter satisfies your regulatory obligations is a legal determination and remains with your compliance function. The tone scores come from a model that shares training data with the model it grades, so it tends to reward text that sounds like generated text, and we have not yet validated it against human raters.

Scope is five cases in one language. Rare decline reasons, joint applications, and multi-product records are untested. Results are not guaranteed to reproduce across model versions, since a silent vendor update can change behaviour without notice.

RECOMMENDATION

Under these conditions, for this task, we recommend a supervised pilot on a single decline reason with 100 percent human review and the automated checks running as a hard gate before any draft reaches an officer. Confidence: moderate on the deterministic findings, low on tone.

ADDITIONAL METRICS

Evaluation cost was approximately USD 0.001 for 5 judged calls, averaging
2.98 seconds per evaluation. That figure is negligible and should not drive
any decision. At production volume the dominant cost is not inference but
the human review time the pilot requires, which is the figure to model
before committing.
