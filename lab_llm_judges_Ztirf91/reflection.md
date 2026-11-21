# Step 6 — Reflection

## 1. How would the evaluation change for French?

If the retailer uses the same policies in French, the expected support decisions stay the same. I would translate the existing cases to preserve coverage and add naturally phrased French requests, including indirect questions about refunds. If the retailer uses a different policy in the target market, I would update the reference answers accordingly.

I would ask a fluent French-speaking reviewer to label clear and borderline replies before checking the judge's agreement. For example, « vérifier si un remboursement est possible » leaves the outcome open, while « encore valider votre remboursement » may imply approval is pending only as a formality. The exact routing-label check can stay the same if the ticketing system uses the same label.

## 2. How would I answer a client asking whether the model is AGI-level?

I would clarify whether the client means broad human-level capability or the ability to handle their support workload independently. Broad capability would require an agreed definition, fresh tasks across multiple domains, appropriate human baselines, and repeated trials. Our five cases provide evidence about a narrow set of support decisions.

For the deployment decision, I would use public benchmarks to shortlist models, then compare candidates on representative cases they have not seen during prompt development. I would explain why I chose the candidate, which alternatives I considered, and how they compare on policy compliance, critical errors, cost, and response time. That evidence would guide which cases to automate and which to escalate.

## 3. What requires human judgment?

I would use human reviewers to assess whether the chatbot acknowledges a frustrated customer in a way that feels respectful in context. In the delayed-parcel case, two replies can both request the order number. A generic apology can feel dismissive when the customer has already spent their lunch break chasing the delivery. An apology keyword only establishes that the word appeared. An LLM judge can flag replies for review, but its rating does not establish how customers experience them.

I would give two support reviewers a small sample of replies without model names and ask them to assess whether each acknowledges the specific inconvenience and avoids blame. They would review independently, then discuss disagreements using concrete examples. Feedback from actual customers would help validate whether those judgments reflect the audience's experience.
