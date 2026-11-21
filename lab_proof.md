# Lab proof — LLMs grading LLMs, with receipts

**Scenario:** Fictional client wants CompanyScope-style AI corporate research notes with source-grounded factual accuracy. The target workflow accepts registry, filing and news evidence and produces short report answers for human due-diligence review.

## 1. Workflow / code export

- [Executable pipeline](llm_judge_evaluation.py) — reads test cases, runs deterministic controls and optionally runs an OpenAI candidate model plus independent rubric-based LLM judge.
- [Five cases with input and ground truth](test_cases.json); [prewritten target answers](fixture_responses.json).
- [Judge design and rubric](evaluation_design.md) includes its full instruction, JSON schema expectations, bias discussion and calibration.
- [Benchmark audit](benchmark_audit.md), [memo](evaluation_memo.md), [reflection](reflection.md), [summary](implementation_summary.md).

## 2. One reproducible run — local offline execution

**Command actually run:**

```bash
python3 llm_judge_evaluation.py --mode offline
```

**Input example (TC03):**

> Vela Components AG, FY2025: current assets EUR 4.8 million; current liabilities EUR 3.2 million. Compute working capital and cite [R1].

**Ground truth:** `EUR 4.8m - EUR 3.2m = EUR 1.6m [R1]`.

**Actual tested candidate fixture:**

> Working capital = EUR 4.8 million minus EUR 3.2 million = EUR 2.0 million. [R1]

**Evidence produced:** The deterministic validator flags `TC03` because it requires `1.6` and rejects `2.0 million`. The program writes [evaluation_results.json](evaluation_results.json), including each original candidate answer, check outcomes and summary. This is not an API request.

**Captured terminal output:**

```text
TC01: static-rule PASS (fixture; no API)
TC02: static-rule PASS (fixture; no API)
TC03: static-rule FAIL (fixture; no API)
TC04: static-rule PASS (fixture; no API)
TC05: static-rule FAIL (fixture; no API)
Summary: {"cases": 5, "rule_based_passes": 3, "rule_based_pass_rate": 0.6,
          "rule_based_failures": ["TC03", "TC05"], "mean_judge_score": null,
          "model_latency_seconds": null, "model_tokens": null,
          "estimated_api_cost_usd": null}
```

## 3. Final output and conclusions

**Offline fixture-control result: 3/5 pass (60%), 2/5 fail (40%).** The intended failures are arithmetic (TC03) and obedience to malicious instructions in a fictional news snippet (TC05). The tests show the local controls can detect those specific planted mistakes, not that an LLM achieved 60% accuracy. Score distribution, judged criteria, candidate/judge timing, actual token usage and cost require a **real live API run** and are intentionally null, not fabricated.

## 4. Failure / limitation encountered

**Limitation:** No `OPENAI_API_KEY` was available in the artifact-generation environment. As a result, the live LLM judge could not be executed and no real model or judge measurements exist yet. A string-matching control can also be too strict: an initial abstention test forbade the substring "beneficial owner is", which also occurs in the correct sentence "The beneficial owner is not established". That rule was corrected, and the final local run now passes TC04. This illustrates why literal checks require human-reviewed negative controls.

## 5. Required live evidence to add before final submission

```bash
python3 -m pip install -r requirements.txt
cp .env.example .env       # only if .env does not exist; add key privately
python3 llm_judge_evaluation.py --mode live --candidate-source generated
python3 -m unittest discover -s tests -v
```

The live command saves `evaluation_results_live.json` and `live_run_summary.md` with real candidate responses, judged scores/reasons, four criterion booleans, per-call latency, token usage, cost estimates and a Markdown evidence record. Review the file and add an actual live command excerpt and a short memo update. **Do not claim this step is completed until you run it.** Keep `.env` out of Git.

## 6. Checklist

- [x] Three benchmark audit cards with contamination, saturation and relevance assessment
- [x] Five original evaluation prompt cards with ground truth and verification plan
- [x] Complete LLM judge rubric, bias and calibration plan
- [x] Client memo, reflection and executable Python pipeline
- [x] One real *offline* reproduction with inputs, output, an observed problem and limitations
- [ ] Run **live** OpenAI candidate and judge requests, commit verified `evaluation_results_live.json`
- [ ] Update memo based on live numbers and compare at least a few decisions with human labels

**All case data are synthetic and fictional; no real companies are evaluated.**
