"""直接執行即可：python3 .github/scripts/test_review.py（不需要 pytest）"""
from review import extract_text, truncate_diff

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

print("全部通過")
