from utils.file_reader import read_file
from utils.search_engine import search_keywords, highlight_text

# 创建测试数据
TEST_TEXT = """
这是一个测试文本，包含一些关键词。
比如Python、Streamlit、文本检索等。
Python是一种流行的编程语言，Streamlit是一个用于构建数据应用的框架。
文本检索是我们工具的核心功能。
"""

TEST_KEYWORDS = ["Python", "Streamlit", "文本检索", "测试"]

print("=== 测试核心功能 ===")

# 测试精确匹配
print("\n1. 测试精确匹配：")
matches, counts = search_keywords(TEST_TEXT, TEST_KEYWORDS, case_sensitive=False)
print(f"找到 {len(matches)} 个匹配项")
for i, match in enumerate(matches):
    print(f"  {i+1}. 位置 {match['start']}-{match['end']}: {match['keyword']} ({match['type']})")
print("出现次数：", counts)

# 测试高亮文本
highlighted = highlight_text(TEST_TEXT, matches)
print("\n2. 测试高亮文本：")
print(highlighted)

# 测试大小写敏感
print("\n3. 测试大小写敏感：")
matches_case, counts_case = search_keywords(TEST_TEXT, ["python"], case_sensitive=True)
print(f"大小写敏感 - 找到 {len(matches_case)} 个匹配项")

matches_no_case, counts_no_case = search_keywords(TEST_TEXT, ["python"], case_sensitive=False)
print(f"大小写不敏感 - 找到 {len(matches_no_case)} 个匹配项")

# 测试模糊匹配
print("\n4. 测试模糊匹配：")
matches_fuzzy, counts_fuzzy = search_keywords(TEST_TEXT, ["Pyton"], use_fuzzy=True, fuzzy_threshold=80)
print(f"模糊匹配 - 找到 {len(matches_fuzzy)} 个匹配项")
for match in matches_fuzzy:
    print(f"  位置 {match['start']}-{match['end']}: {match['keyword']} ({match['type']}, 相似度: {match['similarity']})")

print("\n=== 测试完成 ===")