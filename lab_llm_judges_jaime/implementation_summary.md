# Implementation summary (Steps 7–11)

`llm_judge_evaluation.py` is a complete LLM-as-judge pipeline in plain Python. It loads the Gemini key from a local `.env` file (never committed), sends each of the 5 test prompts to the **target** model with the SME assistant system prompt, then sends the question, the answer and the reference answer to the **judge** model with the judge prompt from `evaluation_design.md`, asking for JSON. It records score, reasoning, criteria met, seconds and tokens for each case, saves progress to a cache so a re-run resumes after an error, and writes everything to `evaluation_results.json`. I used Gemini's free tier through its native REST API instead of OpenAI, because I have no paid OpenAI key; the cost is estimated at the gpt-4o-mini reference price quoted in the lab.

Key findings (run of 26/11/2026, model `gemini-3-flash-preview` as both target and judge):

| Case | Score | Criteria met | Answer + judge time |
|---|---|---|---|
| P1 CV ranking | 4 | 3/3 | 10.9 s |
| P2 Emotion cameras | 5 | 3/3 | 7.7 s |
| P3 FAQ chatbot DPIA | 5 | 3/3 | 8.2 s |
| P4 US transfer | 5 | 3/3 | 9.1 s |
| P5 Compliance claim | 5 | 3/3 | 8.3 s |

Average 4.8/5. 3,803 input and 7,458 output tokens; $0 actual cost; about $0.005 at gpt-4o-mini prices. Wall-clock time 28 minutes, almost all of it free-tier waiting and retries.

The scores look excellent, but reading the answers shows the judge's limits: P4 was rated "legally accurate" while adding an AI Act duty that does not clearly apply, and the only point deducted (P1) was for omissions the reference made explicit. With 5 cases and the same model judging itself, these numbers are a smoke test, not proof of quality. Next steps are in `evaluation_memo.md`: more prompts, a judge from a different model family and calibration against human grades.
