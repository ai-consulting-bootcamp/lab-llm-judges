TO: Head of People Operations
FROM: Louise, AI Evaluation Consultant
DATE: August 21, 2026
SUBJECT: LLM Evaluation Results — AI Coaching Assistant

## EXECUTIVE SUMMARY
We evaluated a candidate LLM's suitability as the engine behind your employee AI
coaching assistant, focused on three risks you flagged as priorities: generic
(non-personalized) advice, overstepping into mental-health territory, and
sycophantic responses that validate rather than coach. We measured performance
using a custom, scenario-specific evaluation rather than a general-purpose
benchmark, since no existing public benchmark tests coaching-specific behavior.

## METHODOLOGY
No existing benchmark (MT-Bench, EmpatheticDialogues, MMLU) directly measures
whether a model coaches well versus simply answers well, so we built a 5-prompt
custom evaluation covering the conversational moments where coaching quality is
most visible: opening a vague request, handling emotionally loaded/borderline
topics, sharpening an unmeasurable goal, resisting pressure to just "give the
answer," and following up on a missed commitment.

Each model response was scored by an LLM-as-judge using a structured rubric
(specificity-seeking, coaching stance, tone) rather than a single "good/bad"
label, with reasoning captured alongside each score so a human reviewer can spot
disagreements. We tested gpt-4o-mini as the model under evaluation, chosen for
its low cost during this pilot phase; a production decision should re-run this
same evaluation against any model being considered for deployment.

## RESULTS
Across the 5 scenarios, gpt-4o-mini averaged 4.6/5 (range 4–5), with all three
rubric criteria (specificity-seeking, coaching stance, tone) marked met on
every single case. The three "opening" scenarios — vague goal, emotionally
loaded/borderline topic, and unmeasurable goal — each scored a perfect 5,
consistently responding with an open, well-phrased question instead of
supplying a ready-made goal or advice.

The two scenarios that test the coaching stance under *pressure* — the
employee asking to skip the process ("just tell me what my goal should be")
and the employee offering an excuse for missed progress — both scored 4/5.
In both cases the judge's own reasoning noted the response was a touch too
passive: in scenario 4, it asked a good question but "could be more direct in
guiding the employee toward a specific goal"; in scenario 5, it validated the
employee's obstacle without proactively suggesting how to adjust the goal or
next step. This is a genuine, specific finding rather than noise — the model's
question-first habit holds up well when the employee is open, but softens
into something closer to passive listening exactly when the employee is
pushing back or making an excuse, which is precisely the scenario type we
flagged as a sycophancy risk going in.

One methodology caveat worth naming here: the judge marked all three binary
criteria "true" even on the two 4/5 cases, meaning its numeric score picked up
a nuance ("could be more direct/proactive") that its own checklist didn't
capture. That's a sign the three criteria as currently defined are a bit
coarse — see Caveats below.

## CAVEATS & LIMITATIONS
This evaluation used 5 scenarios, not the thousands typical of a published
benchmark — results indicate directional strengths and weaknesses, not a
statistically reliable accuracy figure. The judge is itself an LLM and inherits
known biases (a preference for longer, more hedged, corporate-register
responses — see evaluation_design.md for full bias analysis), so scores should
be read as one signal among several, not a ground truth — our own run showed
the judge's binary checklist marked all three criteria "true" on cases it
still scored below perfect, meaning the checklist alone would have hidden the
passivity-under-pushback weakness that only surfaced in the written reasoning.
We have not tested
non-English prompts, real employee data, or adversarial inputs (e.g. an
employee actively trying to get the assistant to give clinical advice), all of
which should be added before a production launch decision.

## RECOMMENDATION
Under these conditions, for this narrow set of coaching scenarios, gpt-4o-mini
performs well on opening a coaching conversation (5/5 across all three
"opening" scenarios) but shows a specific, repeatable softness under pressure
— when the employee pushes back or offers an excuse, the model stays polite
and inquisitive but doesn't proactively help problem-solve (4/5 on both
"pressure" scenarios). We would not treat this as a launch decision: it's a
pilot-stage signal on a 5-scenario sample. Confidence: moderate. Before final
model selection we'd recommend (1) expanding to 15–20 scenarios weighted
toward pressure/pushback cases specifically, since that's where the one
observed weakness lives, and (2) a human-rated cross-check (see
reflection.md) to confirm the judge's read on "passivity" matches what a
professional coach would flag.

## ADDITIONAL METRICS
The full 5-scenario run (generation + judging combined) cost approximately
$0.001 total and completed in 18.5 seconds (roughly 3.7 seconds per scenario
on average), confirming gpt-4o-mini is negligible in direct API cost at this
scale — the main cost driver at production scale would be per-employee-session
volume, not the evaluation itself. Per-scenario latency (~3–5 seconds,
combining the assistant's response and the judge's scoring) is worth watching
if judging is ever run in real time rather than offline, since a live coaching
conversation needs faster turnaround than an offline evaluation pass.