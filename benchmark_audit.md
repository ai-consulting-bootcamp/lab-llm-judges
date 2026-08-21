# Lab | Week 7 | Day 5 | LLMs grading LLMs—with receipts
## John Adams

### Step 2: Find & Critique 3 Existing Benchmarks

#### 1. Benchmark Name: IFBench
Year: 2025 (NeurIPS 2025)
Source: https://github.com/allenai/IFBench

**Why it seemed relevant:**
The chatbot must follow tone/style instructions (sound like John, stay in character, respect formatting rules in the system prompt). IFBench tests precise instruction following on novel, out-of-distribution constraints, which is a direct proxy for whether the model will hold to a persona/style instruction under real conversation rather than drifting off script.

**Contamination risk:**
[x] Low - Model likely not trained on this data
- Explanation: Released 2025 with out-of-distribution constraints specifically designed to avoid the overlap that saturated its predecessor, IFEval.

**Saturation risk:**
[x] Low - Benchmark is challenging
- Explanation: Built specifically because IFEval (2023) became saturated, with small models scoring 80%+. Models that score 80%+ on IFEval scored under 50% on IFBench, showing real headroom.

**Format:**
[x] Free-form text
- Verification functions check whether free-form model output satisfies specific constraints, rather than matching a fixed answer.

**Verdict:**
[x] Adapt it (explain how)
- Use IFBench's constraint-verification approach as a model for testing persona/tone adherence, but swap in constraints specific to John's voice and chatbot rules rather than using IFBench's own generic constraint set as-is.

---

#### 2. Benchmark Name: BFCL (Berkeley Function-Calling Leaderboard)
Year: Ongoing, currently v4 (last updated April 2026)
Source: https://gorilla.cs.berkeley.edu/leaderboard.html

**Why it seemed relevant:**
The chatbot calls tools (Calendly availability check, Calendly booking, email send). BFCL tests whether a model calls the correct function with correct arguments, including multi-turn tool use, which maps directly to the risk of the bot booking the wrong time or hallucinating a tool call.

**Contamination risk:**
[x] Medium - Some overlap possible
- Explanation: BFCL moved from a static v1 dataset (higher contamination/overfitting risk) to live, crowd-sourced queries in v2+ specifically to reduce this, but as an actively-referenced, long-running leaderboard some risk of models being tuned toward its format remains.

**Saturation risk:**
[x] Medium - Some models perform well
- Explanation: Top frontier models score well on core function calling, which is why BFCL has expanded into harder "holistic agentic evaluation" (v4) to keep the benchmark discriminating.

**Format:**
[x] Other: specify
- Structured function/tool-call generation, evaluated via AST-based matching against expected calls rather than free text or multiple choice.

**Verdict:**
[x] Adapt it (explain how)
- Use BFCL's evaluation approach (correct function + correct arguments) as the pattern, but test against John's actual tool schema (Calendly, email) instead of BFCL's generic tool set. Note: independent community critique of BFCL outside Berkeley's own materials was thin in my research, so trustworthiness here is based mostly on the maintainers' own documentation.

---

#### 3. Benchmark Name: SimpleQA Verified
Year: 2025 (revised March 2026)
Source: https://arxiv.org/abs/2509.07968

**Why it seemed relevant:**
The chatbot's top risk is stating something factually wrong about John's background. SimpleQA Verified is a cleaned-up, 1,000-prompt short-form factuality benchmark built specifically to measure hallucination rate, which maps to "does the model state facts about John correctly."

**Contamination risk:**
[x] Low - Model likely not trained on this data
- Explanation: Original SimpleQA (2024) had contamination concerns from public test questions; Verified (2025) removed duplicates and reconciled sources specifically to address this, though as a public benchmark some residual risk remains.

**Saturation risk:**
[x] Low - Benchmark is challenging
- Explanation: Top frontier model (Gemini 2.5 Pro) scores only 55.6 F1 on this benchmark, well short of ceiling.

**Format:**
[x] Free-form text
- Short-form factual question-answer pairs, graded for correctness against a verified reference answer.

**Verdict:**
[x] Reject it (explain why)
- SimpleQA Verified tests parametric knowledge, facts memorized in model weights, not retrieval-augmented answers. John's chatbot answers from a retrieved knowledge base (Pinecone + kb/ files), not from what the base model memorized about him. This benchmark cannot test the actual RAG pipeline's factual accuracy, so it is not usable as-is; a custom RAG-grounded factuality test (see evaluation_design.md) is needed instead.
