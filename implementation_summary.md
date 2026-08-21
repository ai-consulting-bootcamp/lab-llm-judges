# Implementation Summary

## What I built

I implemented the tone judge from Step 4 as a Python function that takes a
decision record and a draft letter and returns a structured JSON verdict:
a 1 to 5 score, per-criterion booleans, the quoted decline sentence, and
the weakest criterion. The judge runs on gpt-4o-mini at temperature 0,
using response_format json_object to keep output parseable, wrapped in
try/except so a malformed response is recorded as a failed evaluation
rather than crashing the run.

The judge does not act alone. A set of deterministic checks runs first and
handles everything a rule can verify: whether the correct decline reason
appears, whether any forbidden reason leaks in, whether the bureau
reference matches the record, whether the manual review right is stated,
and whether the letter stays under 300 words. The judge is reserved for
tone, which no rule can capture. This split is the core design decision:
using a model to check a string match would add cost and variance for no
gain.

I tested five hand-written cases, one per evaluation prompt from Step 3.
Three are clean and two carry planted faults, so I could check whether the
system detects known defects rather than only producing plausible numbers.

## Key findings

The separation held end to end. Mean judge score was 4.2 across five cases,
but the mean is the least interesting number. What matters is that the
judge scored the planted tone case (TC3, warm but condescending and
promising a better future outcome) a 2, flagging both non_condescension
and no_false_hope as failed. The same-family style bias I predicted in the
bias analysis did not appear at this scale, which I note as an observation,
not a guarantee.

The two compliance-fault cases (TC4 asserting a bureau contribution that
did not occur, TC5 inventing a reason for an empty field) both scored high
from the judge, 5 and 4, because their tone was fine and the judge was told
to ignore accuracy. The deterministic gate caught both, giving a gate pass
rate of 0.6, exactly the three clean cases. This is the intended behaviour:
rules catch factual faults, the judge catches tone, and neither
double-counts the other.

The clearest limitation is TC5. It still scored 4 on tone despite inventing
a decline reason, which means the judge score alone would be dangerously
misleading on the single most important failure mode in the scenario. The
gate is what makes the system safe there, not the judge. Cost and latency
were negligible: about $0.001 total and 2.98 seconds per evaluation across
5 calls, so cost is not a constraint on running this more often or on
repeating each case to measure judge variance, which is the first thing I
would add next.