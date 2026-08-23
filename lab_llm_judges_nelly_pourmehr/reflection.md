# Reflection

## Question 1: What would change if the client's data was in French?

I would not reuse English benchmarks or English test prompts as-is. Translated prompts often lose nuance, especially around tone, which matters a lot for a support bot. I would rebuild the 5 test prompts natively in French with a native or fluent speaker, not just translate them.

The biggest new challenge is judge reliability. Most frontier judges are trained mostly on English data and may rate correct French tone or phrasing as lower quality just because it does not match English patterns. I would test the judge on known-good French answers first to check for this bias before trusting its scores.

To verify quality, I would want a native French speaker to review a sample of judge scores against their own judgment, and treat any consistent gap as a sign the judge needs French-specific calibration examples, not just translated ones.

## Question 2: The client asks "is this model AGI-level?"

I would say that is not a question this evaluation can answer, and explain why. AGI is not clearly defined even for humans, so there is no agreed test for it. What we can measure is much narrower: how this model performs on this client's specific tasks, under these specific conditions.

To answer something useful, I would reframe the question. Instead of asking if the model is generally intelligent, I would ask if it reliably handles the client's real failure modes: hallucination, tone, completeness, scope. Those are testable.

I would include a caveat that a model doing well on 5 or even 50 client-specific tests says nothing about its abilities outside that scope. High performance on a narrow task is not evidence of general capability.

## Question 3: What could I not evaluate without a human?

Tone judgment in an emotionally charged situation, like the angry billing complaint prompt, needs a human. An LLM-as-judge can check for surface features, like whether the response contains an apology or avoids promising a refund. It cannot reliably tell if a response actually feels genuine and de-escalating to a real frustrated customer, because that depends on lived context a judge model does not have.

Rule-based checks fail here too, since there is no fixed correct wording. In practice, I would route a sample of these emotionally sensitive responses to a human reviewer on a regular basis, not just once, since tone standards can shift and a one-time human check would not catch drift over time.