# Benchmark Audit - Northwind Living Customer Service Chatbot

**Client scenario:** Northwind Living, a German online retailer for furniture and home goods (about 40,000 customer contacts per month), wants an LLM chatbot as the first line of customer service for returns, delivery, product questions and complaints. Answers must follow the company policy exactly, stay friendly with upset customers, and hand over to a human for legal threats, safety issues or requests outside the policy.

**What we need to measure:** (1) policy accuracy without invented rules, (2) tone with upset customers, (3) correct escalation, (4) consistency across repeated conversations.

---

## Card 1 - τ-bench (tau-bench), retail domain

**Benchmark Name:** τ-bench (Tool-Agent-User benchmark), τ-retail domain
**Year:** 2024 (published at ICLR 2025)
**Source:** Yao, Shinn, Razavi, Narasimhan (Sierra), arXiv 2406.12045 · https://github.com/sierra-research/tau-bench (successor: τ²-bench)

**Why it seemed relevant:**
It is the closest public match to our client. A simulated customer talks to an agent that must follow a **domain-specific policy document** and use tools (order database, returns, exchanges) in a **retail** setting. It also introduced **pass^k**, which measures whether the agent succeeds on *all* k repeated attempts. This matters for a chatbot answering 40,000 customers a month, where a correct answer "most of the time" is not enough.

**Contamination risk:**
- [ ] Low
- [x] **Medium** - Some overlap possible
- [ ] High

*Explanation:* The tasks and policy are public on GitHub since 2024, so newer models may have seen them during training. However, success depends on a multi-turn conversation with a simulated user and on database state, which is harder to memorise than a static Q&A set.

**Saturation risk:**
- [ ] Low
- [x] **Medium** - Some models perform well
- [ ] High

*Explanation:* In the original paper GPT-4o reached only about 61 % pass^1 on retail. Frontier models in 2026 report much higher pass^1 on the retail domain, but **pass^k (consistency) is still far from perfect**, so the benchmark is not fully saturated.

**Format:**
- [ ] Multiple Choice
- [ ] Free-form text
- [ ] Code generation
- [x] **Other:** multi-turn conversation with tool calls; scored by comparing the final database state with the expected one

**Verdict:**
- [ ] Use it as-is
- [x] **Adapt it**
- [ ] Reject it

*How:* Keep the **method** (policy document + simulated customer + pass^k over repeated runs), but replace τ-bench's fictional US retail policy with **Northwind Living's real policy** (30-day returns, non-returnable mattresses and custom items, 48-hour damage reporting, escalation rules) and add German-market cases. τ-bench scores database outcomes only, so add separate checks for **tone** and **escalation**.

---

## Card 2 - IFEval (Instruction-Following Eval)

**Benchmark Name:** IFEval
**Year:** 2023
**Source:** Zhou et al. (Google), "Instruction-Following Evaluation for Large Language Models", arXiv 2311.07911 · https://github.com/google-research/google-research/tree/master/instruction_following_eval

**Why it seemed relevant:**
Our chatbot must follow strict system-prompt instructions: never promise things outside policy, keep answers short, don't ask for unnecessary personal data, escalate in specific cases. IFEval tests whether a model follows **verifiable instructions** (about 25 instruction types, such as word limits, required formats and forbidden words) in around 500 prompts, checked automatically.

**Contamination risk:**
- [ ] Low
- [ ] Medium
- [x] **High** - Model definitely saw this during training

*Explanation:* The prompts have been public since 2023, and IFEval is reported in almost every model release, so model builders optimise for it directly.

**Saturation risk:**
- [ ] Low
- [ ] Medium
- [x] **High** - Many models achieve near-perfect scores

*Explanation:* Leading models score around 95 % on public leaderboards in 2026. Even small models score around 90 %, so IFEval no longer separates good models from bad ones.

**Format:**
- [ ] Multiple Choice
- [x] **Free-form text** (checked with rule-based verifiers)
- [ ] Code generation

**Verdict:**
- [ ] Use it as-is
- [ ] Adapt it
- [x] **Reject it** (as a model-selection benchmark)

*Why:* It is saturated, highly contaminated, and its instructions (e.g. "answer in exactly 3 paragraphs") are **format rules, not business rules**. A high IFEval score does not tell us whether the bot will refuse to promise an out-of-policy refund. We **borrow its idea**: write our own *rule-based* checks for Northwind's rules (e.g. the answer must not contain "free return" for a mattress with the film removed).

---

## Card 3 - MT-Bench (with LLM-as-a-judge)

**Benchmark Name:** MT-Bench (Multi-Turn Benchmark)
**Year:** 2023
**Source:** Zheng et al. (LMSYS), "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena", arXiv 2306.05685 · https://github.com/lm-sys/FastChat

**Why it seemed relevant:**
Customer service is **multi-turn**, and quality is partly subjective (helpfulness, tone). MT-Bench uses 80 two-turn questions across 8 categories (writing, roleplay, reasoning and others) and is the benchmark that popularised **LLM-as-a-judge**, where a strong model scores answers from 1 to 10. That is the method we will use for tone and helpfulness.

**Contamination risk:**
- [ ] Low
- [ ] Medium
- [x] **High** - Model definitely saw this during training

*Explanation:* There are only 80 public questions, available since 2023, and they are widely copied in training and fine-tuning data.

**Saturation risk:**
- [ ] Low
- [ ] Medium
- [x] **High** - Many models achieve near-perfect scores

*Explanation:* Top models have scored around 9 out of 10 for a long time, so the scale no longer separates strong models.

**Format:**
- [ ] Multiple Choice
- [x] **Free-form text** (multi-turn, scored 1-10 by an LLM judge)
- [ ] Code generation

**Verdict:**
- [ ] Use it as-is
- [ ] Adapt it
- [x] **Reject it** (as a dataset), but **reuse the judging method**

*Why:* The questions are general (poetry, maths, coding) and have nothing to do with returns, complaints or German retail policy. We **reject the dataset** but **reuse the method**: an LLM judge with a clear rubric. MT-Bench's paper also documents judge biases (position, verbosity, self-preference), which we use in our judge's bias analysis.

---

## Summary

| Benchmark | Relevance | Contamination | Saturation | Verdict |
|---|---|---|---|---|
| τ-bench (retail) | High: retail policy + simulated customers | Medium | Medium | **Adapt** (our policy, plus tone and escalation checks) |
| IFEval | Medium: instruction following | High | High | **Reject** (borrow rule-based checks) |
| MT-Bench | Low: generic multi-turn chat | High | High | **Reject dataset**, reuse LLM-as-judge method |

**Conclusion:** no public benchmark measures what Northwind actually needs: **its own policy, its tone standard and its escalation rules**. We therefore build a **custom mini-benchmark** (see `evaluation_design.md`), using τ-bench's policy-plus-customer method, IFEval-style rule checks and an MT-Bench-style LLM judge.
