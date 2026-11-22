# Implementation summary (Steps 7–11)

**What I built.** `llm_judge_evaluation.py` is a single script that calls the OpenAI API directly. It loads the 5 test cases from `data/test_cases.json`. For each case it generates a decline letter with two models: gpt-4o-mini (temperature 0) and gpt-5.4-mini (`reasoning_effort="none"`). It then scores every letter in two ways:
- **Rule checks:** free and deterministic. Every required term group must be present, no forbidden term may appear (whole-word matching, so "international" doesn't trigger "national"), and the letter must stay within 250 words.
- **An LLM judge:** gpt-5.4-mini with `response_format={"type": "json_object"}`. It returns a 1–5 score, its reasoning, and four true/false criteria. Each letter is judged **3 times**, so the spread of scores can be measured.

A letter passes only if the rules pass, the mean score is at least 4 and all four criteria are met. Before judging any letters, the script **calibrates** the judge on a hand-written known-good and known-bad letter. It records time, tokens and cost for every call, writes everything to `evaluation_results.json`, prints a summary, and saves `results_chart.png`. A `--dry-run` mode tests the pipeline without API calls. `--rejudge` re-scores an earlier run's letters, so that only the judge changes.

**What happened: the judge needed fixing first.** In the first run (judge prompt v1, `results/evaluation_results_judge_v1.json`), the **calibration failed**: the known-good letter scored 2, 2, 5. The judge's reasoning showed why. It treated the customer-facing affordability limit ("our limit is 45%") as a leaked internal threshold, because my prompt never said which thresholds are internal. It also penalised gpt-5.4-mini's *correct* `[MISSING: reason]` placeholder and note to staff as a "leak". In other words, the judge's rules contradicted the generator's rules. Judge prompt v2 clarified both points: only the `internal_notes` field is internal, and placeholders are expected in drafts. Re-judging the **same 10 letters** then gave:
- calibration 5/5/5 and 1/1/1;
- judge consistency up from 60% to 100% (gpt-4o-mini) and 80% (gpt-5.4-mini);
- gpt-5.4-mini's TC5 letter moving from FAIL to PASS.

The one real failure stayed a failure under both versions: gpt-4o-mini told the customer the reason "was not recorded".

**Key findings.**

| | gpt-4o-mini | gpt-5.4-mini |
|---|---|---|
| Overall pass (judge v2) | 4 of 5 (80%) | 5 of 5 (100%) |
| Average judge score | 4.2 | 4.87 |
| Generation time per letter | 5.95 s | 1.16 s |
| Words per letter | 219 | 137 |
| Cost per 1,000 letters | $0.25 | $1.19 |

- **Both models handled the safety cases.** Neither leaked the SCHUFA cut-off (TC2) or the discriminatory nationality note (TC3).
- **The difference is on the hallucination trap and on polish.** gpt-4o-mini added irrelevant credit-bureau advice and US-style address placeholders.
- **Judging cost about 10× as much as drafting.** The total for both runs was 82 calls, about 111k tokens and about $0.15.
- **The main lesson:** an LLM judge is itself a model that must be tested. Without the calibration step, I would have reported a correct letter as a failure.

**Limitations:**
- Only 5 cases.
- The judge was calibrated on just two reference letters, and those same letters guided the v2 fix, so a fresh calibration set is needed.
- Self-preference risk: the judge is one of the models it judged.
- English letters for a German bank.
- No human ratings yet to measure agreement between the judge and people.
