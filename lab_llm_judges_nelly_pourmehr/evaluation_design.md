# Evaluation Design

## Part A: Evaluation Prompts

### Prompt #1: Feature That Doesn't Exist

Prompt:
"Can I export my dashboard as a PowerPoint file?" (product does not support PowerPoint export, only PDF and CSV)

Ground Truth:
[x] Yes - The correct answer states PowerPoint export is not supported, and offers the real export options (PDF, CSV).

Verification Method:
[x] Rule-based: Response must not claim PowerPoint export exists. Response must mention at least one real export format.
[ ] Human evaluation
[ ] LLM-as-judge

Primary Failure Mode:
Hallucination. Model invents a feature or a workaround that doesn't exist.

Why this prompt matters:
This is the single biggest risk for a support bot. A false "yes" sends the customer down a dead end and damages trust.

---

### Prompt #2: Angry Customer, Billing Issue

Prompt:
"I was charged twice this month and nobody is answering me. This is ridiculous."

Ground Truth:
[ ] Yes
[x] No - There is no single correct sentence, but there is a correct shape of response: acknowledge the issue, apologize, do not promise a refund amount, escalate or point to next step.

Verification Method:
[ ] Rule-based
[ ] Human evaluation
[x] LLM-as-judge: Judge checks for acknowledgment of frustration, no false promise of refund amount, and a clear next step.

Primary Failure Mode:
Incorrect tone. Model is too robotic, too apologetic without action, or promises something support can't guarantee.

Why this prompt matters:
Tone under frustration is where most support bots lose the customer, even if the facts are correct.

---

### Prompt #3: Multi-Step Troubleshooting

Prompt:
"My integration with Slack stopped sending notifications yesterday. I didn't change anything."

Ground Truth:
[x] Yes - Correct answer includes checking Slack app permissions, checking if the integration token expired, and checking notification settings in the product. All three should be covered or the response is incomplete.

Verification Method:
[x] Rule-based: Check response contains at least 2 of the 3 required troubleshooting steps.
[ ] Human evaluation
[x] LLM-as-judge: Judge checks completeness and correct order of steps.

Primary Failure Mode:
Missing information. Model gives one plausible step and stops instead of covering the likely causes.

Why this prompt matters:
Partial troubleshooting wastes the customer's time and generates a repeat ticket.

---

### Prompt #4: Out of Scope Request

Prompt:
"Can you just log into my account and fix the settings for me?"

Ground Truth:
[x] Yes - Correct answer politely declines direct account access, explains why, and offers to guide the customer step by step instead.

Verification Method:
[x] Rule-based: Response must not claim ability to access the account directly.
[ ] Human evaluation
[x] LLM-as-judge: Judge checks the decline is clear but still helpful, not just a flat no.

Primary Failure Mode:
Safety/toxicity boundary. Model implies it can take an action it cannot actually perform, which is a false capability claim, close to hallucination but scoped to permissions.

Why this prompt matters:
Claiming account access it doesn't have creates a security and trust problem, not just a bad answer.

---

### Prompt #5: Ambiguous Short Query

Prompt:
"it's not working"

Ground Truth:
[ ] Yes
[x] No - No single correct answer, but the correct behavior is to ask a clarifying question rather than guess.

Verification Method:
[ ] Rule-based
[ ] Human evaluation
[x] LLM-as-judge: Judge checks if the model asks a clarifying question instead of guessing at a fix.

Primary Failure Mode:
Hallucination by assumption. Model guesses what "it" means and gives a confident but possibly wrong answer.

Why this prompt matters:
Real support tickets are often this vague. Handling ambiguity correctly is a core skill, not an edge case.

## Part B: LLM-as-Judge Prompt

Judge built for Prompt #3: Multi-Step Troubleshooting

Task Description:
The model was asked to help a customer whose Slack integration stopped sending notifications. The model must give troubleshooting steps a support agent would actually give.

Evaluation Criteria:
1. Covers permissions check: Does the response tell the customer to check Slack app permissions?
2. Covers token expiry check: Does the response tell the customer to check if the integration token or connection expired?
3. Covers notification settings check: Does the response tell the customer to check notification settings inside the product?

Reasoning Steps:
Step 1: Read the response and list which of the 3 causes it names, if any.
Step 2: Check if the steps are stated as actions the customer can take, not vague statements like "check your settings."
Step 3: Check the response does not invent a cause not in the 3 listed, unless it also covers at least 2 of the 3 real causes.

Output Format:
{
  "score": [0-1],
  "reasoning": "[Explanation of the score]",
  "criteria_met": {
    "permissions_check": true/false,
    "token_expiry_check": true/false,
    "notification_settings_check": true/false
  }
}

Score rule: score = number of criteria met divided by 3.

## Part C: Bias Analysis

Hidden biases:
The judge may have a length bias. A longer response that lists all 3 steps, even with padding, may score higher than a short, correct response that covers 2 steps clearly. The judge may also carry a style bias toward formal, numbered-list answers, and score a plain-language answer lower even if it says the same thing. There is a domain assumption too. The judge assumes Slack is the integration in question and may misjudge a response that reasonably widens the diagnosis to a general connectivity issue.

Language and cultural assumptions are lower risk here since this prompt is technical and in English, but a judge trained mostly on English data may score a non-native English phrasing as lower quality tone, even when the content is correct.

Calibration:
Reference examples would include one full-marks answer that names all 3 causes in plain language, one partial answer that names 2 causes correctly, and one wrong answer that guesses an unrelated cause like a browser cache issue. These 3 anchors get fed into the judge prompt as few-shot examples so the judge has a fixed scale, not a floating one.

For edge cases, like a response that names a 4th valid cause not in the original 3, the judge should be told explicitly: extra valid causes do not reduce the score, but they cannot replace missing required causes.

If the judge runs too strict, meaning it fails to give credit for causes stated in different words than the reference, add a rule: give credit if the intent matches, not just the exact phrase. If the judge runs too lenient, meaning it gives credit for vague mentions like "check your integration," tighten the criteria to require the customer being told a specific, actionable step, not just a topic area.