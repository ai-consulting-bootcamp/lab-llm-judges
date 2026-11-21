# Evaluation Design · Kleinanzeigen buyer-support chatbot

**Author:** Ayhan Demir · **Date:** 2026-11-20

## The answer key: policy sheet
All ground truth comes from this sheet. The chatbot gets the same sheet in its system prompt, so the test checks whether it **follows** the policy, not whether it remembers it.

Sources: rules 1-5 come from the Kleinanzeigen help page "Was ist „Sicher bezahlen“ - wie funktioniert der Käuferschutz?" (hilfe.kleinanzeigen.de, article 17211553583388), checked on 2026-11-20. That the buyer pays the service fee is stated by several secondary sources (e-recht24, paycal) and matches the help page's cost list. Rules 6-8 are lab assumptions; the fraud steps in rule 7 follow Verbraucherzentrale advice.

```text
Kleinanzeigen "Sicher bezahlen" policy (lab version, checked 2026-11-20)
1. "Sicher bezahlen" is Kleinanzeigen's payment system. Buyer protection (Kaeuferschutz) only covers purchases paid with "Sicher bezahlen".
2. The buyer pays: the item price set by the seller, shipping costs (depending on the carrier), and a service fee of 0.50 EUR + 4.5% of the purchase price.
3. Buyer protection applies when: the item was not shipped; the delivered item differs strongly from the description; the item is counterfeit; a wrong or incomplete item was delivered.
4. If the seller does not ship: the buyer gets the full item price back, including shipping costs if a Hermes label was created. With a DHL label that was not cancelled, the label cost stays with the carrier.
5. If the item differs significantly from the description: the buyer gets the item price back. Return shipping costs are not refunded.
6. (lab assumption) The buyer reports a problem in the Kleinanzeigen app or website, from the purchase. The support assistant cannot open orders, listings, chats or payments and cannot issue refunds itself.
7. (lab assumption) Payments outside "Sicher bezahlen" (for example bank transfer or PayPal) are not covered by buyer protection. For suspected fraud, advise: report the user or listing to Kleinanzeigen, contact your bank, and file a police report.
8. (lab assumption) The assistant cannot see listings. For questions about an item (condition, availability, accessories), the buyer should message the seller through the listing.
```

## Step 3 · Five evaluation prompts
Difficulty: 2 easy, 2 medium, 1 hard. Keyword rules accept English and German words, so a reply in the wrong language is counted once, by the language rule. Each prompt is based on a customer intent from the Bitext retail e-commerce dataset (Hugging Face, CDLA-Sharing 1.0) and rewritten for Kleinanzeigen. Human evaluation is not used in this lab (out of scope); every prompt has a rule-based check plus the LLM judge.

| # | Title | Requirement covered | Difficulty | Bitext intent |
|---|---|---|---|---|
| 1 | Return, item not as described | Returns | Medium | `return_product` |
| 2 | Question about an item the bot cannot see | Product questions | Easy | `availability_online` |
| 3 | Angry complaint, scam after bank transfer | Complaints, safety | Hard | `payment_issue` (tag W, offensive) |
| 4 | Seller has not shipped | Returns, refund | Medium | `delivery_issue` |
| 5 | Fee question in German | Product questions, language | Easy | `payment_methods` |

### Prompt #1: Return, item not as described
**Prompt:**
> I bought a used phone for 180 € with "Sicher bezahlen". The screen has a big crack that was not in the photos or the description. Can I send it back and get my money back?

**Ground Truth:**
[x] Yes - Covered by buyer protection: the item differs strongly from the description (rule 3). Report the problem from the purchase in the app or website (rule 6). If accepted, the item price (180 €) is refunded; return shipping costs are not (rule 5). The bot cannot issue the refund itself (rule 6).
[ ] No

**Verification Method:**
[x] Rule-based: mentions buyer protection ("buyer protection" or "Käuferschutz"); reply in English; max 150 words.
[ ] Human evaluation
[x] LLM-as-judge: are the refund facts right (item price yes, return shipping no), is the next step there, is the tone empathetic?

**Primary Failure Mode:**
Hallucination: promising a full refund including return shipping, or online-shop rules such as a fixed return window.

**Why this prompt matters:**
"Not as described" is the classic marketplace return. Wrong refund details create false expectations and a second complaint.

### Prompt #2: Question about an item the bot cannot see
**Prompt:**
> Hi, is the "Kinderfahrrad 20 Zoll" in the listing still available, and does it come with lights? I want to buy it today.

**Ground Truth:**
[x] Yes - The bot cannot see listings, so it must not say whether the bike is available or has lights (rule 8). Next step: message the seller through the listing.
[ ] No

**Verification Method:**
[x] Rule-based: mentions the seller and a way to reach them ("message", "chat", "contact", "write", "ask", or the German equivalents); reply in English; max 150 words.
[ ] Human evaluation
[x] LLM-as-judge: no invented availability or features, a clear next step, friendly tone.

**Primary Failure Mode:**
Hallucination: inventing "yes, it is available and has lights".

**Why this prompt matters:**
Product questions are frequent and look easy. A confident made-up answer damages trust in the seller and in the platform (CoCoNot's "unsupported request" category).

### Prompt #3: Angry complaint, scam after bank transfer
**Prompt:**
> This is a joke!!! Your useless site let a scammer take my 250 euros. I paid the seller by bank transfer for a PS5 and now he blocked me. Give me my money back NOW or I'm going to the press.

**Ground Truth:**
[x] Yes - A bank transfer is outside "Sicher bezahlen", so buyer protection does not cover it and Kleinanzeigen cannot refund it (rules 1, 7). Next steps: report the user or listing to Kleinanzeigen, contact the bank right away, file a police report (rule 7). No refund promise and no blaming the customer.
[ ] No

**Verification Method:**
[x] Rule-based: mentions the police and the bank; reply in English; max 150 words.
[ ] Human evaluation
[x] LLM-as-judge: an honest "not covered", the three next steps, a calm and empathetic tone without blame.

**Primary Failure Mode:**
Incorrect tone (defensive or blaming) and a false refund promise to calm the customer down.

**Why this prompt matters:**
Fraud complaints are high-emotion and high-risk: a false promise creates liability, a cold reply loses the customer. This is the prompt used for the full judge in Step 4.

### Prompt #4: Seller has not shipped
**Prompt:**
> I paid 60 € for a jacket with "Sicher bezahlen" 9 days ago. The seller still hasn't shipped it and doesn't answer my messages. What happens to my money?

**Ground Truth:**
[x] Yes - Covered: the item was not shipped (rule 3). Report the problem from the purchase (rule 6). The full item price comes back, plus shipping if a Hermes label was created (rule 4). The policy gives no deadline in days, so the reply must not invent one.
[ ] No

**Verification Method:**
[x] Rule-based: mentions buyer protection and getting the money back ("refund", "money back", "reimburse", or the German equivalents); reply in English; max 150 words.
[ ] Human evaluation
[x] LLM-as-judge: no invented deadline, correct refund scope, clear next step.

**Primary Failure Mode:**
Hallucination (an invented deadline such as "the seller has 7 days") or missing information (no next step).

**Why this prompt matters:**
"What happens to my money?" is the most anxious moment of a protected purchase; the answer must be reassuring and exact.

### Prompt #5: Fee question in German
**Prompt:**
> Hallo, ich möchte ein Fahrrad für 100 € mit „Sicher bezahlen“ kaufen. Wie hoch ist die Gebühr und wer muss sie zahlen?

**Ground Truth:**
[x] Yes - Service fee 0,50 € + 4,5 % of the price = **5,00 €** for a 100 € bike, paid by the buyer, plus shipping costs (rule 2). The reply must be in German.
[ ] No

**Verification Method:**
[x] Rule-based: exact amount "5,00 €" (or "5 €" / "5 EUR" / "5 Euro"); reply detected as German; max 150 words.
[ ] Human evaluation
[x] LLM-as-judge: correct fee and payer, German, friendly.

**Primary Failure Mode:**
Wrong language (an English reply to a German customer) and a wrong number.

**Why this prompt matters:**
Most Kleinanzeigen users write in German, and the fee is a closed question with one right answer: the cheapest case to verify automatically.

## Step 4 · The judge (LLM-as-judge)
One judge prompt is used for all 5 cases. The policy, the case's answer key and what each criterion means for that case are passed in as inputs. Below, the judge is filled in for **Prompt #3**. The appendix shows the generic text exactly as the code sends it.

**Task Description:**
Check one reply written by Kleinanzeigen's support chatbot to a buyer. The chatbot's task was to answer a buyer who lost 250 € after paying a seller by bank transfer, using only the Kleinanzeigen policy. The judge receives the policy, the customer's message, the answer key, what each criterion means for this case, and the reply.

**Evaluation Criteria:**
1. **policy_accuracy:** every fact in the reply matches the policy and the answer key; nothing is invented (no deadlines, amounts or rules that are not in the policy). For #3: it says clearly that a bank transfer is not covered by buyer protection.
2. **resolution:** the reply gives the concrete next steps from the answer key and promises nothing the policy does not allow. For #3: report the user or listing, contact the bank, file a police report; no refund promise.
3. **tone_language:** polite and calm, acknowledges the situation, no blame, same language as the customer. For #3: empathetic despite the insults, in English.

**Score anchors (1-5):**
5 = all three met; clear and concise · 4 = all three met, small issue (wordy, a minor detail missing) · 3 = one criterion not met, no wrong facts · 2 = a wrong or invented fact, or a promise the policy does not allow · 1 = several criteria not met, or rude or unsafe

**Reasoning Steps:**
Step 1: List each fact the reply states and compare it with the policy and the answer key.
Step 2: Check the next steps and look for promises the policy does not allow.
Step 3: Check tone and language against the customer's message.
Step 4: Set criteria_met, then choose the score with the anchors. Judge content, not length.

**Output Format:**
```json
{
  "reasoning": "<2-4 sentences>",
  "criteria_met": {"policy_accuracy": true, "resolution": true, "tone_language": true},
  "score": 4
}
```
The reasoning comes first in the JSON, so the judge explains before it scores (the brief's template lists the score first; the keys are the same). Settings: gpt-4o-mini, temperature 0, `response_format={"type": "json_object"}`. A reply counts as PASS at a score of 4 or higher, so precision and recall can be computed in the calibration study.

### Bias analysis
**Hidden biases.** The judge (gpt-4o-mini) grades replies written by gpt-4o-mini and by gpt-5.4-mini, a model from the same provider. LLM judges tend to favour answers that look like their own, so scores for these two models may be inflated compared with a judge from another family. Judges also tend to prefer longer, more apologetic answers. The anchors and the instruction "judge content, not length" push against this, and calibration item C03 (correct but wordy) tests it. Position bias does not apply here, because the judge sees one reply at a time, not a pair.

**Language, culture and domain.** Models are usually stronger in English than in German, so the German case (#5) may be graded less reliably. There is also a cultural assumption: German customers often prefer short, factual answers, while the judge may reward a US-style, very warm tone. On the domain side, the judge may bring in retailer-style return rights (such as an online shop's return window) that do not apply to a private sale between two users. The answer key and the rule "only the policy counts" limit this.

**My own bias in the answer key.** I wrote the answer keys from my reading of the policy, and rules 6-8 are my lab assumptions, not Kleinanzeigen's rules. Any mistake there becomes a judge mistake.

### Calibration strategy
**Reference examples.** Ten replies with known quality, two per score level, each level built by planting a specific defect: wrong refund facts, invented availability, rude tone, a missing next step, an English reply to a German question (Extension 3). The judge runs at temperature 0 on all ten, and I compare its scores with the known levels: exact match, within one point, rank correlation, and pass/fail precision and recall, where "bad" means level 3 or lower. Recall matters most: a bad reply the judge misses reaches a customer.

**Edge cases and adjustments.** If the judge is too lenient (4-5 for a level-2 reply), I add the level-2 examples to the prompt as few-shot anchors and make "an invented deadline means policy_accuracy is false" explicit. If it is too strict (punishing "I can't see the listing"), I sharpen criterion 1, which already states that this is correct. Boundary cases (one minor fact missing: 4 or 3?) are settled in the anchors, not left to the judge. After every prompt change the calibration set is re-run, and the judge model, the prompt and the date are stored with the results.

**Bigger judge and next steps.** Extension 4 runs the same ten items with gpt-5.4-mini. I only switch judges if it is clearly better on recall and F1, weighed against its cost per 1,000 replies. In production, my labels would be replaced by labels from Kleinanzeigen support team leads on about 50 real, anonymised tickets (after a GDPR review); human evaluation is outside this lab.

### Appendix · Judge system prompt, exactly as sent to the API
```text
You are a strict quality reviewer for Kleinanzeigen customer support. Your task is to grade one reply written by a support chatbot to a buyer. You will be given the support policy, the customer's message, an answer key, what each criterion means for this case, and the chatbot's reply.

EVALUATION CRITERIA
1. policy_accuracy: every fact in the reply (fees, refunds, what buyer protection covers) matches the policy and the answer key. Nothing is invented, including deadlines, amounts or rules that are not in the policy. Saying "I can't see that" is correct when the policy says the assistant cannot see it.
2. resolution: the reply gives the customer the concrete next step(s) from the answer key and promises nothing the policy does not allow.
3. tone_language: the reply is polite and calm, acknowledges the customer's situation without blaming them, and is written in the same language as the customer's message.

SCORE ANCHORS
5 = all three criteria met; clear and concise.
4 = all three criteria met, with a small issue (wordy, or one minor detail from the answer key missing).
3 = one criterion not met, but no wrong or invented facts.
2 = a wrong or invented fact, or a promise the policy does not allow.
1 = several criteria not met, or rude or unsafe.

REASONING STEPS
Step 1: List each fact the reply states and compare it with the policy and the answer key. Note any fact that is wrong or not in the policy.
Step 2: Check that the reply gives the next steps from the answer key and does not promise anything the policy does not allow.
Step 3: Check tone and language against the customer's message.
Step 4: Set criteria_met for each criterion, then choose the score with the anchors. Judge content, not length: a longer reply is not a better reply.

OUTPUT FORMAT
Return only a JSON object with these keys, reasoning first:
{"reasoning": "<2-4 sentences>", "criteria_met": {"policy_accuracy": true or false, "resolution": true or false, "tone_language": true or false}, "score": <integer 1-5>}
```
The user message contains the policy, the customer message, the answer key, the per-case criteria and the reply (see `JUDGE_TEMPLATE` in the notebook).
