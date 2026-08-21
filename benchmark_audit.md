## Step 2, Benchmark Audit

### Benchmark Evaluation Card 1

**Benchmark Name:** MMLU (Massive Multitask Language Understanding)  
**Year:** 2020  
**Source:** https://arxiv.org/abs/2009.03300

**Why it seemed relevant:**  
MMLU is the default general-capability benchmark, and it includes law and professional knowledge subsets that appear to touch consumer credit. If a model scores well across professional domains, the intuition is that it "knows enough" to draft a regulated financial letter.

**Contamination risk:**  
[x] High - Model definitely saw this during training  
Explanation: The test set has been publicly available since 2020 and is reproduced across countless papers, repos and leaderboard harnesses. Reported scores cannot be cleanly separated from memorisation.

**Saturation risk:**  
[x] High - Many models achieve near-perfect scores  
Explanation: Frontier models now cluster tightly at the top of the range (current leaderboard figure: [FILL IN]). A benchmark that no longer separates candidate models cannot inform a procurement decision.

**Format:**  
[x] Multiple Choice

**Verdict:**  
[x] Reject it  
Reason: Format mismatch is fatal, not incidental. Our task is generating prose from a structured decision record. A multiple choice test cannot detect a fabricated decline reason, because there is nothing for the model to fabricate. High scores here would tell Nordbank nothing about the risk that actually concerns them.

---

### Benchmark Evaluation Card 2

**Benchmark Name:** TruthfulQA  
**Year:** 2021  
**Source:** https://arxiv.org/abs/2109.07958

**Why it seemed relevant:**  
Our primary failure mode is the model inventing or softening a decline reason. TruthfulQA is the best known benchmark aimed at whether a model generates falsehoods, so it looks like a direct proxy for hallucination risk in our letters.

**Contamination risk:**  
[x] High - Model definitely saw this during training  
Explanation: 817 questions, public since 2021, widely reproduced in training corpora, papers and evaluation harnesses. A high score is at least as consistent with memorisation of the reference answers as with a general disposition toward truthfulness.

**Saturation risk:**  
[ ] Low  [x] Medium  [ ] High  
Explanation: The original paper reported the best model truthful on 58% of questions against 94% for humans, so it was far from saturated at release. Scores have risen substantially since, but the contamination problem makes it hard to read that rise as genuine improvement.

**Format:**  
[x] Free-form text (also administered in a multiple choice variant)

**Verdict:**  
[x] Reject it  
Reason: It measures resistance to well-known human misconceptions, which is a different construct from faithfulness to a document placed in front of the model. Our model will never be asked a trivia question. It will be asked to restate a decline reason it has been given. Scoring well on TruthfulQA would be reassuring theatre.

---

### Benchmark Evaluation Card 3

**Benchmark Name:** SummEval  
**Year:** 2021 (TACL; arXiv preprint 2020)  
**Source:** https://arxiv.org/abs/2007.12626

**Why it seemed relevant:**  
This is the closest structural analogue we found. Judging whether a summary is faithful to its source document is the same shape of problem as judging whether a rejection letter is faithful to its decision record. SummEval also rates consistency, fluency, coherence and relevance, which maps loosely onto our accuracy and clarity requirements.

**Contamination risk:**  
[ ] Low  [x] Medium  [ ] High  
Explanation: Built on the CNN/DailyMail corpus, which is heavily present in training data. The human annotations themselves are less likely to be memorised, but the underlying articles almost certainly are.

**Saturation risk:**  
[x] Low - Benchmark is challenging  
Explanation: Faithfulness remains unsolved. SummEval's own finding was that automatic metrics correlate weakly with human judgment, and its expert and crowd-sourced annotators did not agree closely with each other.

**Format:**  
[x] Free-form text, scored on 5-point Likert scales by human annotators

**Verdict:**  
[x] Adapt it  
How: We borrow the method, not the data. Specifically: (1) the consistency dimension becomes our faithfulness criterion, scored against the decision record rather than a news article; (2) we keep the practice of scoring several independent dimensions separately instead of collapsing quality into one number; (3) we take its annotator disagreement as a warning, and build calibration examples into our judge prompt from the start. We discard the dataset itself, which is English 2017-2019 news summarisation with no compliance dimension.

### Audit conclusion

None of the three benchmarks can tell Nordbank whether a generated letter is compliant. Two fail on construct validity, measuring something adjacent to our concern rather than our concern itself. The third measures the right construct on the wrong domain, in the wrong language, with no regulatory dimension. This is the standard result of a benchmark audit for a narrow regulated use case, and it is the reason Step 3 builds a custom evaluation set instead.
