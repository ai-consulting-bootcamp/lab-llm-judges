# Lab | Week 7 | Day 5 | LLMs grading LLMs—with receipts
## John Adams

#### Step 6: Reflection

**Question 1: What would change in your evaluation design if your client's data was in French?**

If John's knowledge base were in French, the biggest change would be re-testing retrieval and embeddings in French, not just translating text. Embedding models can perform differently across languages. "ALSO"-style ambiguous proper nouns get worse, not better, in a language with more common short words. A similar retrieval-miss risk would need its own French-specific test case, not an assumption that the English one transfers.

The judge prompt itself would also need rework, not just translation. "Professional tone" has different norms in French business communication (more formal address, different conventions for directness) than in English. Scoring "professional middle ground" with an English-tuned judge on French output risks the same cultural bias flagged in Step 4, just amplified.

Verifying quality would mean either a native French speaker doing spot checks, or a French-capable judge model. An English-trained judge grading French text is an unverified assumption, not a safe default.

**Question 2: Your client asks "is this model AGI-level?" How do you respond?**

"AGI-level" is a question worth pushing back on before answering. We don't have a solid definition of intelligence for humans, let alone for machines. Historically, when models hit "human level" on some task, the definition of that task just moves. So "AGI-level" isn't a fixed target you can test against, it shifts.

No evaluation in this project, or realistically available to a small consultancy, can answer that question. It would require testing across a vastly broader range of domains than one client's use case. Even major labs disagree on what would count as sufficient evidence.

The honest answer: this evaluation only tells you whether the model is reliable for this specific task, answering questions about your background and booking calls. It says nothing about general intelligence, and no result here should be used to make a broader claim.

**Question 3: What is the one thing you could not evaluate without a human, and why?**

The one thing I couldn't evaluate without a human is catching a factually wrong answer that sounds confident and plausible. In this project, both the Lucanet/Cloudflare mixup and the internal data leak were caught by reading real chat logs, not by any rule or LLM judge. Neither failure produced an error, a crash, or a flagged pattern. They just looked like normal, fluent answers.

This requires human judgment because a rule-based check only catches what you already thought to check for, and an LLM judge only catches what its own criteria cover. A human reading actual transcripts can notice something wrong that nobody wrote a rule for yet. That is exactly how these two issues were found.

In practice, this means chat logs need regular human spot-checking, not just automated eval runs, especially early on. Automated checks can only test for known failure modes. New failure modes only show up by someone actually reading what real users saw.
