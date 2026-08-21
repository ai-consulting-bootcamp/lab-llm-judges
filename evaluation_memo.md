# Evaluation Memo

**TO:** Retail Client Product and Support Leadership  
**FROM:** Junior AI Consultant  
**DATE:** 21 August 2026  
**SUBJECT:** LLM Evaluation Results — Customer-Service Chatbot

## Executive summary

We evaluated a small five-case demonstration set covering return policy, product facts, complaint handling, safety escalation, and refund-tool sequencing. The offline demonstration scored **4.6/5.0 average** across the cases, with the strongest performance on grounded accuracy and the largest remaining weakness in actionability and tone checks. These results are directional only: they demonstrate the evaluation pipeline, not a production model certification.

## Methodology

The evaluation combined three external benchmark references with a private client-style mini-benchmark. MMLU was treated as a limited background signal for general knowledge; MT-Bench informed the multi-turn and open-ended dialogue design; and BFCL informed structured tool-call and executability checks. Because public benchmarks may have contamination and saturation risks, the private cases were treated as the decision-relevant layer.

The implementation used five hand-authored test cases and a structured judge rubric. The offline run used representative sample responses and deterministic checks so it could run without an API key. A live mode is included for later execution with an OpenAI-compatible API key. The judge scores grounded accuracy, actionability, policy/safety compliance, and tone on a 1–5 scale. Timing and token counts are collected; offline token counts are estimates.

## Results

The demonstration average was 4.6/5.0. Product fact retrieval, complaint handling, and safety escalation passed the basic offline rubric at 5/5. Return eligibility scored 5/5 because it identified the expired window and avoided promising an exception. The refund-tool case scored 3/5 because the sample response described the required tool sequence but did not execute a real tool call. This is the most important reason to add executable tool tests before launch.

The main insight is that overall answer quality is not enough. A chatbot can sound helpful while still making an unauthorized promise or skipping a required authorization step. Tool-call cases therefore need executable, schema-based checks, while complaint and tone cases need human calibration.

## Caveats & limitations

The dataset contains only five examples and is not representative of the full customer distribution. The benchmark references are public and may be contaminated or saturated. The offline responses are illustrative, and no live model comparison was performed. LLM-as-judge scores can show position, length, self-preference, and cultural bias; human agreement must be measured before using the judge as a release gate.

## Recommendation

Under these conditions, for this small demonstration set, proceed with the evaluation design rather than selecting a model from the score alone. Before launch, expand the private set to at least 100 cases, add human labels for safety and tone, and compare two candidate models on quality, tool correctness, latency, token use, and cost. Confidence: **low to moderate** until those steps are complete.

## Additional metrics

Track time per case, input/output tokens, estimated API cost, tool-call success rate, escalation rate, and human-review agreement. A slightly lower-quality model may be preferable if it meets the agreed quality bar with materially lower latency and cost, but only after safety and policy constraints are satisfied.
