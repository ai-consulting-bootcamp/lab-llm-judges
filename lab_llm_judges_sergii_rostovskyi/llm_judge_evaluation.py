"""Run a retail-support evaluation with independent candidate and judge calls."""

import argparse
import json
import os
import re
import statistics
import tempfile
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from openai import APIError, OpenAI

ROOT = Path(__file__).resolve().parent
CANDIDATE = "gpt-4o-mini"
JUDGE = "gpt-5.4-mini"
RATE_USD_PER_MILLION = {CANDIDATE: (0.15, 0.075, 0.60), JUDGE: (0.75, 0.075, 4.50)}
CRITERIA = ("accuracy", "completeness", "policy_safety", "customer_experience")


def object_schema(properties):
    return {
        "type": "object",
        "properties": properties,
        "required": list(properties),
        "additionalProperties": False,
    }


CANDIDATE_SCHEMA = object_schema({
    "reply": {"type": "string"},
    "outcome": {
        "type": "string",
        "enum": ["eligible", "incompatible", "refund_estimate", "need_order_number", "escalate"],
    },
    "refund_eur": {"type": ["number", "null"]},
})
JUDGE_SCHEMA = object_schema({
    "score": {"type": "integer"},
    "reasoning": {"type": "string"},
    "criteria_met": object_schema({key: {"type": "boolean"} for key in CRITERIA}),
})


def call_model(client, model, purpose, instructions, payload, schema):
    started = time.perf_counter()
    try:
        response = client.responses.create(
            model=model,
            instructions=instructions,
            input=payload,
            text={"format": {
                "type": "json_schema", "name": purpose, "schema": schema, "strict": True,
            }},
            max_output_tokens=600,
            store=False,
            **({"reasoning": {"effort": "none"}} if model == JUDGE else {"temperature": 0}),
        )
    except APIError as exc:
        status = getattr(exc, "status_code", None)
        code = exc.code or "unavailable"
        detail = exc.body.get("message") if isinstance(exc.body, dict) else None
        detail = detail if isinstance(detail, str) else "No API error detail returned."
        if client.api_key:
            detail = detail.replace(client.api_key, "[redacted]")
        detail = re.sub(r"\bsk-[A-Za-z0-9_*-]+", "[redacted]", detail)
        detail = " ".join(detail.split())[:600]
        message = f"{purpose} with {model} failed ({type(exc).__name__}, code {code})"
        if status is not None:
            message += f", HTTP {status}"
        raise RuntimeError(f"{message}: {detail}") from exc
    elapsed = round(time.perf_counter() - started, 6)
    if response.status != "completed" or not response.output_text or response.usage is None:
        raise ValueError(f"{purpose}: incomplete response, refusal, or missing usage.")
    try:
        data = json.loads(response.output_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{purpose}: model returned invalid JSON.") from exc
    usage = response.usage
    cached = usage.input_tokens_details.cached_tokens if usage.input_tokens_details else 0
    reasoning = usage.output_tokens_details.reasoning_tokens if usage.output_tokens_details else 0
    input_rate, cached_rate, output_rate = RATE_USD_PER_MILLION[model]
    cost = ((usage.input_tokens - cached) * input_rate + cached * cached_rate
            + usage.output_tokens * output_rate) / 1_000_000
    metrics = {
        "response_id": response.id,
        "model": response.model,
        "seconds": elapsed,
        "input_tokens": usage.input_tokens,
        "cached_input_tokens": cached,
        "output_tokens": usage.output_tokens,
        "reasoning_tokens": reasoning,
        "total_tokens": usage.total_tokens,
        "estimated_cost_usd": round(cost, 9),
    }
    return data, metrics


def rubric_score(criteria_met):
    score = 1 + sum(criteria_met.values())
    return score if criteria_met["policy_safety"] else min(score, 2)


def judge_reply(client, judge_prompt, case, reply):
    payload = {
        "original_prompt": case["prompt"],
        "reference_requirements": case["ground_truth"],
        "case_specific_criteria": case["criteria"],
        "candidate_reply": reply,
    }
    raw, metrics = call_model(client, JUDGE, "reply_evaluation", judge_prompt,
                              json.dumps(payload, ensure_ascii=False), JUDGE_SCHEMA)
    flags = raw["criteria_met"]
    if set(flags) != set(CRITERIA) or any(type(value) is not bool for value in flags.values()):
        raise ValueError("Judge returned invalid criteria flags.")
    if type(raw["score"]) is not int or not 1 <= raw["score"] <= 5 or not raw["reasoning"].strip():
        raise ValueError("Judge returned an invalid score or evidence explanation.")
    score = rubric_score(flags)
    return {**raw, "model_reported_score": raw["score"], "score": score,
            "score_adjusted_to_rubric": score != raw["score"]}, metrics


def exact_checks(case, answer):
    return {
        "outcome_matches": answer["outcome"] == case["outcome"],
        "refund_matches": answer["refund_eur"] == case["refund_eur"],
        "word_count_within_limit": 0 < len(answer["reply"].split()) <= 90,
    }


def calibrate(client, judge_prompt, case):
    anchors = [
        ("R05_positive", "I understand how frustrating it is to contact us three times about the damaged chair. "
         "We already have your photos and order number. Our resolutions team can review your case "
         "and assess what compensation, if any, is available.", True),
        ("R05_unsafe_promise", "I understand how frustrating it is to contact us three times about the damaged chair. "
         "We already have your photos and order number. Our resolutions team can review your case, "
         "and I guarantee you'll receive a €30 coupon today.", False),
    ]
    results = []
    for anchor_id, reply, expected_safety in anchors:
        assessment, metrics = judge_reply(client, judge_prompt, case, reply)
        expected = dict.fromkeys(CRITERIA, True)
        expected["policy_safety"] = expected_safety
        results.append({
            "id": anchor_id,
            "reply": reply,
            "expected_criteria_met": expected,
            "expected_score": rubric_score(expected),
            "matches_expected": assessment["criteria_met"] == expected,
            "judge": assessment,
            "judge_metrics": metrics,
        })
    return results


def evaluate_case(client, judge_prompt, case):
    candidate, generation = call_model(
        client, CANDIDATE, "retail_reply",
        "You draft Northline Home customer support replies using only the supplied case facts. "
        "Choose the structured outcome by task type: eligible for a return-eligibility question, "
        "incompatible for a product-fit question, refund_estimate when asked to calculate a refund, "
        "need_order_number when a missing-delivery investigation needs the order number, and "
        "escalate when a complaint needs review by the resolutions team.",
        case["prompt"], CANDIDATE_SCHEMA,
    )
    judge, evaluation = judge_reply(client, judge_prompt, case, candidate["reply"])
    checks = exact_checks(case, candidate)
    return {
        "id": case["id"],
        "title": case["title"],
        "prompt": case["prompt"],
        "ground_truth": case["ground_truth"],
        "expected_outcome": case["outcome"],
        "expected_refund_eur": case["refund_eur"],
        "expected_criteria": case["criteria"],
        "candidate": candidate,
        "exact_checks": checks,
        "judge": judge,
        "criteria_met_count": sum(judge["criteria_met"].values()),
        "case_pass": all(checks.values()) and judge["score"] == 5,
        "generation_metrics": generation,
        "judge_metrics": evaluation,
    }


def usage_totals(calls):
    fields = ("input_tokens", "cached_input_tokens", "output_tokens",
              "reasoning_tokens", "total_tokens", "estimated_cost_usd", "seconds")
    return {field: round(sum(call[field] for call in calls), 9) for field in fields}


def aggregate(cases, anchors, wall_seconds):
    scores = [row["judge"]["score"] for row in cases]
    distribution = Counter(scores)
    total = len(cases)
    passed = sum(row["case_pass"] for row in cases)
    return {
        "case_count": total,
        "case_pass_count": passed,
        "case_pass_rate": passed / total,
        "exact_outcome_accuracy": sum(row["exact_checks"]["outcome_matches"] for row in cases) / total,
        "exact_refund_accuracy": sum(
            row["exact_checks"]["refund_matches"] for row in cases if row["expected_refund_eur"] is not None
        ) / sum(row["expected_refund_eur"] is not None for row in cases),
        "numeric_refund_case_count": sum(row["expected_refund_eur"] is not None for row in cases),
        "average_score": statistics.mean(scores),
        "minimum_score": min(scores),
        "maximum_score": max(scores),
        "score_distribution": {str(score): distribution[score] for score in range(1, 6)},
        "criterion_pass_counts": {
            key: sum(row["judge"]["criteria_met"][key] for row in cases) for key in CRITERIA
        },
        "calibration_anchor_matches": sum(row["matches_expected"] for row in anchors),
        "candidate_totals": usage_totals([row["generation_metrics"] for row in cases]),
        "judge_totals": usage_totals([row["judge_metrics"] for row in cases]),
        "calibration_totals": usage_totals([row["judge_metrics"] for row in anchors]),
        "run_wall_seconds": round(wall_seconds, 6),
    }


def write_text(path, text):
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                     delete=False) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    try:
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    default_env = ROOT / ".env"
    if not default_env.is_file():
        default_env = ROOT.parent / ".env"
    parser.add_argument("--env-file", type=Path, default=default_env)
    args = parser.parse_args()
    load_dotenv(args.env_file, encoding="utf-8-sig")
    if not os.getenv("OPENAI_API_KEY"):
        parser.exit(1, f"OPENAI_API_KEY was unavailable. Checked the environment and {args.env_file.resolve()}.\n")

    cases = json.loads((ROOT / "test_cases.json").read_text(encoding="utf-8"))
    judge_prompt = (ROOT / "judge_prompt.txt").read_text(encoding="utf-8")
    started = time.perf_counter()
    try:
        with OpenAI(timeout=40, max_retries=0) as client:
            complaint = next(case for case in cases if case["id"] == "R05")
            anchors = calibrate(client, judge_prompt, complaint)
            results = []
            for case in cases:
                row = evaluate_case(client, judge_prompt, case)
                results.append(row)
                print(f"{row['id']} | {row['judge']['score']}/5 | "
                      f"{row['criteria_met_count']}/4 criteria | "
                      f"{row['judge_metrics']['seconds']:.2f}s judge time | "
                      f"{row['judge']['reasoning']}", flush=True)
    except RuntimeError as exc:
        parser.exit(1, f"OpenAI API call failed. {exc}\n")
    except (TypeError, ValueError, KeyError) as exc:
        parser.exit(1, f"Evaluation validation failed ({type(exc).__name__}).\n")

    summary = aggregate(results, anchors, time.perf_counter() - started)
    run = {
        "executed_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "openai_api",
        "candidate_model_requested": CANDIDATE,
        "judge_model_requested": JUDGE,
        "settings": {
            "candidate_temperature": 0,
            "judge_reasoning_effort": "none",
            "max_output_tokens_per_call": 600,
            "store_responses": False,
            "rate_usd_per_million_tokens": {
                model: dict(zip(("input", "cached_input", "output"), rates))
                for model, rates in RATE_USD_PER_MILLION.items()
            },
        },
        "calibration": anchors,
        "results": results,
        "summary": summary,
    }
    write_text(ROOT / "evaluation_results.json", json.dumps(run, indent=2, ensure_ascii=False) + "\n")
    write_reports(ROOT, run)
    print(f"{summary['case_pass_count']}/{summary['case_count']} cases passed; "
          f"mean judge score {summary['average_score']:.2f}/5.")


def write_reports(root, run):
    summary = run["summary"]
    rows = run["results"]
    anchors = run["calibration"]
    count = summary["case_count"]
    passed = summary["case_pass_count"]
    mean = summary["average_score"]
    matches = summary["calibration_anchor_matches"]
    candidate, judge, calibration = (summary[key] for key in
                                     ("candidate_totals", "judge_totals", "calibration_totals"))
    totals = usage_totals([candidate, judge, calibration])
    outcome_correct = sum(row["exact_checks"]["outcome_matches"] for row in rows)
    refund_count = summary["numeric_refund_case_count"]
    refund_correct = round(summary["exact_refund_accuracy"] * refund_count)
    scores = ", ".join(f"{score}/5: {n}" for score, n in summary["score_distribution"].items())
    criteria = ", ".join(f"{key.replace('_', ' ')} {n}/{count}"
                         for key, n in summary["criterion_pass_counts"].items())
    weak = [row for row in rows if not row["case_pass"]]
    example = weak[0] if weak else next(row for row in rows if row["id"] == "R05")
    exact_failures = [name.replace("_", " ") for name, ok in example["exact_checks"].items() if not ok]
    failed_checks = f" Failed exact checks: {', '.join(exact_failures)}." if exact_failures else ""
    evidence = " ".join(example["judge"]["reasoning"].split())
    highlight = f"For {example['id']} ({example['title'].lower()}), the judge reported: {evidence}{failed_checks}"
    if matches == len(anchors):
        calibration_finding = "Both labeled anchors matched the expected flags, including the unauthorized-coupon case."
    else:
        calibration_finding = f"Only {matches}/{len(anchors)} anchors matched the expected flags, so judge-dependent results need manual review."
    table = [
        "| Case | Score | Criteria met | Exact checks | Judge seconds | Case tokens | Est. USD | Judge evidence |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        gen, ev = row["generation_metrics"], row["judge_metrics"]
        usage = usage_totals([gen, ev])
        note = " ".join(row["judge"]["reasoning"].split()).replace("|", "\\|")
        table.append(f"| {row['id']} | {row['judge']['score']}/5 | {row['criteria_met_count']}/4 "
                     f"| {sum(row['exact_checks'].values())}/3 | {ev['seconds']:.2f} "
                     f"| {usage['total_tokens']:,} | ${usage['estimated_cost_usd']:.6f} | {note} |")
    detail = "\n".join(table)
    write_text(root / "implementation_summary.md", f"""# Implementation summary

I used the OpenAI Responses API to generate one structured reply for each of five fictional retail cases with `{CANDIDATE}`. The code checks the outcome, refund field, and word limit directly. `{JUDGE}` grades the reply against four binary criteria using the case's policy and reference. The JSON export retains the raw reply, criterion verdicts, evidence, requested and returned model IDs, and per-call timings and usage.

The candidate passed {passed}/{count} cases and had a mean judge score of {mean:.2f}/5. The score distribution was {scores}. Criterion passes were {criteria}. {highlight}

{calibration_finding} The five candidate calls and five case-grading calls used {candidate['total_tokens'] + judge['total_tokens']:,} tokens and cost an estimated ${candidate['estimated_cost_usd'] + judge['estimated_cost_usd']:.6f}. Two calibration calls added {calibration['total_tokens']:,} tokens and an estimated ${calibration['estimated_cost_usd']:.6f}. The full run took {summary['run_wall_seconds']:.2f} seconds. These measurements cover one sequential run.

{detail}
""")

    write_text(root / "evaluation_memo.md", f"""# Evaluation memo

**To** Northline Home Customer Support Operations  
**From** Serge Rostovskyi  
**Date** {run['executed_at_utc'][:10]} (UTC)  
**Subject** Evaluation of the retail support drafting assistant

## Executive summary

I evaluated whether the drafting assistant could answer common support requests accurately, respect store policy, and give customers a clear next step. It passed {passed} of {count} synthetic cases in this run. The findings support a larger supervised evaluation before any decision on customer-facing use.

## Methodology

I used five English-language cases covering a return deadline, product compatibility, a discounted refund, a missing parcel, and a repeated complaint. Each case had a fixed policy record and explicit reference requirements. I audited τ-bench Retail, IFEval, and BFCL as proxies and based the measured results on Northline's cases.

GPT-4o mini drafted one answer per case. I checked the structured outcome, refund field, and word limit in Python. GPT-5.4 mini independently graded accuracy, completeness, policy safety, and customer experience with the candidate's identity withheld. A case passed when all exact checks and all four criteria passed.

## Results

The candidate's outcome was correct in {outcome_correct}/{count} cases. The numeric refund was correct in {refund_correct}/{refund_count} applicable case(s). The mean judge score was {mean:.2f}/5. {calibration_finding}

{highlight} Across the five cases, the criterion pass counts were {criteria}. The candidate was evaluated as a single option, so the results provide no relative ranking.

## Caveats and limitations

Five hand-written cases give limited coverage of real support traffic. Public benchmark exposure creates a possible contamination risk, and near-ceiling performance on simpler benchmark slices can hide differences on tougher cases. Neither proxy rankings nor these case results establish reliability on live policy updates, multilingual requests, or real tool actions.

The rubric constrains the judge's scoring, but tone assessment and paraphrase interpretation can still vary. I ran each case once and used two labeled calibration examples from one scenario. The reported pass rate describes this particular configuration and sample.

## Recommendation

Under these conditions, GPT-4o mini is a candidate for a staff-reviewed drafting trial, with low confidence in generalization. Before enabling customer-facing use, I would ask two support reviewers to label a private holdout of recent cases, track disagreement, and require reliable accuracy on refund amounts and zero unauthorized commitments in that holdout.

## Additional metrics

The evaluation used {totals['total_tokens']:,} tokens and cost an estimated ${totals['estimated_cost_usd']:.6f} including calibration. Sequential wall time was {summary['run_wall_seconds']:.2f} seconds. The estimate covers API token charges. Energy use and emissions were unmeasured. Comparing those impacts would require provider-side measurements, alongside case quality, rework, and latency.
""")


if __name__ == "__main__":
    main()
