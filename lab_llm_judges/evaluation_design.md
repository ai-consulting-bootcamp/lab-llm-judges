# Evaluation Design — Retail Customer Service Chatbot

## 5 Custom Evaluation Prompts

---

### Prompt #1: Standard Return Request

**Prompt:**
> A customer writes: "Hi, I bought a pair of running shoes (Order #ORD-88214) two weeks ago and they don't fit right. The arch support is way too high and it's causing me foot pain. I'd like to return them. What do I need to do?"
>
> Company policy: Returns accepted within 30 days of purchase. Items must be unworn and in original packaging. Footwear worn outdoors is not eligible for return. Refund to original payment method within 5–7 business days.
>
> Respond as the customer service chatbot.

**Ground Truth:**
[x] Yes — The response should: (1) acknowledge the customer's discomfort, (2) confirm the order is within the 30-day window, (3) ask whether the shoes have been worn outdoors, (4) explain the return process including packaging requirements, (5) mention the 5–7 business day refund timeline.

**Verification Method:**
[x] LLM-as-judge — Judge evaluates empathy, policy accuracy, completeness, and whether the chatbot correctly asks about outdoor use before confirming the return.

**Primary Failure Mode:**
Omitting the critical eligibility check (outdoor wear) and directly promising a return without verifying the condition. This could lead to the retailer accepting returns on worn shoes.

**Why this prompt matters:**
Returns are the most common customer service interaction. Getting the policy right while maintaining empathy is the minimum bar for deployment. A chatbot that skips eligibility checks or misquotes timelines creates operational and financial risk.

---

### Prompt #2: Out-of-Stock Product Inquiry

**Prompt:**
> Customer message: "I've been looking at the EcoBreeze Portable Fan (SKU: EB-4420) on your website for weeks and it keeps saying out of stock. When will it be available again? I really need it before summer. Can you check for me?"
>
> Internal data: The EcoBreeze Portable Fan is discontinued and will not be restocked. A successor model, the EcoBreeze Pro Fan (SKU: EB-5500), launches next month at $10 more than the original.
>
> Respond as the customer service chatbot.

**Ground Truth:**
[x] Yes — The response should: (1) not promise restocking, (2) clearly state the product is discontinued, (3) suggest the upcoming EcoBreeze Pro as an alternative, (4) not fabricate an availability date for the original product, (5) offer to notify the customer when the Pro model launches.

**Verification Method:**
[x] Rule-based + LLM-as-judge — Rule-based: check that the response does NOT contain phrases like "will be back in stock" or fabricated dates. LLM-as-judge: evaluate how diplomatically the discontinuation is communicated and whether the alternative suggestion feels helpful.

**Primary Failure Mode:**
Hallucination — the model invents a restock date or falsely promises availability. This is a critical failure because it sets incorrect customer expectations and damages trust.

**Why this prompt matters:**
Discontinued products are a common edge case that tests whether the model respects the provided data or defaults to optimistic but false reassurances. Hallucinated availability dates are among the most damaging chatbot errors in retail.

---

### Prompt #3: Angry Customer Complaint (Tone Stress Test)

**Prompt:**
> Customer message: "This is absolutely ridiculous. I ordered a birthday gift for my daughter THREE WEEKS AGO and it still hasn't arrived. The tracking hasn't updated in 10 days. I paid for express shipping!! I want a full refund AND the item. This is the worst shopping experience I've ever had. I'm telling everyone to avoid your store."
>
> Internal data: Order #ORD-70331, placed 21 days ago. Express shipping selected. Carrier tracking shows package stuck at regional hub since day 11. Estimated delivery was day 5. No insurance purchased.
>
> Company policy: If express shipping exceeds the guaranteed delivery window, customer receives a shipping refund. Item refund requires the package to be formally declared lost by the carrier (30+ days). Customers can file a carrier investigation after 15 days.
>
> Respond as the customer service chatbot.

**Ground Truth:**
[x] Yes — The response should: (1) empathize with the situation without being defensive, (2) acknowledge this is about a child's birthday, (3) offer a shipping refund immediately since the express guarantee was missed, (4) explain the carrier investigation process, (5) NOT promise a full item refund yet since the package has not been declared lost, (6) remain professional and calm despite the hostile tone.

**Verification Method:**
[x] LLM-as-judge — Judge evaluates: emotional tone (empathetic but professional, not defensive or sycophantic), policy accuracy (shipping refund yes, full refund premature), de-escalation quality, and whether the chatbot avoids matching the customer's hostility.

**Primary Failure Mode:**
Incorrect tone — either being overly apologetic and promising refunds beyond what policy allows (creating financial liability) or being too rigid and policy-focused, ignoring the emotional context (escalating the situation).

**Why this prompt matters:**
Angry customers are the highest-stakes interaction. The chatbot must simultaneously de-escalate, follow policy, and avoid making unauthorized promises. This tests the model's ability to handle emotional pressure while maintaining accuracy.

---

### Prompt #4: Cross-Sell During Support (Boundary Test)

**Prompt:**
> Customer message: "Hey, quick question — does the bamboo cutting board you sell work okay in the dishwasher? I bought one last month and want to make sure I'm caring for it properly."
>
> Product info: The Bamboo Cutting Board (SKU: BCB-200) is NOT dishwasher safe. Must be hand-washed with mild soap and dried immediately. Periodic oiling with food-grade mineral oil recommended. The store also sells a Bamboo Care Oil Kit (SKU: BCO-100, $12.99).
>
> Company guideline: Support agents may mention complementary products ONLY if directly relevant to the customer's question. Do not push unrelated products. Recommendations should feel natural, not salesy.
>
> Respond as the customer service chatbot.

**Ground Truth:**
[x] Yes — The response should: (1) clearly state the board is NOT dishwasher safe, (2) provide care instructions (hand wash, dry immediately), (3) mention the oiling recommendation, (4) optionally and naturally mention the Bamboo Care Oil Kit since it is directly relevant, (5) NOT aggressively upsell or mention unrelated products.

**Verification Method:**
[x] LLM-as-judge — Judge evaluates: accuracy of the dishwasher safety warning, completeness of care instructions, whether any product mention feels natural versus forced, and whether the response stays focused on the customer's actual question.

**Primary Failure Mode:**
Missing information — failing to clearly state the board is not dishwasher safe (burying the answer in general care advice) or going overboard on cross-selling, turning a simple care question into a sales pitch.

**Why this prompt matters:**
This tests whether the model can balance being helpful with being appropriately restrained. Over-selling erodes trust; under-informing risks product damage. The prompt also tests whether the model prioritizes the safety-critical information (not dishwasher safe) over secondary details.

---

### Prompt #5: Multi-Issue Request (Complexity Test)

**Prompt:**
> Customer message: "Hi, I have a few things I need help with:
> 1. My last order (#ORD-55102) arrived with a cracked ceramic mug. I want a replacement, not a refund.
> 2. I have a gift card with code GC-8827-AXKP and I'm not sure how much is left on it.
> 3. Can you update my shipping address to 42 Elm Street, Portland, OR 97201 for future orders?
>
> Thanks!"
>
> Internal data: Order #ORD-55102 contains a ceramic mug (damaged noted in photo upload), a candle, and a tea towel. Replacement mugs in stock. Gift card GC-8827-AXKP has $14.50 remaining. Address update requires identity verification (last 4 digits of payment card on file).
>
> Respond as the customer service chatbot.

**Ground Truth:**
[x] Yes — The response should address ALL three issues: (1) confirm replacement mug will be shipped (since damage is verified and stock exists), (2) provide the $14.50 gift card balance, (3) explain that the address update requires identity verification and ask for last 4 digits. No issue should be skipped or merged with another.

**Verification Method:**
[x] Rule-based + LLM-as-judge — Rule-based: check for presence of "$14.50", "42 Elm Street" or address reference, order number "#ORD-55102", and some form of verification request. LLM-as-judge: evaluate whether each issue is handled clearly and separately, and whether the response feels organized rather than jumbled.

**Primary Failure Mode:**
Incomplete response — the model addresses one or two issues but drops the third, or conflates them in a confusing way. Multi-part requests are a known failure mode where models tend to focus on the first or most emotionally salient item and neglect the rest.

**Why this prompt matters:**
Real customer service tickets frequently contain multiple requests. A chatbot that only partially resolves a ticket forces the customer to write back, increasing support volume and frustration. This tests both comprehensiveness and organizational clarity.

---

## LLM-as-Judge Prompt Design

### Selected Prompt: Prompt #3 — Angry Customer Complaint

#### Task Description

You are evaluating a customer service chatbot's response to an angry customer whose express-shipped birthday gift is severely delayed. The customer is hostile and demands a full refund plus the item. The chatbot has access to order data showing the package is stuck at a carrier hub (not yet officially lost) and company policy that allows a shipping refund but requires 30+ days for an item refund.

#### Evaluation Criteria

1. **Empathy & Tone** — Does the response acknowledge the customer's frustration and the personal context (daughter's birthday) without being defensive, dismissive, or excessively sycophantic?
2. **Policy Accuracy** — Does the response correctly offer a shipping refund (policy-compliant) while NOT prematurely promising a full item refund (which is not yet authorized per policy)?
3. **De-escalation Quality** — Does the response calm the situation by validating feelings, providing concrete next steps, and avoiding language that could further inflame the customer?
4. **Completeness** — Does the response address the shipping refund, explain the carrier investigation process, and provide a clear path forward with realistic timelines?
5. **Professional Boundaries** — Does the response avoid matching the customer's hostile tone, avoid blaming the carrier excessively, and avoid making unauthorized promises?

#### Reasoning Steps

Step 1: Read the chatbot's response and check if it acknowledges the emotional context (birthday, frustration). Score empathy.

Step 2: Compare every factual claim and promise in the response against the provided policy. Flag any promise of a full item refund as a policy violation. Confirm that a shipping refund is offered.

Step 3: Assess the overall tone — is it calm, professional, and human? Or is it robotic/dismissive/overly apologetic? Check for de-escalation techniques (validation, concrete actions, timeline).

Step 4: Verify completeness — are all actionable next steps mentioned? (Shipping refund, carrier investigation filing, what happens if the package is declared lost.)

Step 5: Check for boundary violations — does the chatbot make promises beyond its authority, blame third parties excessively, or respond emotionally to the hostility?

#### Output Format

```json
{
  "score": "[1-5 scale: 1=critical failures, 2=major issues, 3=acceptable, 4=good, 5=excellent]",
  "reasoning": "[2-4 sentences explaining the overall assessment]",
  "criteria_met": {
    "empathy_and_tone": true/false,
    "policy_accuracy": true/false,
    "de_escalation_quality": true/false,
    "completeness": true/false,
    "professional_boundaries": true/false
  },
  "critical_failures": "[List any critical errors like wrong policy information or hostile tone, or 'none']"
}
```

#### Full Judge System Prompt

```
You are an expert evaluator assessing customer service chatbot responses for a retail company. You must evaluate strictly against the criteria below. Be fair but rigorous — a deployed chatbot must get these right.

CONTEXT:
- A customer is furious about a 3-week delayed express shipment meant as a birthday gift for their daughter.
- Order tracking shows the package is stuck at a carrier hub (day 11 of being stuck, day 21 since order).
- Company policy: shipping refund is owed because the express guarantee was missed. Full item refund requires the carrier to formally declare the package lost (30+ days). Customer can file a carrier investigation after 15 days.
- The customer demands a full refund AND the item.

EVALUATION CRITERIA:
1. Empathy & Tone: The response must acknowledge frustration and the birthday context. It should sound human, warm, and professional — not robotic or scripted. It must not be defensive or dismissive.
2. Policy Accuracy: The response MUST offer a shipping refund. The response must NOT promise a full item refund at this stage. If the response promises both a full refund and the item, this is a critical policy violation.
3. De-escalation Quality: The response should validate feelings before jumping to policy. It should provide concrete next steps rather than vague reassurances. It should not use corporate jargon excessively.
4. Completeness: The response should cover (a) empathy/acknowledgment, (b) shipping refund offer, (c) carrier investigation process, (d) what happens next if the package is declared lost, (e) any immediate alternatives (e.g., reorder at a discount).
5. Professional Boundaries: The response should not match the customer's hostility, should not make unauthorized promises, and should not excessively blame the shipping carrier.

SCORING GUIDE:
- 5 (Excellent): All criteria met, empathetic and accurate, could be sent as-is.
- 4 (Good): Minor issues (e.g., slightly robotic tone, one missing detail) but policy-accurate.
- 3 (Acceptable): Mostly correct but has a notable gap (e.g., missing carrier investigation mention or slightly off tone).
- 2 (Major Issues): Policy error or significant tone problem (too defensive, too sycophantic, or missing the shipping refund).
- 1 (Critical Failure): Promises unauthorized refund, responds hostilely, or contains factual errors about the order.

Respond ONLY with valid JSON matching this schema:
{
  "score": <integer 1-5>,
  "reasoning": "<string>",
  "criteria_met": {
    "empathy_and_tone": <boolean>,
    "policy_accuracy": <boolean>,
    "de_escalation_quality": <boolean>,
    "completeness": <boolean>,
    "professional_boundaries": <boolean>
  },
  "critical_failures": "<string>"
}
```

---

## Bias Analysis

**Hidden biases the judge might have:**

The judge prompt likely carries a verbosity bias — LLM judges tend to reward longer, more detailed responses even when a concise answer would serve the customer better. A short, empathetic, policy-accurate response that gets straight to the point might score lower than a verbose one that rehashes every detail, simply because the judge equates length with thoroughness. This is particularly problematic in customer service, where overly long responses can feel bureaucratic and actually worsen the customer experience.

There is also a potential cultural bias in how "empathy" is defined. The judge prompt assumes a Western communication style where explicitly naming emotions ("I understand how frustrating this must be") signals empathy. In some cultural contexts, empathy is expressed through action (immediately offering the refund) rather than verbal validation. A response that jumps straight to solving the problem without emotional preamble might score lower on empathy despite being culturally appropriate for some customer bases.

Finally, the judge may have a style bias toward formal, polished language. A response that uses casual, friendly phrasing ("That's really rough, I'm sorry") might score lower than one using corporate-professional language ("I sincerely apologize for the inconvenience"), even though research on customer satisfaction suggests warmth often outperforms formality in support contexts.

---

## Calibration Strategy

**Reference examples for calibration:**

To calibrate the judge, I would prepare 4–6 anchor responses at known quality levels. A "5" anchor would be a response that was validated by experienced customer service managers as deployment-ready. A "1" anchor would contain a clear policy violation (promising a full refund when not authorized). Mid-range anchors (2, 3, 4) would each have one specific, identifiable flaw — for example, a "3" might be policy-accurate but emotionally flat. I would include these anchors as few-shot examples in the judge prompt so the LLM can calibrate its internal scoring scale against concrete references rather than abstract descriptions.

**Handling edge cases and calibration drift:**

For edge cases — such as a response that is factually perfect but written in broken English, or one that is beautifully empathetic but misses a policy detail — I would run the judge multiple times (3–5 runs at temperature 0) and average the scores. If variance exceeds 1 point across runs, the case is flagged for human review. This approach accepts that LLM judges have inherent variance and builds that into the evaluation pipeline rather than pretending each judgment is deterministic.

If testing reveals the judge is consistently too strict (average scores below 2.5 across known-good responses) or too lenient (scoring known-bad responses above 3), I would adjust the scoring guide anchors. Rather than changing the criteria, I would add more calibration examples at the problematic score levels. The goal is to shift the score distribution without changing what the judge looks for, which preserves criterion validity while fixing calibration.
