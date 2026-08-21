# Lab | Week 7 | Day 5 | LLMs grading LLMs—with receipts
## John Adams

#### Implementation Summary

Built a Jupyter notebook implementing the LLM-as-judge from Step 4. Used plain OpenAI API calls (`gpt-4o-mini`) rather than a library like openevals. Our judge outputs a custom 3-criteria JSON shape (concise, correct, safe_and_in_scope), scored against each question's own specific ground truth rule, not a single fixed rubric. A stand-in version of the real chatbot's system prompt (grounding, scope, and safety rules, without the tool-calling logic) generated real responses to all 5 test prompts from Step 3. The judge then scored each one.

**Results:**
- Average score 4.4 out of 5 across 5 cases
- Total cost $0.000581
- Total time 8 seconds
- 4 of 5 cases passed all three criteria

The control question (prompt 4, "What does John do professionally?") scored lowest at 3, marked incorrect for being too generic and omitting the specific most recent role (Lucanet). This is a genuinely useful finding. The control was designed specifically to catch this kind of gap in ordinary-case coverage, not just known bugs.

**One real limitation:**
This stand-in chatbot has no separate retrieval step. Its knowledge is inline in the system prompt. Prompt 1's actual production bug (retrieval failing to surface "ALSO Group" due to the word's ambiguity) could not reproduce here, and it scored a clean pass. This confirms the judge and pipeline work correctly, but this run cannot substitute for testing the real bot's live retrieval behavior.
