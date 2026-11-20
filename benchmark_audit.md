# Benchmark Audit

## Benchmark 1: IFEval

**Benchmark Name:** Instruction-Following Evaluation (IFEval)  
**Year:** 2023  
**Source:** https://arxiv.org/abs/2311.07911

### Why it seemed relevant

IFEval measures how reliably language models follow explicit instructions and constraints. This is relevant to the AI Food Concierge because restaurant recommendations must respect user requirements such as budget limits, dietary restrictions, and the requested number of recommendations.

### Contamination Risk

- [ ] Low
- [x] Medium
- [ ] High

**Explanation:** IFEval is a publicly available benchmark published in 2023. Its evaluation prompts may have appeared in training datasets or model development workflows, but direct exposure cannot be confirmed without information about the evaluated model's training data.

### Saturation Risk

- [ ] Low
- [x] Medium
- [ ] High

**Explanation:** Strong models can achieve high scores on verifiable instruction-following tasks, reducing the benchmark's ability to distinguish between leading models. However, performance still varies, particularly when several constraints must be satisfied simultaneously.

### Format

- [ ] Multiple Choice
- [x] Free-form text
- [ ] Code generation
- [ ] Other

### Verdict

- [ ] Use it as-is
- [x] Adapt it
- [ ] Reject it

**Explanation:** IFEval is relevant but does not directly measure restaurant recommendation quality. We would adapt its instruction-following principles to test whether the AI Food Concierge respects dietary restrictions, budget constraints, and other user preferences using a controlled synthetic dataset.

## Benchmark 2: HaluEval

**Benchmark Name:** HaluEval – A Large-Scale Hallucination Evaluation Benchmark for Large Language Models  
**Year:** 2023  
**Source:** https://arxiv.org/abs/2305.11747

### Why it seemed relevant

HaluEval evaluates whether language models can recognize hallucinated information in generated text. This is relevant to the AI Food Concierge because recommendations must not contain invented restaurant details, unsupported dietary claims, or fabricated availability information.

### Contamination Risk

- [ ] Low
- [x] Medium
- [ ] High

**Explanation:** HaluEval is publicly available and has been widely used in LLM research since 2023. Models may have encountered its examples during training or development, but actual exposure cannot be confirmed without access to the models' training data.

### Saturation Risk

- [x] Low
- [ ] Medium
- [ ] High

**Explanation:** Hallucination detection remains challenging, and published evaluation results show substantial performance differences across models. There is insufficient evidence that HaluEval is consistently solved at near-perfect accuracy.

### Format

- [ ] Multiple Choice
- [ ] Free-form text
- [ ] Code generation
- [x] Other: Binary hallucination classification (Yes/No)

### Verdict

- [ ] Use it as-is
- [x] Adapt it
- [ ] Reject it

**Explanation:** HaluEval provides useful principles for detecting hallucinations, but its original dataset is not specific to restaurant recommendations. We would adapt its evaluation approach to identify claims that are unsupported by our controlled synthetic restaurant dataset. This would allow us to assess factual consistency without requiring live restaurant data.

## Benchmark 3: MT-Bench

**Benchmark Name:** MT-Bench – Multi-Turn Benchmark  
**Year:** 2023  
**Source:** https://arxiv.org/abs/2306.05685

### Why it seemed relevant

MT-Bench evaluates the quality of language model responses across multi-turn conversations using LLM-based evaluation. This is relevant to the AI Food Concierge because users may refine their restaurant preferences during a conversation, requiring the model to maintain context and incorporate new constraints.

### Contamination Risk

- [ ] Low
- [x] Medium
- [ ] High

**Explanation:** MT-Bench has been publicly available since 2023, creating a risk that its test questions have been included in model training or evaluation workflows. However, direct exposure cannot be verified without access to the evaluated models' training data.

### Saturation Risk

- [ ] Low
- [ ] Medium
- [x] High

**Explanation:** MT-Bench has become a widely used evaluation benchmark, and strong contemporary models achieve scores close to the upper end of its rating scale. Score compression among high-performing models may limit its ability to distinguish between their capabilities.

### Format

- [ ] Multiple Choice
- [x] Free-form text
- [ ] Code generation
- [x] Other: Multi-turn dialogue evaluated by an LLM judge

### Verdict

- [ ] Use it as-is
- [x] Adapt it
- [ ] Reject it

**Explanation:** MT-Bench provides a useful framework for evaluating conversational quality and context retention. However, its original questions are not specific to restaurant recommendations. We would adapt its principles to evaluate whether the AI Food Concierge correctly handles follow-up requests and changing user preferences. A small number of synthetic conversation examples would be sufficient for our limited evaluation scope.