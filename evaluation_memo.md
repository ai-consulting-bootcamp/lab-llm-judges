TO: Retail Client Stakeholder
FROM: [Your Name]
DATE: August 24, 2026
SUBJECT: LLM Evaluation Results — Retail Customer Service Chatbot (Complaint Handling)

# EXECUTIVE SUMMARY
We evaluated a candidate LLM-based customer service chatbot on its ability to handle
frustrated-customer complaints — specifically, whether responses de-escalate the
situation, acknowledge the customer's frustration, and offer a concrete, policy-consistent
resolution. This memo reports results from a custom LLM-as-judge evaluation designed
for this use case, since no existing public benchmark adequately tests tone and
policy-grounded resolution together in a retail complaint context.

# METHODOLOGY
We designed 5 custom evaluation prompts spanning basic policy lookups, conditional
edge cases, ambiguous multi-intent requests, adversarial policy-bending attempts, and
tone-sensitive complaint scenarios. This memo focuses on the complaint/de-escalation
case, evaluated using an LLM-as-judge (gpt-4o-mini) scoring three criteria: empathy/
acknowledgment, concrete resolution, and tone appropriateness, on a 1-5 scale.

We audited 3 existing academic benchmarks (MultiWoz, ABCD, EchoMind) beforehand and
found none directly applicable — MultiWoz and ABCD are dialogue-state-tracking datasets
without a tone/empathy scoring dimension, and EchoMind evaluates audio-based emotional
cues, not text. This justified building a custom evaluation rather than reusing an
off-the-shelf benchmark.

We tested 4 hand-crafted response variants against the same frustrated-customer message
(a "good" response hitting all three criteria, plus three flawed variants: generic/
deflecting, empathetic-but-no-resolution, and policy-correct-but-dismissive) to confirm
the judge could reliably discriminate response quality before wider deployment.

# RESULTS
Average score across the 4 test cases was 2.25/5. The judge correctly distinguished
quality: the well-constructed response scored 5/5 (all three criteria met), while the
three flawed responses scored 1-2/5. Criteria-level pass rates were: empathy/
acknowledgment 2/4, concrete resolution 1/4, tone appropriateness 2/4 — resolution was
the criterion most often missed, suggesting that responses in this test set were more
likely to sound sympathetic than to actually offer a concrete fix. One notable finding:
the "dismissive" response did technically state the correct refund/replacement policy,
yet was still scored as failing "concrete resolution" — indicating the judge's
assessment of resolution may be influenced by tone rather than being fully independent,
which we flag as a calibration issue to address (see Caveats).

# CAVEATS & LIMITATIONS
This evaluation used a single LLM judge, which carries known biases — notably a
tendency to favor longer, more elaborately worded empathy over concise but sincere
responses, and in this run, an apparent tendency to conflate "resolution" with "tone"
rather than scoring them independently. Results are based on a small custom test set
(4 examples) and have not been validated against human ratings; before production
deployment, we recommend a larger, human-annotated sample to confirm judge calibration
and correct the resolution/tone conflation observed here. These results reflect
performance under these specific prompts and this specific policy configuration; they
should not be generalized to all complaint types or to other LLM providers/versions
without re-testing.

# RECOMMENDATION
Under these conditions, for this specific complaint-handling task, the evaluation
approach itself works well — the judge reliably separated good from flawed responses.
However, we do not yet have enough real chatbot outputs evaluated to make a model
deployment recommendation; we recommend running this judge against a larger sample of
actual model-generated responses (not hand-crafted variants) before drawing conclusions
about production readiness, with moderate confidence in the judge's discriminative
ability and lower confidence in generalizing from this 4-case pilot.

# ADDITIONAL METRICS
Average judge evaluation time was approximately 1.8 seconds per case, with total cost
of $0.000534 for all 4 evaluations (roughly $0.00013/case) using gpt-4o-mini at current
pricing. At this rate, evaluating a sample of 100 real complaint transcripts weekly
would cost approximately $0.013/week — negligible, making this approach highly viable
for ongoing production quality monitoring at scale.