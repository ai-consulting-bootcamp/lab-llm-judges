"""Provider adapter and structured judge parsing."""

import json
import re
from typing import Any

from .models import JudgeResult, TokenUsage
from .prompts import JUDGE_PROMPT


def _content(response: Any) -> str:
    content = response.choices[0].message.content
    return content if isinstance(content, str) else "" if content is None else str(content)


def call_chat_model(client: Any, prompt: str, model: str, temperature: float = 0.0, json_mode: bool = False) -> tuple[str, TokenUsage]:
    kwargs: dict[str, Any] = {"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": temperature}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    response = client.chat.completions.create(**kwargs)
    return _content(response), TokenUsage.from_api_usage(getattr(response, "usage", None))


def _parse_json(text: str) -> dict[str, Any]:
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.I | re.S)
    try:
        value = json.loads(cleaned)
    except json.JSONDecodeError:
        start, end = cleaned.find("{"), cleaned.rfind("}")
        if start < 0 or end <= start:
            raise
        value = json.loads(cleaned[start : end + 1])
    if not isinstance(value, dict):
        raise ValueError("Judge response must be a JSON object")
    return value


def normalize_judge_result(raw: str) -> JudgeResult:
    try:
        data = _parse_json(raw)
        score = int(data["score"])
        if score not in range(1, 6):
            raise ValueError("score must be between 1 and 5")
        criteria = data.get("criteria_met") or {}
        return JudgeResult(score, str(data.get("reasoning", "")), {key: bool(criteria.get(key, False)) for key in ("conflict_handling", "uncertainty_fidelity", "source_faithfulness")}, data.get("critical_fail"), list(data.get("conflicts_found_in_source") or []), dict(data.get("evidence") or {}), raw)
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        return JudgeResult(None, "", {}, None, raw_response=raw, parse_error=f"Could not parse judge JSON: {exc}")


def judge_output(client: Any, source_record: str, system_output: str, model: str) -> tuple[JudgeResult, TokenUsage]:
    prompt = JUDGE_PROMPT.replace("{source_record}", source_record).replace("{system_output}", system_output)
    raw, usage = call_chat_model(client, prompt, model, temperature=0.0, json_mode=True)
    return normalize_judge_result(raw), usage
