"""Typed domain models used throughout the evaluation pipeline."""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass(frozen=True)
class EvaluationCase:
    case_id: str
    title: str
    prompt_template: str
    source_record: str
    ground_truth: str
    verification_method: str
    primary_failure_mode: str
    rule_checker: str
    expected_criteria: dict[str, bool] = field(default_factory=dict)
    judgeable: bool = False

    def render_prompt(self) -> str:
        return self.prompt_template.replace("{source_record}", self.source_record)


@dataclass
class TokenUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

    @classmethod
    def from_api_usage(cls, usage: Any) -> "TokenUsage":
        if usage is None:
            return cls()
        return cls(
            int(getattr(usage, "prompt_tokens", 0) or 0),
            int(getattr(usage, "completion_tokens", 0) or 0),
            int(getattr(usage, "total_tokens", 0) or 0),
        )

    def add(self, other: "TokenUsage") -> None:
        self.prompt_tokens += other.prompt_tokens
        self.completion_tokens += other.completion_tokens
        self.total_tokens += other.total_tokens


@dataclass
class JudgeResult:
    score: Optional[int]
    reasoning: str
    criteria_met: dict[str, bool]
    critical_fail: Optional[bool]
    conflicts_found_in_source: list[str] = field(default_factory=list)
    evidence: dict[str, Any] = field(default_factory=dict)
    raw_response: str = ""
    parse_error: Optional[str] = None


@dataclass
class CaseResult:
    case_id: str
    title: str
    prompt: str
    ground_truth: str
    verification_method: str
    primary_failure_mode: str
    expected_criteria: dict[str, bool]
    model_response: str
    latency_seconds: float
    target_usage: TokenUsage
    rule_checks: dict[str, Any]
    judge: Optional[JudgeResult] = None
    judge_latency_seconds: Optional[float] = None
    judge_usage: TokenUsage = field(default_factory=TokenUsage)
    estimated_cost: Optional[float] = None
    error: Optional[str] = None
