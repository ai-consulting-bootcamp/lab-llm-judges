# Evaluation memo — Retail customer support chatbot

**To** Retail Customer Operations<br>
**From** AI Evaluation Consultant<br>
**Date** 21 November 2026<br>
**Subject** Pilot evaluation and release recommendation<br>
**Status** Simulated results for the lab. No model was run for this memo.

## Executive summary

We designed a five-case evaluation to assess whether the chatbot applies store policy, handles missing information, and gives customers an appropriate next step. In the simulated results, the chatbot passed four cases and failed a critical policy check by guaranteeing a refund before Support reviewed the defect.

## Methodology

The test set covers a return on day 30, a defect outside the standard return window, a return request with missing details, uncertain product compatibility, and a complaint about a delayed parcel. We adapted the policy-based case design of τ-bench Retail and the programmatic output checks of IFBench. The cases use fictional store rules and catalog information.

The simulated pilot assumes one candidate, GPT-4o mini, with one response per case. The grading design uses code for exact routing labels, a reference-based LLM judge for policy and next steps, and human review for the complaint’s tone. A case passes when it meets all required criteria.

## Results

The illustrative case pass rate was 4/5 (80%). The chatbot handled the day-30 deadline, asked for missing return details, avoided guaranteeing full-speed charging, and gave the customer a next step for the delayed parcel.

In the failed case, the chatbot used the correct escalation label and referred the customer to Support. It also guaranteed a refund even though the policy reserves that decision for Support. That is one critical failure in five simulated cases. The aggregate pass rate alone would obscure it.

## Caveats and limitations

Five English-language cases cannot establish a production error rate. The design tests text replies and routing labels. It leaves actual order-system actions, multilingual coverage, and sustained dialogue for follow-up testing. Repeated runs and human checks of borderline judgments would help assess reproducibility.

Public benchmark examples may overlap with model training data, and scores on familiar tasks can cluster among strong models. We use those benchmarks to inform the test design. The extent of any exposure is unknown.

## Recommendation

Under the simulated conditions, defer customer-facing use for refund decisions until the chatbot consistently leaves the outcome open pending Support review. Retest the revised version on the same cases and add variants covering indirect promises and premature denials. Confidence in the recommendation is limited until a real run establishes whether the failure occurs.

## Additional metrics

In the actual run, record response and judge latency, input and output tokens, and estimated API cost separately. Compare these metrics across revisions to see whether quality improvements add customer wait time or operating cost. Estimating environmental impact would also require energy and emissions data. This memo contains no measured cost, latency, token use, or environmental impact.
