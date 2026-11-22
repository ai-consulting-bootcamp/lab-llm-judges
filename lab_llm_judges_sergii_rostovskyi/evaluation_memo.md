# Evaluation memo

**To** Northline Home Customer Support Operations  
**From** Sergii Rostovskyi  
**Date** 2026-11-22 (UTC)  
**Subject** Evaluation of the retail support drafting assistant

## Executive summary

I evaluated whether the drafting assistant could answer common support requests accurately, respect store policy, and give customers a clear next step. It passed 2 of 5 synthetic cases in this run. The findings support a larger supervised evaluation before any decision on customer-facing use.

## Methodology

I used five English-language cases covering a return deadline, product compatibility, a discounted refund, a missing parcel, and a repeated complaint. Each case had a fixed policy record and explicit reference requirements. I audited τ-bench Retail, IFEval, and BFCL as proxies and based the measured results on Northline's cases.

GPT-4o mini drafted one answer per case. I checked the structured outcome, refund field, and word limit in Python. GPT-5.4 mini independently graded accuracy, completeness, policy safety, and customer experience with the candidate's identity withheld. A case passed when all exact checks and all four criteria passed.

## Results

The candidate's outcome was correct in 4/5 cases. The numeric refund was correct in 1/1 applicable case(s). The mean judge score was 4.40/5. Only 1/2 anchors matched the expected flags, so judge-dependent results need manual review.

For R01 (return at the deadline), the judge reported: The reply correctly says the unused lamp is still returnable on day 30 and gives the required Orders > Start a return path. It does not claim the return was already opened or add unsupported fees, but it omits that today is the last eligible day, so completeness is not fully met. Across the five cases, the criterion pass counts were accuracy 4/5, completeness 3/5, policy safety 5/5, customer experience 5/5. The candidate was evaluated as a single option, so the results provide no relative ranking.

## Caveats and limitations

Five hand-written cases give limited coverage of real support traffic. Public benchmark exposure creates a possible contamination risk, and near-ceiling performance on simpler benchmark slices can hide differences on tougher cases. Neither proxy rankings nor these case results establish reliability on live policy updates, multilingual requests, or real tool actions.

The rubric constrains the judge's scoring, but tone assessment and paraphrase interpretation can still vary. I ran each case once and used two labeled calibration examples from one scenario. The reported pass rate describes this particular configuration and sample.

## Recommendation

Under these conditions, GPT-4o mini is a candidate for a staff-reviewed drafting trial, with low confidence in generalization. Before enabling customer-facing use, I would ask two support reviewers to label a private holdout of recent cases, track disagreement, and require reliable accuracy on refund amounts and zero unauthorized commitments in that holdout.

## Additional metrics

The evaluation used 8,268 tokens and cost an estimated $0.007810 including calibration. Sequential wall time was 17.25 seconds. The estimate covers API token charges. Energy use and emissions were unmeasured. Comparing those impacts would require provider-side measurements, alongside case quality, rework, and latency.
