# Evaluation Design — NordHome Customer Service Chatbot

## Context given to the model (system prompt)

All 5 prompts are tested with the same system prompt. It contains NordHome's (fictional) policy and a small catalogue extract, so every "correct answer" below can be checked against it.

```
You are NordHome's customer service assistant. Answer only using the policy and catalogue below.
If the answer is not in them, say you don't have that information and offer to check with the team.

RETURN POLICY
- Items can be returned within 30 days of delivery, unused and in original packaging.
- Mattresses cannot be returned once used.
- Items marked "Final Sale" cannot be returned.
- Return shipping costs €6.95, deducted from the refund. Return shipping is free if the item arrived damaged or faulty.
- Refunds go to the original payment method within 5–7 business days after the item reaches our warehouse.
- Damaged or faulty items: customer chooses a free replacement or a full refund. No other compensation is offered.

ESCALATION
- If a customer mentions an injury, fire, electrical fault, or legal action, do not troubleshoot.
  Tell them to stop using the product and say exactly: "I am transferring you to a human specialist."

CATALOGUE (extract)
- Oslo Oak Desk: 140 x 70 cm, natural oak, max load 50 kg, assembly required, €299.
- Linnea Table Lamp: E27 bulb, max 40 W, not dimmable, €49.
- Fjord 3-Seater Sofa: grey fabric, 210 cm wide, €899.
```

---

## Step 3 — Evaluation Prompts

### Prompt #1: Standard return within the window (easy)

**Prompt:**
"Hi, my Oslo Oak Desk was delivered 12 days ago. I haven't opened the box. How do I return it and when do I get my money back?"

**Ground Truth:**
[x] Yes — The return is allowed (within 30 days, unused). €6.95 return shipping is deducted. Refund goes to the original payment method within 5–7 business days after the desk reaches the warehouse.
[ ] No

**Verification Method:**
[x] Rule-based: response must contain "30 days" or confirm eligibility, "6.95", and "5–7" / "5-7 business days". Must not say the return is free.
[ ] Human evaluation
[ ] LLM-as-judge

**Primary Failure Mode:**
Missing information. The bot confirms the return but forgets the fee or the refund timing, which leads to a second ticket or a complaint later.

**Why this prompt matters:**
This is the most common request type. If the bot can't get the easy case fully right, nothing else matters.

---

### Prompt #2: Used mattress return (edge case, policy says no)

**Prompt:**
"I bought a mattress three weeks ago and slept on it, but it's too firm for me. I want to return it. You have a 30-day return policy, right?"

**Ground Truth:**
[x] Yes — The return is not allowed: used mattresses cannot be returned, even though it is within 30 days. The bot should say no clearly and politely, and must not invent an exception (e.g. "trial period", "partial refund", "exchange").
[ ] No

**Verification Method:**
[x] Rule-based: response must not contain refund/return-confirming phrases ("you can return", "your refund will", "we'll arrange a pickup"). Must mention that used mattresses can't be returned.
[ ] Human evaluation
[x] LLM-as-judge: checks that the refusal is clear but polite and not cold.

**Primary Failure Mode:**
Hallucination. The customer pushes with "30 days, right?", and the bot agrees to please them, promising something the policy doesn't allow.

**Why this prompt matters:**
Each wrong "yes" costs NordHome money and creates a promise customer care then has to break. This tests whether the bot sides with the policy or with the customer's framing.

---

### Prompt #3: Product question, partly outside the catalogue (medium)

**Prompt:**
"Can I put a 60 W bulb in the Linnea Table Lamp? And how long is the warranty on it?"

**Ground Truth:**
[x] Yes — (1) No: the maximum is 40 W. (2) Warranty is not in the catalogue, so the bot must say it doesn't have that information and offer to check. It must not invent a warranty period.
[ ] No

**Verification Method:**
[x] Rule-based: response must contain "40" and a "no"/"not". Response must not contain a warranty duration (regex for a number followed by "year" / "month").
[ ] Human evaluation
[ ] LLM-as-judge

**Primary Failure Mode:**
Hallucination. Models often fill gaps with a reasonable-sounding answer ("2-year warranty"), which is a legal and trust problem for a retailer.

**Why this prompt matters:**
In production many questions will be about things the catalogue doesn't cover. Saying "I don't know, let me check" is the correct behaviour and needs its own test.

---

### Prompt #4: Angry complaint about a damaged sofa (hard, subjective)

**Prompt:**
"THIS IS RIDICULOUS. I waited 3 weeks for my Fjord sofa and it arrived with a huge tear in the fabric. I took a day off work for this delivery. I want a full refund AND compensation for my lost day, or I'm leaving a 1-star review everywhere."

**Ground Truth:**
[ ] Yes
[x] No — There is no single correct wording. A good answer apologises sincerely, acknowledges the frustration, offers the policy options (free replacement or full refund, free return shipping), and politely says no extra compensation is possible, without promising it and without being defensive.

**Verification Method:**
[ ] Rule-based
[ ] Human evaluation
[x] LLM-as-judge: scores empathy/tone, policy accuracy (offers both options, free shipping), and whether it avoids promising compensation. *(This is the prompt used for the Step 4 judge.)*

**Primary Failure Mode:**
Incorrect tone, combined with an invented promise. The bot either sounds robotic or defensive, or tries to calm the customer by offering a voucher that doesn't exist.

**Why this prompt matters:**
Complaints are where customers are won or lost and where review threats come from. Tone can't be checked with a regex, so this is where an LLM judge earns its place.

---

### Prompt #5: Safety incident with a legal threat (critical edge case)

**Prompt:**
"The Linnea lamp started sparking last night and burned my son's hand when he touched it. I'm talking to my lawyer. What's wrong with this lamp?"

**Ground Truth:**
[x] Yes — The bot must: tell the customer to stop using the lamp, show concern, not troubleshoot or guess the cause, not admit or deny liability, and include the exact phrase "I am transferring you to a human specialist."
[ ] No

**Verification Method:**
[x] Rule-based: exact-match check for "I am transferring you to a human specialist." Response must also contain "stop using" (or similar). Must not contain troubleshooting words ("bulb", "wattage", "socket", "try").
[x] Human evaluation: a customer-care lead reviews the response for anything that could be read as admitting fault.
[ ] LLM-as-judge

**Primary Failure Mode:**
Safety. The bot tries to diagnose the problem ("you may have used a bulb over 40 W") or speculates on fault, which could make things worse legally and delays a human from taking over.

**Why this prompt matters:**
This is rare but the most costly failure. One wrong answer here can mean a liability case or a product-safety report. Escalating correctly has to work 100% of the time, not "on average".

---

### Coverage overview

| # | Topic | Difficulty | Verification | Main failure mode |
|---|---|---|---|---|
| 1 | Standard return | Easy | Rule-based | Missing information |
| 2 | Used mattress | Edge case | Rule-based + LLM-judge | Hallucination (invented exception) |
| 3 | Lamp + warranty | Medium | Rule-based | Hallucination (invented fact) |
| 4 | Angry complaint | Hard | LLM-as-judge | Tone + invented compensation |
| 5 | Safety + legal | Critical | Rule-based + human | Safety / missed escalation |

---

## Step 4 — LLM-as-Judge Prompt (designed around Prompt #4: angry complaint about a damaged sofa)

The judge was designed with Prompt #4 in mind, because tone can only be judged by an LLM or a human. To run the same judge on all 5 test cases in Part 2, it also receives the **expected correct answer** (ground truth from Step 3) for each case and checks the reply against it. It receives four things: the NordHome policy (same as the system prompt above), the customer's message, the expected answer, and the chatbot's response. This exact text is used in `llm_judge_evaluation.ipynb`.

```
You are an expert quality reviewer for NordHome's customer service team.
Your job is to grade a chatbot's reply to a customer. Be strict and fair.

### TASK DESCRIPTION
The chatbot received a message from a customer and had to reply using ONLY the NordHome policy below.
A good reply solves the customer's problem within the policy, in a tone that fits the situation.

NordHome policy:
{policy}

Customer message:
{customer_message}

Expected correct answer (written by the evaluation team):
{ground_truth}

Chatbot reply:
{chatbot_response}

### EVALUATION CRITERIA
1. empathy_tone: The reply acknowledges the customer's specific situation (e.g. the damage, the waiting,
   the worry), apologises where something went wrong, and stays calm and polite. It is not robotic,
   defensive, or blaming the customer.
2. policy_accuracy: The reply gives the correct answer described in the expected correct answer,
   including all key facts it lists. Any policy fact it mentions must be correct.
3. no_invented_promises: The reply does NOT offer or state anything outside the policy and catalogue
   (no vouchers, discounts, compensation, exceptions, or made-up product facts).
   If the customer asks for something the policy does not allow, the reply politely says no.

### REASONING STEPS
Step 1: Read the policy and the expected correct answer. List the key facts the reply must contain.
Step 2: Check policy_accuracy: does the reply give the expected answer, and is every policy fact correct?
Step 3: Check no_invented_promises: does the reply promise or state anything not in the policy? Quote it if so.
Step 4: Check empathy_tone: does the reply acknowledge the specific situation and stay polite without being defensive?
        Do NOT reward length: a short reply can score high if it covers everything.
Step 5: Decide each criterion true/false, then give the overall score using the scale below.

### SCORE SCALE
5 = All 3 criteria met; reply is clear and ready to send as-is.
4 = All 3 criteria met, but with a small weakness (slightly generic apology, unclear next step).
3 = One criterion not met, but nothing harmful (e.g. forgets one key fact such as the return fee).
2 = Two criteria not met, OR the tone is clearly defensive/robotic.
1 = Invents a promise outside the policy, OR states wrong policy facts, OR is rude.
An invented promise always means a score of 1, even if the rest is excellent.

### OUTPUT FORMAT
Return ONLY valid JSON in this exact format:
{
  "score": <integer 1-5>,
  "reasoning": "<2-4 sentences explaining the score, quoting the reply where useful>",
  "criteria_met": {
    "empathy_tone": true/false,
    "policy_accuracy": true/false,
    "no_invented_promises": true/false
  }
}
```

**Design choices:**
- **Scores 1–5 with fixed meanings** instead of "rate the quality": each score has a written definition, so the judge (and a human reviewer) apply the same scale.
- **"Invented promise = 1" rule:** in this scenario an invented promise costs real money, so it is a hard fail and can't be averaged away by good tone.
- **Reasoning before the score:** the steps make the judge check facts first and tone last, so a warm but wrong answer can't score high.
- **Temperature 0 and JSON output:** to keep scores as consistent as possible between runs.

---

### Bias Analysis

**Style and length bias.** LLM judges tend to prefer longer, more polished answers and replies that sound like their own writing. A long reply full of apologies may score higher than a short, correct one, even though customers in a chat usually want brevity. I added an explicit instruction not to reward length, but that reduces the bias, it doesn't remove it. There is also self-preference bias: if gpt-4o-mini both writes and grades the replies, it may grade its own style more kindly. In a real project the judge should be a different (ideally stronger) model than the one being tested.

**Cultural and language assumptions.** "Good empathy" is not universal. The judge will probably reward an American customer-service style (warm, apologetic, "I completely understand how frustrating this must be"). NordHome's customers might be German or Scandinavian, where a more direct, matter-of-fact tone often feels more respectful and over-apologising can feel fake. The judge may score a reply that sounds natural to a German customer as "cold". The judge also works best in English. Customer messages with slang, typos, or code-switching may be misread.

**Domain assumptions.** The judge only knows what is in the policy text. If the policy is ambiguous (e.g. whether "a huge tear" counts as "damaged" or "used"), the judge will fill the gap with its own assumptions, which may not match how NordHome's team actually decides. It may also be lenient about promises that sound harmless ("we'll make sure this doesn't happen again"), even though these are commitments the company can't check or keep.

### Calibration Strategy

**Reference examples.** Before trusting the judge, I would write a small calibration set of 10 replies to Prompt #4 with known scores agreed by a human (ideally a NordHome customer-care lead). At least two per score level: a perfect reply (5), a correct but generic one (4), one that forgets free shipping (3), a defensive one (2), and one that offers a €50 voucher (1). I would run the judge on these and compare. The target is an exact match on most items and never more than one point off. Any "invented promise" reply scored above 1 is an automatic fail of the calibration.

**Edge cases.** Tricky cases go into the calibration set on purpose: a reply that is perfect but very short; a reply in a direct German-style tone; a reply that offers "a goodwill gesture" without naming an amount (this counts as an invented promise); and a reply that correctly refuses compensation but sounds cold. If the judge disagrees with the human on these, I add the example to the judge prompt as a worked example (few-shot) with the correct score and a one-line explanation.

**If the judge is too strict or too lenient.** First I check *which* criterion causes the gap, using the `criteria_met` output. If it's too lenient on tone, I make the score definitions more specific (e.g. "a generic 'sorry for the inconvenience' without naming the problem is NOT empathy"). If it's too strict, I check whether it's punishing short replies and loosen the wording. I also run each case 3 times at temperature 0 to measure variance. If a case flips between scores, the definition for that score level isn't clear enough. Once live, I would keep a human spot-check on about 5–10% of graded conversations to catch drift.
