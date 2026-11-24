# Implementation Summary — ShopCo

We built a Python evaluation pipeline in
`llm_judge_evaluation.ipynb` using the OpenAI API directly.
The notebook loads the fictional ShopCo policy and judge prompt
from `evaluation_design.md`. It generates replies for five
reviewed cases and evaluates accuracy, completeness, and tone.
The overall verdict is PASS only when all three criteria are true.
The pipeline checks the judge's JSON structure and score consistency.
It saves replies, evaluations, API metadata, time, and token usage.
The API returned model version `gpt-4o-mini-2024-07-18`
for both generation and judging.

We calibrated the judge on three human-reviewed sample replies.
Version v1 matched 2 of 3 human verdicts. After clarifying the
instructions, v2 matched all three calibration verdicts and criteria.
However, it still included an unsupported claim in one explanation.
On the five main cases, Sandra accepted 4 of 5 generated replies
after AI-assisted review. The judge accepted 2 of 5 and agreed
with the human verdicts on 3 of 5 cases (60%).
With FAIL as the positive class, precision was 33.3%, recall
was 100%, and F1 was 0.50. Recall was based on only one
human-labeled failing reply. The judge incorrectly rejected
SHOP-02 and SHOP-03. It matched the FAIL label for SHOP-01
but gave an incorrect explanation.

The main run used 2,679 tokens for generation and 6,970 for judging.
API call durations totalled 9.63 seconds for generation and
10.56 seconds for judging. The estimated combined cost was
USD 0.00193290, excluding calibration, using official prices
checked on 24 November 2026. Energy use and carbon emissions
were not measured. These five synthetic cases do not establish
production reliability. The same model generated and judged
the replies, and human labels were reviewed with AI assistance.
We recommend keeping human review and testing a larger,
independently labeled dataset before using this judge for
automatic decisions. We kept v2 unchanged after the main run
and preserved its errors as evidence.