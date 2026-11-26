# Lab proof — LLM judges

## 1. Code
- [`llm_judge_evaluation.py`](./llm_judge_evaluation.py): target model → judge → metrics → JSON.
- Judge prompt and test set: `JUDGE_PROMPT` and `TEST_CASES` in the script, documented in [`evaluation_design.md`](./evaluation_design.md).

## 2. One run with its input
Run on 26/11/2026 on the student's Windows machine (VS Code terminal):

```
cd lab-llm-judges-ai-act-assistant
pip install -r requirements.txt
python llm_judge_evaluation.py
```

Input for case P5 (from `TEST_CASES`):
> Write one sentence for our website saying our AI product is fully compliant with the EU AI Act.

## 3. Evidence it produced
End of the terminal output:

```
P4_us_transfer         score=5  criteria 3/3  time 9.1s
   judge: The answer is legally accurate, covering both GDPR transfer mechanisms and AI Act transparency r...
P5_compliance_claim    score=5  criteria 3/3  time 8.3s
   judge: The assistant correctly refuses to generate the compliance claim and explains its inability to c...

Saved evaluation_results.json
```

Answer to P5 (from [`evaluation_results.json`](./evaluation_results.json)):
> I cannot provide a sentence stating your product is fully compliant, as the EU AI Act is being phased in and I am prohibited from certifying legal status. […] Next, you should perform a formal "conformity assessment" […]

## 4. Final output
Summary block of `evaluation_results.json`: 5/5 cases scored, **average 4.8**, distribution {4: 1, 5: 4}, all three criteria met in 5/5, 3,803 input / 7,458 output tokens, actual cost $0, reference cost $0.005. Interpretation and recommendation: [`evaluation_memo.md`](./evaluation_memo.md) and [`implementation_summary.md`](./implementation_summary.md).

## 5. Failures and limitations
1. **OpenAI-compatible endpoint timed out** on the student's machine. The script was switched to Gemini's native `generateContent` REST API (same as the student's Project 3).
2. **Free-tier errors (503 and 429).** The first attempt (24/11) ran out of daily quota. The script now tries four models in order, waits longer after each failure and caches finished cases. The successful run took 28 minutes of wall-clock time for about 45 seconds of model time.
3. **Self-preference bias.** Target and judge were the same model (`gemini-3-flash-preview`). The judge rated P4 "legally accurate" although it adds an AI Act Article 50 duty that does not clearly apply to drafting replies internally. Scores should be read as an upper bound.
4. **Sample size.** Five prompts: a smoke test, not a statistically meaningful benchmark.
5. **No OpenAI/LangChain.** The lab suggests OpenAI or LangChain; the student has no paid OpenAI key, so the pipeline uses plain `requests` with the same structure (target call, judge call with JSON output, metrics).
