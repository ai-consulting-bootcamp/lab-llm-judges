"""Command-line interface for the evaluation package."""

import argparse
import json
import os
import sys
from typing import Optional, Sequence

from .config import DEFAULT_JUDGE_MODEL, DEFAULT_OUTPUT_PATH, DEFAULT_TARGET_MODEL, create_openai_client, load_environment
from .dataset import build_cases
from .pipeline import render_analysis, run_evaluation, save_results


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run the clinical-record LLM evaluation.")
    parser.add_argument("--run", action="store_true", help="Call target and judge models.")
    parser.add_argument("--list-cases", action="store_true", help="List cases without an API call.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--model", default=os.getenv("TARGET_MODEL", DEFAULT_TARGET_MODEL))
    parser.add_argument("--judge-model", default=os.getenv("JUDGE_MODEL", DEFAULT_JUDGE_MODEL))
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--input-cost-per-million", type=float)
    parser.add_argument("--output-cost-per-million", type=float)
    args = parser.parse_args(argv)
    load_environment()
    if args.list_cases:
        for case in build_cases():
            print(f"{case.case_id}: {case.title}")
        if not args.run:
            return 0
    if not args.run:
        print("No API call made. Use --run to evaluate the cases.")
        return 0
    try:
        report = run_evaluation(create_openai_client(), target_model=args.model, judge_model=args.judge_model, temperature=args.temperature, input_cost_per_million=args.input_cost_per_million, output_cost_per_million=args.output_cost_per_million)
        destination = save_results(report, args.output)
        print(json.dumps(report["aggregate"], indent=2))
        print(render_analysis(report["analysis"], report["aggregate"]))
        print(f"Saved detailed results to {destination}")
        return 0
    except Exception as exc:
        print(f"Evaluation failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
