# Benchmark Audit

**Client scenario:** A retailer wants a customer-service chatbot that can handle returns,
product questions, and complaints. Key concerns: helpfulness, tone, and resolution rate —
particularly for frustrated customers reporting repeated delivery/damage failures (see
[`evaluation_memo.md`](./evaluation_memo.md) and [`llm_judge_evaluation.py`](./llm_judge_evaluation.py)).

Three benchmarks were sourced from the "instruction following / dialogue" category and
evaluated for fit against this scenario.

---

## Benchmark 1: MultiWOZ

```
Benchmark Name: MultiWOZ (Multi-Domain Wizard-of-Oz)
Year: 2018 (v2.2 revision: 2020)
Source: Budzianowski et al., "MultiWOZ - A Large-Scale Multi-Domain Wizard-of-Oz Dataset
for Task-Oriented Dialogue Modelling," EMNLP 2018. https://arxiv.org/abs/1810.00278
(v2.2: https://arxiv.org/abs/2007.12720)

Why it seemed relevant:
MultiWOZ is one of the most widely used task-oriented dialogue benchmarks, covering
multi-turn conversations across domains like hotel, restaurant, and taxi booking. It
structurally resembles a retail support conversation — a customer states a goal, the
system must track slots/intents across turns — so it looked like a plausible stand-in
for testing whether a chatbot correctly extracts order details from a complaint.

Contamination risk:
[x] High - Model definitely saw this during training
Explanation: MultiWOZ has been public since 2018, is one of the most cited dialogue
datasets in NLP, and is commonly included in instruction-tuning and pretraining data
mixes. Any current frontier model has almost certainly seen this data directly or
via derivative works.

Saturation risk:
[x] High - Many models achieve near-perfect scores
Explanation: Joint goal accuracy and slot-filling accuracy on MultiWOZ have been
climbing for years; the dialogue-state-tracking leaderboard is widely considered
close to saturated for standard slot types, so it would no longer discriminate
between strong candidate models.

Format:
[x] Free-form text (multi-turn dialogue transcripts with structured belief-state /
slot-value annotations)

Verdict:
[x] Reject it (explain why)
MultiWOZ measures slot/state-tracking accuracy (did the system correctly track
"hotel: 2 nights, city: Cambridge"), not tone, empathy, or policy-consistent
resolution. It has no complaint-handling or de-escalation scenarios, and
contamination + saturation mean even a strong score would say little about
real-world performance on this client's use case.
```

---

## Benchmark 2: ABCD (Action-Based Conversations Dataset)

```
Benchmark Name: ABCD (Action-Based Conversations Dataset)
Year: 2021
Source: Chen, Chen, Su, Xiong, "Action-Based Conversations Dataset: A Corpus for
Building More In-Depth Task-Oriented Dialogue Systems," NAACL 2021 (ASAPP).
https://arxiv.org/abs/2104.00783

Why it seemed relevant:
ABCD is the closest of the three to the client's actual use case: it's built from
customer-agent transcripts where the agent must follow a policy "flowchart"
(verify identity, look up an order, choose an action such as refund, replacement,
or escalation) — structurally very similar to the refund/replacement policy check
our complaint-handling prompt tests.

Contamination risk:
[x] Medium - Some overlap possible
Explanation: ABCD is public and has been available since 2021, so it's plausible
recent models have seen it, but it's far less ubiquitous in training corpora than
MultiWOZ — it hasn't become a standard pretraining-mix inclusion the way older
dialogue datasets have.

Saturation risk:
[x] Medium - Some models perform well
Explanation: Intent/slot classification on ABCD is comparatively easy for modern
models, but full-dialogue "action" prediction and cascading dialogue success still
show meaningful gaps between models — it isn't fully saturated.

Format:
[x] Other: Free-form dialogue transcripts + structured "action" labels drawn from
a fixed policy tree (a hybrid of free-form text and constrained classification)

Verdict:
[x] Adapt it (explain how)
ABCD doesn't score tone or empathy, and its action taxonomy doesn't match this
client's specific refund/replacement policy, so it can't be used as-is. But its
overall structure — a policy tree the agent must follow correctly while handling
a live customer request — was used as a structural template for designing our
own complaint-handling prompt and judge criteria, rather than as a scored
benchmark.
```

---

## Benchmark 3: EchoMind

```
Benchmark Name: EchoMind (audio-based emotional-cue recognition benchmark)
Year: Unverified
Source: Encountered during an initial keyword search for "customer service emotion
recognition benchmark"; unlike MultiWOZ and ABCD, a canonical paper/citation for
this benchmark could not be independently re-verified while writing this audit.
Treat the entry below as illustrative of a *class* of benchmark (speech-emotion
recognition, e.g. datasets in the style of IEMOCAP/MELD) rather than as a
verified single source — flagged explicitly rather than fabricating a citation.

Why it seemed relevant:
It appeared in a search for benchmarks that score "emotional appropriateness" of
a response, which sounded directly relevant to judging whether our chatbot
de-escalates a frustrated customer.

Contamination risk:
[ ] Low
[ ] Medium
[x] High - Model definitely saw this during training
Explanation: Cannot be assessed with confidence given the unverified source — 
treated conservatively as high/unknown risk rather than assumed low.

Saturation risk:
[ ] Low
[ ] Medium
[x] High - Many models achieve near-perfect scores
Explanation: Same caveat as above — without a verifiable source, saturation
cannot be responsibly assessed, so this is treated as a disqualifying unknown
rather than given the benefit of the doubt.

Format:
[x] Other: Audio recordings with emotion labels (speech-emotion recognition)

Verdict:
[x] Reject it (explain why)
Two independent disqualifiers: (1) modality mismatch — it scores *audio* prosody
cues, and our chatbot's channel is text, so even a verified version of this
benchmark wouldn't transfer; (2) the citation could not be confirmed during this
audit, which on its own is a reject-worthy red flag for any benchmark a client
report would need to stand behind. Included here deliberately, despite the
reject verdict, as a reminder to always verify a benchmark's source before
citing it in client-facing work.
```

---

## Audit conclusion

None of the three benchmarks directly transfers to this scenario: two (MultiWOZ,
ABCD) test slot/state-tracking or policy-action accuracy without any tone/empathy
dimension, and the third (EchoMind) has a modality mismatch and an unverifiable
citation. This is the basis for building a **custom evaluation** (see
[`evaluation_design.md`](./evaluation_design.md)) rather than adopting an existing
benchmark as-is.
