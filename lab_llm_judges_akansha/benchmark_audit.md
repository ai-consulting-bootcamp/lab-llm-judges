# Benchmark Audit & Critique

## Client Context
**Client Scenario (Financial Services):** A German consumer lender wants to automate the generation of consumer-facing credit rejection notices (Kreditabsagen) following loan applications. 
**Requirements** The system must accurately map credit-decision data into the notice, follow the client's compliance-approved German/EU disclosure requirements, respect data-protection and automated-decision constraints, and communicate the decision clearly and respectfully in German.
**Key Concerns** incorrect creditworthiness information, fabricated rejection reasons, inappropriate use or disclosure of personal data, discriminatory language or reasoning, failure to recognize when human/compliance review is required, and misleading claims about automated decision-making or appeal/review options.

---

### Benchmark Evaluation Card 1

* **Benchmark Name:** FinQA (Financial Numerical Reasoning)
* **Year:** 2021
* **Source:** https://github.com/czyssrs/FinQA 
* **Citations:** *Ye et al., FinQA: A Dataset of Numerical Reasoning over Financial Data, EMNLP 2021.* , [arxiv](https://arxiv.org/abs/2109.00122)

**Why it seemed relevant:**
FinQA evaluates multi-step numerical reasoning over structured financial reports and unstructured tabular data. Since Adverse Action Notices require accurate interpretation of applicant debt-to-income (DTI) ratios, revolving credit utilization, and credit score metrics, FinQA tests the foundational reasoning capabilities required to parse credit profiles.

**Contamination risk:**
* [X] Medium - Some overlap possible  
* **Explanation:** FinQA has been publicly available since 2021 and has been widely reproduced and redistributed. Because training-data composition for modern proprietary models is not fully disclosed, overlap cannot be ruled out. We therefore treat FinQA scores as potentially contaminated rather than assuming they measure clean generalization.

**Saturation risk:**
* [X] High - Many models achieve near-perfect scores  
* **Explanation:** SOTA models achieve >85% execution accuracy on FinQA's numerical tasks, making it less effective as a standalone discriminator for modern frontier LLMs.

**Format:**
* [X] Other: Free-form program generation and numerical extraction

**Verdict:**
* [ ] Use it as-is
* [X] Adapt it
* [ ] Reject it  
* **Explanation:** We adapt the tabular credit parsing concept but replace general earnings reports with consumer credit bureau files (e.g., Experian/Equifax extracts) tailored to consumer lending thresholds.

---

### Benchmark Evaluation Card 2

* **Benchmark Name:** LegalBench (Contract & Statutory Rule QA)
* **Year:** 2023
* **Source:** https://github.com/HazyResearch/legalbench
* **Citations:** *Guha et al., LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models, NeurIPS 2023.* , [arxiv](https://arxiv.org/abs/2308.11462)

**Why it seemed relevant:**
LegalBench measures legal reasoning across 162 specialized subtasks, including contract analysis and statutory interpretation. It directly tests whether LLMs can enforce legal rules and extract exact statutory definitions, which mirrors the compliance checks required for Regulation B disclosures.

**Contamination risk:**
* [X] Medium - Some overlap possible  
* **Explanation:** LegalBench was released publicly in 2023, so exposure during training or later post-training cannot be ruled out. The specialized expert-created tasks reduce the likelihood of simple memorization, but do not establish zero contamination.

**Saturation risk:**
* [X] Medium - Some models perform well  
* **Explanation:** While general legal QA yields moderate scores, subtasks requiring multi-jurisdictional compliance or exact negative constraints still show performance gaps across mid-tier models.

**Format:**
* [X] Free-form text
* [X] Multiple Choice

**Verdict:**
* [ ] Use it as-is
* [X] Adapt it  
* [ ] Reject it 
* **Explanation:** We adapt LegalBench's "Rule QA" methodology to evaluate ECOA Regulation B section 1002.9 requirements (e.g., mandatory 30-day notice timeline, principal rejection reason constraints, CFPB notice text).

---

### Benchmark Evaluation Card 3

* **Benchmark Name:** IFEval (Instruction-Following Evaluation)
* **Year:** 2023
* **Source:** https://github.com/google-research/google-research/tree/master/instruction_following_eval
* **Citations:** [Zhou et al., Instruction-Following Evaluation for Large Language Models, arXiv 2023.](https://arxiv.org/abs/2311.07911)

**Why it seemed relevant:**
IFEval tests a model's ability to follow explicit negative and positive constraints (e.g., "start with X", "do not use words Y", "format as 4 bullet points"). Adverse Action (loan rejection) Notices require rigid structural adherence (e.g., exactly 1 to 4 principal denial reasons, specific bold headings, exact disclosure phrases).

**Contamination risk:**
* [X] Medium - Some overlap possible 
* **Explanation:** IFEval uses programmatically verifiable synthetic prompts with customizable rule combinations. Its programmatic verification reduces memorization usefulness, but it doesn't prove that the underlying prompts weren't seen.

**Saturation risk:**
* [X] Low - Benchmark is challenging  
* **Explanation:** State-of-the-art models struggle when 3 or more negative and structural constraints are stacked simultaneously in a single prompt.

**Format:**
* [X] Free-form text (evaluated via rule-based constraint checks)

**Verdict:**
* [ ] Use it as-is
* [X] Adapt it  
* [ ] Reject it 
* **Explanation:** We adapt IFEval's programmatic constraint-checking methodology rather than using its original prompts. This allows us to test client-specific requirements such as required adverse-action fields, allowed reason counts, prohibited unsupported statements, and exact disclosure components.
