# Reflection — ShopCo Evaluation

## 1. What would change if the client's data was in French?

I would change the language of communication with the customer.
I would also adapt the test prompts, reference answers, and judge
instructions to French. Translation alone would not be enough:
dates, currency formats, and polite expressions need careful review.
Public benchmark results in English would not prove that the model
works equally well in French.

If I did not speak French well, I would ask a competent French
speaker to review every case and reference answer. A bilingual
reviewer could check that the policy keeps the same meaning.
I would then test the judge against human labels in French,
including complaints and incomplete requests. I would report
these results separately from the English evaluation.

## 2. How would you answer a client who asks whether the model
is AGI-level?

I would first ask what the client means by AGI-level and which
business abilities they want to assess. This expression is too
broad to answer with a ShopCo support test. Our evaluation checks
specific abilities: following a policy, asking for missing
information, and writing appropriate replies.

I would explain that five cases cannot demonstrate general
intelligence. Even perfect results would only describe performance
on those cases under those conditions. A broader assessment would
need many different tasks, new situations, independent testing,
and clear definitions. I would focus the recommendation on
evidence relevant to ShopCo rather than make a general claim
about intelligence.

## 3. What could you not evaluate without a human, and why?

I would need a responsible person at ShopCo to confirm that the
policy and reference answers are correct and complete for the
business. This person can explain missing rules, exceptions,
and operational details. The fictional policy in this lab was
reviewed by me, but it is not a verified real company policy.

A rule-based check or LLM judge can compare a reply with documents.
However, this does not prove that the documents reflect the
company's actual decisions. In practice, I would ask the support
lead to approve the policy and answer key before testing.
They would also review unclear cases and judge disagreements.
Our experiment showed why: a judge can give a correct verdict
with an incorrect explanation.