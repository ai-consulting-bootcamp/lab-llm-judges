# Step 6 – Reflection: LLM Evaluation Design

## Question 1: What would change in your evaluation design if your client's data was in French?

If the AI Food Concierge operated with French-language data, the evaluation prompts, expected responses, and judging criteria would need to reflect French linguistic conventions. Existing English-language benchmarks such as IFEval could provide methodological guidance, but their original results would not establish performance in French. We would therefore adapt our five custom evaluation prompts and create French-language reference responses.

Additional challenges would include regional food terminology, dietary expressions, currency formatting, and linguistic ambiguity. Quality verification would combine rule-based checks for objective requirements with an LLM judge capable of evaluating French responses. A fluent French-speaking human reviewer would validate selected outputs to identify translation errors, cultural misunderstandings, and inappropriate recommendations.

## Question 2: Your client asks, "Is this model AGI-level?" – How do you respond?

The term Artificial General Intelligence (AGI) does not have a universally accepted operational definition. Our evaluation measures specific capabilities of an LLM within the AI Food Concierge use case, including instruction following, factual consistency, and context retention. Successful performance on these tasks would not demonstrate general intelligence.

Assessing broader capabilities would require substantially more diverse evaluations covering reasoning, learning, problem-solving, adaptation to unfamiliar situations, and performance across multiple domains. Even strong results across such benchmarks would require careful interpretation because benchmark contamination, limited task coverage, and evaluation methodology can distort conclusions. Therefore, we cannot make a credible AGI-level claim based on this limited evaluation.

## Question 3: What is the one thing you could not evaluate without a human, and why?

One aspect requiring human judgment is whether restaurant recommendations are genuinely useful and appropriate in a realistic customer context. Automated evaluations can verify budget limits, dietary requirements, and factual consistency, but they cannot fully determine whether an answer meets a person's expectations or feels trustworthy.

An LLM judge may approximate subjective quality, but its assessment can reflect linguistic preferences, hidden assumptions, or systematic biases. In practice, we would ask a small group of human reviewers to assess selected recommendations for clarity, usefulness, and perceived reliability. Their feedback would be compared with automated judge scores to identify disagreements and improve the evaluation rubric. This would complement rather than replace objective rule-based verification.