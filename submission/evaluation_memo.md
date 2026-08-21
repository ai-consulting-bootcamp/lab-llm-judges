TO: VP of Procurement, Tier-1 Automotive Supplier
FROM: Jay, AI Consulting
DATE: August 21, 2026
SUBJECT: LLM Evaluation Results -- Should-Cost Negotiation-Prep Summarization

EXECUTIVE SUMMARY
We evaluated an LLM-based negotiation-prep summarization layer built on top
of a should-cost engine, focusing on numerical accuracy, hallucination
resistance, and professional tone under five representative scenarios drawn
from real RFQ complexity, including missing data and multi-currency stacks.

METHODOLOGY
Because general-purpose financial benchmarks (FinQA, FinanceBench) are
either too contaminated for a reliable current-model score or don't match
this specific summarization use case, we built five custom test prompts
modeled directly on the should-cost engine's actual data shapes: clean cost
breakdowns, incomplete data, closely-ranked cost drivers, raw-to-professional
tone conversion, and multi-currency/incoterm complexity. Each was scored
using a combination of rule-based numerical checks and an LLM-as-judge
evaluator we designed and calibrated, evaluated on gpt-4o-mini for
cost-realistic deployment conditions.

RESULTS
Across the five test cases, the evaluation produced an average score of 0.8
(min 0.5, max 1.0). Three cases scored a full 1.0: the clean baseline
(Prompt 1), the ambiguous-ranking case (Prompt 3), and the tone-rewrite case
(Prompt 4) -- all correctly handled with no missing-data issues or
fabrication. Prompt 2 (missing freight data) scored 0.5 on this run: the
generated summary correctly acknowledged the missing freight field by name,
but nonetheless derived an implied freight figure from the supplier quote,
which is exactly the fabrication failure mode this evaluation was designed
to catch -- the judge correctly flagged it. Prompt 5 (multi-currency) also
scored 0.5, but for a different reason: the arithmetic was fully correct and
all required data was present, yet the judge penalized the response for not
explicitly narrating its EUR-to-USD conversion step. We assess this as a
judge-side false negative (documented in the Caveats section below), not a
genuine model failure.

CAVEATS & LIMITATIONS
This evaluation used five hand-designed prompts, not a statistically large
sample -- results indicate directional risk areas, not a certified accuracy
rate. The LLM-as-judge carries its own bias: testing confirmed a predicted
tendency to reward explicit hedging language over implicit-but-correct
handling of complete data, which produced at least one false negative
(Prompt 5). Additionally, because response generation used temperature 0.7
to simulate realistic production variance, re-running the evaluation
produces different generated responses each time, meaning scores from
different runs are not directly comparable without controlling for this.
Findings reflect gpt-4o-mini specifically and would need re-validation for
any other model.

RECOMMENDATION
Based on the design and testing framework applied here, under these
conditions and for this specific task, we recommend piloting the
summarization layer with mandatory human review on any output touching
incomplete data or multi-currency stacks, since these are precisely where
both genuine model risk (Prompt 2) and judge-side false negatives (Prompt 5)
appeared. Clean, single-currency, complete-data cases can carry lower-touch
review. Confidence in this recommendation is moderate, reflecting the small
sample size and the documented judge bias.

ADDITIONAL METRICS
The full five-prompt evaluation suite (five generation calls plus five judge
calls) completed in under 40 seconds and at gpt-4o-mini pricing costs a
small fraction of a cent per run, making continuous evaluation economically
trivial relative to the cost of a bad negotiation memo reaching a supplier
conversation.
