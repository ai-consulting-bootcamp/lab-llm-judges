# Evaluation Design - Retail Customer Service Chatbot

## Scenario Summary
The retailer wants a customer service chatbot that can handle returns, product questions, and complaints. The system should be helpful, calm, and resolution-oriented, while avoiding policy hallucinations and unsafe promises. The main failure modes are incorrect policy claims, evasive answers, weak escalation handling, and a tone that feels cold or defensive.

## Retail Policy Assumptions
For this evaluation, use the following working policy as ground truth:
- Returns are allowed within 30 days of delivery with proof of purchase.
- Opened items are only returnable if defective.
- Damaged or missing items should be handled with apology, evidence collection if needed, and a replacement or refund path.
- Product compatibility must not be guessed if the model or specification is missing.
- Complaints should be acknowledged and moved toward a concrete resolution or escalation.

## Prompt 1

Prompt #1: Late Return Request

Prompt:
A customer says: "I bought a speaker 37 days ago and opened it, but I do not like the sound. Can I return it for a refund?"

Ground Truth:
[x] Yes - The correct answer is to explain that the 30-day return window has passed and that opened items are not eligible for a standard refund unless defective. The response should offer a helpful alternative such as checking for a defect claim, exchange policy, or escalation.

Verification Method:
[ ] Rule-based: Check for a 30-day denial, a defect exception, and a request for the order number.
[ ] Human evaluation: A human would judge whether the refusal is respectful and whether the next step feels genuinely helpful.
[x] LLM-as-judge: Check policy adherence, empathy, clarity, and whether the response offers a concrete next step instead of inventing a refund.

Primary Failure Mode:
Hallucinating a refund policy or sounding dismissive when denying the return.

Why this prompt matters:
This is a common retail support edge case where the assistant has to balance policy enforcement with a useful and respectful answer. It is a good test of both tone and resolution quality.

## Prompt 2

Prompt #2: Damaged Arrival Complaint

Prompt:
A customer says: "My order arrived with a cracked item and one accessory missing. I am pretty angry."

Ground Truth:
[x] Yes - The correct answer is to apologize, acknowledge the issue, request any needed evidence such as photos or order number, and offer a replacement or refund path according to policy.

Verification Method:
[ ] Rule-based: Check for an apology, a request for photos or order number, and an explicit replacement or refund option.
[ ] Human evaluation: A human would judge whether the message lowers tension and makes the customer feel heard.
[x] LLM-as-judge: Check for empathy, completeness, and a clear resolution path.

Primary Failure Mode:
Missing the apology, failing to explain the next step, or over-focusing on policy instead of resolution.

Why this prompt matters:
Complaint handling is a high-stakes support moment where a bad tone can escalate the situation. The model should lower frustration and move the case toward recovery.

## Prompt 3

Prompt #3: Product Compatibility Question

Prompt:
A customer asks: "Will your USB-C charger work with a 2021 Dell XPS 13 and fast charge it?"

Ground Truth:
[x] Yes - The correct answer is to avoid guessing if the exact wattage and device charging requirements are not known. The response should request the exact charger model or explain the general compatibility caveat.

Verification Method:
[ ] Rule-based: Check that the answer avoids saying it probably works unless the exact charger model or wattage is confirmed.
[ ] Human evaluation: A human would judge whether the answer is appropriately cautious for a technical compatibility question.
[x] LLM-as-judge: Check whether the answer avoids unsupported claims and asks for the missing specification.

Primary Failure Mode:
Fabricating compatibility or giving overconfident technical advice.

Why this prompt matters:
Product questions are where hallucinations are most damaging because customers may buy the wrong item or blame the retailer for bad advice.

## Prompt 4

Prompt #4: Missing Tracking Update

Prompt:
A customer says: "Your tracking page has not updated in four days. Where is my package?"

Ground Truth:
[x] Yes - The correct answer is to apologize, explain that the assistant cannot see live carrier data unless integrated, and give the next action such as checking order status, confirming address, or escalating to shipping support.

Verification Method:
[ ] Rule-based: Check for an apology, a statement that live carrier data is unavailable, and a next action such as order lookup or escalation.
[ ] Human evaluation: A human would judge whether the answer sounds honest and actually helps the customer move forward.
[x] LLM-as-judge: Check for transparency, helpfulness, and a practical next step.

Primary Failure Mode:
Pretending to know the package location or giving a generic non-answer.

Why this prompt matters:
Delivery issues are frequent in retail, and the assistant should not overclaim visibility into systems it does not have access to.

## Prompt 5

Prompt #5: Price Match Complaint

Prompt:
A customer says: "I bought this jacket last week and now it is on sale. I want the difference refunded."

Ground Truth:
[x] Yes - The correct answer is to avoid inventing a price-match policy. The response should say that the policy depends on the store rules, ask for the order number or receipt, and offer to check eligibility.

Verification Method:
[ ] Rule-based: Check that the assistant does not promise a refund and instead asks for the receipt or order number.
[ ] Human evaluation: A human would judge whether the answer is appropriately cautious and still useful.
[x] LLM-as-judge: Check for policy caution, clarity, and a helpful verification path.

Primary Failure Mode:
Making up a price-match policy or giving an unjustified promise.

Why this prompt matters:
This case checks whether the assistant can stay useful when the policy is unclear or branch-specific.

## Judge Prompt

Task Description:
You are evaluating a retail customer service assistant. The assistant should be helpful, polite, accurate about policy, and able to move the conversation toward resolution.

Evaluation Criteria:
1. Helpfulness: Does the response directly address the customer's issue and provide a useful next step?
2. Tone: Is the response calm, respectful, empathetic, and free of blame?
3. Policy adherence: Does the response avoid inventing policy or making unsupported promises?
4. Resolution quality: Does the response clearly move the case toward closure, escalation, or the correct support path?

Score Anchors:
1. Score 1: The response is materially wrong, evasive, or unsafe. It may invent policy, ignore the customer's issue, or fail to provide any useful next step.
2. Score 3: The response is directionally correct and partially helpful, but one or two criteria are weak. It may be polite but vague, cautious but incomplete, or helpful but not fully resolution-oriented.
3. Score 5: The response is fully aligned with the retail support goal. It is accurate, empathetic, specific, and gives a clear path to resolution without unsupported promises.

Reasoning Steps:
Step 1: Check whether the response answers the customer with the correct retail policy or a careful uncertainty statement.
Step 2: Check whether the tone is supportive and de-escalating.
Step 3: Check whether the response gives a concrete next action that a support agent or customer can follow.

Output Format:
{
  "score": 1,
  "reasoning": "Short explanation of the score.",
  "criteria_met": {
    "helpfulness": true,
    "tone": true,
    "policy_adherence": true,
    "resolution_quality": true
  }
}

## Bias Analysis
This judge can inherit several hidden biases. First, it may prefer concise, polished English and overrate responses that sound fluent even if they are incomplete. That is risky in customer support because a warm tone can hide a weak policy answer. Second, it may assume a particular retail policy or customer-service style that reflects a specific store culture rather than a universal standard. Third, it may reward hedged answers too much when the task actually requires a firm policy statement.

A second bias comes from the judge model's own alignment behavior. If the judge is trained to be overly helpful, it may give partial credit to responses that sound cooperative but never solve the problem. That would inflate scores on cases where the assistant should clearly escalate or deny a request. For this reason, the rubric should treat unsupported promises as serious errors even when the answer sounds polite.

## Calibration Strategy
Start with a small calibration set of clearly good, clearly bad, and borderline retail responses. Use those anchor examples to confirm that score 5 means policy-correct, empathetic, and action-oriented, while score 1 means wrong policy, poor tone, or no resolution path. If the judge is too strict, include one or two examples showing that short but correct answers can still score well. If the judge is too lenient, add explicit penalties for fabricated policy claims and vague non-answers.

I would also calibrate on failure type. A response that is polite but wrong on policy should score lower than a blunt but correct response, because correctness and resolution matter more than style alone. To reduce variance, keep temperature at 0, use structured JSON output, and rerun a few borderline cases to confirm that scores are stable enough for reporting.
