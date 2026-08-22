import json
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

RESULTS_FILE = Path("evaluation_results.json")


# ---------------------------------------------------------
# Load results
# ---------------------------------------------------------

if not RESULTS_FILE.exists():
    raise FileNotFoundError(
        "evaluation_results.json was not found. "
        "Run llm_judge_evaluation.py first."
    )


with open(RESULTS_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)


aggregate = data["aggregate"]
results = data["results"]


# ---------------------------------------------------------
# Detailed results
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("DETAILED EVALUATION RESULTS")
print("=" * 70)


for result in results:

    criteria = result["criteria_met"]

    criteria_passed = sum(
        bool(value)
        for value in criteria.values()
    )

    criteria_total = len(criteria)

    reasoning = result["reasoning"]

    # Keep terminal output readable
    if len(reasoning) > 200:
        reasoning = reasoning[:200] + "..."

    print(f"\nCase: {result['id']}")
    print(f"Score: {result['score']}/5")

    print(
        "Criteria met: "
        f"{criteria_passed}/{criteria_total}"
    )

    print(
        "Time: "
        f"{result['timing_seconds']['total']:.2f} seconds"
    )

    print(
        "Tokens: "
        f"{result['tokens']['total']}"
    )

    print(
        "Estimated cost: "
        f"${result['estimated_cost_usd']['total']:.6f}"
    )

    print(f"Judge reasoning: {reasoning}")


# ---------------------------------------------------------
# Aggregate summary
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("AGGREGATE SUMMARY")
print("=" * 70)

print(
    f"Model tested: {aggregate['model_tested']}"
)

print(
    f"Judge model: {aggregate['judge_model']}"
)

print(
    f"Cases evaluated: {aggregate['number_of_cases']}"
)

print(
    f"Average score: {aggregate['average_score']}/5"
)

print(
    f"Score range: "
    f"{aggregate['minimum_score']}-"
    f"{aggregate['maximum_score']}"
)

print(
    f"Total time: "
    f"{aggregate['total_time_seconds']:.2f} seconds"
)

print(
    f"Total tokens: {aggregate['total_tokens']}"
)

print(
    "Estimated total cost: "
    f"${aggregate['estimated_total_cost_usd']:.6f}"
)


# ---------------------------------------------------------
# Score distribution
# ---------------------------------------------------------

scores = [
    result["score"]
    for result in results
]

score_distribution = Counter(scores)

print("\nScore distribution:")

for score in sorted(score_distribution):
    print(
        f"  Score {score}: "
        f"{score_distribution[score]} case(s)"
    )


# ---------------------------------------------------------
# Criteria performance
# ---------------------------------------------------------

print("\nCriteria performance:")

criterion_names = list(
    results[0]["criteria_met"].keys()
)

criterion_pass_rates = []

for criterion in criterion_names:

    passed = sum(
        bool(result["criteria_met"][criterion])
        for result in results
    )

    pass_rate = passed / len(results)

    criterion_pass_rates.append(pass_rate)

    readable_name = criterion.replace("_", " ").title()

    print(
        f"  {readable_name}: "
        f"{passed}/{len(results)} "
        f"({pass_rate:.0%})"
    )


# ---------------------------------------------------------
# Key insights
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("KEY INSIGHTS")
print("=" * 70)


if len(set(scores)) == 1 and scores[0] == 5:

    print(
        "- All five test cases received the maximum score."
    )

    print(
        "- No criterion-level failures were detected."
    )

    print(
        "- The model correctly handled explicit criteria, "
        "exclusion logic, missing information, multiple "
        "criteria, and ambiguous clinical information."
    )

    print(
        "- Because there is no score variation, this small "
        "synthetic dataset does not strongly discriminate "
        "model capability."
    )

    print(
        "- More diverse and difficult cases would be needed "
        "before making conclusions about real-world clinical "
        "performance."
    )

else:

    low_score_cases = [
        result["id"]
        for result in results
        if result["score"] < 4
    ]

    print(
        f"- Lowest score: {min(scores)}/5"
    )

    if low_score_cases:
        print(
            "- Cases requiring further review: "
            + ", ".join(low_score_cases)
        )


# ---------------------------------------------------------
# Visualization 1: Scores by case
# ---------------------------------------------------------

case_labels = [
    result["id"].replace("case_", "")
    for result in results
]

plt.figure(figsize=(9, 5))

plt.bar(
    case_labels,
    scores,
)

plt.ylim(0, 5.5)

plt.xlabel("Test case")
plt.ylabel("Judge score (1–5)")
plt.title("LLM Evaluation Scores by Test Case")

plt.xticks(
    rotation=25,
    ha="right",
)

plt.tight_layout()

plt.savefig(
    "score_distribution.png",
    dpi=150,
)

plt.close()


# ---------------------------------------------------------
# Visualization 2: Criterion pass rates
# ---------------------------------------------------------

readable_criteria = [
    criterion.replace("_", " ").title()
    for criterion in criterion_names
]

pass_percentages = [
    rate * 100
    for rate in criterion_pass_rates
]

plt.figure(figsize=(9, 5))

plt.barh(
    readable_criteria,
    pass_percentages,
)

plt.xlim(0, 100)

plt.xlabel("Pass rate (%)")
plt.ylabel("Evaluation criterion")
plt.title("Evaluation Criterion Pass Rates")

plt.tight_layout()

plt.savefig(
    "criteria_pass_rates.png",
    dpi=150,
)

plt.close()


print(
    "\nCharts saved:"
    "\n- score_distribution.png"
    "\n- criteria_pass_rates.png"
)