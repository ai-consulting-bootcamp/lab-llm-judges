# Benchmark Audit — ShopCo

## Client Scenario

ShopCo is a fictional online retailer that wants to use an LLM
chatbot to answer questions about returns, products, and complaints.
Replies must follow the provided store policy, use only available
information, and be clear, polite, and helpful.
The main risks are invented information, incorrect refund promises,
and incomplete answers.

## Audit Scope

We reviewed three existing benchmarks to inform our custom evaluation.
We will not run the full benchmarks or report official benchmark scores.

Contamination ratings are cautious estimates. Public data may have
been used during training, but public availability does not prove this.

Saturation depends on the model, benchmark version, and evaluation
conditions. Where evidence is missing, we report this limitation
instead of making an unsupported claim.

## 1. IFEval

**Benchmark Name:** Instruction-Following Evaluation (IFEval)
**Year:** 2023
**Source:** https://arxiv.org/abs/2311.07911
**Category:** Instruction following

### Why it seemed relevant

ShopCo replies must follow clear instructions. IFEval checks
instructions that can be verified with code, such as word limits
and required words. However, these checks do not prove that a
reply follows the refund policy.

### Contamination risk

**Medium — possible exposure; not confirmed.**

The prompts are public, so training overlap is possible.
We do not know whether our selected model saw them during training.

### Saturation risk

**High risk for distinguishing strong instruction-following models.**

The IFBench paper reports overfitting to familiar verifiable
constraints and poor generalization to new constraints.
Its introduction also describes IFEval as quickly saturated.

This supports a high saturation-risk assessment for model
selection. It does not mean every model scores perfectly
or that instruction following is solved.

Additional source:
https://arxiv.org/abs/2507.02833

### Format

Free-form text with automatic checks for verifiable instructions.

### Verdict

**Adapt it.**

We will use its approach to design automatic checks for ShopCo.
We will check policy accuracy separately and use an LLM judge
for qualities such as tone. Our results will not be official
IFEval scores.

## 2. Tau-bench

**Benchmark Name:** Tau-bench — Tool-Agent-User Interaction
in Real-World Domains
**Year:** 2024
**Source:** https://arxiv.org/abs/2406.12045
**Category:** Customer service, policy following, and tool use

### Why it seemed relevant

Tau-bench includes customer service tasks in retail. Agents must
follow store policies, understand customer requests, and use tools.
This is relevant to ShopCo's return and refund rules.

### Contamination risk

**Medium — possible exposure; not confirmed.**

The benchmark data is public, so training overlap is possible.
We cannot confirm whether our selected model saw it.

### Saturation risk

**Low in the original study; current status not confirmed.**

The models tested in the original study had difficulty completing
tasks consistently. These historical results do not prove how
current models perform.

### Format

Multi-turn conversations, tool calls, and checks of the final
database state.

### Verdict

**Adapt it.**

We will create original ShopCo cases inspired by its policy-based
retail tasks. We will evaluate replies, including incorrect refund
promises and missing information.

We will not execute transactions or check a real database.
Our results will not be official Tau-bench scores.

## 3. MT-Bench

**Benchmark Name:** MT-Bench
**Year:** 2023
**Source:** https://arxiv.org/abs/2306.05685
**Category:** Multi-turn conversation and response quality

### Why it seemed relevant

MT-Bench uses an LLM judge to evaluate conversational responses.
Its paper also studies judge biases, including preferences related
to answer position, answer length, and the judge's own model.

This helps us design a ShopCo judge that checks clear criteria
instead of rewarding a reply only because it sounds good.

### Contamination risk

**Medium — possible exposure; not confirmed.**

The questions and evaluation materials are public.
Training overlap is possible, but we cannot confirm it for
our selected model.

### Saturation risk

**Not confirmed — further evidence needed.**

We have not verified recent, comparable results showing whether
many models achieve scores close to the maximum.
Judge preferences can also affect scores.

### Format

Free-form, multi-turn responses evaluated by an LLM judge.

### Verdict

**Adapt its evaluation approach.**

We will write original ShopCo prompts and use a judge with explicit
criteria: accuracy, completeness, and tone.

A reply must fail if it promises a refund that breaks store policy,
even if it is polite. We will not reward extra length by itself.

Our small evaluation will not reproduce the full multi-turn
MT-Bench setup or produce official MT-Bench scores.

## Overall Decision

No benchmark fully matches ShopCo's needs.

We will build five original evaluation prompts using ShopCo's
fictional policy. We will use automatic checks where suitable
and an LLM judge where interpretation is needed.

Sandra must review every test case and reference answer before
execution. AI assistance does not replace this human review.

## Final Audit Limitations

Sources were reviewed on 24 November 2026.

- IFEval: additional evidence supports a high saturation risk
  for distinguishing strong models on familiar constraints.
- Tau-bench: the low saturation assessment refers to the
  original 2024 study. Current saturation was not established.
- MT-Bench: current saturation was not established from the
  sources reviewed. We retain this uncertainty rather than
  assign an unsupported Low, Medium, or High rating.

The API returned `gpt-4o-mini-2024-07-18`.
We do not have access to its complete training data.
Therefore, benchmark contamination is possible but unconfirmed.

Our ShopCo results are custom evaluation results.
They are not official scores on these public benchmarks.