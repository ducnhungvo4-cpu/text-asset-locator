import re
from fuzzywuzzy import fuzz


def find_exact_matches(text, keyword, case_sensitive=True):
    """精确匹配关键词"""
    matches = []
    if case_sensitive:
        pattern = re.escape(keyword)
        for match in re.finditer(pattern, text):
            matches.append({
                'start': match.start(),
                'end': match.end(),
                'keyword': keyword,
                'type': 'exact'
            })
    else:
        pattern = re.escape(keyword)
        for match in re.finditer(pattern, text, re.IGNORECASE):
            matches.append({
                'start': match.start(),
                'end': match.end(),
                'keyword': keyword,
                'type': 'exact'
            })
    return matches


def find_fuzzy_matches(text, keyword, threshold=80, case_sensitive=True):
    """模糊匹配关键词"""
    matches = []
    words = text.split()
    keyword_len = len(keyword)
    
    for i, word in enumerate(words):
        if case_sensitive:
            similarity = fuzz.ratio(keyword, word)
        else:
            similarity = fuzz.ratio(keyword.lower(), word.lower())
        
        if similarity >= threshold:
            # 找到该词在原文中的位置
            start_pos = text.find(word)
            while start_pos != -1:
                # 检查是否是独立单词
                prev_char = text[start_pos - 1] if start_pos > 0 else ' '
                next_char = text[start_pos + len(word)] if start_pos + len(word) < len(text) else ' '
                if not prev_char.isalnum() and not next_char.isalnum():
                    matches.append({
                        'start': start_pos,
                        'end': start_pos + len(word),
                        'keyword': keyword,
                        'type': 'fuzzy',
                        'similarity': similarity
                    })
                    break
                start_pos = text.find(word, start_pos + 1)
    
    return matches


def search_keywords(text, keywords, case_sensitive=True, use_fuzzy=False, fuzzy_threshold=80):
    """搜索多个关键词"""
    all_matches = []
    keyword_counts = {}
    
    for keyword in keywords:
        if not keyword or keyword.strip() == '':
            continue
            
        keyword = keyword.strip()
        # 精确匹配
        exact_matches = find_exact_matches(text, keyword, case_sensitive)
        all_matches.extend(exact_matches)
        
        # 模糊匹配（如果开启）
        new_fuzzy_matches = []
        if use_fuzzy:
            fuzzy_matches = find_fuzzy_matches(text, keyword, fuzzy_threshold, case_sensitive)
            # 去重：模糊匹配不与精确匹配重叠
            exact_positions = {(m['start'], m['end']) for m in exact_matches}
            new_fuzzy_matches = [
                m for m in fuzzy_matches 
                if (m['start'], m['end']) not in exact_positions
            ]
            all_matches.extend(new_fuzzy_matches)
        
        # 统计关键词出现次数
        keyword_counts[keyword] = len(exact_matches) + len(new_fuzzy_matches)
    
    # 按位置排序
    all_matches.sort(key=lambda x: x['start'])
    
    return all_matches, keyword_counts


def highlight_text(text, matches, chunk_size=1000):
    """生成带高亮标记的文本，支持分段处理"""
    if not matches:
        return text
    
    # 按位置排序
    matches.sort(key=lambda x: x['start'])
    
    result = []
    last_end = 0
    
    # 处理长文本时添加换行符，提高可读性
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i+chunk_size]
        result.append(chunk)
        if i + chunk_size < len(text):
            result.append('<br><br>')
    
    text_with_breaks = ''.join(result)
    
    # 重新计算匹配位置（考虑添加的换行符）
    adjusted_matches = []
    break_count = 0
    for match in matches:
        # 计算该位置前添加的换行符数量
        break_count = sum(1 for i in range(0, match['start'], chunk_size) if i > 0)
        adjusted_start = match['start'] + break_count * 8  # <br><br> 占8个字符
        adjusted_end = match['end'] + break_count * 8
        adjusted_matches.append({
            **match,
            'start': adjusted_start,
            'end': adjusted_end
        })
    
    # 重新生成高亮文本
    final_result = []
    last_end = 0
    
    for match in adjusted_matches:
        # 添加匹配前的文本
        final_result.append(text_with_breaks[last_end:match['start']])
        
        # 添加带高亮的匹配文本
        matched_text = text_with_breaks[match['start']:match['end']]
        highlight_class = 'highlight-exact' if match['type'] == 'exact' else 'highlight-fuzzy'
        final_result.append(f'<span class="{highlight_class}">{matched_text}</span>')
        
        last_end = match['end']
    
    # 添加最后一段文本
    final_result.append(text_with_breaks[last_end:])
    
    return ''.join(final_result)


def get_unique_keywords(matches):
    """从匹配结果中获取唯一关键词"""
    keywords = set()
    for match in matches:
        keywords.add(match['keyword'])
    return list(keywords)