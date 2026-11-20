# Evaluation Design – AI Food Concierge

## Step 3 – Custom Evaluation Prompts

### Prompt #1: Budget and Dietary Restrictions

**Prompt:**

You are an AI Food Concierge. Recommend exactly one Italian restaurant that offers vegan options and costs no more than €30 per person.

Use only the following synthetic restaurant data:

- Trattoria Verde: Italian, €24 per person, vegan options available.
- Pasta Porto: Italian, €28 per person, no vegan options.
- Osteria Luna: Italian, €35 per person, vegan options available.

Provide the restaurant name and a brief explanation based only on the supplied information.

**Ground Truth:**

- [x] Yes – Trattoria Verde is the only restaurant satisfying all constraints: Italian cuisine, vegan options, and a price of €30 or less.
- [ ] No

**Verification Method:**

- [x] Rule-based: Verify that the response recommends Trattoria Verde and does not recommend Pasta Porto or Osteria Luna.
- [x] LLM-as-judge: Assess whether the explanation correctly reflects the supplied data without introducing unsupported claims.
- [ ] Human evaluation

**Primary Failure Mode:**

Failure to respect multiple constraints simultaneously, particularly recommending a restaurant that exceeds the budget or does not offer vegan options.

**Why this prompt matters:**

The AI Food Concierge must consistently respect user constraints when generating recommendations. This test provides an objectively verifiable example of whether the model can select a suitable restaurant from a controlled dataset.

### Prompt #2: Missing Information and Hallucination Prevention

**Prompt:**

You are an AI Food Concierge. A user asks:

"Does Trattoria Verde offer gluten-free pasta?"

Use only the following synthetic restaurant data:

- Restaurant: Trattoria Verde
- Cuisine: Italian
- Average price: €24 per person
- Vegan options: Available
- Gluten-free options: Not specified

Answer the user's question clearly and briefly. Do not introduce information that is not supported by the provided data.

**Ground Truth:**

- [x] Yes – The available data does not specify whether Trattoria Verde offers gluten-free pasta. The model must acknowledge this uncertainty and avoid confirming or denying availability.
- [ ] No

**Verification Method:**

- [ ] Rule-based
- [x] LLM-as-judge: Evaluate whether the response accurately communicates the missing information and avoids unsupported claims.
- [x] Human evaluation: Assess whether the response communicates uncertainty clearly and helpfully.

**Primary Failure Mode:**

Hallucination – the model incorrectly claims that gluten-free pasta is available or unavailable despite insufficient information.

**Why this prompt matters:**

Restaurant datasets may contain incomplete information. The AI Food Concierge must distinguish between confirmed facts and unknown details to avoid misleading users, particularly when dietary requirements are involved.

### Prompt #3: Multi-Turn Context Retention

**Prompt:**

You are an AI Food Concierge. Use only the following synthetic restaurant data:

- Trattoria Verde: Italian, €24 per person, vegan options available.
- Pasta Porto: Italian, €28 per person, no vegan options.
- Osteria Luna: Italian, €35 per person, vegan options available.

Conversation:

User: "I am looking for an Italian restaurant with a budget of €30 per person."

Assistant: "Trattoria Verde and Pasta Porto both fit your budget."

User: "Actually, I also need vegan options. Which restaurant should I choose?"

Respond to the user's latest message while respecting all previously stated requirements.

**Ground Truth:**

- [x] Yes – The correct recommendation is Trattoria Verde because it offers Italian cuisine, costs €24 per person, and provides vegan options. Pasta Porto does not offer vegan options, while Osteria Luna exceeds the original budget.
- [ ] No

**Verification Method:**

- [x] Rule-based: Verify that Trattoria Verde is recommended and neither Pasta Porto nor Osteria Luna is recommended as a suitable alternative.
- [x] LLM-as-judge: Evaluate whether the response correctly retains the original budget constraint and incorporates the new dietary requirement.
- [ ] Human evaluation

**Primary Failure Mode:**

Context loss – the model forgets the original budget constraint or fails to apply the newly introduced vegan requirement.

**Why this prompt matters:**

Users frequently modify their preferences during a conversation. The AI Food Concierge must preserve relevant previous requirements while incorporating new information to generate consistent recommendations.

---

### Prompt #4: Conflicting Constraints and No Suitable Match

**Prompt:**

You are an AI Food Concierge. A user asks:

"Please recommend an Italian restaurant that offers vegan options and costs no more than €20 per person."

Use only the following synthetic restaurant data:

- Trattoria Verde: Italian, €24 per person, vegan options available.
- Pasta Porto: Italian, €28 per person, no vegan options.
- Osteria Luna: Italian, €35 per person, vegan options available.

Recommend a restaurant only if it satisfies all requirements. If none qualifies, explain the situation briefly and suggest which constraint the user could reconsider. Do not invent additional restaurants.

**Ground Truth:**

- [x] Yes – None of the available restaurants satisfies all requirements. The model should explicitly state that no suitable match exists and may suggest increasing the budget to at least €24 per person to include Trattoria Verde.
- [ ] No

**Verification Method:**

- [x] Rule-based: Verify that no restaurant is presented as satisfying the €20 budget and vegan requirement simultaneously.
- [x] LLM-as-judge: Evaluate whether the explanation is accurate, transparent, and provides a reasonable suggestion without violating the original constraints.
- [ ] Human evaluation

**Primary Failure Mode:**

Constraint violation – the model recommends a restaurant that does not meet the user's requirements instead of acknowledging that no suitable match exists.

**Why this prompt matters:**

Real restaurant searches may produce no valid matches. The AI Food Concierge must communicate such limitations accurately instead of prioritizing a recommendation over the user's explicit requirements.

---

### Prompt #5: Structured Output and Instruction Following

**Prompt:**

You are an AI Food Concierge. Select the cheapest Italian restaurant that offers vegan options and costs no more than €30 per person.

Use only the following synthetic restaurant data:

- Trattoria Verde: Italian, €24 per person, vegan options available.
- Pasta Porto: Italian, €28 per person, no vegan options.
- Osteria Luna: Italian, €35 per person, vegan options available.

Return your answer as a valid JSON object using exactly these three keys:

- "restaurant"
- "price_eur"
- "reason"

The "restaurant" value must be a string, "price_eur" must be a number, and "reason" must be a short string explaining why the restaurant meets the requirements.

Do not include Markdown formatting, additional keys, or text outside the JSON object.

**Ground Truth:**

- [x] Yes – The model must select Trattoria Verde with a numeric price of 24 and an explanation reflecting the vegan and budget requirements.

Expected output example:

```json
{
  "restaurant": "Trattoria Verde",
  "price_eur": 24,
  "reason": "Italian restaurant with vegan options within the €30 budget."
}
```

- [ ] No

**Verification Method:**

- [x] Rule-based: Parse the response as JSON and verify the exact keys, required data types, correct restaurant name, and numeric price.
- [x] LLM-as-judge: Assess whether the explanation is factually consistent with the supplied data and correctly justifies the selection.
- [ ] Human evaluation

**Primary Failure Mode:**

Instruction-following failure – the model returns invalid JSON, incorrect values, unsupported explanations, or additional text that violates the requested format.

**Why this prompt matters:**

Structured responses are important when integrating LLM outputs into automated applications. The AI Food Concierge must produce machine-readable results that follow a predefined schema while maintaining factual accuracy.

---

## Step 4 – LLM-as-Judge Design

### Selected Evaluation Task

**Prompt #1: Budget and Dietary Restrictions**

The LLM-as-Judge evaluates whether an AI Food Concierge correctly selects a restaurant from a controlled synthetic dataset while respecting the user's requirements.

### 1. Task Description

The evaluated model is asked to recommend exactly one Italian restaurant that offers vegan options and costs no more than €30 per person.

The available synthetic restaurant data is:

- Trattoria Verde: Italian, €24 per person, vegan options available.
- Pasta Porto: Italian, €28 per person, no vegan options.
- Osteria Luna: Italian, €35 per person, vegan options available.

**Ground Truth:** Trattoria Verde is the only restaurant satisfying all requirements.

The judge receives the original task prompt and the evaluated model's response. It must assess the response exclusively against the provided information, without relying on external knowledge.

### 2. Evaluation Criteria

**Criterion 1 – Recommendation Accuracy**

The response must recommend exactly one restaurant: Trattoria Verde.

- The selected restaurant must satisfy all user requirements.
- No unsuitable restaurant may be recommended as an additional option.

**Criterion 2 – Factual Consistency**

The response must accurately represent the provided restaurant data.

- Trattoria Verde costs €24 per person.
- Vegan options are available.
- No unsupported restaurant properties, services, or availability claims may be introduced.

**Criterion 3 – Explanation Quality**

The response must provide a brief, understandable explanation of why the selected restaurant meets the user's requirements.

- The explanation should reference relevant constraints.
- It should be clear and factually supported.
- Unnecessary information should not influence the score.

### 3. Reasoning Steps

The judge must perform the following checks before assigning a score:

**Step 1 – Check Recommendation Accuracy**

Identify the restaurant recommended by the evaluated model. Compare it with the ground truth and determine whether exactly one suitable restaurant was selected.

**Step 2 – Check Factual Consistency**

Compare all factual statements in the response against the synthetic restaurant dataset. Identify incorrect or unsupported claims.

**Step 3 – Check Explanation Quality**

Determine whether the response clearly explains why the restaurant meets the user's requirements. Focus on correctness and clarity rather than writing style or response length.

**Step 4 – Assign a Score**

Apply the following scoring rubric:

| Score | Description |
|---|---|
| 5 | Correct recommendation, accurate information, and clear explanation of all relevant constraints. |
| 4 | Correct recommendation and accurate information, but explanation is incomplete or vague. |
| 3 | Correct recommendation, but response contains an unsupported or materially inaccurate additional claim. |
| 2 | Incorrect recommendation, although parts of the explanation demonstrate some understanding of the requirements. |
| 1 | Incorrect or missing recommendation with substantial violations of the requirements. |

The judge must assess each criterion independently and provide a concise explanation of the final score.

### 4. Judge Prompt and Output Format

**System Prompt:**

You are an impartial LLM evaluator assessing the quality of AI Food Concierge responses.

Evaluate the candidate response using only the original prompt, the supplied restaurant data, and the established ground truth.

Follow these rules:

1. Assess recommendation accuracy, factual consistency, and explanation quality independently.
2. Do not use external restaurant information or make assumptions beyond the supplied data.
3. Do not reward unnecessarily long or elaborate responses.
4. Do not penalize concise responses when they satisfy all requirements.
5. Apply the scoring rubric consistently.
6. Return a valid JSON object only, without Markdown formatting or additional commentary.

**User Prompt Template:**

Original task:

`{original_prompt}`

Candidate model response:

`{model_response}`

Ground truth:

Trattoria Verde is the only correct recommendation. It is an Italian restaurant costing €24 per person and offering vegan options.

Evaluate the candidate response according to the three criteria and the scoring rubric.

Return exactly this JSON structure:

```json
{
  "score": 5,
  "reasoning": "Brief evidence-based explanation of the assigned score.",
  "criteria_met": {
    "criterion_1": true,
    "criterion_2": true,
    "criterion_3": true
  }
}
```

The score must be an integer between 1 and 5.

Each criterion must be represented by a Boolean value. The reasoning must explain any criteria that were not met.

The JSON structure above is an example of the required output format, not a predetermined evaluation result.

---

### 5. Bias Analysis

**Potential Hidden Biases**

An LLM-as-Judge may favor responses that are longer, more detailed, or written in a particular style, even when shorter answers are equally correct. It may also prefer familiar wording or expressions that resemble its own typical responses. These preferences could influence the final score independently of factual accuracy.

In the AI Food Concierge scenario, the judge may also rely on assumptions about restaurant services, dietary requirements, or pricing. For example, it might infer that an Italian restaurant offers particular dishes without supporting evidence. To reduce these risks, the judge is explicitly instructed to evaluate only the supplied synthetic data and use clearly defined criteria rather than subjective preferences.

### 6. Calibration Strategy

**Reference Examples and Consistency**

Before using the judge in the complete evaluation, it should be tested against a small set of reference responses with known quality levels. These should include a fully correct recommendation, a recommendation that violates the budget constraint, and a response that invents unsupported restaurant details. The expected scores should be assigned in advance based on the evaluation rubric.

**Handling Edge Cases and Score Adjustment**

Edge cases should include responses that recommend the correct restaurant but provide incomplete explanations, or responses that include correct information alongside unsupported claims. If the judge consistently assigns scores that are too strict or too lenient compared with the reference evaluations, the scoring descriptions should be clarified and the reference examples tested again. Human review of disagreements can help improve calibration. Because LLM judgments may vary between runs, repeated evaluations can also be used to assess scoring consistency.