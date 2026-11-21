# Client evaluation memo — CompanyScope report quality

**TO:** Head of Legal Operations, fictional client
**FROM:** AI Consulting & Integration team
**DATE:** 21 November 2026
**SUBJECT:** Evidence-grounded company report evaluation — harness validation, not model certification

## Executive summary

We designed an evaluation for a CompanyScope-style assistant that drafts company-research reports from registry records, accounts and external snippets. This is an **offline harness test**, not a live generative-model study. It detects two planted errors but does not establish deployment fitness.

## Methodology

Three public benchmarks informed the design: FinanceBench for documentary numerical reasoning, RAGBench for evidence grounding, and LegalBench for legal-domain reasoning and extraction. None represents our full workflow, so we created five fictional cases with cited reference answers. The cases cover legal identity, source freshness, arithmetic, lack of ownership data and prompt injection.

The executable has two modes. The completed local run checks prewritten responses against literal reference constraints, recording pass/fail and the specific missing or forbidden phrases. Live mode generates answers and sends them to a rubric-driven OpenAI judge, recording 1–5 grades, criterion flags, tokens, latency and estimated charges. **No live API calls were possible in the preparation environment**, and no model-versus-model comparison has been performed.

## Results

On the five fixture cases, deterministic checks passed **3/5 (60%)** and failed **2/5 (40%)**. The failed examples were an intentionally incorrect working-capital result (EUR 2.0m instead of EUR 1.6m) and an intentionally unsafe response claiming sanctions clearance after obeying an instruction in retrieved news text. The identity, freshness and abstention fixtures passed.

These numbers assess the **constructed fixtures and static checker**, not CompanyScope's actual model accuracy. Judge scores, API time, tokens and costs are **not available** until live execution.

## Caveats and limitations

The small English-only synthetic set can reject legitimate paraphrases or miss subtle false claims. Public benchmark exposure creates possible contamination; no evidence establishes which examples a deployed model saw during training. A single LLM judge may prefer confident fluent text, share the target model's failure modes or vary from run to run. Actual retrieval and compliance decisions are out of scope.

## Recommendation

**Do not authorize autonomous client-facing due-diligence or sanctions conclusions from these results.** As a next step, run the supplied five cases using actual candidate and judge calls, compare judge flags to expert labels, and expand to at least 50 consented, representative client cases. Confidence in the *harness demonstration* is moderate; confidence in any untested model's production suitability is **not established**.

## Additional metrics

For each evaluated answer, monitor factual severity, abstention accuracy, citation validity, hallucination and injection failure rates, plus generation/judging latency, input/output tokens and estimated cost. Energy and carbon impacts cannot be inferred reliably from token billing alone; provider and infrastructure data would be needed for environmental assessment. Balance extra review and judge-call cost against avoided factual-risk exposure.
