"""Evaluation orchestration, metrics, analysis, and persistence."""

import json
import time
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence

from .checks import CHECKERS
from .client import call_chat_model, judge_output
from .config import DEFAULT_JUDGE_MODEL, DEFAULT_OUTPUT_PATH, DEFAULT_TARGET_MODEL
from .models import CaseResult, EvaluationCase, TokenUsage
from .dataset import build_cases


def generate_model_response(client: Any, case: EvaluationCase, model: str = DEFAULT_TARGET_MODEL, temperature: float = 0.0) -> tuple[str, TokenUsage, float]:
    """Generate one target response and return text, usage, and elapsed time."""
    started = time.perf_counter()
    output, usage = call_chat_model(client, case.render_prompt(), model, temperature)
    return output, usage, time.perf_counter() - started


def evaluate_case(client: Any, case: EvaluationCase, target_model: str = DEFAULT_TARGET_MODEL, judge_model: str = DEFAULT_JUDGE_MODEL, temperature: float = 0.0) -> CaseResult:
    started = time.perf_counter()
    try:
        output, target_usage, latency = generate_model_response(client, case, target_model, temperature)
        result = CaseResult(case.case_id, case.title, case.render_prompt(), case.ground_truth, case.verification_method, case.primary_failure_mode, case.expected_criteria, output, latency, target_usage, CHECKERS[case.rule_checker](output))
        if case.judgeable:
            judge_started = time.perf_counter()
            result.judge, result.judge_usage = judge_output(client, case.source_record, output, judge_model)
            result.judge_latency_seconds = time.perf_counter() - judge_started
        return result
    except Exception as exc:
        return CaseResult(case.case_id, case.title, case.render_prompt(), case.ground_truth, case.verification_method, case.primary_failure_mode, case.expected_criteria, "", time.perf_counter() - started, TokenUsage(), {"passed": False, "checks": [], "score": 0.0}, error=f"{type(exc).__name__}: {exc}")


def _cost(result: CaseResult, input_rate: Optional[float], output_rate: Optional[float]) -> Optional[float]:
    if input_rate is None or output_rate is None:
        return None
    inputs = result.target_usage.prompt_tokens + result.judge_usage.prompt_tokens
    outputs = result.target_usage.completion_tokens + result.judge_usage.completion_tokens
    return round(inputs * input_rate / 1_000_000 + outputs * output_rate / 1_000_000, 8)


def estimate_case_cost(result: CaseResult, input_cost_per_million: Optional[float], output_cost_per_million: Optional[float]) -> Optional[float]:
    """Public name for per-case cost estimation."""
    return _cost(result, input_cost_per_million, output_cost_per_million)


def estimate_cost(summary: Mapping[str, Any], input_cost_per_million: Optional[float], output_cost_per_million: Optional[float]) -> Optional[float]:
    """Estimate aggregate cost from a summary and current provider rates."""
    if input_cost_per_million is None or output_cost_per_million is None:
        return None
    target, judge = summary["target_usage"], summary["judge_usage"]
    inputs = target["prompt_tokens"] + judge["prompt_tokens"]
    outputs = target["completion_tokens"] + judge["completion_tokens"]
    return round(inputs * input_cost_per_million / 1_000_000 + outputs * output_cost_per_million / 1_000_000, 8)


def summarize_results(results: Sequence[CaseResult]) -> dict[str, Any]:
    target, judge = TokenUsage(), TokenUsage()
    for result in results:
        target.add(result.target_usage)
        judge.add(result.judge_usage)
    scores = [r.judge.score for r in results if r.judge and r.judge.score is not None]
    costs = [r.estimated_cost for r in results if r.estimated_cost is not None]
    total_time = sum(r.latency_seconds for r in results)
    return {"cases": len(results), "successful_cases": sum(r.error is None for r in results), "rule_passes": sum(bool(r.rule_checks.get("passed")) for r in results), "rule_pass_rate": round(sum(bool(r.rule_checks.get("passed")) for r in results) / len(results), 4) if results else None, "average_rule_score": round(sum(r.rule_checks.get("score", 0) for r in results) / len(results), 4) if results else None, "average_judge_score": round(sum(scores) / len(scores), 4) if scores else None, "judge_scores": scores, "total_target_latency_seconds": round(total_time, 4), "average_target_latency_seconds": round(total_time / len(results), 4) if results else None, "total_judge_latency_seconds": round(sum(r.judge_latency_seconds or 0 for r in results), 4), "target_usage": asdict(target), "judge_usage": asdict(judge), "estimated_cost": round(sum(costs), 8) if costs else None}


def analyze_results(results: Sequence[CaseResult]) -> dict[str, Any]:
    criteria: dict[str, dict[str, int]] = {}
    judge_criteria: dict[str, dict[str, int]] = {}
    for result in results:
        for check in result.rule_checks.get("checks", []):
            stats = criteria.setdefault(check["name"], {"passed": 0, "total": 0})
            stats["total"] += 1
            stats["passed"] += int(bool(check["passed"]))
        if result.judge:
            for name, passed in result.judge.criteria_met.items():
                stats = judge_criteria.setdefault(name, {"passed": 0, "total": 0})
                stats["total"] += 1
                stats["passed"] += int(bool(passed))

    def rates(values: dict[str, dict[str, int]]) -> dict[str, dict[str, Any]]:
        return {name: {**value, "pass_rate": round(value["passed"] / value["total"], 4)} for name, value in values.items()}

    scores = [r.judge.score for r in results if r.judge and r.judge.score is not None]
    return {"judge_score_distribution": {str(score): scores.count(score) for score in range(1, 6)}, "rule_criteria_performance": rates(criteria), "judge_criteria_performance": rates(judge_criteria), "failed_case_ids": [r.case_id for r in results if not r.rule_checks.get("passed")], "key_insights": [f"Rule checks failed for: {', '.join(r.case_id for r in results if not r.rule_checks.get('passed'))}." if any(not r.rule_checks.get("passed") for r in results) else "All rule-based checks passed."]}


def render_analysis(analysis: Mapping[str, Any], aggregate: Mapping[str, Any]) -> str:
    lines = ["Evaluation analysis", "===================", "Judge score distribution:"]
    for score in range(1, 6):
        count = analysis.get("judge_score_distribution", {}).get(str(score), 0)
        lines.append(f"  {score}: {'#' * count} ({count})")
    lines += ["", "Rule criterion performance:"]
    for name, stats in analysis.get("rule_criteria_performance", {}).items():
        lines.append(f"  {name}: {stats['passed']}/{stats['total']} ({stats['pass_rate']:.0%})")
    lines += ["", f"Target time: {aggregate.get('total_target_latency_seconds', 0):.3f}s total", f"Tokens: {aggregate.get('target_usage', {}).get('total_tokens', 0)} target + {aggregate.get('judge_usage', {}).get('total_tokens', 0)} judge", f"Estimated cost: {aggregate.get('estimated_cost') if aggregate.get('estimated_cost') is not None else 'not provided'}", "", "Key insights:"]
    lines += [f"  - {item}" for item in analysis.get("key_insights", [])]
    return "\n".join(lines)


def run_evaluation(client: Any, cases: Optional[Sequence[EvaluationCase]] = None, target_model: str = DEFAULT_TARGET_MODEL, judge_model: str = DEFAULT_JUDGE_MODEL, temperature: float = 0.0, input_cost_per_million: Optional[float] = None, output_cost_per_million: Optional[float] = None) -> dict[str, Any]:
    results = [evaluate_case(client, case, target_model, judge_model, temperature) for case in list(cases or build_cases())]
    for result in results:
        result.estimated_cost = _cost(result, input_cost_per_million, output_cost_per_million)
    return {"generated_at": datetime.now(timezone.utc).isoformat(), "target_model": target_model, "judge_model": judge_model, "temperature": temperature, "cases": [asdict(r) for r in results], "aggregate": summarize_results(results), "analysis": analyze_results(results)}


def save_results(report: Mapping[str, Any], output_path: str | Path = DEFAULT_OUTPUT_PATH) -> Path:
    destination = Path(output_path)
    destination.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return destination
