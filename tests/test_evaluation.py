"""No external packages required: python3 -m unittest discover -s tests -v"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from llm_judge_evaluation import load_json, rule_checks, validate_judge, estimate_cost_usd, ROOT


class TestCompanyScopeEval(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = load_json(ROOT / "test_cases.json")
        cls.fixtures = load_json(ROOT / "fixture_responses.json")

    def test_fixture_cases_expected_outcomes(self):
        expected = {"TC01": True, "TC02": True, "TC03": False, "TC04": True, "TC05": False}
        actual = {case["id"]: rule_checks(case, self.fixtures[case["id"]])["passed"] for case in self.cases}
        self.assertEqual(actual, expected)

    def test_judge_json_valid(self):
        sample = {"score": 2, "reasoning": "Unsupported conclusion", "criteria_met": {
            "groundedness": False, "factual_accuracy": False, "uncertainty_handling": False, "instruction_resilience": True}}
        self.assertEqual(validate_judge(sample), sample)

    def test_judge_json_bad_score(self):
        sample = {"score": 6, "reasoning": "Wrong", "criteria_met": {
            "groundedness": False, "factual_accuracy": False, "uncertainty_handling": False, "instruction_resilience": True}}
        with self.assertRaises(ValueError):
            validate_judge(sample)

    def test_cost_estimate(self):
        expected = (1000 * 0.15 + 500 * 0.6) / 1000000
        self.assertEqual(estimate_cost_usd({"input_tokens": 1000, "output_tokens": 500}, 0.15, 0.6), expected)

    def test_missing_usage_not_costed(self):
        self.assertIsNone(estimate_cost_usd({"input_tokens": None, "output_tokens": None}, 0.15, 0.6))


if __name__ == "__main__":
    unittest.main()
