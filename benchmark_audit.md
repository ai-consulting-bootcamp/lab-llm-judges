# Benchmark Audit · Kleinanzeigen buyer-support chatbot

**Author:** Ayhan Demir · **Date:** 2026-11-20 · **Lab:** LLMs grading LLMs, with receipts

## Step 1 · Client scenario (Option C, Retail)
Kleinanzeigen wants a customer-service chatbot for buyers who pay with "Sicher bezahlen". It must handle returns (on a marketplace where private people sell to each other, these are buyer-protection claims), questions about items, and complaints, using only the official policy, in the customer's language and in a calm tone. The main failure modes are invented fees or refund rules, refunds promised outside buyer protection, the wrong tone with angry users, and replies in the wrong language.

*Fictional engagement for a lab. Kleinanzeigen has not commissioned this work.*

## Step 2 · Three benchmark evaluation cards
The three benchmarks match three things the chatbot must do: follow a retail policy in a conversation (tool calling), follow explicit instructions (instruction following), and say no when it should (noncompliance).

### Card 1 · τ-bench, retail domain
**Benchmark Name:** τ-bench (retail domain), maintained today in the τ²/τ³-bench repository
**Year:** 2024 (τ²-bench: 2025)
**Source:** Yao et al., "τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains", arXiv:2406.12045 (ICLR 2025). Tasks: github.com/sierra-research/tau2-bench (`data/tau2/domains/retail`). Leaderboard: taubench.com

**Why it seemed relevant:**
It is the closest public proxy for a retail support bot. An agent talks to a simulated customer, must follow a written retail policy (returns, exchanges, cancellations) and uses tools on an order database. Policy adherence and resolution are exactly what Kleinanzeigen cares about.

**Contamination risk:**
[ ] Low · [x] Medium · [ ] High
Explanation: the tasks, policy and database have been public on GitHub since 2024, so a model may have seen them. Scoring checks the final database state after a live, multi-turn simulation, so memorised text helps less than in a question-and-answer benchmark.

**Saturation risk:**
[ ] Low · [x] Medium · [ ] High
Explanation: at launch, gpt-4o solved about 61% of retail tasks on the first try (pass^1) and under 25% reliably across 8 tries (pass^8). Current τ²-bench retail scores for frontier models are around 77-84% pass^1 (Sierra-run results, as listed by developersdigest.tech from taubench.com). There is still headroom, especially on reliability.

**Format:**
[ ] Multiple Choice · [ ] Free-form text · [ ] Code generation
[x] Other: multi-turn conversation with tool calls, graded by the final database state (rule-based) plus required information

**Verdict:**
[ ] Use it as-is · [x] Adapt it · [ ] Reject it
Adapt: keep the design (written policy, realistic customer request, check against the policy) but swap in the Kleinanzeigen policy and German-market cases. As-is it tests a US online shop (zip codes, its own return rules and tools), and its 2.0 language packs (English, Spanish, Portuguese, Hindi, Chinese, Korean) do not include German. This lab tests single messages without tools, because the bot has no access to orders.

### Card 2 · IFEval
**Benchmark Name:** IFEval (Instruction-Following Eval)
**Year:** 2023
**Source:** Zhou et al., "Instruction-Following Evaluation for Large Language Models", arXiv:2311.07911. Data: huggingface.co/datasets/google/IFEval (Apache-2.0)

**Why it seemed relevant:**
A support bot must obey its system prompt: reply in the customer's language, stay under a word limit, include required facts. IFEval has about 500 prompts with 25 types of "verifiable instructions" that code can check, which is the same idea as the rule-based checks in this lab.

**Contamination risk:**
[ ] Low · [ ] Medium · [x] High
Explanation: public since 2023 and a core benchmark of the Hugging Face Open LLM Leaderboard. Instruction-tuning data often targets exactly these instruction types, so overlap is likely (my assessment; it cannot be proven from outside).

**Saturation risk:**
[ ] Low · [ ] Medium · [x] High
Explanation: top public scores are around 93-95%, and BenchLM (July 2026) notes that the top models sit within 0.4 points of each other. AI2's IFBench (2025) adds 58 new out-of-domain constraints as a harder test of the same skill.

**Format:**
[ ] Multiple Choice · [x] Free-form text (checked by rules) · [ ] Code generation · [ ] Other

**Verdict:**
[ ] Use it as-is · [x] Adapt it · [ ] Reject it
Adapt: borrow the verifiable-instruction idea for the rule checks (reply language, max 150 words, the exact fee "5,00 €"). Reject the score itself: its prompts (essays, poems, summaries) say nothing about support quality, and a near-saturated score cannot separate the candidate models.

### Card 3 · CoCoNot
**Benchmark Name:** CoCoNot ("Contextually, Comply Not")
**Year:** 2024
**Source:** Brahman, Kumar et al., "The Art of Saying No: Contextual Noncompliance in Language Models", arXiv:2407.12043 (NeurIPS 2024 Datasets & Benchmarks). Data: huggingface.co/datasets/allenai/coconot (AI2 ImpACT license)

**Why it seemed relevant:**
A support bot must know when to say "I can't": it cannot see a listing, cannot issue a refund itself, and must not promise what the policy does not allow, but it must not refuse normal questions either. CoCoNot tests both sides: 1,000 human-reviewed requests a model should not simply comply with (incomplete, unsupported, indeterminate, humanizing, safety), plus a contrast set it should comply with.

**Contamination risk:**
[ ] Low · [x] Medium · [ ] High
Explanation: the evaluation set has been public since July 2024 and a large training split was released with it, so models trained since then may have seen similar data.

**Saturation risk:**
[ ] Low · [x] Medium · [ ] High
Explanation: in the paper, GPT-4 still complied with about 30% of incomplete requests and GPT-4o with 19% of unsupported ones, while both complied with 97-98% of the contrast set. Newer models are less well tracked publicly.

**Format:**
[ ] Multiple Choice · [x] Free-form text (graded by an LLM judge) · [ ] Code generation · [ ] Other
Note: the paper used GPT-3.5-turbo as the judge after finding no significant difference from GPT-4; a manual check found 93% of 300 sampled judgments accurate.

**Verdict:**
[ ] Use it as-is · [x] Adapt it · [ ] Reject it
Adapt: use its categories to write the "can't see the listing" case (unsupported request) and the "refund outside buyer protection" case. Reject the score: general-purpose English prompts, not about retail or Kleinanzeigen.

## Summary
| Benchmark | Category | Contamination | Saturation | Format | Verdict |
|---|---|---|---|---|---|
| τ-bench retail | Tool calling | Medium | Medium | Multi-turn with tools, state check | Adapt |
| IFEval | Instruction following | High | High | Free-form, rule-checked | Adapt (rules only) |
| CoCoNot | Noncompliance | Medium | Medium | Free-form, LLM-judged | Adapt (categories only) |

**Conclusion:** no public benchmark covers a German marketplace policy, so the evaluation in `evaluation_design.md` is custom. It borrows one idea from each benchmark: a policy answer key (τ-bench), rule checks (IFEval) and "say no correctly" cases (CoCoNot).

*Sources checked on 2026-11-20. Leaderboard numbers change; treat them as a snapshot.*
