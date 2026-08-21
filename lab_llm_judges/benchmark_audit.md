# Benchmark Audit — Retail Customer Service Chatbot

## Client Scenario

A mid-size online retailer wants to deploy an LLM-powered customer service chatbot that handles returns, product questions, order tracking, and complaint resolution. The chatbot must provide accurate, empathetic, and policy-compliant responses. Key failure modes include hallucinating return policies, giving incorrect order status, using a dismissive or robotic tone, and failing to follow structured response formats required by the retailer's support platform.

---

## Benchmark 1: MT-Bench

**Benchmark Name:** MT-Bench (Multi-Turn Benchmark)  
**Year:** 2023  
**Source:** Zheng, L. et al. "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena." NeurIPS 2023.  
Paper: https://arxiv.org/abs/2306.05685  
Code: https://github.com/lm-sys/FastChat/tree/main/fastchat/llm_judge

**Why it seemed relevant:**  
MT-Bench evaluates multi-turn conversational ability across 80 two-turn question pairs. Customer service interactions are inherently multi-turn — a customer first describes an issue, then follows up with clarifications, pushback, or additional requests. MT-Bench tests whether a model can maintain context and coherence across turns, which directly maps to our chatbot's need to handle escalating conversations without losing track of the original complaint.

**Contamination risk:**  
[x] High - Model definitely saw this during training  
Explanation: MT-Bench has been one of the most widely used LLM benchmarks since mid-2023. Its 80 questions are publicly available in the FastChat repository and have been extensively discussed in papers, blog posts, and leaderboards. Most frontier models have almost certainly encountered these prompts during training or RLHF tuning.

**Saturation risk:**  
[x] High - Many models achieve near-perfect scores  
Explanation: Top models regularly score above 9.0 out of 10 on MT-Bench. The benchmark was designed to be challenging in 2023, but rapid model improvement has compressed the scoring range. The differences between leading models are now within the noise margin of LLM-as-judge evaluation variance.

**Format:**  
[x] Free-form text

**Verdict:**  
[x] Reject it  
Explanation: While MT-Bench tests relevant capabilities (multi-turn coherence, instruction following), its high contamination and saturation risks make it unreliable for distinguishing between candidate models in 2025/2026. Additionally, its questions cover general categories (math, reasoning, coding, writing) rather than customer service-specific scenarios. We would need to build custom multi-turn prompts tailored to retail support interactions.

---

## Benchmark 2: IFEval (Instruction-Following Eval)

**Benchmark Name:** IFEval (Instruction-Following Evaluation)  
**Year:** 2023  
**Source:** Zhou, J. et al. "Instruction-Following Evaluation for Large Language Models." arXiv:2311.07911, November 2023.  
Paper: https://arxiv.org/abs/2311.07911  
Code: https://github.com/google-research/google-research/tree/master/instruction_following_eval

**Why it seemed relevant:**  
IFEval focuses on verifiable instruction-following — constraints like word count, keyword inclusion, formatting requirements, and structural rules. Our retail chatbot must adhere to strict response templates: including order numbers in specific formats, following escalation scripts, and structuring responses with required sections (greeting, resolution, next steps). IFEval's approach of testing objectively verifiable constraints maps well to these operational requirements.

**Contamination risk:**  
[x] Medium - Some overlap possible  
Explanation: IFEval's approximately 500 prompts are publicly available on GitHub, but it is less widely discussed than benchmarks like MMLU or MT-Bench. Some models may have been exposed to it during training, particularly since it was adopted by the Open LLM Leaderboard v2 in 2024, increasing its visibility.

**Saturation risk:**  
[x] Medium - Some models perform well  
Explanation: While top models achieve high scores, the benchmark retains discriminative power because instruction-following at scale (multiple constraints per prompt) remains genuinely challenging. The gap between frontier and mid-tier models is still meaningful.

**Format:**  
[x] Free-form text (with rule-based verification)

**Verdict:**  
[x] Adapt it  
Explanation: IFEval's methodology is excellent — verifiable constraints evaluated automatically — but its specific instructions are generic. We should adopt IFEval's verification approach (rule-based checks for format compliance) and create retail-specific verifiable constraints: "Include the order number in format #ORD-XXXXX," "End the response with a satisfaction check question," "Do not mention competitor brands." This gives us the objectivity of IFEval with domain relevance.

---

## Benchmark 3: MMLU (Massive Multitask Language Understanding)

**Benchmark Name:** MMLU  
**Year:** 2021  
**Source:** Hendrycks, D. et al. "Measuring Massive Multitask Language Understanding." ICLR 2021.  
Paper: https://arxiv.org/abs/2009.03300  
Dataset: https://huggingface.co/datasets/cais/mmlu

**Why it seemed relevant:**  
Our chatbot needs domain knowledge about retail operations — return policies, shipping logistics, warranty terms, and consumer rights. MMLU tests broad knowledge across 57 subjects, including business, law, and professional domains. A model scoring well on MMLU's professional-level questions might correlate with an ability to accurately discuss warranty law or consumer protection regulations.

**Contamination risk:**  
[x] High - Model definitely saw this during training  
Explanation: MMLU is arguably the single most widely used LLM benchmark. Its questions have been publicly available since 2020 and are included in virtually every LLM evaluation pipeline. Multiple studies have demonstrated contamination concerns, with models showing inflated scores on MMLU questions that appeared in training data.

**Saturation risk:**  
[x] High - Many models achieve near-perfect scores  
Explanation: Frontier models now regularly exceed 88–90% accuracy on MMLU. The 4-choice multiple-choice format means random chance yields 25%, and the gap between that baseline and top model scores has compressed to the point where MMLU alone cannot meaningfully differentiate between leading models.

**Format:**  
[x] Multiple Choice

**Verdict:**  
[x] Reject it  
Explanation: MMLU's multiple-choice format does not reflect how a chatbot uses knowledge in practice. A model can select the correct answer about consumer protection law on a multiple-choice test but still fail to apply that knowledge correctly when drafting a return denial letter. The format mismatch, combined with severe contamination and saturation risks, makes MMLU unsuitable for our evaluation. We need free-form prompts that test whether the model can retrieve and correctly apply policy knowledge in realistic customer interactions.
