# Reflection

## Question 1: What would change if your client's data was in French?

The should-cost data itself (numbers, currency codes, part specs) wouldn't
need translation, but the negotiation-prep summaries would, and that is
where real risk enters. Benchmarks like FinQA and FinanceBench are
English-only, so they offer no baseline for whether gpt-4o-mini hallucinates
more in French financial writing -- a plausible risk given English-skewed
training data. New challenges include precise translation of procurement
terminology, where subtle shifts in meaning are easy to miss. For quality
verification, a native French-speaking reviewer should be in the loop for
the LLM-as-judge step at least initially, since the judge-prompt calibration
done here was entirely in English with no evidence it transfers -- the judge
itself may have blind spots in a language it evaluates less confidently in.

## Question 2: Your client asks "is this model AGI-level?"

The question needs unpacking before it's answerable. "AGI-level" isn't a
single measurable threshold; it's a claim about general, human-equivalent
reasoning across essentially any domain, and nothing in this evaluation
tests for that. What was actually tested is narrow: can this specific model,
on this specific task, avoid hallucinating and produce professional output.
A model can excel at that and still fail badly on unrelated tasks. Answering
the AGI question would require evaluation across dozens of unrelated
domains, tests of transfer to genuinely novel problems, and an
operational definition of "general" the field hasn't settled on. The honest
answer to a client: this evaluation tells you whether the model is good at
your job, not whether it is a general intelligence -- and any vendor
claiming to have measured the latter with confidence should be treated with
skepticism.

## Question 3: What is the one thing you could not evaluate without a human?

Whether the negotiation tone actually lands with a specific supplier
relationship. Prompt 4 tests professional tone in the abstract, but real
negotiation prep depends on history with that specific supplier -- a note
appropriately firm for a supplier pushed back on before might be needlessly
aggressive for a new, cooperative one. Neither rule-based checks nor an
LLM-as-judge has access to that relational context; it is tacit knowledge a
procurement lead carries, not data present in any input. In practice, LLM
output should function as a first draft a human procurement lead calibrates
against their actual relationship with the supplier -- the LLM can cover
structure, accuracy, and base tone, but the last mile requires someone who
has sat across the table from that supplier before.
