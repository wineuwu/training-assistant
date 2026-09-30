"""直接執行即可：python3 .github/scripts/test_review.py（不需要 pytest）"""
from review import BOT_LOGIN, extract_text, find_last_sha, truncate_diff

# 沒超過上限：原樣回傳
assert truncate_diff("abc", 10) == ("abc", False)

# 超過上限：被截斷，且長度不超過上限
text, truncated = truncate_diff("abcdef", 3)
assert truncated and text == "abc"

# 中文一字 3 bytes，切在字中間時不能留下亂碼
text, truncated = truncate_diff("你好", 4)
assert truncated and text == "你"

# 取出 Gemini 回應裡的文字
response = {"candidates": [{"content": {"parts": [{"text": "ok"}]}}]}
assert extract_text(response) == "ok"

A, B, FAKE = "a" * 40, "b" * 40, "f" * 40


def comment(login: str, sha: str) -> dict:
    return {"login": login, "body": f"review\n<!-- ai-review:sha={sha} -->"}


# 沒有任何留言：回 None
assert find_last_sha([]) is None

# 只有一般留言、沒有標記：回 None
assert find_last_sha([{"login": BOT_LOGIN, "body": "hello"}]) is None

# 取最新一則 bot 留言的標記
assert find_last_sha([comment(BOT_LOGIN, A), comment(BOT_LOGIN, B)]) == B

# 別人貼的假標記不能信，即使它是最新的
assert find_last_sha([comment(BOT_LOGIN, A), comment("someone", FAKE)]) == A

print("全部通過")
