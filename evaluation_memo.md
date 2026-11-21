# Client Evaluation Memo

**TO:** VP of Retail Lending & Chief Compliance Officer, Meridian Community Bank  
**FROM:** Senior AI Evaluation Consultant  
**DATE:** November 21, 2026  
**SUBJECT:** LLM Evaluation Results — Automated Adverse Action Loan Letters  

---

### EXECUTIVE SUMMARY
We designed a targeted evaluation pipeline to assess whether `gpt-4o-mini` can draft factually accurate, empathetic, and ECOA/FCRA-compliant adverse action letters directly from structured underwriting records. Because public benchmarks proved either mismatched or heavily saturated, we built a custom 5-scenario regulatory test suite combining deterministic compliance rules with a 4-criterion LLM-as-judge rubric. The checked-in results are from a deterministic offline simulation of candidate and judge responses; they validate the pipeline mechanics but are not independent evidence of live model performance.

### METHODOLOGY
Our benchmark audit reviewed **IFEval**, **FinQA**, and **TruthfulQA** against Meridian's lending requirements. We rejected FinQA (corporate 10-K arithmetic) and TruthfulQA (general-knowledge trivia) and adapted IFEval's programmatic constraint-checking approach into deterministic regex guardrails for mandatory statutory notices and prohibited terms. We then constructed five domain-specific evaluation scenarios covering standard bureau-backed denials, internal-only denials with no credit pull, noisy underwriter notes containing protected-class attributes, conditional counteroffers, and incomplete-application closures. The live path generates candidates with `gpt-4o-mini` (`temperature=0.2`) and evaluates them with a compliance-gated `gpt-4o-mini` judge (`temperature=0.0`); the checked-in artifact uses the offline fixtures.

### RESULTS
Across the five offline fixture scenarios, the simulated judge produced a mean score of **4.0 / 5.0** (median `5.0`, range `2` to `5`), passing all four rubric criteria on **3 of 5 cases (`60%`)**. The fixtures exercise two high-risk failures: on `TC-03`, the candidate echoes `"fixed pension"` from a raw underwriter note and triggers the prohibited-term guardrail; on `TC-04`, the candidate includes forward-looking language implying future approval. A live API run is required before treating these values as model-performance results.

### CAVEATS & LIMITATIONS
These results reflect a compact 5-case diagnostic pilot and cannot be interpreted as a statistical guarantee of zero fair-lending violations across all retail loan products. Public LLM benchmarks suffer from training-data contamination and score saturation, and even custom LLM-as-judge evaluations exhibit self-preference bias and sensitivity to prompt wording. Furthermore, an automated judge cannot verify live regulatory changes or substitute for formal legal sign-off by Meridian's compliance counsel.

### RECOMMENDATION
Once confirmed by a live, adequately sampled evaluation and legal review, we would consider advancing `gpt-4o-mini` to a **human-in-the-loop staging pilot** for first-draft generation only, with confidence limited by the current simulation evidence. Any customer-facing use should require: (1) upstream redaction of free-text underwriter notes so only structured ECOA-approved reason codes reach the LLM, and (2) synchronous regex plus LLM-as-judge pre-screening that routes any letter scoring below `4/5` or triggering a prohibited-term flag to a compliance specialist.

### ADDITIONAL METRICS
Beyond rubric accuracy, the offline artifact reports **8.54 seconds** total simulated evaluation time, **5,748 total tokens** (`4,979` input / `769` output), and an estimated cost of **$0.001209 USD** under the configured pricing assumptions. These are fixture telemetry values, not observed live service metrics. Production cost, latency, and environmental impact must be measured from actual traffic and current provider data.
