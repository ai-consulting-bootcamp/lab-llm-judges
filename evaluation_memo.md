# Lab | Week 7 | Day 5 | LLMs grading LLMs—with receipts
## John Adams

#### Step 5: Write a 1-Page "Evaluation Memo" to Your Client

TO: John Adams
FROM: [Consultant]
DATE: 2026-08-21
SUBJECT: LLM Evaluation Results, Virtual Coffee Chat Bot

**EXECUTIVE SUMMARY**
We evaluated the chat bot's RAG pipeline and safety guardrails against 5 custom test prompts covering factual retrieval, brand tone, scope safety, and tool calling. This checks whether the bot represents your professional background accurately and stays within its intended scope before wider recruiter use.

**METHODOLOGY**
We designed 5 custom prompts rather than relying on public benchmarks. No existing benchmark tests a RAG pipeline against a specific individual's private knowledge base. Prompts were built from a mix of previously observed issues (retrieval misses, internal data leakage) and one deliberate control question with no known trap. Results aren't only measuring known bugs.

Each response was scored using its matching method: rule based checks for factual and safety prompts, an LLM-as-judge for the brand tone prompt. The judge follows a 4-part design (task, criteria, reasoning steps, structured output).

This was a small internal pass (5 prompts, single run), using generated stand-in responses rather than a full production API run. It should be read as a directional check, not a comprehensive benchmark.

**RESULTS**
4 of 5 test cases passed. The control question, tone question, safety probe, and booking flow all performed correctly. The one failure was the factual retrieval prompt ("Did John work at ALSO?"). The bot failed to surface a real fact from the knowledge base. This mirrors a previously logged, now-fixed issue where the retrieval step under-weighted short, common-word company names.

No hallucinated facts, no impersonation, and no internal data leakage were observed in this run.

**CAVEATS & LIMITATIONS**
This is a 5-prompt sample, not a statistically powered test. The LLM-as-judge carries known biases (style and length preferences) not yet calibrated against a larger hand-labeled set. Results are from a single run; LLM outputs vary, so scores could shift on repeat runs.

**RECOMMENDATION**
Under these conditions, the bot performs reliably on tone, safety, and tool calling. Retrieval of short, common proper nouns remains a risk, worth re-testing after any retrieval configuration change. Confidence: moderate, enough to continue limited use, not yet enough for unmonitored, high-volume recruiter traffic.

**ADDITIONAL METRICS**
This pass did not measure real token usage, latency, or cost, since it used generated stand-in responses rather than live API calls. A full implementation run (Part 2 of this evaluation) will capture real per-call token counts, latency, and estimated cost using gpt-4o-mini.
