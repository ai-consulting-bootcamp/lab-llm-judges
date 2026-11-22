"""Environment and provider configuration."""

import os
from pathlib import Path
from typing import Any, Optional


DEFAULT_TARGET_MODEL = "gpt-4o-mini"
DEFAULT_JUDGE_MODEL = "gpt-4o-mini"
DEFAULT_OUTPUT_PATH = "evaluation_results.json"


def load_environment(env_path: str | Path = ".env") -> None:
    """Load a dotenv file without overwriting explicitly exported variables."""
    path = Path(env_path)
    if not path.exists():
        return
    try:
        from dotenv import load_dotenv
    except ImportError:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip("'\""))
    else:
        load_dotenv(path)


def create_openai_client(api_key: Optional[str] = None) -> Any:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("Install dependencies with: pip install openai python-dotenv") from exc
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is not set in .env or the environment.")
    return OpenAI(api_key=key)
