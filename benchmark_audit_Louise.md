# Benchmark Audit

**Scenario:** A company deploys an AI coaching assistant for employees to help them
define personal/professional development goals and improve performance in their
current role. Requirements: goals must be specific, measurable, and genuinely
derived from what the employee said (not generic templates); the assistant must
maintain a supportive, non-judgmental coaching tone (not directive or clinical);
it must recognize when a topic falls outside coaching scope (e.g. mental health
distress, HR/legal issues, harassment) and redirect appropriately. Main concerns:
generic advice that ignores what the employee actually said, the assistant
overstepping into therapy territory, and sycophantic responses that just validate
rather than ask probing coaching questions (e.g. GROW model, powerful questions).

---

## Benchmark 1: MT-Bench

**Year:** 2023 (Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot
Arena")
**Source:** https://arxiv.org/abs/2306.05685

**Why it seemed relevant:**
MT-Bench evaluates multi-turn conversational quality using LLM-as-judge, which
matches the mechanics of a coaching conversation (multi-turn, context-dependent,
judged on helpfulness/relevance rather than a single correct answer). It's also
the reference implementation most tutorials point to for building an LLM-judge
pipeline, so it's a natural starting point to borrow judging methodology from.

**Contamination risk:**
- [x] High - Model definitely saw this during training
- Explanation: the 80 questions and reference answers have been public on GitHub
  since 2023 and are widely cited/reproduced in papers, blog posts, and
  leaderboards, so current frontier models have almost certainly seen this data.

**Saturation risk:**
- [x] High - Many models achieve near-perfect scores
- Explanation: leaderboard data shows scores clustering near the top of the 1–10
  scale for capable models, with limited separation between them, and the
  benchmark's general categories (writing, roleplay, reasoning, coding, etc.)
  are now comfortably within range for most frontier models.

**Format:**
- [x] Free-form text (LLM-judged on a 1–10 scale, single or pairwise)

**Verdict:**
- [x] Reject it (explain why)
- MT-Bench is domain-generic — its 8 categories (writing, roleplay, extraction,
  reasoning, math, coding, STEM/humanities knowledge) contain nothing about
  coaching technique, and none of its questions test whether a model asks good
  probing questions versus giving generic advice. Its judging *methodology*
  (single-answer grading with a 1–10 scale and written rubric) is worth reusing,
  but the benchmark's content isn't fit for this use case.

---

## Benchmark 2: EmpatheticDialogues

**Year:** 2019 (Rashkin et al., "Towards Empathetic Open-domain Conversation
Models: A New Benchmark and Dataset", ACL 2019)
**Source:** https://aclanthology.org/P19-1534/

**Why it seemed relevant:**
25k crowdsourced conversations grounded in a labeled emotion, where a "listener"
responds to a "speaker" describing a situation. Tone and emotional attunement are
exactly one of the failure modes I'm worried about (sycophantic or clinical
tone), so a dataset built specifically to test empathetic responding is a
plausible fit.

**Contamination risk:**
- [x] High - Model definitely saw this during training
- Explanation: the dataset has been public since 2019, is hosted on Hugging Face
  and Kaggle, and is a standard citation in empathy/dialogue papers — very likely
  in pretraining data for any recent LLM.

**Saturation risk:**
- [ ] Medium - some models perform well on the underlying task, but there's no
  single leaderboard number to point to since it's typically used for
  fine-tuning/evaluation of smaller dialogue models rather than frontier LLMs.

**Format:**
- [x] Free-form text (originally designed for retrieval/generation with human
  eval, not exact-match)

**Verdict:**
- [x] Adapt it (explain how)
- The dataset measures *empathetic acknowledgment* ("I'm sorry to hear that,
  that sounds hard") — useful but insufficient for coaching, where the goal
  isn't just to validate feelings but to move the employee toward a specific,
  actionable goal. I'd adapt it by using its situation-grounded conversation
  *format* as a template — real employee-goal scenarios in place of the original
  emotional situations — but replace its empathy-only grading with a rubric that
  also checks whether the model asked a clarifying/probing question rather than
  just validating.

---

## Benchmark 3: MMLU (Massive Multitask Language Understanding)

**Year:** 2021 (Hendrycks et al., "Measuring Massive Multitask Language
Understanding")
**Source:** https://arxiv.org/abs/2009.03300

**Why it seemed relevant:**
Included deliberately as a check on my own instinct to reach for a well-known,
"respected" general benchmark — it's often the first name that comes up when
people ask "how do we evaluate this model," so it's worth showing explicitly why
it doesn't apply here.

**Contamination risk:**
- [x] High - Model definitely saw this during training

**Saturation risk:**
- [x] High - Many models achieve near-perfect scores
- Explanation: frontier models now score in the 85–90%+ range, and recent work
  ("Are We Done with MMLU?", NAACL 2025) documents label errors and ceiling
  effects in the benchmark itself.

**Format:**
- [x] Multiple Choice

**Verdict:**
- [x] Reject it (explain why)
- MMLU tests recall of factual, multiple-choice academic knowledge across 57
  subjects (law, medicine, history, etc.). No coaching conversation requires
  answering an exam question — the coaching assistant's job is to ask good
  questions and stay in scope, not to demonstrate subject-matter recall. Including
  this card is meant to demonstrate the audit skill of correctly rejecting a
  well-known but irrelevant benchmark, rather than using popularity as a proxy
  for fit.
