## Benchmark 1: IFEval (Instruction-Following Eval)

**Year:** 2023
**Source:** Zhou et al., "Instruction-Following Evaluation for Large Language Models", https://arxiv.org/abs/2311.07911

**Why it seemed relevant:**
Our rejection letters must reliably include specific elements (the rejection reason, the appeal route, a contact point) and follow format rules. IFEval tests exactly this kind of behaviour, whether a model obeys explicit, verifiable instructions, and checks it with rule-based verification rather than subjective grading.

**Contamination risk:** ☑ High
IFEval is public on GitHub and Hugging Face and is widely used on leaderboards since 2023. It is very likely to be in the training data of recent models, and vendors actively optimise for it.

**Saturation risk:** ☑ High
Frontier models score close to the ceiling on IFEval, so it no longer separates strong models well.

**Format:** ☑ Other: free-form text responses checked by ~25 types of programmatic, verifiable instructions (e.g. "include keyword X", "write at least 300 words", "no commas")

**Verdict:** ☑ Adapt it
The method is valuable: rule-based checks on verifiable instructions. The content is not: its instructions are generic format constraints ("answer in all caps"), not banking requirements. We will borrow the approach and write our own verifiable checks, e.g. "letter mentions the specific rejection reason", "includes the complaint procedure (Kifid)", "does not mention age, nationality or pregnancy".

## Benchmark 2: LegalBench

**Year:** 2023
**Source:** Guha et al., "LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models", https://arxiv.org/abs/2308.11462

**Why it seemed relevant:**
Rejection letters are a regulated communication: they must state a lawful reason and not misrepresent the applicant's rights. LegalBench is the best-known benchmark for legal reasoning in LLMs, with 162 tasks built together with legal professionals, so it looked like the natural way to test a model's grasp of compliance-relevant content.

**Contamination risk:** ☑ Medium
The dataset is public on GitHub and Hugging Face, so some leakage into training data is likely. Many tasks were newly written for the benchmark rather than scraped from the web, which lowers the risk compared to older benchmarks.

**Saturation risk:** ☑ Medium
Strong models perform well on simpler tasks (e.g. issue spotting, definitions), but harder rule-application and interpretation tasks still show clear differences between models.

**Format:** ☑ Other: mostly classification and short-answer tasks (yes/no, multiple choice, short extraction); very few free-form generation tasks

**Verdict:** ☑ Reject it
LegalBench is built mainly on US law (contracts, US statutes, US case law), while our client operates under Dutch and EU consumer-credit rules. More importantly, it tests legal *reasoning* through short answers, not *writing* a clear, empathetic letter for a consumer. A high LegalBench score would tell the client little about whether generated letters are accurate, complete and appropriate in tone.

## Benchmark 3: BBQ (Bias Benchmark for QA)

**Year:** 2021
**Source:** Parrish et al., "BBQ: A Hand-Built Bias Benchmark for Question Answering", https://arxiv.org/abs/2110.08193

**Why it seemed relevant:**
A rejection letter that reflects bias, e.g. hinting that age or nationality played a role, is both a legal risk (discrimination) and a reputational one. BBQ measures whether models rely on social stereotypes across nine protected dimensions, including age, nationality, disability and gender, which overlaps directly with this failure mode.

**Contamination risk:** ☑ High
BBQ has been public since 2021 and is part of standard safety evaluation suites (e.g. HELM). It has almost certainly been seen during training, and model developers explicitly tune for it.

**Saturation risk:** ☑ Medium
Modern models score highly on the disambiguated questions, where the context gives the answer. The ambiguous questions, where the correct answer is "unknown", remain more informative, but the gap between top models is narrowing.

**Format:** ☑ Multiple Choice (three options, including an "unknown" option)

**Verdict:** ☑ Adapt it
The multiple-choice format does not match our free-text letter generation, and its scenarios are US-centric. Its core design idea is valuable, though: include a protected attribute in the context that should *not* influence the output. We adapt this in our own Prompt #4, where the applicant's file mentions age and nationality, and we check that neither appears in the letter or affects the stated reason.

## Conclusion

None of the three benchmarks measures what our client needs: accurate, complete, compliant and empathetic rejection letters under Dutch/EU rules. Public benchmarks are either saturated and likely contaminated (IFEval, BBQ) or focused on a different jurisdiction and task type (LegalBench). This justifies building a small custom evaluation (see `evaluation_design.md`), borrowing IFEval's rule-based verification and BBQ's protected-attribute design.