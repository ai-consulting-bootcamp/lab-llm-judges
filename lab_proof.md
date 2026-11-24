# Lab Proof — LLMs Grading LLMs with Receipts

## Scenario and Goal

ShopCo is a fictional online retailer.
We evaluated customer support replies against a fictional policy
and checked whether an LLM judge agreed with human-reviewed labels.

## Implementation

- Code: [Evaluation notebook](llm_judge_evaluation.ipynb)
- Design and policy: [Evaluation design](evaluation_design.md)
- Benchmark review: [Benchmark audit](benchmark_audit.md)
- Approach: OpenAI API directly.
- Response and judge model returned by the API:
  `gpt-4o-mini-2024-07-18`.
- Main judge prompt version: `shopco-v2`.
- Criteria: accuracy, completeness, and tone.
- PASS requires all three criteria to be true.

## Example Run — SHOP-02

### Input

Current date: 2026-12-01.

The customer received order SC-102 on 2026-11-21.
The product is unused, has its original packaging, and cost EUR 150.
The customer asks whether they will get their money back.

### Expected Behaviour

The reply should explain that the product meets the return
conditions, but the refund requires human approval.
It should provide a next step without guaranteeing approval.

### Generated Output

The reply included:

> However, because the cost of the product is EUR 150,
> human approval is required for the refund process.

It also recommended contacting customer support.

The full reply is saved in
[generated_responses.json](generated_responses.json).

### Human Review and Judge Evidence

Sandra accepted the reply after AI-assisted review:
accuracy, completeness, and tone were all true.

The judge returned FAIL with accuracy false.
Its explanation incorrectly said that the reply did not clarify
the human approval requirement.

The saved API input was inspected and contained the correct
policy, case, reference, and complete candidate reply.
The approval requirement was explicitly present in that reply.

- Human labels: [human_review.json](human_review.json)
- Judge output and saved input:
  [evaluation_results.json](evaluation_results.json)

## Main Results

| Measure | Result |
|---|---:|
| Cases | 5 |
| Human-reviewed response pass rate | 4/5 — 80% |
| Judge response pass rate | 2/5 — 40% |
| Judge–human verdict agreement | 3/5 — 60% |
| FAIL detection precision | 33.3% |
| FAIL detection recall | 100% |
| FAIL detection F1 | 0.50 |
| Generation tokens | 2,679 |
| Judging tokens | 6,970 |
| Sum of API call durations | 20.19 seconds |
| Estimated main-run cost | USD 0.00193290 |

FAIL is the positive class for precision, recall, and F1.
Recall is based on only one human-labeled failing reply.
Time and cost exclude calibration and human review.

## Calibration and Failures

- [Calibration v1](calibration_v1_results.json):
  2/3 verdicts agreed with human labels.
- [Calibration v2](calibration_v2_results.json):
  3/3 verdicts and criteria agreed after clarifying instructions.

The v2 explanation for CAL-02 still included an unsupported claim.
In the main run, the judge incorrectly rejected SHOP-02 and SHOP-03.
For SHOP-01, it matched the human FAIL label but gave an incorrect
explanation instead of identifying the unsupported assumption
about return instructions.

We preserved these results and did not adjust the judge again
using the main cases.

## Final Output and Recommendation

The pipeline produced structured results and aggregate metrics.
However, the judge is not reliable enough for automatic decisions
under these test conditions. Human review remains necessary.

Five synthetic cases, AI-assisted human labels, and the same model
for generation and judging limit the conclusions.
The experiment does not establish production reliability.

## Supporting Documents

- [Implementation summary](implementation_summary.md)
- [Client evaluation memo](evaluation_memo.md)
- [Reflection](reflection.md)

## AI Assistance

AI helped draft documents, code, and proposed review labels.
Sandra reviewed the five cases, references, calibration examples,
and main response labels. Judge explanations were checked against
the actual replies. Reported metrics come from the recorded runs.

## Optional Extensions

The two-model comparison, classmate evaluation, extended
10-example calibration study, and judge cost comparison
were not performed.