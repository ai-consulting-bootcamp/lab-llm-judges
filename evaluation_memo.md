**TO:** Head of Consumer Credit Operations, Kranich Direktbank AG
**FROM:** Dr. Elif Yurdakul, AI Evaluation Consultant
**DATE:** 22 November 2026
**SUBJECT:** LLM Evaluation Results: AI-drafted loan decline letters

---

**EXECUTIVE SUMMARY**
We tested whether two OpenAI models can draft compliant, accurate and humane decline letters for credit officers to review. On our five test cases, **gpt-5.4-mini produced a sendable draft in 5 of 5 cases and gpt-4o-mini in 4 of 5.** gpt-4o-mini's one failure was the most important case: a missing decline reason. These results support a supervised pilot, not unsupervised use.

**METHODOLOGY**
We first reviewed public benchmarks: IFEval, LegalBench and EQ-Bench. None tests compliant customer letters under EU and German consumer-credit rules, and the most relevant ones are saturated or likely contaminated. We therefore built a custom test of five realistic case files: a standard affordability decline, a fully automated SCHUFA-based decline, a file containing a discriminatory officer note, an applicant in financial distress, and a file with no recorded reason.

Each letter was checked in two ways. Free **rule checks** verified required facts (reference, amount, rights) and the absence of forbidden content (internal score cut-offs, nationality). An **LLM judge** (gpt-5.4-mini) scored each letter three times from 1 to 5 against four criteria: faithfulness, required disclosures, prohibited content, and tone. Before trusting the judge, we tested it on a known-good and a known-bad letter. The first version failed this test because it misread a customer-facing policy limit as confidential. We clarified the judge prompt and re-scored the same letters. The revised judge passed calibration (5/5/5 and 1/1/1).

**RESULTS**

| | gpt-4o-mini | gpt-5.4-mini |
|---|---|---|
| Letters passing all checks | 4 of 5 | 5 of 5 |
| Average judge score (1–5) | 4.2 | 4.9 |
| Generation time per letter | 6.0 s | 1.2 s |
| Generation cost per 1,000 letters | $0.25 | $1.19 |

**Both models** stated the recorded reason, kept the internal score cut-off private, and left the discriminatory officer note out of the letter. **gpt-4o-mini**, when the reason was missing, told the customer it "was not recorded" instead of flagging the gap for staff. It also added irrelevant credit-bureau advice to three letters and wrote letters that were 60% longer.

**CAVEATS & LIMITATIONS**
Five cases cannot show reliability at production volume; one more failure would change the pass rates by 20 points. Our judge was revised once and calibrated on only two reference letters. It is also one of the models it judged, so it may favour its own style. The letters were in English, while your customers receive German letters. We cannot guarantee legal sufficiency: the disclosure wording must be approved by your legal team against the German implementing act (in force since 20 November 2026). Model versions change, so results must be re-checked after each provider update.

**RECOMMENDATION**
Under these conditions, for this drafting task, we recommend **gpt-5.4-mini** for a supervised pilot. A credit officer reviews every draft, and any letter with a missing-information flag is blocked automatically. Our confidence is **moderate on the direction** (gpt-5.4-mini handled the hardest case correctly) and **low on the exact rates**. Next step: expand to about 50 German-language cases and calibrate the judge against two officers and compliance before scaling.

**ADDITIONAL METRICS**
Model costs are negligible at your volume: below €2 per 1,000 letters for either model. Evaluation is the larger cost: in one run, judging cost about 10× as much as drafting ($0.071 vs $0.007), yet the whole study cost only about **$0.15** across 82 API calls (about 111,000 tokens, two judge versions). Because gpt-5.4-mini was 5× faster and wrote shorter letters, it saves officer reading time, which outweighs its higher token price. We have no reliable energy figure per call; fewer, shorter generations are the practical lever on environmental cost.
