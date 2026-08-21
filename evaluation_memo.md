# Evaluation Memo — TenderAI

**TO:** Client — Engineering & Consulting Company  
**FROM:** AI Evaluation Consultant  
**DATE:** August 21, 2026  
**SUBJECT:** LLM Evaluation Results — TenderAI RAG Assistant

## EXECUTIVE SUMMARY

This evaluation assessed a TenderAI-style Retrieval-Augmented Generation (RAG) assistant using a custom five-case evaluation focused on evidence grounding, compliance judgment, instruction following, and contradictory evidence handling. Across the five test cases, the LLM-as-judge produced an average score of 3.60/5, with results ranging from 2/5 to 5/5. The results indicate strong performance on straightforward evidence-based tasks but weaknesses in multi-document reasoning and contradictory evidence handling.

## METHODOLOGY

The evaluation strategy combined an audit of three existing benchmarks with a custom evaluation designed specifically for the TenderAI use case. MMLU was reviewed as a general knowledge and reasoning benchmark, IFEval as an instruction-following benchmark, and RGB as a RAG-focused benchmark. These benchmarks provide useful contextual signals but were not treated as direct measures of TenderAI production readiness.

The custom evaluation contained five test cases covering evidence sufficiency, evidence-based project identification, multi-document reasoning, instruction following, and contradictory evidence. An LLM-as-judge using `gpt-4o-mini` evaluated each response against evidence grounding, correct compliance judgment, hallucination avoidance, and explanation quality. Evaluation time and token usage were also recorded.

## RESULTS

The five test cases produced an average score of **3.60/5**, with a minimum score of **2/5** and a maximum of **5/5**. T1 Evidence Sufficiency and T2 Evidence-Based Project Identification both received 5/5, indicating strong performance on straightforward evidence-grounded tasks. T3 Multi-Document Reasoning and T4 Instruction Following each received 3/5.

The most significant weakness appeared in T5 Contradictory Evidence, which received **2/5**. The candidate response relied on a 120 MW figure from one document while failing to acknowledge conflicting evidence stating 48 MW. For a tender-analysis system, this is an important failure mode because conflicting evidence should be identified and verified before a compliance claim is made.

The complete evaluation took **11.086 seconds** and used **2,155 total tokens** across the five judge evaluations: 1,658 input tokens and 497 output tokens.

## CAVEATS & LIMITATIONS

This evaluation contains only five deliberately designed test cases and therefore cannot establish production-level accuracy or general model performance. The results should be interpreted as diagnostic evidence about the tested behaviors rather than as a definitive performance estimate.

LLM-as-judge evaluation can introduce evaluator bias and variability. Benchmark contamination and saturation can also affect comparisons with public benchmarks. Larger test sets, calibration examples, repeated evaluations, and human evaluation would be required before making a high-confidence production decision.

## RECOMMENDATION

Under these evaluation conditions, TenderAI should prioritize models and system configurations that demonstrate reliable evidence grounding and, particularly, robust handling of insufficient and contradictory evidence. The current results do not justify a production-readiness claim. Confidence in any model recommendation should remain **moderate to low** until the evaluation is expanded with a larger and more representative dataset.

## ADDITIONAL METRICS

Accuracy or judge score alone is insufficient for selecting a production model. Future evaluations should track response latency, token consumption, API cost, failure rates by category, and potentially environmental impact. Human agreement with the LLM judge should also be measured because automated evaluation should support rather than completely replace human review for high-impact tender decisions.

## Current Status

**Benchmark audit:** Complete

**Evaluation design:** Complete

**Implementation:** Complete

**Execution:** Complete

**Production recommendation:** Not yet established