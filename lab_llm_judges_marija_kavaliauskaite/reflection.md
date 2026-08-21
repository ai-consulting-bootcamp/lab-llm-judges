# Reflection

## Q1 — What would change if the client's data was in French?

I would create French test prompts and reference examples rather than translating only the final English benchmark. The dataset should represent French phrasing, tone, ambiguity, and culturally relevant creative language, because an English-only benchmark can hide language-representation bias. Native or fluent French reviewers should assess whether MIRA preserves nuance and whether the campaign language feels natural rather than translated.

I would also review multilingual benchmarks for useful test patterns, but still keep MIRA-specific cases. Before trusting automated scores, I would compare the judge with fluent human ratings in French and test whether its strictness, consistency, or preference for polished language changes across languages.

## Q2 — Client asks: “Is this model AGI-level?”

“AGI-level” is not a useful conclusion from this evaluation. The benchmark is deliberately task-specific: it tests five examples of MIRA creative-direction behaviour under defined conditions. Strong performance would support only a cautious claim that the model handled these prompts and criteria well in this run.

It would not demonstrate broad intelligence, reliable transfer to unrelated tasks, autonomy, or general problem-solving ability. AGI itself has no single accepted operational definition, and a five-case product evaluation cannot resolve that debate. I would report the measured task behaviour and its limits instead of using a broad label.

## Q3 — What is one thing you cannot properly evaluate without a human?

I cannot properly determine whether a final creative direction genuinely feels visually coherent, distinctive, and appropriate to the person's intended brand identity without human review. Rules can confirm five frames, required sections, and prohibited terms, but they cannot fully assess taste, emotional resonance, visual tension, originality, or whether the direction feels personally right.

An LLM judge can help identify contradictions and generic language, yet it may reproduce style biases or reward polished wording. I would ask a human creative reviewer—and, where possible, the client—to review a sample alongside the automated evaluation.
