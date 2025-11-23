import os
import re
import json
from dataclasses import dataclass
from types import SimpleNamespace
from typing import List, Dict, Optional
import requests


def _load_env(path: Optional[str] = None) -> Dict[str, str]:
    base = path or os.path.join(os.path.dirname(__file__), ".env")
    out: Dict[str, str] = {}
    if os.path.exists(base):
        with open(base, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                m = re.match(r"([^=]+)=(.*)", line)
                if not m:
                    continue
                k = m.group(1).strip()
                v = m.group(2).strip().strip('"')
                out[k] = v
    return out


ENV = _load_env()
DEFAULT_API_KEY = ENV.get("LLM_API_KEY") or os.environ.get("LLM_API_KEY")
DEFAULT_BASE = (ENV.get("LLM_BASE") or os.environ.get("LLM_BASE") or "https://api.groq.com/openai/v1").rstrip("/")
DEFAULT_MODEL = ENV.get("LLM_MODEL") or os.environ.get("LLM_MODEL") or "llama-2-7b"


class _ChatCompletions:
    def __init__(self, parent: "GroqClient"):
        self._parent = parent

    def create(self, *, model: str, messages: List[Dict], temperature: float = 0.2, max_tokens: int = 512):
        payload = {"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
        resp = requests.post(self._parent._url, headers=self._parent._headers, json=payload, timeout=self._parent._timeout)
        try:
            body = resp.json()
        except Exception:
            body = {"raw": resp.text}

        # Normalize to a simple object with .choices[0].message.content to match expected SDK usage
        if resp.status_code >= 400:
            raise RuntimeError(f"LLM error {resp.status_code}: {body}")

        # Attempt to extract model-style response
        try:
            content = None
            if isinstance(body, dict) and body.get("choices"):
                c = body["choices"][0]
                # choice may contain message dict
                if isinstance(c, dict) and c.get("message") and isinstance(c["message"], dict):
                    content = c["message"].get("content")
                elif isinstance(c, dict) and c.get("text"):
                    content = c.get("text")
            if content is None:
                # fallback to raw text
                content = json.dumps(body, ensure_ascii=False)
        except Exception:
            content = json.dumps(body, ensure_ascii=False)

        # Build a SimpleNamespace mimicking SDK response
        msg = SimpleNamespace(content=content)
        choice = SimpleNamespace(message=msg)
        return SimpleNamespace(choices=[choice], raw=body)


class GroqClient:
    """Adapter that exposes a `.chat.completions.create(...)` interface similar to SDKs used in the codebase.

    Usage:
        client = GroqClient(api_key=..., base_url=...)
        resp = client.chat.completions.create(model=model, messages=messages)
        text = resp.choices[0].message.content
    """

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, timeout: int = 30):
        self._api_key = api_key or DEFAULT_API_KEY
        if not self._api_key:
            raise RuntimeError("LLM_API_KEY not provided to GroqClient and not found in environment")
        self._base = (base_url or DEFAULT_BASE).rstrip('/')
        self._timeout = timeout
        self._url = f"{self._base}/chat/completions"
        self._headers = {"Authorization": f"Bearer {self._api_key}", "Content-Type": "application/json"}
        self.chat = SimpleNamespace(completions=_ChatCompletions(self))


if __name__ == "__main__":
    # quick smoke test when executed directly
    client = GroqClient()
    msgs = [{"role": "user", "content": "Olá Groq, teste rápido do adapter."}]
    r = client.chat.completions.create(model=DEFAULT_MODEL, messages=msgs)
    print("== RESPONSE TEXT ==")
    print(r.choices[0].message.content)
    print("== RAW ==")
    print(json.dumps(getattr(r, 'raw', {}), ensure_ascii=False, indent=2))
