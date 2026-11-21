# Reflection: Critical Challenges in LLM Evaluation Design

## 1. Adapting the Evaluation Design for French-Language Client Data
If Meridian's underwriting records and customer communications were in French, adapting the evaluation would require more than translating prompts. The regulatory baseline would shift from US ECOA/FCRA rules to the applicable French and EU frameworks, including consumer-credit law, GDPR requirements around automated decisions and human intervention, and Banque de France credit-registry disclosures. Deterministic checks would therefore need to be rebuilt around verified French legal terminology, not translated American notices.

Language quality would also require native review: formal *vouvoiement*, appropriate salutations, gender agreement, and culturally suitable directness all affect whether a refusal feels respectful. I would calibrate the judge on French letters reviewed by native-speaking compliance and customer-experience experts, use a bilingual legal glossary, and test both legal precision and customer comprehension.

---

## 2. Responding to a Client Asking: "Is This Model AGI-Level?"
If an executive asks whether a model scoring `5/5` on adverse-action letters is “AGI-level,” I would answer **no**. That score demonstrates bounded performance on a constrained text-transformation task; the model receives the facts and does not make the underwriting decision. AGI would imply much broader, reliable flexibility across unfamiliar domains, including reasoning, planning, tool use, and adaptation.

A broader claim would require diverse, uncontaminated evaluations of open-world reasoning, novel tool interaction, mathematics, causal discovery, and adaptation. For Meridian, confusing drafting fluency with general intelligence would create governance risk by encouraging autonomous credit decisions. The model should remain limited to controlled communications support.

---

## 3. What Cannot Be Evaluated Without a Human, and Why
The aspect that cannot be reliably evaluated without a human is **authentic empathetic impact combined with regulatory accountability**. A denial may cause financial stress or stigma. An LLM judge can check politeness and prohibited wording, but it cannot reliably determine whether standardized empathy feels hollow, patronizing, or emotionally jarring to a real borrower.

Automated checks also cannot assume legal accountability or resolve ambiguous fair-lending risks under changing supervisory guidance. I would use a tiered model: deterministic and judge screening for every letter; mandatory compliance review for counteroffers, edge cases, and outputs scoring below `4`; and monthly blind audits by compliance and customer-experience specialists on a sample of approved letters.
