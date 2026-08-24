# Reflection

## Question 1: What would change if the client's data was in French?

If the client's data was in French, I would first check whether the benchmarks and judge prompts I used are even valid in French. ABCD and the Bitext dataset are both English, so I could no longer use them, even as inspiration, without a real risk that the phrasing patterns do not transfer. I would need to either find French equivalents or write the 5 custom prompts directly in French, working with a native speaker or the client's own French support transcripts, rather than translating my English prompts, since a direct translation often sounds unnatural and would not test the model the way a real French customer writes.

A new challenge is that the judge itself needs to be checked in French too. An LLM judge that works well in English is not guaranteed to score French responses fairly, it might be stricter about grammar than actual tone quality, or miss subtle politeness markers that matter in French customer service (such as the use of "vous" versus "tu"). I would build a small French calibration set with human labels, the same way described in the bias analysis, and check the judge's agreement with those labels before trusting its scores. I would also flag to the client that my confidence in the French evaluation is lower until this calibration step is done, since I have far less experience validating judges in French than in English.

## Question 2: The client asks, "is this model AGI-level?"

I would start by clarifying what the client actually means, since "AGI-level" is not a precise or agreed-upon term. Most likely they mean something like "is this model smart enough that I do not need many more safeguards," which is a very different, answerable question. I would explain that AGI usually refers to a system matching or beating humans across almost all cognitive tasks, and that no evaluation I ran, or that currently exists, is designed to test for that. My evaluation only covers 5 narrow customer service scenarios, so it says nothing about general intelligence.

What I can answer is a much narrower and more useful question: does this model reliably handle my specific tasks, within the scope I tested. To get closer to a real answer, I would need many more test cases across the client's actual traffic, ongoing monitoring in production, and testing across a wider range of skills beyond customer service. Even then, I would caveat that passing my tests only tells me about performance on tasks similar to what I tested, not a general claim about the model's intelligence, and that models can fail in new and unexpected ways once real customers use them.

## Question 3: What could you not evaluate without a human, and why?

The one thing I could not fully evaluate without a human is whether a response would actually make a real, upset customer feel heard and satisfied, not just whether it followed the right structure. An LLM judge can check whether a response mentions the customer's issue and offers a next step, but it cannot fully capture the emotional impact of tone, timing, or word choice on an actual person in a bad mood, especially across different cultural backgrounds or communication styles.

This is hard for LLM-as-judge or rule-based methods because both methods score against a written description of "good," and no written description fully captures how varied real customers react. A rule-based check can only catch clear failures like a missing refund offer, and an LLM judge inherits its own biases (as discussed in the bias analysis), so it can rate a technically correct but emotionally flat response as "good" when a real customer would still be frustrated.

In practice, I would include human evaluation as a sampling step, having support agents or a small customer panel review a sample of real chatbot transcripts on a regular basis, comparing their judgment to the LLM judge's scores, and using disagreements to catch blind spots and recalibrate the judge over time, rather than trying to fully replace human review with automation.
