# LLMs grading LLMs — EU AI Act & GDPR assistant for SMEs

**Scenario:** a consultancy is building an assistant that answers small businesses' questions about the EU AI Act and the GDPR. It must be legally accurate, avoid claiming compliance and give a clear next step. Full description in `benchmark_audit.md`.

**Approach:** audit 3 public benchmarks (all rejected or adapted) → design 5 custom prompts with reference answers and an LLM judge → run them in Python → report with caveats.

**Start here:** [`lab_proof.md`](./lab_proof.md) — the run, its evidence, the final output and the limitations.

## File map

| File | What it is |
|---|---|
| `lab_proof.md` | Entry point for the reviewer: code, one run with input and evidence, output, failures |
| `benchmark_audit.md` | Step 1 scenario and Step 2 audit of LegalBench, LexGLUE and TruthfulQA |
| `evaluation_design.md` | Step 3 five prompt cards and Step 4 judge prompt, bias analysis and calibration |
| `evaluation_memo.md` | Step 5 one-page memo to the client |
| `reflection.md` | Step 6 answers to the three reflection questions |
| `llm_judge_evaluation.py` | Steps 7–11 pipeline: target model, judge, metrics |
| `evaluation_results.json` | Output of the run of 26/11/2026 |
| `implementation_summary.md` | What was built and the key findings |
| `requirements.txt` | Python dependencies |

## How to run

```bash
pip install -r requirements.txt
# create .env next to the script with: GEMINI_API_KEY=your_key
python llm_judge_evaluation.py
```

The script writes `evaluation_results.json`. On a free-tier error (503/429) run it again: it resumes from `run_cache.json`. Optional: set `TARGET_MODEL` / `JUDGE_MODEL` to choose other Gemini models.
