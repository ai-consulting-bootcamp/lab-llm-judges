## Step 3, Five Evaluation Prompts

### Shared input format

Every prompt supplies the model with a decision record and asks for a full draft letter. Field names are fixed so the checks can be automated.

```text
DECISION RECORD
  applicant_name:
  product:
  decision_date:
  primary_reason:
  secondary_reason:
  bureau_consulted:
  bureau_score_used: true | false
```

### Prompt 1 - Reason fidelity (single reason)

Record: primary_reason = "insufficient documented income for the requested term"; secondary_reason = none; bureau_score_used = false.

Ground truth: the letter states insufficient documented income as the reason, and states no other reason. Because bureau_score_used is false, the letter must not reference a credit bureau at all.

Verification: automated. String and paraphrase check for the income reason, plus a blocklist check that no other decline reason from our taxonomy (payment history, existing obligations, bureau score, employment duration) appears, plus a check that no bureau name appears.

Why this prompt: this is the cheapest possible test of our single worst failure mode. If a model fails here it is disqualified before we spend money on judged evaluation.

### Prompt 2 - Mandatory element presence

Record: primary_reason = "level of existing credit obligations"; bureau_consulted = "SCHUFA"; bureau_score_used = true.

Ground truth: the letter contains all four mandatory elements. The stated reason. A statement of the right to request manual review, with the mechanism for doing so. A reference to the bureau consulted, because the score contributed. Under 300 words.

Verification: automated, four independent boolean checks plus a word count. Scored 0 to 4 rather than pass/fail, so partial failures are visible.

Why this prompt: omission is a silent failure. Nobody complains about a missing sentence, and it surfaces years later in an audit. Automating this check is strictly better than judging it, because the answer is binary and a judge would only add cost and noise.

### Prompt 3 - Tone under pressure

Record: primary_reason = "adverse payment history on an existing obligation"; applicant has been a customer for eleven years.

Ground truth: no single correct text. The letter must be neither condescending nor moralising about the payment history, and must not imply the decision is reversible or that the applicant should reapply imminently. It must acknowledge the relationship without using it to soften the factual finding.

Verification: LLM-as-judge, three separate scores for condescension, false hope, and plain language. Human spot-check on 20% of cases during the pilot, to calibrate the judge before we trust it unsupervised.

Why this prompt: this is a genuine judgment call that no rule can capture, and the emotionally loaded record is where tone drift is most likely. The eleven-year relationship is deliberate bait toward false warmth.

### Prompt 4 - Conditional logic

Two paired records, identical except that bureau_score_used is true in one and false in the other, with the same primary_reason in both.

Ground truth: the bureau reference appears in the first letter and is absent from the second. Everything else should be substantially equivalent.

Verification: hybrid. The presence and absence of the bureau reference is automated. Whether the two letters are otherwise equivalent, meaning the model did not silently restructure its reasoning, requires a judge comparing the pair.

Why this prompt: conditional obligations are where compliance actually breaks. A model that mentions the bureau every time passes Prompt 2 and still creates a legal problem, because it is asserting a bureau contribution that did not occur. Testing a matched pair catches what a single case cannot.

### Prompt 5 - Adversarial, incomplete record

Record: primary_reason = "" (empty); all other fields populated.

Ground truth: the model must not produce a finished letter. Correct behaviour is to refuse or to return a draft with an explicit flag that the decline reason is missing and must be supplied. Any letter that names a plausible-sounding reason is a critical failure, regardless of how well written it is.

Verification: hybrid. Automated check for whether any reason from our taxonomy appears, which should be zero. Judge assessment of whether the model's flag is clear enough for a loan officer to act on.

Why this prompt: production data has missing fields. This tests whether the model's default is to fill gaps or to surface them, which is the single most important disposition for a regulated drafting task. It is also the only prompt here where the desired output is not a letter, which makes it the one most likely to be quietly failed.

## Step 4, Judge Design

### Judge prompt

You are evaluating a draft loan rejection letter written by a language model for a German retail bank. A human loan officer will review and sign the letter before it is sent. Your job is to score the draft, not to rewrite it.

TASK DESCRIPTION
The model received a structured decision record and was asked to write the applicant-facing rejection letter. In this case the decline reason is adverse payment history on an existing obligation, and the applicant has been a customer of the bank for eleven years. You are assessing tone only. Factual accuracy and the presence of mandatory elements are checked separately by automated rules; do not score them, and do not lower a score because a required sentence is missing.

EVALUATION CRITERIA

1. Non-condescension. The letter states the finding without lecturing, moralising, or implying the applicant is financially irresponsible. Neutral factual statements about payment history are correct and must not be penalised. Advice the applicant did not ask for, and language that positions the bank as an instructor, are failures.

2. No false hope. The letter does not imply the decision may be reversed, that reapplying soon is likely to succeed, or that the outcome is provisional. Note carefully: informing the applicant of their right to request a manual review is required and is NOT false hope. False hope is a prediction about the outcome, not a statement of a procedural right.

3. Plain language. A reader without financial training understands the letter on one reading. Failures include unexplained jargon, sentences over roughly 25 words, nested subordinate clauses, and bureaucratic passive constructions that hide who decided what.

REASONING STEPS

Step 1: Read the letter once and identify the sentence that communicates the decline. Quote it.
Step 2: Assess criterion 1. Look specifically for evaluative language about the applicant as a person, as distinct from factual language about the account.
Step 3: Assess criterion 2. Separate procedural statements from predictive statements. Only predictive statements can create false hope.
Step 4: Assess criterion 3. Identify the single least readable sentence and judge whether a lay reader would follow it.
Step 5: Assign the overall score. Take the LOWEST of the three criteria rather than the average. A letter that is warm and readable but condescending is not a passable letter.

SCORE ANCHORS
5 = Sendable as drafted. Neutral, clear, no implied promises.
4 = Sendable after a trivial edit of one phrase.
3 = Usable structure, but one criterion clearly fails and a human must rewrite at least one sentence.
2 = Two criteria fail, or the tone would plausibly generate a complaint.
1 = The bank would not send this. Openly judgemental, or promises an outcome it cannot deliver.

OUTPUT FORMAT
Return only valid JSON, no preamble and no code fences.

```json
{
  "decline_sentence": "the sentence you quoted in Step 1",
  "score": 1-5,
  "reasoning": "two to four sentences citing specific wording",
  "criteria_met": {
    "non_condescension": true/false,
    "no_false_hope": true/false,
    "plain_language": true/false
  },
  "lowest_criterion": "name of the weakest criterion"
}
```

### Bias analysis

The judge and the model under test are both LLMs trained on overlapping data, which means they share a house style. A letter that sounds like generated text will read as fluent to the judge even when it is generic. The reverse also applies: authentically stiff German banking prose, which is what Nordbank's existing letters look like and what their customers expect, may be scored down as cold when it is in fact normal and appropriate for the genre. This is a style bias operating in both directions, and it is the largest threat to the validity of these scores.

There is a cultural and linguistic layer on top. Our criteria were written in English and encode an Anglo-American service norm in which warmth signals professionalism. German business correspondence uses a formal register that an English-trained judge can misread as unfriendly, and the formal address convention has no clean English equivalent. If we ever run the judge on German output while the judge prompt stays in English, we are measuring the letter against the wrong cultural baseline. Related: our plain language criterion penalises long sentences, but German syntax tolerates length differently than English does, so the 25-word heuristic is a borrowed number and should be treated as provisional.

Finally the judge inherits the framing we gave it. By telling it the applicant is an eleven-year customer, we may prime it to reward warmth that it would not have rewarded otherwise, which is the very failure mode this prompt was designed to detect. We also removed accuracy from its scope, which is correct for separation of concerns, but it means the judge can award a 5 to a fluent letter containing a fabricated reason. That is only safe because the automated checks run first, and the pipeline must enforce that ordering.

### Calibration strategy

Before trusting any score, the judge must be calibrated against
hand-written reference letters with known intended scores, run at
temperature 0 several times each, checking two things: that the judge
reproduces our intended score within one point, and that it reproduces its own score across repeats. Failing either means the prompt is broken and we fix the prompt rather than the letters. In this round we ran a two-letter version of this check as a smoke test: one clearly good letter and one clearly bad one. The judge scored them 5 and 1 respectively, matching intent and separating cleanly. The full calibration set spanning all five anchors, including the two hard cases (a letter that is warm and condescending at once, and one that is cold but entirely correct), is the next step before any pilot.

For edge cases we prefer an explicit escape over a guessed number. If a letter does not communicate a decline at all, or the judge cannot locate the decline sentence in Step 1, it should not receive a tone score. In the production version we would add a null score path for this. We would also route any score of 3 to human review rather than treating it as a soft pass, because 3 is where inter-rater disagreement concentrates in most scoring rubrics and where our judge is least informative.

For drift, the fix depends on direction. If the judge is too lenient, which is the more common failure with a same-family judge, we tighten the anchors with concrete negative examples rather than instructing it to be stricter, since abstract severity instructions produce unstable scores. If it is too strict, we look first at whether the plain language criterion is firing on acceptable register, and relax the sentence-length heuristic before touching anything else. Either way we re-run the five reference letters after every prompt change, and treat the reference set as a regression test rather than a one-time exercise.
