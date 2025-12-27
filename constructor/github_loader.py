import base64
import requests
from urllib.parse import urlparse


def parse_repo(url: str):
    url = url.rstrip("/")
    if url.endswith(".git"):
        url = url[:-4]
    p = urlparse(url)
    if p.netloc != "github.com":
        return None, None
    parts = [x for x in p.path.split("/") if x]
    if len(parts) < 2:
        return None, None
    return parts[0], parts[1]


def fetch_repo(owner: str, repo: str, max_files: int = 10):
    headers = {"Accept": "application/vnd.github.v3+json"}
    api = f"https://api.github.com/repos/{owner}/{repo}"
    r = requests.get(api, headers=headers, timeout=10)
    r.raise_for_status()
    meta = r.json()

    readme = ""
    r = requests.get(f"{api}/readme", headers=headers, timeout=10)
    if r.status_code == 200:
        readme = base64.b64decode(r.json().get("content", "")).decode("utf-8", "ignore")

    tree = requests.get(
        f"{api}/git/trees/{meta.get('default_branch','main')}?recursive=1",
        headers=headers,
        timeout=15,
    ).json()

    files = []
    for item in tree.get("tree", []):
        if len(files) >= max_files:
            break
        if item.get("type") == "blob" and item.get("size", 0) <= 200_000:
            files.append(item["path"])

    contents = []
    for path in files:
        r = requests.get(f"{api}/contents/{path}", headers=headers, timeout=10)
        if r.status_code == 200 and "content" in r.json():
            try:
                text = base64.b64decode(r.json()["content"]).decode("utf-8", "ignore")
                contents.append({"path": path, "content": text})
            except Exception:
                pass

    return {
        "name": meta.get("name"),
        "description": meta.get("description"),
        "languages": requests.get(f"{api}/languages", headers=headers).json(),
        "readme": readme,
        "files": contents,
    }
