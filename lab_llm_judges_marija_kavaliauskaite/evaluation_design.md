# MIRA evaluation design

## Five custom evaluation prompts

### Prompt 1 — Explicit visual preference adherence

**Prompt:** Create a three-part editorial direction for a small architecture studio. Use only a muted neutral palette, an architectural concrete setting, hard directional light, and minimal styling. Avoid saturated colours, soft romantic light, decorative props, and outdoor nature imagery. Include palette, lighting, styling, and composition sections.

**Ground Truth:** Yes.
**Explanation:** Frame count, required sections, required visual features, and prohibited features are explicitly stated and can be checked.

**Verification Method:** Rule-based plus LLM-as-judge.
**Explanation:** Rules can detect sections and prohibited terms; the judge assesses whether the complete direction genuinely respects the constraints.

**Primary Failure Mode:** Ignoring explicit visual choices.
**Why this prompt matters:** MIRA must translate direct preferences into output without adding a conflicting aesthetic.

### Prompt 2 — User input precedence

**Prompt:** Develop a campaign direction for a wellness founder. Background context might suggest calm beige minimalism, but the user's direct choice is vivid cobalt and orange, playful asymmetry, direct flash, and an energetic urban night setting. Treat the direct choice as authoritative. Do not revert to beige minimalism. Explain the decision briefly and propose three frames.

**Ground Truth:** Yes.
**Explanation:** The authoritative choices and the conflicting default are explicit.

**Verification Method:** Rule-based plus human evaluation.
**Explanation:** Keywords can show basic compliance, while a human checks whether the overall concept still quietly defaults to the rejected aesthetic.

**Primary Failure Mode:** Overriding direct user input with inferred context.
**Why this prompt matters:** MIRA's product rule is that direct answers and visual choices take precedence over inference.

### Prompt 3 — Campaign consistency

**Prompt:** Create a five-frame editorial campaign for an independent ceramic artist. The direction is quiet precision: chalk, charcoal, and clay colours; hard morning side-light; a raw plaster studio; restrained styling; tactile close-ups; no greenery and no glossy luxury cues. For each frame specify subject, composition, lighting, palette, and continuity link. Keep all five frames part of one coherent story.

**Ground Truth:** No.
**Explanation:** There are explicit constraints, but creative coherence and usefulness do not have one uniquely correct answer.

**Verification Method:** LLM-as-judge plus human evaluation.
**Explanation:** The judge applies a consistent rubric at scale; a human reviewer remains necessary for genuine visual coherence and distinctiveness.

**Primary Failure Mode:** Contradictory styling, colour, lighting, composition, or atmosphere across frames.
**Why this prompt matters:** A campaign is valuable only if its separate images feel intentionally connected.

### Prompt 4 — Hallucination resistance

**Prompt:** The only known facts are: the client makes hand-bound notebooks and wants an editorial campaign that feels precise and tactile. Propose an initial direction. Clearly label unknowns and questions. Do not invent the client's age, location, personality, customer demographics, personal history, preferred colours, or business scale.

**Ground Truth:** Yes.
**Explanation:** Unsupported biographical and preference claims can be identified against the limited source information.

**Verification Method:** Rule-based plus human evaluation.
**Explanation:** Rules can flag prohibited categories; a human checks subtler unsupported implications.

**Primary Failure Mode:** Hallucinating preferences or identity details.
**Why this prompt matters:** MIRA should expose uncertainty instead of turning inference into fact.

### Prompt 5 — Specificity and usefulness

**Prompt:** Give actionable editorial direction for a sustainable furniture maker launching one chair. Include precise choices for styling, lighting, a named colour palette, composition, location/atmosphere, and a five-shot sequence. Avoid empty phrases such as "authentic," "elevated," or "timeless" unless each is translated into a concrete visual decision.

**Ground Truth:** No.
**Explanation:** Many directions could be useful; quality depends on specificity and internal fit rather than one correct response.

**Verification Method:** LLM-as-judge plus human evaluation.
**Explanation:** A rubric can check coverage and specificity, but a creative reviewer should assess whether the choices are practically usable.

**Primary Failure Mode:** Generic creative language.
**Why this prompt matters:** Consultants need production-ready choices, not attractive but vague wording.

## LLM-as-judge prompt for Prompt 3

### Task Description

The evaluated model must create a coherent five-frame editorial campaign for an independent ceramic artist. Every frame must specify subject, composition, lighting, palette, and a continuity link. The campaign must preserve chalk, charcoal, and clay colours; hard morning side-light; a raw plaster studio; restrained styling; tactile close-ups; and exclusions for greenery and glossy luxury cues. Direct requirements must take priority over assumptions.

### Evaluation Criteria

1. **Instruction adherence:** Delivers exactly five identifiable frames with every requested field and respects exclusions.
2. **Preference fidelity:** Preserves the supplied palette, light, setting, styling, and tactile emphasis without conflicting additions.
3. **Campaign consistency:** Frames share a recognisable visual system and narrative progression without contradictions.
4. **Specificity and usefulness:** Directions are concrete enough to guide styling, photography, and sequencing rather than relying on vague adjectives.
5. **No unsupported assumptions:** Does not state unprovided biography, audience, identity, or preferences as fact.

### Scoring

- **1 — Major failure:** Misses the task or contradicts central requirements.
- **2 — Several important failures:** Some relevant content, but multiple requirements or consistency links fail.
- **3 — Acceptable but inconsistent:** Core task is present, with notable gaps or generic/contradictory moments.
- **4 — Strong with minor issues:** Meets nearly all requirements; issues are limited and do not undermine the campaign.
- **5 — Fully meets requirements:** Complete, specific, coherent, faithful, and free of unsupported assumptions.

### Reasoning steps

The judge should: (1) identify explicit requirements; (2) compare the response with each requirement; (3) identify contradictions and unsupported additions; (4) assess campaign-wide consistency and practical usefulness; and (5) assign one overall score. The reasoning returned to the user should be concise and should cite observable response features, not hidden chain-of-thought.

### Structured output

```json
{
  "score": 4,
  "reasoning": "Concise evidence-based explanation",
  "criteria_met": {
    "instruction_adherence": true,
    "preference_fidelity": true,
    "campaign_consistency": true,
    "specificity": true,
    "no_unsupported_assumptions": false
  }
}
```

The implementation requests JSON, removes optional code fences, extracts the first complete JSON object when needed, validates types and ranges, retries the judge once, and records a per-case error rather than stopping the full run.

## Bias analysis

An LLM judge is scalable, but it is not objective. Position bias can favour whichever requirement or response appears first, while length bias may reward a longer answer even when it is less faithful. If the judge and evaluated model share a model family, self-preference bias may favour familiar phrasing or reasoning patterns. The pointwise design avoids direct A/B ordering effects, but it does not remove these biases.

Style bias is especially important for MIRA. A judge may prefer polished, verbose English and mistake that presentation quality for stronger creative direction. It may also apply English-language or culturally narrow assumptions about what looks "premium," "coherent," or "good." Explicit criteria, concise reasoning, rule checks, repeated runs, and human creative review reduce—but do not eliminate—these risks.

## Calibration strategy

Calibration should use three MIRA-specific examples for the same campaign prompt: a known weak response that violates palette and frame requirements, a medium response that follows the brief but stays generic, and a strong reference response written or approved by a human creative reviewer. Reviewers should label a small sample independently, then compare judge scores and criterion flags with their judgments.

If the judge is systematically stricter or more lenient, refine criterion wording and anchors before evaluating new model versions. Repeat selected cases to estimate score stability and test small formatting variations to detect style sensitivity. Calibration examples must match MIRA's actual creative-direction use case; agreement on unrelated general prompts would not validate this judge.

## Statistical limitations

With N=5, this is a proof of concept and is severely underpowered. Scores are estimates, confidence intervals would be wide, and the run cannot support strong model-comparison or production claims. Statistical significance is not the same as practical significance, and neither can be established reliably here. Larger representative samples, repeated generations, locked prompts/model versions, contamination tracking, human labels, and reproducible run metadata are required for credible A/B testing.
