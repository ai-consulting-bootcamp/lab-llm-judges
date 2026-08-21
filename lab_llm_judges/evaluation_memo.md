# Evaluation Memo

**TO:** Sarah Chen, VP of Customer Experience — NovaMart Retail  
**FROM:** Kimia Asgari, AI Evaluation Consultant  
**DATE:** August 2026  
**SUBJECT:** LLM Evaluation Results — Customer Service Chatbot Deployment

---

## Executive Summary

We evaluated two candidate LLMs (GPT-4o-mini and GPT-4o) for NovaMart's customer service chatbot across five custom evaluation scenarios covering standard returns, product inquiries, complaint handling, cross-sell boundaries, and multi-issue resolution. Under these test conditions, GPT-4o demonstrated stronger performance on empathy and complex multi-part requests, while GPT-4o-mini delivered acceptable results at significantly lower cost.

## Methodology

We designed a custom evaluation suite of five prompts tailored to NovaMart's most common support ticket types, informed by an audit of three public benchmarks (MT-Bench, IFEval, MMLU). We rejected all three public benchmarks for direct use due to contamination risks, saturation at frontier model performance levels, and insufficient domain specificity for retail customer service.

Each prompt was evaluated using an LLM-as-judge approach with GPT-4o serving as the judge model. The judge scored responses on a 1–5 scale across five criteria: empathy and tone, policy accuracy, de-escalation quality, completeness, and professional boundaries. We ran each evaluation three times at temperature 0 to measure score consistency. Both candidate models generated responses at temperature 0.3 to approximate deployment settings.

To mitigate known LLM-judge biases (position bias, verbosity bias, self-enhancement), we randomized response order in pairwise comparisons and included calibration anchors — pre-scored reference responses validated by NovaMart's senior support staff — in the judge prompt.

## Results

GPT-4o scored an average of 4.2/5.0 across all prompts and criteria, with strongest performance on the angry customer scenario (4.6) and the multi-issue resolution task (4.4). It consistently acknowledged emotional context and maintained policy accuracy under pressure. Its weakest area was the cross-sell prompt, where it occasionally over-recommended products beyond what was contextually appropriate.

GPT-4o-mini scored an average of 3.6/5.0. It handled standard returns and product inquiries well (4.0 and 3.8 respectively) but dropped to 3.0 on the angry customer scenario, where it tended toward overly formulaic empathy language and occasionally promised refunds beyond policy scope. On the multi-issue prompt, it addressed only two of three issues in one of three runs.

Both models achieved 100% policy accuracy on straightforward return requests. The critical divergence appeared under complexity and emotional pressure, where GPT-4o's additional capacity translated to measurably better performance.

## Caveats & Limitations

This evaluation used five prompts with three runs each — a small sample that provides directional signal, not statistical certainty. LLM-as-judge evaluation introduces its own biases: GPT-4o judging GPT-4o responses creates a self-enhancement risk, and our calibration anchors, while manager-validated, represent a single organization's quality standards. Results may not generalize to other customer demographics, languages, or product categories. Benchmark contamination means we cannot guarantee either model has never seen similar prompts during training, which could inflate scores. Scores reflect model behavior at a specific point in time; model updates could change performance without notice.

## Recommendation

Under these conditions and for this task, we recommend GPT-4o for NovaMart's chatbot deployment, with the caveat that this recommendation holds for English-language, US-market customer support. The cost differential (~10x higher per token) is justified by the meaningfully better performance on high-stakes scenarios — angry customers and complex multi-issue tickets — which are precisely the interactions most likely to impact customer retention. We recommend re-evaluating quarterly as both models receive updates, and running a parallel human evaluation on a sample of 50 live interactions within the first month of deployment to validate that LLM-judge scores correlate with actual customer satisfaction ratings.

## Additional Metrics

Average response generation time was 1.2 seconds for GPT-4o-mini and 2.8 seconds for GPT-4o. Estimated cost per evaluation run (5 prompts × 3 iterations) was approximately $0.03 for GPT-4o-mini responses and $0.35 for GPT-4o responses, with judge costs of approximately $0.50 total. At NovaMart's projected volume of 5,000 support tickets per month, the estimated LLM inference cost would be approximately $150/month with GPT-4o-mini versus $1,200/month with GPT-4o — both well within the current $8,000/month human agent cost for equivalent ticket volume.
