"""GitHub REST API v3 loader — repo metadata, README, up to 40 source files."""
from __future__ import annotations

import base64
import re
from datetime import datetime

import requests

from shared.config import GITHUB_TOKEN, MAX_REPO_FILES

API = "https://api.github.com"

CODE_EXT = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".c", ".cpp", ".h", ".hpp",
    ".go", ".rs", ".rb", ".php", ".cs", ".swift", ".kt", ".scala", ".sql",
    ".sh", ".yml", ".yaml", ".toml", ".json", ".md", ".txt", ".html", ".css",
}
SKIP_PARTS = (
    "node_modules/", "dist/", "build/", ".git/", "venv/", "__pycache__/",
    "assets/", "images/", "img/", "fonts/", "vendor/", ".idea/",
)
MAX_FILE_BYTES = 100_000


def _headers() -> dict:
    h = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        h["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return h


def parse_repo_url(url: str) -> tuple[str, str]:
    m = re.search(r"github\.com[/:]([\w.\-]+)/([\w.\-]+?)(?:\.git)?/?$", url.strip())
    if not m:
        raise ValueError("That doesn't look like a GitHub repository URL. Expected github.com/owner/repo")
    return m.group(1), m.group(2)


def get_rate_limit() -> dict:
    r = requests.get(f"{API}/rate_limit", headers=_headers(), timeout=15)
    core = r.json().get("resources", {}).get("core", {})
    return {
        "remaining": core.get("remaining", 0),
        "limit": core.get("limit", 60),
        "reset": datetime.fromtimestamp(core.get("reset", 0)),
    }


def _get(url: str) -> requests.Response:
    r = requests.get(url, headers=_headers(), timeout=30)
    if r.status_code == 404:
        raise RuntimeError("Repository not found. Check the URL — private repos are not supported.")
    if r.status_code == 403 and r.headers.get("X-RateLimit-Remaining") == "0":
        reset = datetime.fromtimestamp(int(r.headers.get("X-RateLimit-Reset", 0)))
        raise RuntimeError(
            f"GitHub API rate limit exceeded. Resets at {reset:%Y-%m-%d %H:%M:%S}. "
            "Add a GITHUB_TOKEN to .env to raise the limit from 60 to 5000 req/hour."
        )
    r.raise_for_status()
    return r


def fetch_repository(url: str) -> dict:
    """Return {"meta": {...}, "readme": str, "files": [{"path", "content"}, ...]}."""
    owner, repo = parse_repo_url(url)

    meta_raw = _get(f"{API}/repos/{owner}/{repo}").json()
    meta = {
        "full_name": meta_raw.get("full_name", f"{owner}/{repo}"),
        "description": meta_raw.get("description") or "",
        "language": meta_raw.get("language") or "",
        "stars": meta_raw.get("stargazers_count", 0),
        "topics": meta_raw.get("topics", []),
        "default_branch": meta_raw.get("default_branch", "main"),
        "html_url": meta_raw.get("html_url", url),
    }

    # README (best-effort)
    readme = ""
    try:
        rd = _get(f"{API}/repos/{owner}/{repo}/readme").json()
        readme = base64.b64decode(rd.get("content", "")).decode("utf-8", errors="replace")
    except Exception:
        pass

    # Full tree → filter → cap at MAX_REPO_FILES
    tree = _get(
        f"{API}/repos/{owner}/{repo}/git/trees/{meta['default_branch']}?recursive=1"
    ).json().get("tree", [])

    candidates = [
        t for t in tree
        if t.get("type") == "blob"
        and any(t["path"].endswith(e) for e in CODE_EXT)
        and not any(s in t["path"] for s in SKIP_PARTS)
        and t.get("size", 0) <= MAX_FILE_BYTES
    ]
    candidates.sort(key=lambda t: (t["path"].count("/"), t["path"]))
    candidates = candidates[:MAX_REPO_FILES]

    files: list[dict] = []
    for t in candidates:
        try:
            item = _get(f"{API}/repos/{owner}/{repo}/contents/{t['path']}").json()
            content = base64.b64decode(item.get("content", "")).decode("utf-8", errors="replace")
            if content.strip():
                files.append({"path": t["path"], "content": content})
        except Exception:
            continue  # skip unreadable/binary files

    if not files and not readme:
        raise RuntimeError("Could not read any files from this repository.")

    return {"meta": meta, "readme": readme, "files": files}
