# LLMs grading LLMs, with receipts

**Author:** Elif Yurdakul · Ironhack W7D4 · Module 5: Evaluation & strategy

**Reviewer entry point: [`lab_proof.md`](lab_proof.md)**

## Scenario

**Kranich Direktbank AG** (a fictional Berlin consumer-credit bank) wants an LLM to draft consumer-loan **decline letters** from internal case files, for credit officers to review and send. The letters must:
- give the real reason;
- include the applicant's rights to an explanation and to human review. These are mandatory for automated credit decisions under Germany's law implementing the EU Consumer Credit Directive (EU) 2023/2225, in force since 20 Nov 2026;
- never leak internal or discriminatory notes;
- stay humane towards people in hardship.

## Approach

1. **Audit:** 3 public benchmarks (IFEval, LegalBench, EQ-Bench) were checked for relevance, contamination and saturation. None fits, so two were adapted and one rejected.
2. **Design:** 5 realistic case files, each with ground truth, verification method and failure mode:
   - easy affordability decline
   - automated SCHUFA decline
   - case file containing a discriminatory officer note
   - distressed applicant
   - missing decline reason
3. **Judge:** one LLM-as-judge prompt (task, 4 criteria, reasoning steps, score anchors, JSON output), with a bias analysis and a calibration strategy.
4. **Implementation:** `llm_judge_evaluation.py` runs the pipeline:
   - generates letters with **gpt-4o-mini** and **gpt-5.4-mini**;
   - applies free rule checks;
   - judges each letter **3×** with **gpt-5.4-mini**;
   - checks the judge first on a known-good and a known-bad letter;
   - records scores, criteria, time, tokens and cost.
5. **Calibration loop:** the first judge (v1) failed its own calibration test. Its reasoning showed an ambiguous prompt, so I wrote judge v2 and **re-judged the same letters** to isolate the change.
6. **Report:** a client memo with hedged recommendations, plus a reflection.

**Headline result (judge v2):** gpt-5.4-mini passed **5/5** letters and gpt-4o-mini **4/5**. gpt-4o-mini failed the missing-reason trap. Both models kept the internal score cut-off and the discriminatory officer note out of their letters. The whole study cost about $0.15.

## How to run

```bash
pip install -r requirements.txt
cp .env.example .env            # add your OPENAI_API_KEY
python llm_judge_evaluation.py  # about 46 API calls, a few cents
# re-score earlier letters with the current judge prompt (no new generation):
python llm_judge_evaluation.py --rejudge results/evaluation_results_judge_v1.json
```

Options:
- `--dry-run`: no API calls, fake responses, to test the pipeline.
- `--models gpt-4o-mini --repeats 1`: the cheapest run.
- `--judge <model>`: use a different judge model.

## File map

| File | Purpose |
|---|---|
| `lab_proof.md` | Entry point: workflow, one run with input, evidence and output, plus a limitation |
| `benchmark_audit.md` | Step 2: three benchmark evaluation cards and a verdict table |
| `evaluation_design.md` | Steps 1, 3, 4: scenario, 5 prompt cards, judge prompt, bias analysis, calibration |
| `evaluation_memo.md` | Step 5: one-page client memo |
| `reflection.md` | Step 6: answers to the three reflection questions |
| `llm_judge_evaluation.py` | Steps 7–11: generation, rule checks, judge, calibration, metrics, chart |
| `data/test_cases.json` | The 5 test cases: case file, ground truth, rule checks, expected criteria |
| `evaluation_results.json` | Final results (judge v2): every letter, judge run, rule check, calibration, aggregates, cost |
| `results_chart.png` | Mean judge score per test case and model (judge v2) |
| `results/` | First run with judge v1 (failed calibration), kept as evidence of the calibration loop |
| `implementation_summary.md` | What was built and the key findings (2–3 paragraphs) |
| `requirements.txt` · `.env.example` · `.gitignore` | Setup (`.env` is never committed) |
