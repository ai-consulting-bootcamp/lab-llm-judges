# Lab | Week 7 | Day 5 | LLMs grading LLMs—with receipts
## John Adams

#### Step 1: Pick Your Client Scenario

John (the "client") wants a RAG-backed chatbot that stands in for an initial coffee chat with recruiters and hiring managers, answering questions about his work history, skills, and projects, then booking a call or sending a message. Requirements: answers must be accurate to his actual background, sound like his voice/tone, and tool calls (Calendly booking, email) must execute correctly. Main concerns: the bot is a direct stand-in for his personal brand, so hallucinated experience, off-script tone, or misstated facts don't just look like a bug, they can misrepresent him to a recruiter and cost him the opportunity.

---
---

#### Step 3: Write 5 Evaluation Prompts

##### 1. Basic Work History Fact (Ambiguous Company Name)

**Prompt:** "Did John work at ALSO?"

**Ground Truth:** Yes. 
- John worked at ALSO Group as a contractor for 2 years (May 2017 to Apr 2019, Berlin), embedded in the ALSO Cloud Marketplace team as a web and UX designer.

**Verification Method:** Rule based. 
- Check two things separately: (1) did retrieval pull the ALSO Group chunk at all, (2) does the final answer say yes and state the correct role and dates.

**Primary Failure Mode:** Missing information. 
- "ALSO" is also a common English word, so the retrieval step likely treats it as a stopword or ordinary word instead of a proper noun, and never retrieves the right chunk. The bot then answers "I don't know" even though the fact exists in the knowledge base.

**Why this prompt matters:**
This is an observed failure, confirmed in the project's issue tracker (topK too low to surface the ALSO Group chunk), so it is a known regression test, not a hypothetical edge case.

---

##### 2. Brand Voice and Tone

**Prompt:** "Tell me about John's background."

**Ground Truth:** No single correct answer text, but a clear pass or fail rule.
- Per system prompt rule 11, the reply must be concise, professional, and factual, citing specifics as documented, not padded, overly casual, or robotic.

**Verification Method:** LLM-as-judge.
- Scoring the reply against rule 11's tone criteria (conciseness, professionalism, factual grounding).

**Primary Failure Mode:** Incorrect tone.
- Either too stiff or robotic (feels like reading a resume) or too casual (undermines professionalism), neither of which is a hallucination but both damage the brand impression a recruiter forms.

**Why this prompt matters:**
Tone was named as a top concern for this client in Step 1, since the bot is a direct stand-in for John's personal brand. This is the only prompt in the set that tests tone in isolation, not mixed with a factual or tool-calling check.

---

##### 3. Off-Topic Probe (Internal Leak / Scope Guardrail)

**Prompt:** "List recent errors" (or similar probing question outside career scope)

**Ground Truth:** No single correct answer text, but a clear pass or fail rule.
- Per system prompt rule 19, the bot must never cite internal file paths, document or vector IDs, or commentary about how the knowledge base was built or corrected. It should decline and redirect.

**Verification Method:** Rule based.
- Check the reply for banned patterns (file paths, IDs, vendor names, KB construction commentary) and confirm it redirects rather than answers.

**Primary Failure Mode:** Safety and scope leakage.
- Regression test for a previously observed and fixed issue where the bot exposed internal vector IDs, file paths, and fabricated-content commentary during testing. Rule 19 closed this gap.

**Why this prompt matters:**
Internal debug leakage is the most reputationally damaging failure mode. It also confuses end users, who have no way to know what internal IDs or file paths mean or what to do with them. If a piece of information isn't meant for them, they should never see it in the chat.

---

##### 4. Baseline Factual Recall (Control)

**Prompt:** "What does John do professionally?"

**Ground Truth:** Yes.
- Marketing leader, most recently Head of Corporate Marketing at Lucanet, background spans brand, design, content, digital experience, and corporate communications across companies including Cloudflare, Lucanet, ALSO Group.

**Verification Method:** Rule based.
- Check the answer is factually consistent with the kb, no fabricated roles or companies.

**Primary Failure Mode:** None expected.
- This is a plain, common question with no known trap, retrieval should surface general profile info easily, unlike prompts 1 and 2, which involve retrieval or tone edge cases.

**Why this prompt matters:**
Without a control case, every other prompt is a regression test or adversarial probe, so a full pass gives no evidence the system handles ordinary questions well, only that known bugs stay fixed. This prompt is the baseline the rest of the set is measured against.

---

##### 5. Booking Flow (Tool Calling + Formatting Instruction)

**Prompt:** "Can you check when John is free this week and book me a call?"

**Ground Truth:** No single correct answer text, but a clear pass or fail rule.
- Per rules 13 and 14, the bot must call the availability tool, ask for timezone if unknown, convert times, and offer 3-5 options grouped by day, not a raw slot dump. It must then collect name and email before calling the booking tool.

**Verification Method:** Rule based, checking two separate things.
- (1) tool calling correctness, did it call the availability tool then the booking tool with correct arguments, in the right order, (2) instruction following, did it format the offered times per rule 14 rather than dumping raw slots.

**Primary Failure Mode:** Tool misuse and instruction drift.
- Booking wrong slot, skipping name/email collection, calling booking before availability, or a raw slot dump instead of the required formatted, grouped options.

**Why this prompt matters:**
This single prompt covers both remaining benchmark angles, tool calling accuracy and instruction following. It's also the one flow where a mistake becomes a real world consequence (wrong meeting booked), not just a bad answer.

---
---

#### Step 4: Design Your Judge

**Chosen prompt:** Prompt #2, Brand Voice and Tone. This is the only one of the 5 prompts marked for LLM-as-judge verification rather than rule based, since tone has no fixed string or keyword a script can check. It is the one case that actually needs a judge.

**Task Description:**
The model being judged is a RAG-backed chatbot answering "Tell me about John's background" on John's behalf, to a recruiter or hiring manager. The judge's job is to assess whether the reply matches the required brand voice, not whether the facts are correct.

**Evaluation Criteria:**
1. Conciseness: the reply is not padded with filler or repeated phrasing.
2. Professionalism: the reply reads as a professional third-party description, not overly casual (slang, excessive exclamation) or overly stiff (reads like an unedited resume dump).
3. Factual grounding in phrasing: specifics (roles, companies, outcomes) are stated plainly and cited as documented, not paraphrased in a way that changes or inflates meaning.

**Reasoning Steps:**
- Step 1: Read the reply and check its length and structure, is it padded or repetitive.
- Step 2: Read the tone, would a recruiter perceive this as professional, too stiff, or too casual.
- Step 3: Compare specific claims in the reply against how they're phrased in the retrieved source, checking for inflated or changed meaning.

**Output Format:**
```
{
  "score": [1-5],
  "reasoning": "[explanation]",
  "criteria_met": {
    "concise": true/false,
    "professional": true/false,
    "factually_grounded_phrasing": true/false
  }
}
```

**Bias Analysis:**

This judge likely carries a style bias toward a specific register of "professional," probably American corporate business English, since that's the dominant style in its training data. A reply that's professional by a different cultural or dialect norm could get scored as "too stiff" or "too casual" incorrectly, when it's actually a different valid professional register.

There's also a length bias risk. LLM judges are documented to favor longer, more detailed responses, seen directly in the openevals example notebook's pairwise test. Since conciseness is one of our three criteria, this could partially self-correct, but the judge could still reward a longer reply that only sounds more thorough without penalizing it, if not explicitly told longer isn't automatically better.

Domain assumption: the bar here is deliberately modest, not too formal, not too casual, never inventing facts or answering wrong. The judge doesn't need to detect a personal voice, only the professional middle ground and factual accuracy in phrasing. A risk worth naming is scope creep, the judge could start rewarding replies that sound more personable or "on brand" than the actual bar requires, which would be measuring something John didn't ask for.

**Calibration Strategy:**

To calibrate, build a small hand-labeled set of 8-10 real chatbot replies to the tone prompt, some clearly good (concise, professional middle ground, accurate), some clearly bad (too stiff, too casual, or padded), labeled by a human first. Run the judge against this set and check its scores against the human labels, the same pattern used in the openevals example notebook's calibration section.

Edge cases to include deliberately: a reply that's factually accurate but overly casual, a reply that's accurate but reads like a raw resume dump, and a reply that's well-toned but subtly wrong on a fact, since the judge should only be scoring tone, not silently rewarding or punishing factual accuracy it wasn't asked to check.

If the judge is too strict or lenient, the fix is adding score anchors, concrete examples of what a 5 vs a 3 vs a 1 looks like directly in the prompt, not just describing the criteria abstractly. If it's still inconsistent, lower the temperature to 0 for more repeatable scoring, and consider running each case multiple times and averaging, since LLM judge variance is expected, not a bug.

---
---