"""Production-oriented clinical-record LLM evaluation package."""

from .dataset import build_cases, build_test_dataset
from .pipeline import run_evaluation, save_results

__all__ = ["build_cases", "build_test_dataset", "run_evaluation", "save_results"]
