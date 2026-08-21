# Benchmark Audit — TenderAI

## Client Scenario

A consulting and engineering company wants to use a Retrieval-Augmented Generation (RAG) assistant to analyze tender requirements and draft evidence-grounded tender responses. The system must provide accurate answers based on the company's knowledge base, identify when evidence is insufficient, follow required response formats, and avoid unsupported claims or hallucinations.

The main evaluation concerns are accuracy, grounding, instruction following, completeness, compliance judgment, and hallucination avoidance.

---

# Benchmark 1 — MMLU

**Benchmark Name:** Massive Multitask Language Understanding (MMLU)

**Year:** 2021

**Source:** Hendrycks et al., "Measuring Massive Multitask Language Understanding"

**Source URL:** https://arxiv.org/abs/2009.03300

### Why it seemed relevant

MMLU evaluates broad knowledge and reasoning across 57 subjects using multiple-choice questions. This is relevant to TenderAI because the underlying model needs general knowledge and reasoning capabilities to understand technical, business, and compliance-related language.

However, MMLU does not directly evaluate whether a RAG system retrieves the correct company evidence or avoids unsupported claims from a client's knowledge base.

### Contamination risk

**Medium**

MMLU is a well-known, publicly available benchmark and there is published research investigating benchmark contamination and memorization risks. However, contamination cannot be assumed for every model without model-specific evidence about its training data.

Therefore, the risk is classified as medium rather than high.

### Saturation risk

**High for this use case**

MMLU has become a widely used general-purpose benchmark and is less discriminative for distinguishing highly capable models on the specific capabilities required by TenderAI. High performance on MMLU would not demonstrate that a model is reliable for evidence-grounded tender analysis.

This does not mean MMLU is useless. It means its score should not be treated as a direct proxy for TenderAI performance.

### Format

**Multiple choice**

### Verdict

**Adapt / use as a secondary signal**

MMLU could provide background information about general model capability, but it should not be the primary evaluation for TenderAI.

The custom evaluation should focus instead on grounding, retrieval-related behavior, unsupported-claim rejection, and compliance assessment.

---

# Benchmark 2 — IFEval

**Benchmark Name:** Instruction-Following Evaluation (IFEval)

**Year:** 2023

**Source:** Zhou et al., "Instruction-Following Evaluation for Large Language Models"

**Source URL:** https://arxiv.org/abs/2311.07911

### Why it seemed relevant

IFEval evaluates whether language models follow explicit, objectively verifiable instructions. The benchmark contains approximately 500 prompts covering 25 types of verifiable instructions.

This is relevant to TenderAI because the production system may have strict requirements for how an evaluation or response should be structured. For example, TenderAI might be required to return a status, evidence, gap, and recommendation in a specified format.

### Contamination risk

**Medium**

IFEval was publicly released in 2023 and has been widely used in LLM evaluation. Therefore, training-data exposure is possible for some models.

However, without evidence about the training data of a specific model, it would be inappropriate to claim that the model definitely saw IFEval during training.

### Saturation risk

**Medium**

IFEval provides objective and reproducible instruction-following checks, which makes it useful. However, strong instruction-tuned models can achieve relatively high performance on standard instruction-following tests.

For TenderAI, the bigger limitation is that generic instructions may not represent the specific formatting and workflow requirements of a real tender-analysis system.

### Format

**Free-form text with objectively verifiable constraints**

### Verdict

**Adapt**

We should adapt the principle of IFEval to TenderAI-specific instructions.

For example, we could require the model to return exactly:

* STATUS
* EVIDENCE
* GAP
* RECOMMENDATION

We could then verify automatically whether the required fields are present and whether the response follows the expected structure.

---

# Benchmark 3 — RGB

**Benchmark Name:** Retrieval-Augmented Generation Benchmark (RGB)

**Year:** 2023 preprint / 2024 AAAI publication

**Source:** Chen et al., "Benchmarking Large Language Models in Retrieval-Augmented Generation"

**Source URL:** https://arxiv.org/abs/2309.01431

### Why it seemed relevant

RGB is specifically designed to evaluate LLM behavior in Retrieval-Augmented Generation settings.

It evaluates four capabilities:

1. Noise robustness
2. Negative rejection
3. Information integration
4. Counterfactual robustness

These capabilities map closely to important TenderAI risks.

For example, TenderAI must be able to ignore irrelevant retrieved documents, recognize when the knowledge base does not contain sufficient evidence, combine information from multiple documents, and avoid accepting false or contradictory information.

### Contamination risk

**Medium**

RGB was publicly released in 2023 and is available as a research benchmark. Therefore, exposure during model training is possible.

However, contamination cannot be established for a particular model without information about its training data.

### Saturation risk

**Low–Medium**

The original RGB research identified continuing weaknesses in several RAG capabilities, particularly negative rejection, information integration, and handling false information.

This suggests that the benchmark can still provide useful diagnostic information. However, it is not specifically designed around TenderAI's domain, documents, terminology, or compliance rules.

### Format

**RAG evaluation using retrieved passages and questions/tasks**

### Verdict

**Adapt**

RGB is the most directly relevant of the three benchmarks for TenderAI.

Rather than using RGB unchanged, we should adapt its principles to create a client-specific evaluation set.

For example:

**Tender requirement:** The supplier must demonstrate experience delivering offshore wind projects above 100 MW.

**Retrieved evidence:** The knowledge base contains projects of 48 MW, 35 MW, and 22 MW.

**Expected behavior:** The system should identify the requirement as insufficiently supported and should not invent a qualifying project.

---

# Overall Benchmark Audit

| Benchmark | Main Capability                 | Relevance to TenderAI | Contamination Risk | Saturation Risk        | Verdict           |
| --------- | ------------------------------- | --------------------- | ------------------ | ---------------------- | ----------------- |
| MMLU      | General knowledge and reasoning | Medium                | Medium             | High for this use case | Adapt / secondary |
| IFEval    | Instruction following           | High                  | Medium             | Medium                 | Adapt             |
| RGB       | RAG capabilities                | Very High             | Medium             | Low–Medium             | Adapt             |

## Overall Conclusion

None of the three benchmarks is sufficient by itself to determine whether TenderAI is production-ready.

MMLU provides information about broad model knowledge and reasoning, while IFEval provides information about instruction-following behavior. RGB is more directly relevant because it evaluates important RAG capabilities.

However, a professional client evaluation should not rely solely on public benchmarks. TenderAI should also be evaluated using a small, domain-specific test set based on realistic tender requirements and the client's actual knowledge base.

The custom evaluation should specifically test grounding, evidence sufficiency, hallucination avoidance, instruction following, completeness, and compliance judgment.

This custom evaluation will therefore be the primary focus of the next stage of the lab.

## Sources

* Hendrycks et al. (2021), "Measuring Massive Multitask Language Understanding": https://arxiv.org/abs/2009.03300
* Zhou et al. (2023), "Instruction-Following Evaluation for Large Language Models": https://arxiv.org/abs/2311.07911
* Chen et al. (2023/2024), "Benchmarking Large Language Models in Retrieval-Augmented Generation": https://arxiv.org/abs/2309.01431
