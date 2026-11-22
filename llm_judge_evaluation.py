"""
llm_judge_evaluation.py: LLM-as-judge evaluation of loan decline letters.

Client scenario: Kranich Direktbank AG (fictional, Berlin) wants an LLM to draft consumer-loan
decline letters from internal case files. Letters must be accurate, compliant (GDPR Art. 22 /
EU Consumer Credit Directive 2023/2225 explanation and human-review rights) and humane.

Pipeline (lab Steps 7-11)
-------------------------
1. Load 5 test cases (data/test_cases.json): case file, ground truth, rule checks.
2. GENERATE a letter for each case with each model under test (default: gpt-4o-mini, gpt-5.4-mini).
3. RULE CHECKS (free, deterministic): required terms, forbidden terms, word limit.
4. LLM JUDGE (judge prompt from evaluation_design.md, JSON output): score 1-5, reasoning,
   4 criteria. Each letter is judged N times (default 3) to measure judge consistency.
5. CALIBRATION: before trusting the judge, it grades a known-good and a known-bad letter.
6. Metrics: scores, criteria, pass rate, time, tokens, cost -> evaluation_results.json,
   plus a chart (results_chart.png) and a printed summary.

Run
---
    pip install -r requirements.txt
    python llm_judge_evaluation.py                 # full run (about 45 API calls, < $0.05)
    python llm_judge_evaluation.py --dry-run       # no API calls, fake responses, tests the pipeline
    python llm_judge_evaluation.py --models gpt-4o-mini --repeats 1   # cheapest run
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEST_CASES_FILE = ROOT / "data" / "test_cases.json"

DEFAULT_MODELS = ["gpt-4o-mini", "gpt-5.4-mini"]
DEFAULT_JUDGE = "gpt-5.4-mini"

# USD per 1M tokens, OpenAI pricing page (checked 22 Nov 2026)
PRICES = {
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-5.4-mini": {"input": 0.75, "output": 4.50},
}

# --------------------------------------------------------------------------------------
# Prompts
# --------------------------------------------------------------------------------------
GENERATOR_SYSTEM_PROMPT = """You are a correspondence assistant at Kranich Direktbank AG, Berlin.
Draft a consumer-loan decline letter in English from the case file you receive.

Rules:
- Address the applicant by name and quote the reference number and loan amount.
- State the main reason for the decision exactly as recorded in the case file, in plain language.
  Never add reasons that are not in the case file.
- Tell the applicant they can ask for an explanation of the assessment, express their point of view,
  and request that a member of staff reviews the decision. If the decision was fully automated,
  say so and explain the right to human intervention.
- If a credit bureau was consulted, name it and say the applicant can request their data from it and
  have incorrect entries corrected.
- Never include internal notes, internal thresholds or scores, or anything about protected
  characteristics (e.g. nationality, ethnicity, religion, health).
- Never promise a different outcome or recommend other lenders.
- If information needed for the letter is missing from the case file, do not invent it: write
  [MISSING: <what is missing>] in the letter and add a note to staff at the end.
- Be clear, respectful and empathetic. Maximum 250 words. Contact: Customer Service, 030 1234 5678,
  kredit@kranich-direktbank.example
"""

JUDGE_PROMPT = """# Task description
You are evaluating a consumer-loan DECLINE LETTER drafted by an AI assistant for Kranich
Direktbank AG (Germany). The assistant received an internal case file and had to write a letter to
the applicant that is accurate, compliant with EU consumer-credit and data-protection rules
(right to an explanation, right to human review, credit-bureau transparency), and humane.

# Inputs
<case_file>
{case_file}
</case_file>

<letter>
{letter}
</letter>

# Evaluation criteria
1. faithfulness: Every fact in the letter (name, reference, amount, reason) matches the case file.
   The decline reason is the recorded reason, with nothing invented. If the reason is missing from
   the case file, the letter must NOT invent one and must flag the gap instead.
2. required_disclosures: The letter tells the applicant they can get an explanation and request a
   human review / contest the decision; if the decision was fully automated it says so; if a credit
   bureau was consulted it is named with the right to access/correct their data; contact details given.
3. prohibited_content: The letter contains NONE of: content from the case file's internal_notes field
   (e.g. scorecard cut-offs, individual scores, officer comments), references to protected
   characteristics (nationality, origin, health, etc.), promises of a different outcome,
   recommendations of other lenders, legal threats or blame.
4. tone_clarity: Plain, respectful, empathetic language suited to the applicant's situation;
   neither cold/bureaucratic nor patronising or falsely hopeful; well structured and concise.

# Important clarifications (judge prompt v2)
- Everything in the case file EXCEPT the internal_notes field is customer-facing. The main_reason may be
  quoted in full, including any policy limit it contains (e.g. "our affordability limit is 45%"). Stating it
  is correct, not a leak.
- The letter is a DRAFT that a credit officer reviews before sending. When information is missing from the
  case file, a clearly marked placeholder such as [MISSING: ...] plus a separate "Note to staff" is the
  REQUIRED, correct behaviour. Do not treat that note as leaked internal information.
- Telling the applicant that the reason "was not recorded" (instead of flagging it for staff) is NOT
  acceptable: it fails faithfulness and required_disclosures, because the applicant gets no reason.
- Advice that does not fit the case (e.g. suggesting a credit-bureau check when no bureau was consulted)
  counts against tone_clarity if it confuses the applicant.

# Reasoning steps
Step 1: Read the case file. Note the recorded reason, decision process, bureau use and any internal
        notes that must stay internal.
Step 2: Check faithfulness fact by fact against the case file. An invented reason is a severe error.
Step 3: Check each required disclosure, then scan for every type of prohibited content.
Step 4: Judge tone and clarity from the applicant's point of view.
Step 5: Choose the score using the anchors below, then write the JSON.

# Score anchors (1-5)
5 = all four criteria fully met; could be sent as is.
4 = all criteria met with a minor weakness (e.g. slightly long, one awkward phrase).
3 = one criterion clearly not met but no severe error (e.g. a missing disclosure, cold tone).
2 = a severe error (e.g. invented or wrong reason, leaked internal information) OR two criteria not met.
1 = harmful: discriminatory content, multiple severe errors, or misleading the applicant.

# Output format
Return ONLY a JSON object:
{{
  "score": <integer 1-5>,
  "reasoning": "<2-4 sentences explaining the score, citing the letter>",
  "criteria_met": {{
    "faithfulness": <true|false>,
    "required_disclosures": <true|false>,
    "prohibited_content": <true|false>,
    "tone_clarity": <true|false>
  }}
}}
Note: "prohibited_content": true means the letter is FREE of prohibited content.
"""

JUDGE_VERSION = "v2"  # v1 = first run (failed calibration); v2 = clarified prompt

CRITERIA = ["faithfulness", "required_disclosures", "prohibited_content", "tone_clarity"]

# Calibration letters for TC1 (known quality): the judge must give GOOD >= 4 and BAD <= 2.
CALIBRATION_LETTERS = {
    "known_good": """Dear Mr Becker,

Thank you for your application for a personal loan of EUR 15,000 (reference KD-2026-0412).

After careful review, we are unable to offer you this loan. The monthly repayments, together with your existing commitments, would take about 52% of your net monthly income. Our responsible-lending limit is 45%, which protects customers from repayments they may struggle to afford.

You have the right to receive an explanation of how we assessed your application, to tell us your point of view, and to ask a member of our credit team to review the decision. Simply reply to this letter or call us, quoting your reference number.

If your circumstances change, for example your income increases or existing commitments end, you are welcome to apply again.

Customer Service: 030 1234 5678 | kredit@kranich-direktbank.example

Kind regards,
Kranich Direktbank AG""",
    "known_bad": """Dear Customer,

Your loan application was rejected. Our system flagged you as high risk and your score was below our internal cut-off, and the officer noted concerns about your background. Decisions are final and cannot be appealed.

You may want to try another lender. We are sure you will be approved next time.

Kranich Direktbank""",
}


# --------------------------------------------------------------------------------------
# API helpers
# --------------------------------------------------------------------------------------
class LLM:
    """Thin wrapper around the OpenAI client that records tokens, time and cost.
    In --dry-run mode it returns deterministic fake responses (no network, no cost)."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        if not dry_run:
            from dotenv import load_dotenv
            from openai import OpenAI

            load_dotenv(override=True)
            if not os.getenv("OPENAI_API_KEY"):
                raise SystemExit("OPENAI_API_KEY missing: add it to .env (see .env.example)")
            self.client = OpenAI()

    @staticmethod
    def _params(model: str, purpose: str) -> dict:
        if model.startswith("gpt-5"):
            # gpt-5 family: no temperature; reasoning tokens count toward max_completion_tokens
            effort = "none" if purpose == "generate" else "low"
            return {"max_completion_tokens": 2000, "reasoning_effort": effort}
        return {"temperature": 0, "max_tokens": 700}

    def chat(self, model: str, messages: list[dict], purpose: str, json_mode: bool = False) -> dict:
        start = time.perf_counter()
        if self.dry_run:
            text, p_tok, c_tok = _fake_response(messages, purpose)
        else:
            kwargs = self._params(model, purpose)
            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}
            r = self.client.chat.completions.create(model=model, messages=messages, **kwargs)
            text = (r.choices[0].message.content or "").strip()
            p_tok, c_tok = r.usage.prompt_tokens, r.usage.completion_tokens
        price = PRICES.get(model, {"input": 0, "output": 0})
        return {
            "text": text,
            "model": model,
            "prompt_tokens": p_tok,
            "completion_tokens": c_tok,
            "cost_usd": (p_tok * price["input"] + c_tok * price["output"]) / 1_000_000,
            "seconds": round(time.perf_counter() - start, 2),
        }


def _fake_response(messages: list[dict], purpose: str) -> tuple[str, int, int]:
    """Deterministic stand-in for --dry-run."""
    if purpose == "generate":
        case = messages[-1]["content"]
        ref = re.search(r"KD-\d{4}-\d{4}", case).group(0)
        return (f"Dear applicant,\n\nRe: {ref}. We cannot offer this loan. You may request an explanation "
                f"and a human review of the decision.\n\nCustomer Service: 030 1234 5678", 380, 90)
    score = random.choice([2, 3, 4, 5])
    crit = {c: random.random() > 0.3 for c in CRITERIA}
    return json.dumps({"score": score, "reasoning": "Dry-run fake judgement.", "criteria_met": crit}), 900, 120


# --------------------------------------------------------------------------------------
# Steps
# --------------------------------------------------------------------------------------
def format_case_file(case_file: dict) -> str:
    return "\n".join(f"{k}: {v}" for k, v in case_file.items())


def generate_letter(llm: LLM, model: str, case: dict) -> dict:
    """Step 9: generate the model response for one test case."""
    try:
        return llm.chat(model, [
            {"role": "system", "content": GENERATOR_SYSTEM_PROMPT},
            {"role": "user", "content": "Case file:\n" + format_case_file(case["case_file"])},
        ], purpose="generate")
    except Exception as e:  # keep going if one call fails
        return {"text": "", "error": str(e), "model": model, "prompt_tokens": 0,
                "completion_tokens": 0, "cost_usd": 0.0, "seconds": 0.0}


def _forbidden_hit(term: str, text: str) -> bool:
    """Whole-word match; a trailing * means prefix match (e.g. 'afford*' matches 'affordable')."""
    if term.endswith("*"):
        return re.search(r"\b" + re.escape(term[:-1].lower()), text) is not None
    if re.fullmatch(r"[\w\s-]+", term):
        return re.search(r"\b" + re.escape(term.lower()) + r"\b", text) is not None
    return term.lower() in text


def run_rule_checks(letter: str, rules: dict) -> dict:
    """Deterministic checks: every required group present, no forbidden term, word limit."""
    low = letter.lower()
    missing = [g[0] for g in rules["required_any"] if not any(t.lower() in low for t in g)]
    forbidden = [t for t in rules["forbidden"] if _forbidden_hit(t, low)]
    words = len(letter.split())
    return {
        "passed": not missing and not forbidden and words <= rules["max_words"],
        "missing_required": missing,
        "forbidden_found": forbidden,
        "word_count": words,
        "within_word_limit": words <= rules["max_words"],
    }


def judge_letter(llm: LLM, judge_model: str, case_file: dict, letter: str) -> dict:
    """Step 8: the LLM-as-judge function. Returns score, reasoning, criteria_met + usage."""
    prompt = JUDGE_PROMPT.format(case_file=format_case_file(case_file), letter=letter or "[EMPTY LETTER]")
    try:
        res = llm.chat(judge_model, [{"role": "user", "content": prompt}], purpose="judge", json_mode=True)
        parsed = json.loads(res["text"])
        score = int(parsed["score"])
        crit = {c: bool(parsed.get("criteria_met", {}).get(c, False)) for c in CRITERIA}
        return {"score": score, "reasoning": parsed.get("reasoning", ""), "criteria_met": crit,
                "parse_error": None, **{k: res[k] for k in ("prompt_tokens", "completion_tokens", "cost_usd", "seconds")}}
    except Exception as e:  # JSON or API failure: record it, don't crash
        return {"score": None, "reasoning": "", "criteria_met": {c: None for c in CRITERIA},
                "parse_error": f"{type(e).__name__}: {e}", "prompt_tokens": 0, "completion_tokens": 0,
                "cost_usd": 0.0, "seconds": 0.0}


def summarise_judgements(runs: list[dict]) -> dict:
    scores = [r["score"] for r in runs if r["score"] is not None]
    crit_votes = {c: [r["criteria_met"][c] for r in runs if r["criteria_met"][c] is not None] for c in CRITERIA}
    majority = {c: (sum(v) > len(v) / 2) if v else None for c, v in crit_votes.items()}
    return {
        "mean_score": round(statistics.mean(scores), 2) if scores else None,
        "min_score": min(scores) if scores else None,
        "max_score": max(scores) if scores else None,
        "stdev": round(statistics.pstdev(scores), 2) if len(scores) > 1 else 0.0,
        "consistent": len(set(scores)) == 1 if scores else False,
        "criteria_majority": majority,
        "criteria_met_count": sum(1 for v in majority.values() if v),
        "parse_errors": sum(1 for r in runs if r["parse_error"]),
    }


def run_calibration(llm: LLM, judge_model: str, case: dict, repeats: int) -> dict:
    """Check the judge on letters of known quality before trusting it."""
    out = {}
    for label, letter in CALIBRATION_LETTERS.items():
        runs = [judge_letter(llm, judge_model, case["case_file"], letter) for _ in range(repeats)]
        s = summarise_judgements(runs)
        expected_ok = (s["mean_score"] or 0) >= 4 if label == "known_good" else (s["mean_score"] or 5) <= 2
        out[label] = {"summary": s, "as_expected": expected_ok, "runs": runs}
    out["judge_calibrated"] = all(v["as_expected"] for k, v in out.items() if k != "judge_calibrated")
    return out


# --------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--models", nargs="+", default=DEFAULT_MODELS, help="models under test")
    ap.add_argument("--judge", default=DEFAULT_JUDGE, help="judge model")
    ap.add_argument("--repeats", type=int, default=3, help="judge runs per letter (consistency check)")
    ap.add_argument("--dry-run", action="store_true", help="fake responses, no API calls")
    ap.add_argument("--rejudge", metavar="RESULTS_JSON",
                    help="re-use the letters in an earlier results file (skip generation) so only the judge changes")
    args = ap.parse_args()

    llm = LLM(dry_run=args.dry_run)
    cases = json.loads(TEST_CASES_FILE.read_text(encoding="utf-8"))
    previous = {}
    if args.rejudge:
        old = json.loads(Path(args.rejudge).read_text(encoding="utf-8"))
        previous = {(r["model"], r["case_id"]): r for r in old["results"]}
        args.models = old["run_info"]["models_under_test"]
        print(f"Re-judging the letters from {args.rejudge} (no new generation)")
    t0 = time.perf_counter()

    print(f"Judge prompt {JUDGE_VERSION} | Judge: {args.judge} | models under test: {', '.join(args.models)} | repeats: {args.repeats}")
    print("\n[1/3] Calibrating the judge on a known-good and a known-bad letter ...")
    calibration = run_calibration(llm, args.judge, cases[0], args.repeats)
    for label in CALIBRATION_LETTERS:
        c = calibration[label]
        print(f"   {label:<11} mean score {c['summary']['mean_score']} (runs: "
              f"{[r['score'] for r in c['runs']]}) -> {'OK' if c['as_expected'] else 'UNEXPECTED'}")
    print("   Judge calibrated:", calibration["judge_calibrated"])

    print("\n[2/3] Generating letters and judging them ...")
    results = []
    for model in args.models:
        for case in cases:
            if previous:
                prev = previous[(model, case["id"])]
                gen = {"text": prev["letter"], **prev["generation"]}
            else:
                gen = generate_letter(llm, model, case)
            rules = run_rule_checks(gen["text"], case["rule_checks"])
            runs = [judge_letter(llm, args.judge, case["case_file"], gen["text"]) for _ in range(args.repeats)]
            summ = summarise_judgements(runs)
            passed = bool(rules["passed"] and (summ["mean_score"] or 0) >= 4 and summ["criteria_met_count"] == 4)
            results.append({
                "case_id": case["id"], "title": case["title"], "difficulty": case["difficulty"],
                "primary_failure_mode": case["primary_failure_mode"], "model": model,
                "ground_truth": case["ground_truth"], "letter": gen["text"], "generation": {k: v for k, v in gen.items() if k != "text"},
                "rule_checks": rules, "judge_runs": runs, "judge_summary": summ, "overall_pass": passed,
            })
            print(f"   {model:<13} {case['id']:<28} judge {summ['mean_score']} {[r['score'] for r in runs]} "
                  f"| criteria {summ['criteria_met_count']}/4 | rules {'PASS' if rules['passed'] else 'FAIL'} "
                  f"| {'PASS' if passed else 'FAIL'}")

    # ---- aggregates (Step 10)
    total_seconds = round(time.perf_counter() - t0, 1)
    per_model = {}
    for model in args.models:
        rs = [r for r in results if r["model"] == model]
        scores = [r["judge_summary"]["mean_score"] for r in rs if r["judge_summary"]["mean_score"] is not None]
        gen_cost = sum(r["generation"]["cost_usd"] for r in rs)
        judge_cost = sum(j["cost_usd"] for r in rs for j in r["judge_runs"])
        per_model[model] = {
            "avg_judge_score": round(statistics.mean(scores), 2) if scores else None,
            "min_judge_score": min(scores) if scores else None,
            "max_judge_score": max(scores) if scores else None,
            "overall_pass_rate": round(sum(r["overall_pass"] for r in rs) / len(rs), 2),
            "rule_pass_rate": round(sum(r["rule_checks"]["passed"] for r in rs) / len(rs), 2),
            "criteria_pass_rates": {c: round(sum(bool(r["judge_summary"]["criteria_majority"][c]) for r in rs) / len(rs), 2) for c in CRITERIA},
            "judge_consistency_rate": round(sum(r["judge_summary"]["consistent"] for r in rs) / len(rs), 2),
            "avg_generation_seconds": round(statistics.mean(r["generation"]["seconds"] for r in rs), 2),
            "avg_letter_words": round(statistics.mean(r["rule_checks"]["word_count"] for r in rs), 1),
            "generation_tokens": {"prompt": sum(r["generation"]["prompt_tokens"] for r in rs),
                                  "completion": sum(r["generation"]["completion_tokens"] for r in rs)},
            "generation_cost_usd": round(gen_cost, 6),
            "generation_cost_per_1000_letters_usd": round(gen_cost / len(rs) * 1000, 4),
            "judge_cost_usd": round(judge_cost, 6),
        }
    all_judge = [j for r in results for j in r["judge_runs"]] + [j for k in CALIBRATION_LETTERS for j in calibration[k]["runs"]]
    totals = {
        "total_seconds": total_seconds,
        "api_calls": (0 if previous else len(results)) + len(all_judge),
        "total_tokens": sum(r["generation"]["prompt_tokens"] + r["generation"]["completion_tokens"] for r in results)
                        + sum(j["prompt_tokens"] + j["completion_tokens"] for j in all_judge),
        "total_cost_usd": round((0 if previous else sum(r["generation"]["cost_usd"] for r in results)) + sum(j["cost_usd"] for j in all_judge), 6),
        "avg_judge_seconds": round(statistics.mean(j["seconds"] for j in all_judge), 2) if all_judge else None,
        "judge_parse_errors": sum(1 for j in all_judge if j["parse_error"]),
    }

    output = {
        "run_info": {"timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                     "dry_run": args.dry_run, "judge_model": args.judge, "judge_prompt_version": JUDGE_VERSION,
                     "letters_reused_from": args.rejudge, "models_under_test": args.models,
                     "judge_repeats": args.repeats, "prices_usd_per_1m_tokens": PRICES,
                     "pass_rule": "rule checks pass AND mean judge score >= 4 AND all 4 criteria met (majority vote)"},
        "calibration": calibration, "per_model": per_model, "totals": totals, "results": results,
    }
    out_file = ROOT / ("evaluation_results_dryrun.json" if args.dry_run else "evaluation_results.json")
    out_file.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")

    # ---- summary report (Step 11)
    print("\n[3/3] Summary")
    for model, m in per_model.items():
        print(f"\n  {model}: avg judge score {m['avg_judge_score']} (min {m['min_judge_score']}, max {m['max_judge_score']}), "
              f"overall pass {m['overall_pass_rate']:.0%}, rule checks {m['rule_pass_rate']:.0%}, "
              f"judge consistent on {m['judge_consistency_rate']:.0%} of letters")
        print("     criteria pass rates:", ", ".join(f"{c} {v:.0%}" for c, v in m["criteria_pass_rates"].items()))
        print(f"     generation: {m['avg_generation_seconds']}s/letter, {m['avg_letter_words']} words, "
              f"${m['generation_cost_per_1000_letters_usd']} per 1,000 letters")
    print(f"\n  Totals: {totals['api_calls']} API calls, {totals['total_tokens']:,} tokens, "
          f"${totals['total_cost_usd']:.4f}, {totals['total_seconds']}s, judge parse errors: {totals['judge_parse_errors']}")
    print("\n  Judge reasoning on failed letters (shortened):")
    for r in results:
        if not r["overall_pass"]:
            why = r["judge_runs"][0]["reasoning"][:220] if r["judge_runs"] else ""
            rule_note = "" if r["rule_checks"]["passed"] else f" [rules: missing {r['rule_checks']['missing_required']}, forbidden {r['rule_checks']['forbidden_found']}]"
            print(f"   - {r['model']} / {r['case_id']}: {why}{rule_note}")
    _save_chart(results, args.models, cases, dry_run=args.dry_run)
    print(f"\nSaved {out_file.name}")


def _save_chart(results: list[dict], models: list[str], cases: list[dict], dry_run: bool) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed: skipping chart")
        return
    ids = [c["id"].split("_")[0] for c in cases]
    fig, ax = plt.subplots(figsize=(8, 4))
    width = 0.8 / len(models)
    for i, model in enumerate(models):
        vals = [next((r["judge_summary"]["mean_score"] or 0 for r in results if r["model"] == model and r["case_id"].startswith(cid)), 0) for cid in ids]
        ax.bar([x + i * width for x in range(len(ids))], vals, width, label=model)
    ax.axhline(4, ls="--", lw=1, color="grey")
    ax.set_xticks([x + width * (len(models) - 1) / 2 for x in range(len(ids))], ids)
    ax.set_ylim(0, 5.2); ax.set_ylabel("mean judge score (1-5)")
    ax.set_title("Judge score per test case (dashed line = pass threshold 4)")
    ax.legend(); plt.tight_layout()
    name = "results_chart_dryrun.png" if dry_run else "results_chart.png"
    plt.savefig(ROOT / name, dpi=130)
    print(f"Saved {name}")


if __name__ == "__main__":
    main()
