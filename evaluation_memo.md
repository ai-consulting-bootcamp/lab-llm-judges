# LLM Evaluation Memo — MNM AG

**TO:** MNM AG Management  
**FROM:** AI Evaluation Consultant  
**DATE:** 20 November 2026  
**SUBJECT:** Preliminary Evaluation of the Vendor Management AI Assistant

## Executive Summary

This memo presents a proposed evaluation of MNM AG's fictional Dynamics 365 Finance & Operations Vendor Management AI Assistant. The assessment focuses on factual correctness, adherence to company policies, completeness and prevention of unsupported financial guidance. The results described below are illustrative and will be replaced with actual measurements after implementation.

## Methodology

The evaluation design draws on three 2025 benchmarks: EKRAG for enterprise knowledge grounding, IFBench for instruction following and GroUSE for assessing LLM-judge reliability. These benchmarks inform the evaluation approach; their original datasets have not been executed against the MNM AG assistant.

Five custom test cases cover vendor creation, legal-entity restrictions, payment terms, bank-detail changes and unavailable vendor information. Each case includes a defined ground truth and verification method. An LLM judge will assess generated responses against three criteria: accuracy, policy compliance and safety/groundedness, using a five-point scoring rubric. Rule-based checks will supplement the judge where appropriate.

## Results — Illustrative Only

The planned evaluation is expected to reveal whether the assistant can provide accurate procedural guidance and correctly handle company-specific information. Particular attention will be given to answers involving bank-detail verification and unavailable financial data, where unsupported recommendations could create significant business risks.

For reporting purposes, a hypothetical score of 4/5 would indicate a generally correct response with minor omissions, while a score of 1/5 would indicate an incorrect or unsafe response. These are examples of scoring interpretation, not measured model performance. Actual scores, criteria results and execution times will be recorded during the Python evaluation.

## Caveats and Limitations

The evaluation uses five synthetic cases based on fictional company policies. Consequently, the results cannot establish production readiness, regulatory compliance or reliability across all Dynamics 365 F&O workflows.

Although newer benchmarks were selected to reduce potential exposure to older public test datasets, contamination cannot be ruled out. LLM judges may also demonstrate scoring inconsistencies, style preferences or unsupported domain assumptions. Repeated testing and human review would improve confidence.

## Recommendation

MNM AG should proceed with a limited technical evaluation rather than immediate production deployment. Under the defined fictional conditions, the proposed framework provides a reasonable starting point for identifying answer-quality and safety risks. Confidence in operational suitability remains low until the test cases have been executed and the findings independently reviewed.

## Additional Metrics

Beyond response quality, the implementation should measure evaluation latency, token consumption and estimated API costs. These indicators will help assess whether automated evaluation is practical and cost-effective. Environmental impact may be discussed qualitatively, but precise emissions should not be claimed without suitable measurement data.