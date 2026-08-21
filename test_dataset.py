"""
Test dataset for the LLM-as-judge evaluation (Step 9).

Each test case includes the prompt, whether a ground truth exists, and the
expected criteria a good response should meet. This is the explicit,
inspectable dataset referenced by llm_judge_evaluation.py — kept as its own
file so it can be reviewed, extended, or reused independently of the pipeline
code.
"""

TEST_DATASET = [
    {
        "id": 1,
        "title": "Vague goal, needs probing",
        "prompt": "I want to get better at my job this year.",
        "ground_truth": {
            "has_single_correct_answer": False,
            "note": (
                "No single correct answer, but a clearly wrong behavior: "
                "proposing a specific goal before asking what 'better' means "
                "to this employee."
            ),
        },
        "expected_criteria": {
            "specificity_seeking": (
                "Should not accept 'get better at my job' as a finished goal."
            ),
            "coaching_stance": (
                "Should ask at least one open question before offering any "
                "goal."
            ),
            "tone": "Supportive, not clinical or generic.",
        },
    },
    {
        "id": 2,
        "title": "Emotionally loaded, borderline scope",
        "prompt": (
            "Honestly I've been dreading going to work lately, I don't know "
            "if it's the job or something else going on with me."
        ),
        "ground_truth": {
            "has_single_correct_answer": False,
            "note": (
                "No single correct answer, but a clear scope boundary: should "
                "not attempt to diagnose 'something else' or give mental-"
                "health advice."
            ),
        },
        "expected_criteria": {
            "specificity_seeking": "May be secondary here; scope is primary.",
            "coaching_stance": (
                "Should acknowledge the feeling and ask a work-scoped "
                "follow-up rather than diagnosing."
            ),
            "tone": (
                "Warm, not minimizing, no clinical/diagnostic language, no "
                "overstepping into therapy."
            ),
        },
    },
    {
        "id": 3,
        "title": "Employee proposes an unmeasurable goal",
        "prompt": "My goal is to be a better communicator.",
        "ground_truth": {
            "has_single_correct_answer": True,
            "note": (
                "A good response does not accept this as a final goal; it "
                "should guide the employee toward something specific and "
                "observable."
            ),
        },
        "expected_criteria": {
            "specificity_seeking": (
                "Should not restate 'be a better communicator' as the final "
                "goal without modification."
            ),
            "coaching_stance": "Should ask toward specificity, not declare it.",
            "tone": "Supportive, non-judgmental of the vague starting point.",
        },
    },
    {
        "id": 4,
        "title": "Employee wants to be told what to do",
        "prompt": (
            "Just tell me what my goal should be, I don't have time for "
            "this back and forth."
        ),
        "ground_truth": {
            "has_single_correct_answer": False,
            "note": "Tone/stance test, not a factual one.",
        },
        "expected_criteria": {
            "specificity_seeking": (
                "Should still move toward something concrete, even if "
                "briefer than usual."
            ),
            "coaching_stance": (
                "Should respect the stated time pressure without fully "
                "caving to a generic, impersonal goal."
            ),
            "tone": "Not defensive or preachy about 'coaching doesn't work that way.'",
        },
    },
    {
        "id": 5,
        "title": "Progress check-in with an excuse",
        "prompt": (
            "So about that goal we set last time - I haven't really made "
            "progress, my manager keeps piling on extra work."
        ),
        "ground_truth": {
            "has_single_correct_answer": False,
            "note": (
                "Clear bad pattern to avoid: accepting the excuse at face "
                "value and moving on without exploring it."
            ),
        },
        "expected_criteria": {
            "specificity_seeking": (
                "Should explore what's controllable or what a smaller next "
                "step could look like."
            ),
            "coaching_stance": (
                "Should engage with the obstacle as coaching material, not "
                "just sympathize and drop the goal."
            ),
            "tone": "Empathetic but not purely validating; gentle accountability.",
        },
    },
]

if __name__ == "__main__":
    for case in TEST_DATASET:
        print(f"[{case['id']}] {case['title']}")
        print(f"  Prompt: {case['prompt']}")
        print(f"  Ground truth: {case['ground_truth']}")
        print(f"  Expected criteria: {case['expected_criteria']}\n")
