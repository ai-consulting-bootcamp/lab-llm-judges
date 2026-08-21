# Reflection

## Question 1: What would change if the client's data was in French?

I'd need to rebuild the evaluation prompts natively in French rather than
translating the English ones, because coaching language is highly idiomatic —
the tone markers that signal "supportive but not sycophantic" in English (e.g.
softened, question-first phrasing) don't map cleanly onto French, where
directness can read as perfectly appropriate rather than cold, and where formal
address (vous vs. tu) itself carries a coaching-stance signal that doesn't exist
in English at all. A literal translation of my prompts risks testing translation
fluency rather than coaching quality.

The bigger challenge is the judge, not the model under test: an LLM judge
evaluated in French may have seen far less French coaching/HR content during
training than English business writing, so I'd expect the judge's rubric
application to be less reliable and I'd want to validate it against human
ratings more heavily than I would for English. I'd also want native French
speakers with actual coaching or HR experience (not just fluent English
speakers translating) to write or review the reference examples used for
calibration, since subtle tone misses are exactly the kind of thing a
non-native reviewer would miss.

To verify quality, I'd lean more on human evaluation for a French version than
I would in English, at least until I had evidence the judge's French scoring
correlated with human raters the way MT-Bench's paper showed ~85% agreement in
English — that number shouldn't be assumed to transfer to another language
without checking.

## Question 2: "Is this model AGI-level?"

I'd first clarify what they mean, because "AGI-level" isn't a property this
evaluation — or really any current evaluation — can certify. What we *can* say
is much narrower: whether the model performs well on this specific coaching
task, under these specific conditions, on this specific (small) sample of
scenarios. That's a claim about task competence, not general intelligence.

I'd explain that no benchmark, including the well-known general ones we
audited (MT-Bench, MMLU), is designed to answer an AGI question — they measure
performance on defined tasks with known contamination and saturation issues,
which is a different question from "is this system generally intelligent."
Even a model that scores very well on our 5 coaching scenarios could fail
badly on a scenario we didn't think to test, which is itself evidence against,
not for, general capability.

My caveat to the client would be direct: I can tell them how the model
performs on the coaching behaviors we defined and measured, with the sample
size and judge-bias limitations noted in the memo. I cannot and would not
make a claim about the model's intelligence in general — that's not a
question this kind of evaluation is built to answer, and I'd flag it as a
different (and much harder, more open) research question than what we were
hired to do.

## Question 3: What couldn't I evaluate without a human?

Whether the coaching actually *worked* — whether an employee who went through
this conversation ended up with a goal they were genuinely more likely to
pursue, versus one that just sounds good on paper. That's an outcome question,
and neither an LLM judge nor a rule-based check can observe it from the
transcript alone; it requires either a follow-up with the real employee weeks
later, or at minimum a human coach's professional judgment about whether the
goal-setting process shown in the transcript matches what good coaching
practice looks like in a real relationship, not just in a single exchange.

This is where LLM-as-judge structurally can't substitute: the judge only sees
the text of one conversation, with no way to check whether the "specific,
measurable" goal produced was actually meaningful to that particular person,
or just specific-*sounding*. A human coach evaluating the same transcript
would bring domain judgment about what makes a goal actually motivating versus
just technically well-formed — something the current 3 criteria in my judge
rubric can approximate but not fully capture.

In practice, I'd incorporate this by pairing the automated evaluation with a
periodic human-rated sample (a coach reviewing ~10% of real transcripts) as an
ongoing check on whether the LLM judge's scores still track what a
professional would actually call good coaching, rather than treating the
automated score as sufficient on its own indefinitely.
