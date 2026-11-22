# Benchmark audit (Step 2)

**Client scenario:** Kranich Direktbank AG (fictional, Berlin) wants an LLM to draft consumer-loan decline letters from internal case files. The letters must be accurate, compliant and humane. Since 20 November 2026, Germany's law implementing the EU Consumer Credit Directive (EU) 2023/2225 entitles applicants to an explanation and to human intervention when a credit assessment is automated. The key failure modes are: an invented or wrong decline reason, missing rights disclosures, leaked internal or discriminatory information, and a cold or falsely hopeful tone.

What a benchmark would have to test: **(a)** following hard constraints (include X, never Y, length), **(b)** reasoning correctly about regulatory duties, and **(c)** empathetic, appropriate tone. I audited one benchmark for each.

---

## Card 1: IFEval

```
Benchmark Name: IFEval (Instruction-Following Eval)
Year: 2023 (arXiv Nov 2023)
Source: Zhou et al., "Instruction-Following Evaluation for Large Language Models",
        arXiv:2311.07911 · https://github.com/google-research/google-research/tree/master/instruction_following_eval

Why it seemed relevant:
Our letters are full of hard constraints: quote the reference number, include the
review right, stay under 250 words, never mention internal scores. IFEval measures
exactly this kind of "verifiable instruction" (about 500 prompts, 25 constraint types)
with programmatic checks, so no judge is needed.

Contamination risk:
[ ] Low   [ ] Medium   [x] High
Explanation: the prompts and checking code have been public on GitHub and Hugging Face
since 2023, and IFEval is a standard leaderboard metric that model developers optimise
for. Any 2025-26 model has very likely seen the prompts or near-copies of them.

Saturation risk:
[ ] Low   [ ] Medium   [x] High
Explanation: leaderboards in mid-2026 show the top models clustered around 94-95%,
within about half a point of each other, so IFEval no longer separates good models
from great ones. Its successor IFBench (Ai2, NeurIPS 2025) is harder.

Format:
[ ] Multiple Choice  [x] Free-form text (checked by rules)  [ ] Code generation

Verdict:
[ ] Use it as-is   [x] Adapt it   [ ] Reject it
How: keep the METHOD, not the data. Generic constraints ("write in all lowercase")
say nothing about bank letters. I copied the idea of deterministic checks into my own
rule layer: required terms (reference number, "human review"), forbidden terms
(internal cut-off scores, nationality), and a word limit. These checks are written for
our letters and are free to run.
```

## Card 2: LegalBench

```
Benchmark Name: LegalBench
Year: 2023 (NeurIPS 2023, Datasets & Benchmarks Track)
Source: Guha et al., "LegalBench: A Collaboratively Built Benchmark for Measuring Legal
        Reasoning in Large Language Models", arXiv:2308.11462 · https://hazyresearch.stanford.edu/legalbench

Why it seemed relevant:
A decline letter is a regulated document: it must reflect what the law requires
(explanation, human review, credit-bureau transparency). LegalBench is the best-known
legal-reasoning benchmark: 162 tasks covering six types of legal reasoning, built by
legal professionals. It looked like a way to test whether the model "knows the rules".

Contamination risk:
[ ] Low   [x] Medium   [ ] High
Explanation: the tasks are public, and many are built from public sources (US case law,
contracts, CUAD), which are likely in pre-training data. They are less commonly
optimised for than IFEval, so the risk is medium rather than high.

Saturation risk:
[ ] Low   [x] Medium   [ ] High
Explanation: frontier models score high on many classification tasks (issue spotting,
definitions), but harder rule-application and interpretation tasks still separate
models. Saturation is uneven across the 162 tasks.

Format:
[x] Multiple Choice / classification (most tasks)  [x] Free-form text (a few)  [ ] Code generation

Verdict:
[ ] Use it as-is   [ ] Adapt it   [x] Reject it
Why: wrong jurisdiction and wrong task. The tasks are mostly US law and short-answer
classification. None covers GDPR Art. 22, the EU Consumer Credit Directive or German
consumer-credit law, and none asks the model to WRITE a compliant document to a
customer. A high LegalBench score would not show that our letters include the right to
human review. The compliance knowledge we need is encoded directly in my judge criteria
and rule checks instead.
```

## Card 3: EQ-Bench (v1 and v3)

```
Benchmark Name: EQ-Bench (Emotional Intelligence Benchmark); EQ-Bench 3 is the current version
Year: 2023 (v1, arXiv Dec 2023); EQ-Bench 3 released 2025
Source: Paech, "EQ-Bench: An Emotional Intelligence Benchmark for Large Language Models",
        arXiv:2312.06281 · https://eqbench.com · https://github.com/EQ-bench/eqbench3

Why it seemed relevant:
Tone is a main client concern: a rejected applicant (case TC4 has just lost her job) must
be treated with empathy, without false hope. EQ-Bench measures emotional intelligence.
v1 asks models to rate the emotional intensity of characters in tense dialogues (60
questions). EQ-Bench 3 uses multi-turn role-plays scored by an LLM judge (Claude Sonnet
3.7) on dimensions such as demonstrated empathy and pragmatic EI.

Contamination risk:
[ ] Low   [x] Medium   [ ] High
Explanation: v1's 60 questions are public and small, so they are easy to memorise. v3's
role-play scenarios are also public, but its scoring is judge-based and harder to game
by memorisation. Medium overall.

Saturation risk:
[ ] Low   [x] Medium   [ ] High
Explanation: v1 is close to saturated for frontier models and correlates very strongly
(r = 0.97) with MMLU, so it mostly re-measures general ability. v3's Elo leaderboard still
separates models, but it is relative (pairwise) rather than an absolute "good enough" bar.

Format:
[ ] Multiple Choice  [x] Free-form text (v3 role-play, LLM-judged)  [x] Other: numeric emotion ratings (v1)

Verdict:
[ ] Use it as-is   [x] Adapt it   [ ] Reject it
How: borrow the RUBRIC IDEA, not the scenarios. Relationship conflicts and workplace
mediation are far from a formal bank letter, and "assertive" or "warm" role-play
behaviour is not what a regulated letter needs. I adapted the judged-empathy dimension
into one narrow criterion in my judge (tone_clarity: respectful, empathetic, neither cold
nor patronising nor falsely hopeful). It sits next to compliance criteria, so a warm
letter that leaks internal data still fails. EQ-Bench 3 also uses a single proprietary
judge, a bias I avoid copying blindly (see judge calibration in evaluation_design.md).
```

---

## Conclusion of the audit

| Benchmark | Measures | Contamination | Saturation | Verdict |
|---|---|---|---|---|
| IFEval | Following verifiable constraints | High | High (~95% at the top) | **Adapt** its method into rule checks |
| LegalBench | Legal reasoning (US-centric) | Medium | Medium | **Reject**: wrong jurisdiction and task format |
| EQ-Bench | Emotional intelligence | Medium | Medium (v1 near-saturated) | **Adapt** its empathy rubric into one judge criterion |

**No public benchmark tests what the client needs:** faithful, EU-compliant, humane decline letters from German case files. Each one covers at most a slice of the problem, and the two most relevant are already saturated or contaminated. That justifies the custom mini-benchmark in `evaluation_design.md`: 5 realistic case files, rule checks inspired by IFEval, and an LLM judge whose criteria combine compliance with the empathy dimension adapted from EQ-Bench.

**Sources:**
- Zhou et al. 2023, IFEval: https://arxiv.org/abs/2311.07911
- IFEval leaderboard clustering, July 2026: https://www.benchlm.ai/benchmarks/ifeval
- IFBench (Ai2): https://allenai.org/blog/ifbench-artificial-analysis
- Guha et al. 2023, LegalBench: https://arxiv.org/abs/2308.11462 and https://hazyresearch.stanford.edu/legalbench
- Paech 2023, EQ-Bench: https://arxiv.org/abs/2312.06281
- EQ-Bench 3: https://eqbench.com
- CCD II application date: https://kpmg.com/ie/en/insights/banking/consumer-credit-directive-ii.html
- German implementing act in force 20 Nov 2026: https://www.osborneclarke.com/de/insights/die-neue-verbraucherkreditrichtlinie-ccd-ii-was-marktteilnehmer-jetzt-wissen-und-bis
