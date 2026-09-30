"""PR 開啟或推 commit 時，把新增的 diff 送給 Gemini 並印出 review 結果。

只用標準函式庫，不需要安裝任何套件。
"""

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
)

PROMPT = """你是資深全端工程師，請用繁體中文 review 下面這份 git diff。只列出可行動的問題，並標明檔案與行；沒有問題就回答「Review 完畢，沒有發現問題」。"""


def truncate_diff(diff: str, max_bytes: int) -> tuple[str, bool]:
    raw = diff.encode("utf-8")

    if len(raw) <= max_bytes:
        return diff, False

    return raw[:max_bytes].decode("utf-8", errors="ignore"), True


def extract_text(res: dict) -> str:
    return res["candidates"][0]["content"]["parts"][0]["text"]


def call_review_agent(prompt: str, api_key: str, model: str) -> str:
    body = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
    request = urllib.request.Request(
        GEMINI_URL.format(model=model),
        data=body,
        headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return extract_text(json.load(response))


def main() -> int:
    if os.environ["IS_FORK"] == "true":
        print("fork 的 PR 拿不到 Secrets，略過審查")
        return 0

    base, head = os.environ["BASE"], os.environ["HEAD"]
    max_bytes = int(os.environ.get("MAX_DIFF_BYTES", "100000"))
    print(f"審查範圍: {base}...{head}")

    diff = subprocess.run(
        ["git", "diff", f"{base}...{head}"],
        capture_output=True, text=True, check=True,
    ).stdout
    if not diff.strip():
        print("沒有新增的 diff，略過審查")
        return 0

    diff, truncated = truncate_diff(diff, max_bytes)
    if truncated:
        print(f"diff 超過 {max_bytes} bytes，已截斷")
        diff += "\n\n（diff 已截斷）"

    prompt = f"{PROMPT}\n\n{diff}"
    try:
        review = call_review_agent(prompt, os.environ["GEMINI_API_KEY"], os.environ["GEMINI_MODEL"])
    except urllib.error.HTTPError as error:
        if error.code == 429:
            print("Gemini 額度用完（429），這次略過審查")
            return 0
        raise

    print("===== Gemini review =====")
    print(review)
    return 0


if __name__ == "__main__":
    sys.exit(main())