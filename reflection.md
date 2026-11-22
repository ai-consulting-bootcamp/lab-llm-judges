# Reflection (Step 6)

## Q1. What would change if the client's data were in French?

The audited benchmarks would mostly stop applying: IFEval, LegalBench and EQ-Bench are English-only, and translating them loses legal precision. I would build the test cases natively in French with French-speaking credit staff, anchored on the French transposition of CCD II and the CNIL's guidance on automated decisions.

New challenges: register (vous, formal closings such as "Veuillez agréer…"), gendered agreement, and keyword checks that must handle accents, elision and variants ("nationalité", "d'origine"). Models and judges are usually less reliable outside English, especially on tone.

To verify quality I would run the judge in French with French score anchors and calibrate it against native-speaker credit officers before scaling. Back-translation can catch factual drift (wrong reason or amount) but not tone, so tone stays human-reviewed.

## Q2. "Is this model AGI-level?"

I would say this evaluation cannot answer that, and that it isn't the question the client needs answered. "AGI" has no agreed operational definition, and no benchmark measures it. Scores on hard reasoning tests show narrow progress, not general intelligence.

What I measured is one model writing compliant letters on 5 test cases under one prompt. Even a perfect score means "good enough for this drafting task, under these conditions". Answering the AGI question would need broad, uncontaminated, open-ended tests across domains, and a shared definition first.

Caveats for the client: scores can be inflated by contamination and saturation, results are brittle to prompt changes, and models fail in ways no human expert would, such as inventing a reason. The useful question is: "Is it reliable enough for this task, with which safeguards?" That one we can measure.

## Q3. The one thing I could not evaluate without a human

**Whether a rejected applicant, especially one in distress (TC4), would actually experience the letter as fair and respectful.** A judge can check for empathetic phrasing and banned words, but whether the tone feels sincere, condescending or cold depends on lived experience, culture and the reader's stakes. An LLM judge shares the generator's blind spots, so it measures what a model thinks empathy looks like. Whether the disclosure wording satisfies German law is likewise a lawyer's call.

In practice:
- **Calibration:** credit officers and a compliance reviewer score a 30-letter set used to calibrate the judge.
- **Sampling:** a weekly sample of sent letters, plus every letter where judge runs disagree or the case file contained internal notes.
- **Outcome measure:** complaint rates.
- **Legal sign-off:** a lawyer approves the disclosure template whenever the regulation changes.

The judge triages; humans decide fairness and legality.
