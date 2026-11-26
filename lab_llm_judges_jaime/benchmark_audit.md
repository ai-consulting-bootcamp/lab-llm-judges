# Benchmark audit (Steps 1–2)

## Step 1: Client scenario

**Client:** a European consultancy that is building an AI assistant for small and medium-sized businesses (SMEs). SME owners ask it practical questions about the **EU AI Act** and the **GDPR**, for example "Is this tool high-risk?" or "Can I send this data to a US provider?".

**Requirements:** the assistant must name the correct legal category or article, give a concrete next step in plain language, and say when a lawyer must confirm.

**Main failure modes:**
- inventing or misdating legal obligations (hallucination);
- telling a business it is "compliant" (overclaiming);
- answers that are correct but impossible for a non-lawyer to act on.

---

## Step 2: Three existing benchmarks

### Card 1: LegalBench

```
Benchmark Name: LegalBench
Year: 2023
Source: Guha et al., "LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in
        Large Language Models", NeurIPS 2023 Datasets & Benchmarks (arXiv:2308.11462)

Why it seemed relevant:
162 legal-reasoning tasks (issue spotting, rule recall, rule application, interpretation). It is the
best-known public benchmark for "can a model reason like a lawyer", which is what our assistant must do.

Contamination risk:
[x] Medium - Some overlap possible
Explanation: the tasks have been public on GitHub and Hugging Face since 2023, so recent models may
have seen them. Most tasks are built from US law (contracts, US statutes, US case law).

Saturation risk:
[x] Medium - Some models perform well
Explanation: frontier models score highly on many rule-recall tasks; harder interpretation tasks
still separate models.

Format:
[x] Other: mostly classification and short-answer (yes/no, labels), some free-form

Verdict:
[x] Adapt it
Keep its task taxonomy (rule recall vs. rule application vs. issue spotting) to structure our own
prompts, but do not use its items: they test US law, not the AI Act or the GDPR, and short labels
cannot measure hedging or actionability.
```

### Card 2: LexGLUE

```
Benchmark Name: LexGLUE
Year: 2022
Source: Chalkidis et al., "LexGLUE: A Benchmark Dataset for Legal Language Understanding in English",
        ACL 2022 (arXiv:2110.00976)

Why it seemed relevant:
It includes EU material: EUR-LEX (classifying EU legislation by topic) and ECtHR (European Court of
Human Rights cases). It is the main benchmark with European legal text.

Contamination risk:
[x] High - Model definitely saw this during training
Explanation: EUR-Lex documents and ECtHR judgments are public and widely crawled; the dataset itself
has been public since 2021.

Saturation risk:
[x] Medium - Some models perform well
Explanation: designed for fine-tuned encoder models; large LLMs do well on several sub-tasks.

Format:
[x] Other: multi-label classification of documents

Verdict:
[x] Reject it
It measures whether a model can label legal documents, not whether it can advise a non-lawyer. It
predates the AI Act (adopted 2024), so it cannot test the rules our client cares about.
```

### Card 3: TruthfulQA

```
Benchmark Name: TruthfulQA
Year: 2022
Source: Lin, Hilton & Evans, "TruthfulQA: Measuring How Models Mimic Human Falsehoods", ACL 2022
        (arXiv:2109.07958)

Why it seemed relevant:
Our worst failure is a confident but false legal statement. TruthfulQA measures whether a model
repeats common misconceptions, and includes a law category.

Contamination risk:
[x] High - Model definitely saw this during training
Explanation: 817 questions, public since 2021 and very widely used in model reports.

Saturation risk:
[x] High - Many models achieve near-perfect scores
Explanation: recent models score far above the original baselines; it no longer separates them well.

Format:
[x] Multiple Choice (MC1/MC2) and free-form generation

Verdict:
[x] Adapt it
Reuse the idea, not the items: include "trap" prompts where a plausible answer is wrong (for example
asking for a compliance claim, or assuming legitimate interest covers health data).
```

## Conclusion

None of the three can be used as-is: two are US-centred or pre-date the AI Act, and all three are public enough to be contaminated. We therefore built a **custom 5-prompt benchmark** (see `evaluation_design.md`), written from the course materials on the AI Act and the GDPR, with reference answers the model cannot have seen.
