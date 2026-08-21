# Benchmark Audit — Retail Customer-Service Chatbot

## Client scenario

The client is a fictional online retailer that wants to use an LLM chatbot to answer product questions, explain return eligibility, handle complaints, and call approved support tools. The chatbot must be factually grounded in the retailer’s policy and catalog, empathetic without making promises it cannot keep, and safe when a customer asks for an action that requires authorization. Main failure modes are hallucinated policy, missed constraints, poor tone, and incorrect tool arguments.

## Benchmark 1 — MMLU

**Year:** 2020 paper; ICLR 2021 publication  
**Source:** https://arxiv.org/abs/2009.03300  
**Category:** Knowledge and reasoning  
**Format:** Multiple choice

### Why it seemed relevant

MMLU tests broad knowledge across 57 subjects, including law, business, and other domains. It can provide a rough signal of general knowledge and reasoning that may support customer-service answers.

### Contamination risk

**Medium to high.** The dataset and evaluation code are public and widely used, so training overlap is plausible for modern models. This is a risk assessment, not proof that a particular model saw every item.

### Saturation risk

**High for model selection.** Strong models perform well on many MMLU subjects, so a small score difference may not predict a meaningful difference on this retailer’s policies or product catalog. MMLU also contains known data-quality concerns reported by later audit work.

### Verdict

**Adapt it.** Use selected business, law, and ethics items only as a background sanity check. Do not use MMLU as the main go/no-go test. Replace public questions with private, retailer-specific questions and policy-grounded cases.

## Benchmark 2 — MT-Bench

**Year:** 2023  
**Source:** https://arxiv.org/abs/2306.05685  
**Category:** Multi-turn dialogue and instruction following  
**Format:** Free-form text; commonly evaluated with an LLM judge

### Why it seemed relevant

MT-Bench was designed to test multi-turn conversation and instruction following through open-ended questions. These are relevant to a chatbot that must remember the customer’s issue, ask useful follow-up questions, and produce a coherent final response.

### Contamination risk

**Medium.** The questions and judge methodology are public, so a model may have encountered examples or discussions about them.

### Saturation risk

**Medium to high.** It differentiates general chat quality, but it does not contain the client’s actual return policy, catalog facts, or escalation rules. Scores can also reflect writing style rather than business correctness.

### Verdict

**Adapt it.** Keep the multi-turn structure, but rewrite the cases using realistic retail conversations. Add explicit checks for policy accuracy, required clarification, escalation, and no false promises. Use human spot checks alongside the LLM judge.

## Benchmark 3 — Berkeley Function Calling Leaderboard (BFCL)

**Year:** 2025 paper; benchmark releases continue to evolve  
**Source:** https://proceedings.mlr.press/v267/patil25a.html  
**Category:** Tool/function calling  
**Format:** Structured function calls evaluated for correctness and executability

### Why it seemed relevant

The retailer’s chatbot may need to call tools such as `lookup_order`, `check_return_policy`, or `create_refund_request`. BFCL directly evaluates whether models select functions and construct valid arguments across single, parallel, and more complex calls.

### Contamination risk

**Medium.** The benchmark is public and its tool schemas are available. A model could have seen benchmark examples or similar schemas during training.

### Saturation risk

**Low to medium for advanced cases.** Simple function calls may be easy for strong models, but multi-step, stateful, abstention, and executability cases remain closer to real agent risk.

### Verdict

**Adapt it.** Use BFCL as an external reference for tool-call evaluation, then create private tests with the retailer’s own schemas, authorization rules, invalid states, and “do not call a tool” controls.

## Overall audit conclusion

No public benchmark is sufficient on its own. The recommended strategy is a layered evaluation: use MMLU for a limited background signal, MT-Bench-style conversations for dialogue structure, BFCL-style tests for tool correctness, and a private mini-benchmark for the client’s actual policies, catalog, tone, and escalation requirements.
