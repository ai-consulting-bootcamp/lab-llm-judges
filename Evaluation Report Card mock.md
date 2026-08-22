TO: Clinical Development Leadership

FROM: Nevena Zujko

DATE: 21 August 2026

SUBJECT: LLM Evaluation Results – Clinical Trial Eligibility Screening Assistant

## EXECUTIVE SUMMARY

We evaluated an LLM-based Clinical Trial Eligibility Screening Assistant designed to assess patient records against trial inclusion and exclusion criteria. The evaluation focused on criterion-level accuracy, completeness, evidence grounding, correct handling of missing information, and avoidance of unsupported enrollment decisions.

## METHODOLOGY

The evaluation combined existing benchmark evidence with a custom mini-benchmark tailored to the intended use case. Three relevant external benchmarks were reviewed: TrialGPT criterion-level matching, TREC Clinical Trials 2022, and the SIGIR 2016 Patient–Clinical Trial Matching Collection. These benchmarks were useful for understanding patient–trial matching performance but did not fully match our criterion-level MET / NOT MET / UNKNOWN task, so a custom evaluation was required.

Five synthetic test cases were designed to cover clear inclusion criteria, exclusion criteria, missing clinical information, multi-criterion screening, and ambiguous clinical evidence. Ground-truth classifications were defined in advance. Simple cases were verified using rule-based checks, while more complex cases were evaluated using an LLM-as-judge with explicit criteria for accuracy, completeness, grounding, consistency, and decision boundaries.

For this design-stage memo, the quantitative results below are illustrative and will be replaced by the actual metrics generated during implementation.

## RESULTS

The candidate model performed well on straightforward criteria where the relevant information was explicitly stated in the patient record. It also correctly handled most missing-information cases by returning UNKNOWN rather than inferring unavailable clinical information.

Performance was weaker on cases involving several simultaneous eligibility criteria and ambiguous clinical wording. The main observed failure pattern was overinterpretation of uncertain information, particularly where the patient record suggested but did not confirm a clinical condition.

Illustratively, the model achieved an average judge score of approximately 4/5 across the five cases, with lower scores concentrated in the more complex and ambiguous examples.

## CAVEATS & LIMITATIONS

The evaluation dataset is small and synthetic and therefore cannot establish real-world clinical performance. Public benchmarks may also carry contamination or saturation risks, and none exactly replicate the intended system workflow. LLM-as-judge evaluation itself can introduce variability and bias, particularly when assessing ambiguous medical language.

These results should therefore not be interpreted as evidence that the model is safe for autonomous eligibility determination.

## RECOMMENDATION

Under the tested conditions, the model appears suitable for further evaluation as a decision-support tool, but not for autonomous patient enrollment decisions. Confidence in this recommendation is moderate because the evaluation set is small and does not yet include real-world clinical diversity.

## ADDITIONAL METRICS

The implementation phase should additionally track latency, token usage, API cost per screening case, and evaluation time. These metrics should be considered alongside quality scores when deciding whether the system provides sufficient operational value for broader testing.