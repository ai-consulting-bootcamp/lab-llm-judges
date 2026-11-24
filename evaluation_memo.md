TO: ShopCo Customer Support Manager
FROM: Sandra
DATE: 24 November 2026
SUBJECT: Evaluation of ShopCo Replies and an LLM Judge

## Executive Summary

We tested five customer support replies against ShopCo's fictional
policy. Human review accepted four replies, but the automated judge
agreed with only three of the five human verdicts. Under these
conditions, we recommend keeping human review before using this
judge for automatic quality decisions.

## Methodology

We reviewed IFEval, Tau-bench, and MT-Bench to inform our approach.
We adapted ideas from their methods rather than running the official
benchmarks. Our custom cases covered a normal return, a refund
requiring approval, policy limits, missing information, and a complaint
with an unknown product feature.

We used the OpenAI API directly. Both the response model and judge
returned version gpt-4o-mini-2024-07-18. The judge assessed accuracy,
completeness, and tone. All three criteria had to pass. Sandra reviewed
the cases, references, and generated replies with AI assistance.
Her labels were recorded before the main judge evaluation.

## Results

Four of five generated replies passed human review (80%). The failing
reply assumed that return instructions were included with the order,
although this information was not provided. The judge accepted two
replies (40%) and agreed with three human verdicts (60%).

With FAIL as the positive class, detection precision was 33.3%,
recall was 100%, and F1 was 0.50. The judge rejected two acceptable
replies. For one reply, it claimed that human approval was not
mentioned, although it was explicitly stated. It also matched the
human FAIL label on another reply but gave an incorrect explanation.

## Caveats and Limitations

The judge matched all three calibration verdicts after a prompt
adjustment, but these examples were used to improve the instructions.
They were not an independent validation set. The main evaluation
contained only five synthetic cases and one generated reply per case.
The 100% recall was based on a single failing reply.

Public benchmarks may have training overlap, and current saturation
was not established for all reviewed benchmarks. Our original cases
do not remove possible training overlap with similar tasks.
Model outputs can vary across runs. Using the same model for writing
and judging may introduce bias, and AI-assisted human labels are
not independent expert annotations.

## Recommendation

For these tasks and conditions, the judge is suitable for a limited
experiment with human oversight. It should not automatically approve
or reject customer replies. We recommend independent human labels,
more difficult cases, and checks for unsupported judge explanations.
Confidence in broader performance is low.

## Additional Metrics

The main run used 9,649 tokens. API call durations totalled
20.19 seconds. Estimated cost was USD 0.00193290, using official
prices checked on 24 November 2026. These figures exclude calibration
and human review time. Energy consumption and carbon emissions were
not measured, so no environmental impact estimate is provided.