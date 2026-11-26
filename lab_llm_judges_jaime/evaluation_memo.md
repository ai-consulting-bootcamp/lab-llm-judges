# Evaluation memo

**TO:** Client — SME compliance assistant project
**FROM:** Jaime, AI consultant
**DATE:** 26 November 2026
**SUBJECT:** LLM Evaluation Results — EU AI Act and GDPR assistant for SMEs

## Executive summary
We tested whether a low-cost model can answer typical SME questions on the EU AI Act and the GDPR accurately, cautiously and in plain language. On our 5-question test it scored 4.8 out of 5, but the test is small and the judge was probably lenient, so we recommend a supervised pilot, not an unsupervised launch.

## Methodology
Public benchmarks did not fit: LegalBench is mostly US law, LexGLUE predates the AI Act and TruthfulQA is saturated and contaminated (`benchmark_audit.md`). We wrote 5 prompts from the course materials, covering a high-risk use (CV ranking), a prohibited practice (emotion detection at work), a nuanced "probably not" (DPIA for a FAQ chatbot), an international transfer and a request to certify compliance. Each has a reference answer.

The assistant was `gemini-3-flash-preview` (free tier) with a system prompt limiting answers to 150 words and forbidding compliance claims. An LLM judge scored each answer from 1 to 5 against three criteria: legal accuracy, appropriate hedging, and a clear next step. The judge was the same model family.

## Results
Average score **4.8/5**: four answers scored 5 and one scored 4. All five met the three criteria. The 4 was the CV-ranking answer: correct classification and steps, but no mention of the DPIA or the December 2027 date. The assistant correctly refused to write the compliance sentence and correctly identified the emotion-detection cameras as prohibited.

On review, one answer that scored 5 (US transfer) adds an AI Act transparency duty that does not clearly apply to drafting replies internally. The judge did not flag it. This is our most important finding: **the judge is less reliable than the scores suggest.**

## Caveats and limitations
Five prompts are not a statistically meaningful sample; one different answer moves the average by 0.2. Model and judge are the same family (self-preference bias). The law is changing (the Digital Omnibus moved high-risk dates), so reference answers need regular updates. We tested in English only, at one point in time; the free-tier model may change without notice. We cannot guarantee legal correctness: these scores measure agreement with our references, not legal advice.

## Recommendation
Under these conditions and for this task, the model is good enough for a **pilot in which a person with legal training reviews every answer before it reaches a client**. We have moderate confidence in its ability to classify common cases and to refuse compliance claims, and low confidence in dates and in less common edge cases. Before scaling, expand the test to at least 30 prompts, use a judge from a different model family, and calibrate it against human grades.

## Additional metrics
The run used 3,803 input and 7,458 output tokens at a cost of $0 (free tier). At the reference price of a small paid model (gpt-4o-mini) it would cost about $0.005, so evaluation cost is not a constraint. Model time was about 4–6 seconds per answer and 3–7 seconds per judgment, but the full run took 28 minutes because of free-tier rate limits and retries. In production, a paid tier would remove the waiting; the environmental cost per question is small, but it multiplies with every re-run of the evaluation.
