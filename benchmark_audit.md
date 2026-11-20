# Benchmark Audit — NordHome Customer Service Chatbot

**Scenario:** NordHome, a fictional mid-sized online home-goods retailer, wants an LLM chatbot to handle first-line customer service: return and refund requests, product questions, and complaints. It must apply the return policy exactly, answer product questions only from catalogue data, and stay polite and calm with angry customers. Main concerns: made-up policy terms or product facts, the wrong tone with upset customers, and failing to pass sensitive cases (safety issues, legal threats) to a human.

---

## Benchmark 1 — IFEval

**Benchmark Name:** IFEval (Instruction-Following Eval)
**Year:** 2023
**Source:** Zhou et al., "Instruction-Following Evaluation for Large Language Models", arXiv:2311.07911 — https://arxiv.org/abs/2311.07911

**Why it seemed relevant:**
A customer service bot works under a system prompt full of rules ("keep answers under 120 words", "always offer a ticket number", "never promise a refund before checking eligibility"). IFEval tests whether a model follows explicit instructions, using around 500 prompts covering 25 types of instruction that can be checked automatically.

**Contamination risk:**
[ ] Low
[ ] Medium
[x] High
Explanation: The dataset and code have been public on GitHub since 2023, and IFEval is one of the most widely reported instruction-following scores. Model developers train specifically to do well on it. A follow-up paper (IFBench, 2025) found that many top models do well on IFEval but much worse on new, unseen constraints, which suggests overfitting.

**Saturation risk:**
[ ] Low
[ ] Medium
[x] High
Explanation: Third-party leaderboards (BenchLM, July 2026) show the top models at about 95%, with the top three within 0.4 points of each other. The IFBench authors note that even small models (around 2B parameters) score 80%+. The benchmark no longer separates strong models from each other.

**Format:**
[ ] Multiple Choice
[x] Free-form text
[ ] Code generation
[x] Other: free-form answers, scored automatically by rule-based checks (word counts, keywords, formatting)

**Verdict:**
[ ] Use it as-is
[x] Adapt it
[ ] Reject it
Explanation: The idea is right but the instructions are generic ("write in all lowercase") rather than about business rules. I would keep its approach (rules that can be checked automatically) and write NordHome-specific constraints instead: "mention the 30-day window", "do not state a refund amount", "include the escalation phrase when a safety issue is mentioned". These are cheap to check with regex/keyword rules and have not been seen in any training data.

---

## Benchmark 2 — TruthfulQA

**Benchmark Name:** TruthfulQA
**Year:** 2021 (published at ACL 2022)
**Source:** Lin, Hilton & Evans, "TruthfulQA: Measuring How Models Mimic Human Falsehoods", arXiv:2109.07958 — https://arxiv.org/abs/2109.07958

**Why it seemed relevant:**
Our biggest risk is the bot inventing things: return terms, product specs, delivery promises. TruthfulQA measures whether a model repeats common false beliefs instead of giving a true answer, so it is a common stand-in for "does this model hallucinate?".

**Contamination risk:**
[ ] Low
[ ] Medium
[x] High
Explanation: It is old and public, and contamination has been measured directly. A 2024 study built a new "retro-holdout" version of TruthfulQA and found some models' scores were inflated by up to 16 percentage points on the public version. In January 2025 the authors also released a fixed multiple-choice version because the original format could inflate scores.

**Saturation risk:**
[ ] Low
[x] Medium
[ ] High
Explanation: Not completely maxed out, but the scores are hard to trust because of contamination and the format problem above. Some practitioners also point out that models can score higher by refusing or denying more often, which would be bad behaviour for a helpful chatbot. *(I did not find one authoritative current leaderboard for TruthfulQA, so this rating is a judgement, not a measured figure.)*

**Format:**
[x] Multiple Choice
[x] Free-form text
[ ] Code generation
[ ] Other

**Verdict:**
[ ] Use it as-is
[ ] Adapt it
[x] Reject it
Explanation: It tests general-knowledge myths (health, law, folklore), not whether the bot sticks to *our* documents. A model can score well on TruthfulQA and still invent a NordHome return rule. Hallucination risk for this client has to be tested on its own policy and catalogue, where we know the correct answer and the model cannot have memorised it.

---

## Benchmark 3 — τ-bench (retail domain)

**Benchmark Name:** τ-bench (Tool-Agent-User Interaction Benchmark), τ-retail domain
**Year:** 2024 (ICLR 2025). Updated successor versions: τ²-bench and τ³-bench.
**Source:** Yao, Shinn, Razavi & Narasimhan (Sierra), arXiv:2406.12045 — https://arxiv.org/abs/2406.12045 ; code: https://github.com/sierra-research/tau-bench

**Why it seemed relevant:**
This is the closest match to our use case. A model plays a retail customer-service agent, talks to a simulated customer (played by another LLM), uses order-database tools, and must follow a written policy document. It covers tasks like cancellations, exchanges and returns. Success means the final database state matches the expected result and the agent told the customer everything required. It also introduces pass^k: the chance the agent succeeds on *all* k repeated attempts, which measures reliability, not just one lucky success.

**Contamination risk:**
[ ] Low
[x] Medium
[ ] High
Explanation: The tasks and policies are public on GitHub, so they could end up in training data. But each run is a live multi-turn conversation with a simulated user, so memorising answers helps less than on a static Q&A set. The original repo now warns that its retail/airline tasks are outdated and points to τ³-bench, which fixed task bugs.

**Saturation risk:**
[ ] Low
[x] Medium
[ ] High
Explanation: At launch, GPT-4o solved under 50% of tasks and pass^8 was under 25% in retail. Third-party leaderboards for 2026 report top models at roughly 86–92% on retail (self-reported, harnesses differ). So the top of the board is getting crowded, but pass^k still exposes inconsistency. For reference, gpt-4o-mini, the model this lab uses, scored about 43% on HAL's τ-bench retail leaderboard.

**Format:**
[ ] Multiple Choice
[ ] Free-form text
[ ] Code generation
[x] Other: multi-turn conversation with tool calls, scored by comparing the final database state against the expected one

**Verdict:**
[ ] Use it as-is
[x] Adapt it
[ ] Reject it
Explanation: Right task type and the right reliability metric, but it uses Sierra's own policy and database, not NordHome's. I would use the τ²/τ³ framework as a template: swap in NordHome's return policy and a small sample of NordHome orders, and report pass^k so the client sees how *consistent* the bot is, not just its best score. Scores from different τ-bench versions or domains can't be compared directly, so I would only compare models run on the same version.

---

## Summary

| Benchmark | Contamination | Saturation | Verdict |
|---|---|---|---|
| IFEval | High | High | Adapt (keep the automatic checks, write NordHome-specific rules) |
| TruthfulQA | High | Medium | Reject (general-knowledge myths, not our policy) |
| τ-bench retail | Medium | Medium | Adapt (use the framework with NordHome policy + orders, report pass^k) |

**Takeaway:** No public benchmark answers the client's real question: "does the bot follow *our* policy, with *our* customers, in the right tone?" Public scores are useful for shortlisting models; the go/no-go decision has to come from a custom evaluation (Steps 3–4).
