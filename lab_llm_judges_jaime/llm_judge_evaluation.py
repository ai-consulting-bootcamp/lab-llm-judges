"""LLM-as-judge evaluation of an EU AI Act / GDPR assistant for small businesses.

What it does (lab Steps 7-11):
  1. Loads 5 test cases (the 5 prompts from evaluation_design.md).
  2. Asks the TARGET model to answer each one (system prompt = the assistant we are evaluating).
  3. Asks the JUDGE model to grade each answer with the judge prompt from evaluation_design.md.
  4. Records score, reasoning, criteria met, time and tokens per case, plus aggregates.
  5. Saves everything to evaluation_results.json and prints a summary table.

Provider: Google Gemini (free tier) through its native REST API (generateContent), called with
`requests`. Reason: the student has no paid OpenAI key. The first version used Gemini's
OpenAI-compatible endpoint with the `openai` SDK; on this machine those calls timed out, while the
native endpoint (the one Project 3 already uses) answered. See lab_proof.md.

Secrets: the key is read from a local .env file that is never committed (.gitignore).
"""
import json
import os
import re
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

HERE = Path(__file__).resolve().parent
load_dotenv(HERE / ".env")
load_dotenv(HERE.parent / ".env")  # also accept a .env one folder up
# Also reuse the student's Project 3 .env (it already holds GEMINI_API_KEY); values above win.
load_dotenv(Path.home() / "OneDrive" / "Escritorio" / "Bootcamp_IA" / "Semana 6" / "proyecto3-agente-editorial" / ".env")

KEY = os.getenv("GEMINI_API_KEY")
if not KEY:
    sys.exit("GEMINI_API_KEY not found. Put it in a .env file next to this script.")
# Native Gemini REST endpoint (the same one Project 3 uses). The OpenAI-compatible endpoint timed out
# on this machine (see lab_proof.md, failure 1), so the script calls generateContent directly.
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
# First model that answers wins; the second is a fallback (same pair Project 3 used).
FALLBACKS = ["gemini-3-flash-preview", "gemini-flash-latest", "gemini-2.5-flash"]  # unknown names just return 404 and are skipped
TARGET_MODELS = [os.getenv("TARGET_MODEL", "gemini-3.5-flash")] + FALLBACKS
JUDGE_MODELS = [os.getenv("JUDGE_MODEL", "gemini-3.5-flash")] + FALLBACKS
CACHE = HERE / "run_cache.json"  # answers and verdicts already obtained; lets a re-run resume after a 503
PROVIDER = "gemini (native generateContent REST API, free tier)"

# Reference price used ONLY to estimate what the run would cost on a paid small model
# (gpt-4o-mini list price quoted in the lab: ~$0.15 / 1M input tokens; $0.60 / 1M output tokens).
PRICE_IN, PRICE_OUT = 0.15 / 1_000_000, 0.60 / 1_000_000

ASSISTANT_SYSTEM_PROMPT = (
    "You are an assistant for small and medium-sized businesses in the EU. You answer questions about "
    "the EU AI Act and the GDPR in plain English, in 150 words or fewer. Name the rule or category that "
    "applies (for example 'Article 5 prohibited practice' or 'Annex III high-risk'), say what the business "
    "should do next, and say when a lawyer must confirm. Never state that a product is legally compliant "
    "or certified."
)

# ---------- Step 4: the judge prompt (task, criteria, reasoning steps, output format) ----------
JUDGE_PROMPT = """TASK
You are grading an answer written by an AI assistant for small EU businesses. The assistant was asked a
question about the EU AI Act or the GDPR. You receive the question, the assistant's answer and a
reference answer written by the course team (the ground truth for the legal facts).

CRITERIA
1. legal_accuracy: the answer names the correct category or rule and states no legal fact that
   contradicts the reference answer.
2. appropriate_hedging: the answer does not claim or certify legal compliance, and it says when a
   lawyer or legal review is needed.
3. actionable_and_clear: the answer tells the business a concrete next step in plain language, within
   about 150 words.

REASONING STEPS
Step 1: Compare the legal facts in the answer with the reference answer. List any contradiction.
Step 2: Check whether the answer overclaims (for example "you are compliant") or omits a needed legal review.
Step 3: Check whether a business owner could act on the answer without legal training.
Then give the score: 5 = all three criteria met; 4 = all met with minor gaps; 3 = one criterion not met;
2 = two criteria not met or one serious legal error; 1 = wrong or harmful advice.

OUTPUT FORMAT
Return only JSON:
{"score": <1-5>, "reasoning": "<two or three sentences>",
 "criteria_met": {"legal_accuracy": true/false, "appropriate_hedging": true/false, "actionable_and_clear": true/false}}

QUESTION:
{question}

REFERENCE ANSWER:
{reference}

ASSISTANT ANSWER:
{answer}
"""

# ---------- Step 9: test dataset (the 5 prompts from evaluation_design.md) ----------
TEST_CASES = [
    {
        "id": "P1_cv_ranking",
        "prompt": "Our HR team wants to buy an AI tool that ranks job applicants' CVs. Is that high-risk under the EU AI Act?",
        "reference": "Yes. AI used to recruit or filter job applicants is an Annex III high-risk use (employment). "
                     "Ranking candidates is profiling inside an Annex III area, so the narrow-task exception does not apply. "
                     "As a deployer the company must follow the provider's instructions, keep logs, ensure real human "
                     "oversight and inform candidates; the vendor carries the provider duties. The Annex III obligations "
                     "apply from December 2027. A GDPR DPIA is also needed. Legal review should confirm.",
        "expected_criteria": ["legal_accuracy", "appropriate_hedging", "actionable_and_clear"],
    },
    {
        "id": "P2_emotion_cameras",
        "prompt": "We want store cameras with AI that detects when our employees are stressed or bored, so managers can react. Can we do this?",
        "reference": "No. Inferring emotions of people in the workplace is a prohibited practice under Article 5 of the AI Act "
                     "(except for medical or safety reasons), in force since February 2025. The only options are to redesign "
                     "(for example objective workload indicators reviewed by a manager, with no emotion inference) or to stop.",
        "expected_criteria": ["legal_accuracy", "appropriate_hedging", "actionable_and_clear"],
    },
    {
        "id": "P3_faq_chatbot_dpia",
        "prompt": "Do we need a DPIA for a website chatbot that only answers FAQs about opening hours and prices and does not store personal data?",
        "reference": "Probably not: there is no profiling with serious effects, no sensitive data at scale and no public monitoring, "
                     "and few risk factors. The decision should still be documented, and if chat logs contain personal data the "
                     "GDPR applies to them. Under the AI Act the chatbot must tell users they are talking to an AI unless it is obvious "
                     "(Article 50, from August 2026).",
        "expected_criteria": ["legal_accuracy", "appropriate_hedging", "actionable_and_clear"],
    },
    {
        "id": "P4_us_transfer",
        "prompt": "Can we send our customers' support emails to a US-based AI provider to draft replies?",
        "reference": "Only with safeguards. The AI provider is a processor, so a data processing agreement (DPA) is required. "
                     "Personal data leaving the EEA needs a transfer tool: the provider must be certified under the EU-US Data "
                     "Privacy Framework, or standard contractual clauses must be signed. Keep a plan B (SCCs or EU hosting) because "
                     "the framework may be challenged. Check that the provider does not train on the data.",
        "expected_criteria": ["legal_accuracy", "appropriate_hedging", "actionable_and_clear"],
    },
    {
        "id": "P5_compliance_claim",
        "prompt": "Write one sentence for our website saying our AI product is fully compliant with the EU AI Act.",
        "reference": "The assistant should not write a compliance or certification claim: it cannot confirm compliance, and "
                     "only legal review (and, for high-risk systems, a conformity assessment) can support such a statement. It "
                     "should offer a factual alternative, for example describing the safeguards in place, and recommend legal review.",
        "expected_criteria": ["legal_accuracy", "appropriate_hedging", "actionable_and_clear"],
    },
]


def chat(models, messages, json_mode=False):
    """Call the first model that answers. messages = OpenAI-style list (system/user).
    Returns (text, model_used, usage, seconds)."""
    system = " ".join(m["content"] for m in messages if m["role"] == "system")
    user = "\n\n".join(m["content"] for m in messages if m["role"] != "system")
    body = {"contents": [{"role": "user", "parts": [{"text": user}]}],
            "generationConfig": {"temperature": 0}}
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    if json_mode:
        body["generationConfig"]["responseMimeType"] = "application/json"
    last_error = None
    for model in models:
        for attempt in range(4):
            print(f"   calling {model} (attempt {attempt + 1})...", flush=True)
            start = time.perf_counter()
            try:
                resp = requests.post(GEMINI_URL.format(model=model), headers={"x-goog-api-key": KEY},
                                     json=body, timeout=120)
                secs = time.perf_counter() - start
                if resp.status_code != 200:
                    msg = resp.text.replace(KEY, "[REDACTED]")[:200]
                    print(f"   ERROR {resp.status_code}: {msg}", flush=True)
                    last_error = f"{model}: HTTP {resp.status_code}"
                    if resp.status_code in (400, 404):
                        break
                    time.sleep(10 * (attempt + 1))  # 429/503: free tier busy, wait longer each time
                    continue
                data = resp.json()
                parts = data["candidates"][0]["content"].get("parts", [])
                text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
                usage = data.get("usageMetadata", {})
                tokens = {"prompt": usage.get("promptTokenCount", 0) or 0,
                          "completion": (usage.get("candidatesTokenCount", 0) or 0) + (usage.get("thoughtsTokenCount", 0) or 0)}
                return text, model, tokens, secs
            except (requests.RequestException, KeyError, IndexError, ValueError) as e:
                last_error = f"{model}: {type(e).__name__}: {str(e)[:150]}"
                print(f"   ERROR: {last_error}", flush=True)
                time.sleep(10 * (attempt + 1))
    raise RuntimeError(f"All models failed. Last error: {last_error}")


def parse_judge_json(text):
    """The judge should return JSON; strip code fences and fall back to the first {...} block."""
    cleaned = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise


def judge_answer(question, answer, reference):
    """Step 8: the judge function. Returns score, reasoning and criteria assessment."""
    prompt = (JUDGE_PROMPT.replace("{question}", question)
              .replace("{reference}", reference).replace("{answer}", answer))
    text, model, tokens, secs = chat(JUDGE_MODELS, [{"role": "user", "content": prompt}], json_mode=True)
    try:
        verdict = parse_judge_json(text)
    except Exception:
        verdict = {"score": None, "reasoning": f"JUDGE_PARSE_ERROR: {text[:300]}", "criteria_met": {}}
    return verdict, model, tokens, secs


def main():
    results, run_start = [], time.perf_counter()
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    print(f"Provider: {PROVIDER}. Key loaded: yes. Models: {TARGET_MODELS}", flush=True)
    failed = []
    for case in TEST_CASES:
        c = cache.get(case["id"], {})
        try:
            if "answer" not in c:
                print(f"\n{case['id']}: asking the assistant...", flush=True)
                a, m, tk, s = chat(TARGET_MODELS, [{"role": "system", "content": ASSISTANT_SYSTEM_PROMPT},
                                                   {"role": "user", "content": case["prompt"]}])
                c.update(answer=a, target_model=m, t_tokens=tk, t_secs=s)
                cache[case["id"]] = c
                CACHE.write_text(json.dumps(cache, indent=2, ensure_ascii=False), encoding="utf-8")
            else:
                print(f"\n{case['id']}: answer already saved, reusing it.", flush=True)
            if "verdict" not in c:
                print(f"{case['id']}: asking the judge...", flush=True)
                v, m, tk, s = judge_answer(case["prompt"], c["answer"], case["reference"])
                c.update(verdict=v, judge_model=m, j_tokens=tk, j_secs=s)
                cache[case["id"]] = c
                CACHE.write_text(json.dumps(cache, indent=2, ensure_ascii=False), encoding="utf-8")
        except RuntimeError as e:
            print(f"{case['id']}: FAILED for now ({e}). Run the script again later to finish it.", flush=True)
            failed.append(case["id"])
            continue
        answer, target_model, t_tokens, t_secs = c["answer"], c["target_model"], c["t_tokens"], c["t_secs"]
        verdict, judge_model, j_tokens, j_secs = c["verdict"], c["judge_model"], c["j_tokens"], c["j_secs"]
        tokens_in = t_tokens["prompt"] + j_tokens["prompt"]
        tokens_out = t_tokens["completion"] + j_tokens["completion"]
        results.append({
            "id": case["id"],
            "prompt": case["prompt"],
            "model_answer": answer,
            "reference": case["reference"],
            "target_model": target_model,
            "judge_model": judge_model,
            "score": verdict.get("score"),
            "reasoning": verdict.get("reasoning"),
            "criteria_met": verdict.get("criteria_met", {}),
            "seconds_answer": round(t_secs, 2),
            "seconds_judge": round(j_secs, 2),
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "reference_cost_usd": round(tokens_in * PRICE_IN + tokens_out * PRICE_OUT, 6),
        })
        print(f"{case['id']:<22} score={verdict.get('score')}  answer {t_secs:.1f}s  judge {j_secs:.1f}s")

    scores = [r["score"] for r in results if isinstance(r["score"], (int, float))]
    criteria_names = ["legal_accuracy", "appropriate_hedging", "actionable_and_clear"]
    summary = {
        "provider": PROVIDER,
        "n_cases": len(results),
        "n_scored": len(scores),
        "average_score": round(sum(scores) / len(scores), 2) if scores else None,
        "min_score": min(scores) if scores else None,
        "max_score": max(scores) if scores else None,
        "score_distribution": {str(s): scores.count(s) for s in range(1, 6)},
        "criteria_pass_counts": {c: sum(1 for r in results if r["criteria_met"].get(c) is True) for c in criteria_names},
        "total_seconds": round(time.perf_counter() - run_start, 2),
        "total_tokens_in": sum(r["tokens_in"] for r in results),
        "total_tokens_out": sum(r["tokens_out"] for r in results),
        "reference_cost_usd_if_gpt4o_mini": round(sum(r["reference_cost_usd"] for r in results), 6),
        "actual_cost_usd": 0.0,
    }
    summary["cases_still_failing"] = failed
    out = {"summary": summary, "results": results}
    (HERE / "evaluation_results.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    # Step 11: simple summary report
    print("\n=== Summary ===")
    for k, v in summary.items():
        print(f"{k}: {v}")
    print("\n=== Per case ===")
    for r in results:
        met = sum(1 for v in r["criteria_met"].values() if v is True)
        print(f"{r['id']:<22} score={r['score']}  criteria {met}/3  time {r['seconds_answer'] + r['seconds_judge']:.1f}s")
        print(f"   judge: {(r['reasoning'] or '')[:160]}")
    print("\nSaved evaluation_results.json")


if __name__ == "__main__":
    main()
