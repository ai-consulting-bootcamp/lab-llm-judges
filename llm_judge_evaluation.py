"""Backward-compatible entry point for the modular ``llm_judge`` package.

Use ``python3 llm_judge_evaluation.py --help`` for the CLI. Public functions
remain re-exported here for notebooks and existing callers.
"""

from llm_judge.checks import CHECKERS
from llm_judge.client import call_chat_model, judge_output, normalize_judge_result
from llm_judge.config import *  # noqa: F401,F403
from llm_judge.dataset import CASE_A, CASE_B, CASE_C, build_cases, build_test_dataset
from llm_judge.models import CaseResult, EvaluationCase, JudgeResult, TokenUsage
from llm_judge.pipeline import (analyze_results, estimate_case_cost, estimate_cost, evaluate_case,
                                generate_model_response, render_analysis, run_evaluation,
                                save_results, summarize_results)


if __name__ == "__main__":
    from llm_judge.cli import main

    raise SystemExit(main())
