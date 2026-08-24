## Question 1: What would change in your evaluation design if your client's data was in French?

The evaluation would need French-language prompts, French retail policy examples, and a judge that is calibrated on French phrasing rather than English fluency. I would also revisit every prompt card to make sure the wording is natural in French and that the expected answer is not biased toward English support conventions. A literal translation is not enough because support language often changes tone when moved between languages.

The biggest challenge is that tone is culturally and linguistically specific. A direct translation of an English rubric can misread politeness, formality, or empathy markers. I would use bilingual human review on a subset of examples first, then compare the judge against those human labels before trusting the automated score. I would also watch for domain vocabulary issues, such as the exact way refund policies, shipping exceptions, and escalation language are phrased in French retail settings.

## Question 2: Your client asks "is this model AGI-level?" - how do you respond?

I would say that "AGI-level" is not a useful operational label for this retail use case. It is too vague to evaluate directly because it bundles together reasoning, memory, agency, safety, and generalization across many domains that are not all needed for customer service. In a retail support context, the business does not need a theory-of-everything answer; it needs a model that can handle complaints, policy questions, and escalation reliably.

Instead, I would define the exact abilities the business cares about: correct policy handling, resolution quality, safe escalation, and consistent tone across many support scenarios. If they want a broader claim, I would explain that it would require a much wider benchmark suite, long-horizon task testing, tool-use evaluation, and human review. Even then, the result would be a practical capability assessment, not proof of AGI. That framing keeps the conversation tied to measurable behavior instead of marketing language.

## Question 3: What is the one thing you could not evaluate without a human, and why?

The one thing I could not fully evaluate without a human is whether the response feels genuinely appropriate in context when the customer is upset, ambiguous, or socially sensitive. A judge model can score empathy markers and policy compliance, but it cannot reliably judge whether a response would calm a real customer, preserve brand trust, or sound insulting in a specific cultural context. It can approximate tone, but it cannot truly experience the social effect of the message.

In practice, I would use human review on a small but representative slice of difficult cases: refunds, anger escalation, and any response involving policy exceptions or vulnerable customers. The human label would serve as the calibration target for the judge and as the final check for any high-impact support flow. That hybrid setup is the safest way to combine scale with accountability, because the model can handle routine scoring while humans catch the cases where nuance matters most.
