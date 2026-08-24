# Benchmark Audit

**Client scenario:** A retailer wants a customer service chatbot that can handle returns, product questions, and complaints. Key requirements are helpfulness, correct tone, and a high resolution rate. Main concerns are wrong policy information, unhelpful or rude tone, and failure to escalate cases the bot cannot solve.

Below are 3 benchmarks evaluated for relevance to this scenario.

---

## Benchmark 1: ABCD (Action-Based Conversations Dataset)

Benchmark Name: ABCD (Action-Based Conversations Dataset)
Year: 2021
Source: Chen et al., "Action-Based Conversations Dataset: A Corpus for Building More In-Depth Task-Oriented Dialogue Systems" (ASAPP, NAACL-HLT 2021), https://github.com/asappresearch/abcd

**Why it seemed relevant:**
ABCD contains over 10,000 human to human dialogues covering 55 distinct user intents, where an agent helps a customer with realistic retail support tasks such as refunds, order changes, and account issues, while following a written company policy. This is close to my client's use case: a chatbot that must follow return and complaint policies correctly, not just chat naturally.

**Contamination risk:**
- [x] Medium - Some overlap possible
[Explanation: The dataset has been public since 2020 and is used in dialogue research, so it is plausible that some large models have seen parts of it during training. It is not a widely reported leaderboard benchmark, so heavy memorization is less certain than for a benchmark like MMLU.]

**Saturation risk:**
- [x] Low - Benchmark is challenging
[Explanation: ABCD requires multi-step reasoning over a policy document plus correct action selection, not just fluent text. I could not find a public leaderboard tracking near-ceiling scores on it, which itself is a limitation worth noting rather than a confirmed low score.]

**Format:**
- [x] Free-form text
- [x] Other: dialogue with structured "action" labels (e.g., issue refund, look up order)

**Verdict:**
- [x] Adapt it
[Explanation: Use ABCD's dialogues and policy documents as inspiration for my own custom test prompts (Step 3), rather than running the full benchmark as is. The policy following structure is exactly what I want to test, but the dataset's specific company and policies do not match my client's actual policies.]

---

## Benchmark 2: Bitext Customer Support LLM Chatbot Dataset

Benchmark Name: Bitext Customer Support LLM Chatbot Training Dataset
Year: 2024
Source: Bitext Innovations, Hugging Face, `bitext/Bitext-customer-support-llm-chatbot-training-dataset`

**Why it seemed relevant:**
This dataset has 26,872 question and answer pairs, tagged across 27 intents in 10 categories (such as ORDER, ACCOUNT, PAYMENT, REFUND, DELIVERY) that map closely to retail support. It also tags language variation such as politeness level and typos, which is useful for testing tone.

**Contamination risk:**
- [x] Medium - Some overlap possible
[Explanation: It is a public Hugging Face dataset released to fine-tune customer service chatbots, so it is likely present in the pretraining mix of some models, especially anything trained on recent web and Hugging Face data dumps.]

**Saturation risk:**
- [x] Medium - Some models perform well
[Explanation: The dataset is synthetic, generated with NLP/NLG tooling rather than collected from real customer conversations, so the phrasing patterns are more uniform than real support tickets. I would expect scores to cluster high without much separation between models, since the questions are template-generated rather than genuinely ambiguous.]

**Format:**
- [x] Free-form text

**Verdict:**
- [x] Adapt it
[Explanation: This is a training dataset, not an evaluation benchmark, so it was not built with contamination controls or held out test splits in mind. Best use is to pull realistic customer phrasings and intent categories from it to write my own held out test prompts, not to run it directly as a scored benchmark.]

---

## Benchmark 3: MMLU (Massive Multitask Language Understanding)

Benchmark Name: MMLU
Year: 2020
Source: Hendrycks et al., "Measuring Massive Multitask Language Understanding", also on Papers with Code and Hugging Face Open LLM Leaderboard

**Why it seemed relevant:**
MMLU is one of the most cited general knowledge benchmarks, and it is tempting to use it as a general check of "is this model smart enough" before deploying it for customer service. It covers 57 subjects with multiple choice questions.

**Contamination risk:**
- [x] High - Model definitely saw this during training
[Explanation: MMLU is one of the most widely used and discussed benchmarks in the field. Its questions and answers appear in many public sources, and multiple papers have documented contamination concerns for MMLU across major model families.]

**Saturation risk:**
- [x] High - Many models achieve near-perfect scores
[Explanation: Current frontier models score in the high 80s to low 90s percent range on MMLU, leaving little room to distinguish between strong models, and almost no signal about tone, policy compliance, or complaint handling, which are my client's actual concerns.]

**Format:**
- [x] Multiple Choice

**Verdict:**
- [x] Reject it
[Explanation: Despite being well known, MMLU tests academic multiple choice knowledge, not free-form, policy-bound, tone-sensitive customer service dialogue. High saturation and contamination make it a poor discriminator even on its own terms, and the task format does not match my client's use case at all. Including it here mainly to show why a popular general benchmark is not automatically the right choice for a specific business use case.]
