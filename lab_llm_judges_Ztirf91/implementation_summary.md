# Step 11 — Retail chatbot evaluation results

The Python script loaded five cases from the evaluation design and used LangChain to call GPT-4o mini once for the candidate reply and once for the judge verdict per case. Python then checked the exact first line in the two cases with a routing label. The distribution was **three passes and two failures** on automated checks, with a mean score of **0.60** out of 1 and **13 of 15 criteria met**. The full run took **26.93 seconds**, including **13.62 seconds** for judging. All ten calls reported usage, totaling **2,703 input and 860 output tokens**, with an estimated API cost of **$0.00092145**. [Saved results](evaluation_results.json) · [Pricing basis](https://developers.openai.com/api/docs/models/gpt-4o-mini)

| Case | Score | Criteria met | Generation (s) | Judge (s) | Est. cost (USD) | Main finding |
|---|---:|---:|---:|---:|---:|---|
| R01 — Day-30 return | 0/1 | 2/3 | 2.18 | 2.63 | 0.00014835 | Correct eligibility and return steps. Two trailing spaces after `RETURN_ELIGIBLE`. |
| R02 — Late defect | 0/1 | 2/3 | 3.37 | 2.19 | 0.00021495 | Judge accepted the review explanation and open refund outcome. Two trailing spaces after `ESCALATE`. |
| R03 — Missing return details | 1/1 | 3/3 | 2.25 | 2.38 | 0.00014250 | Asked about both delivery date and use before deciding. |
| R04 — Charger compatibility | 1/1 | 3/3 | 3.95 | 3.58 | 0.00026100 | Preserved the 45 W limit, left full-speed compatibility open, and suggested checking laptop specifications. |
| R05 — Delayed parcel | 1/1 | 3/3 | 1.54 | 2.84 | 0.00015465 | Asked for the order number and explained the investigation step. The lab participant judged the acknowledgment of the customer's frustration sufficient. |

Both failures came from exact label matching. Confirm the ticketing system’s input contract before changing the parser. If it accepts trailing spaces, normalize them explicitly and rerun the same checks. If it requires an exact label, use a structured routing field and verify that the downstream system accepts it. In R02, a human should also check whether “we will need to review your case” identifies Support clearly enough, since the judge inferred that connection. This was one response per case, with the same model family generating and grading the replies. The results describe this run and do not establish a production pass rate.
