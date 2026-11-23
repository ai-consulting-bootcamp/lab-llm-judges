# Evaluation Memo

**TO:** Head of Consumer Lending & Compliance, [Client Bank]
**FROM:** Pieter Albrecht, AI Consultant
**DATE:** 23 November 2026
**SUBJECT:** LLM Evaluation Results: Automated Loan Rejection Letters

## Executive Summary
We tested whether gpt-4o-mini can draft loan rejection letters that are accurate, complete, compliant and empathetic. In this small pilot, the model handled four of five scenarios well, including the bias and Dutch-language cases. However, our automated quality checker made a clear error, which shows that automated evaluation alone is not yet reliable enough to approve letters without human review.

## Methodology
We first reviewed three public benchmarks (IFEval, LegalBench, BBQ). None measures what you need: they are either likely to be in the model's training data, close to their maximum scores, or focused on US law and multiple-choice questions. We therefore built a custom test set of five realistic cases: a standard rejection, an emotional applicant with a negative BKR registration, a record with no stated reason, a record containing age and nationality, and a letter in Dutch at B1 level.

Each letter was checked in two independent ways: rule-based checks (required elements such as the rejection reason and Kifid; forbidden or invented terms) and an "LLM-as-judge", a second model call that scores each letter from 1 to 5 against four criteria, repeated three times. One model (gpt-4o-mini) was tested, acting as both writer and judge.

## Results
The average score was 4.4 out of 5. Four cases scored 5/5 on every run and passed all rule checks. Notably, the model did not mention age or nationality in the bias case, and it wrote a correct letter in Dutch.

The one low score (2/5) was the case with no stated reason. Here the letter correctly avoided inventing a reason, but the judge marked it as failing, contradicting its own explanation. The judge also missed two real issues in that letter: it implied the customer's application was incomplete, and it contained unfilled placeholders. The rule checks and the judge disagreed only on this case, and that disagreement is what exposed the problem.

## Caveats & Limitations
These results come from five test cases and should be read as an indication, not proof. We cannot guarantee performance on your real applicant data, other loan types, or future model versions. The same model wrote and judged the letters, which may make scores too generous. Our judge prompt contained an ambiguity that caused the error above. Legal sufficiency under Dutch and EU rules was not assessed and requires review by your compliance team.

## Recommendation
Under these conditions and for this task, gpt-4o-mini appears suitable as a **drafting assistant**, with every letter reviewed by an employee before sending. We do not recommend fully automated sending at this stage. Our confidence is moderate for letter quality and low for the automated checker. Before scaling, we recommend fixing the judge prompt, testing at least 100 real anonymised cases, using a different model as judge, and having compliance officers review a sample.

## Additional Metrics
The full test (5 letters, 15 judge checks) took 67 seconds and cost $0.005. At scale, generating and checking 10,000 letters would cost roughly $5 in API fees, at about 13 seconds per letter including checks. Cost is therefore negligible; the main cost and risk sit in human review time and in errors that reach customers. Energy use per letter is small, but grows with repeated judge runs and larger models.
