"""Repository analysis with LLaMA 3.1-8B — returns a structured JSON dict."""
from __future__ import annotations

import json

from shared.config import FAST_MODEL
from shared.llm import chat


def _extract_json(text: str) -> dict:
    text = text.replace("```json", "").replace("```", "").strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("no JSON object found")
    return json.loads(text[start : end + 1])


def analyze_repository(fetched: dict) -> dict:
    meta = fetched["meta"]
    file_list = "\n".join(f["path"] for f in fetched["files"][:40])

    prompt = f"""Analyze this software repository and respond with ONLY a JSON object — no prose, no markdown fences.

Repository: {meta['full_name']}
Description: {meta['description']}
Primary language: {meta['language']}
Topics: {', '.join(meta['topics'])}

Files:
{file_list}

README (excerpt):
{fetched.get('readme', '')[:3000]}

Return exactly this JSON shape:
{{
  "purpose": "one clear sentence on what the project does",
  "domain": "the technical/application domain",
  "technologies": ["list", "of", "key", "technologies"],
  "architecture": "2-3 sentences on how the system is structured",
  "key_features": ["3-6 notable features"]
}}"""

    try:
        return _extract_json(chat(prompt, model=FAST_MODEL, temperature=0.2))
    except Exception:
        return {
            "purpose": meta["description"] or f"Software project {meta['full_name']}",
            "domain": meta["language"] or "software engineering",
            "technologies": [meta["language"]] if meta["language"] else [],
            "architecture": "Modular source-code repository.",
            "key_features": meta["topics"][:5],
        }
