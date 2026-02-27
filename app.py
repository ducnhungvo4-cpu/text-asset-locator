import streamlit as st
import pandas as pd
import os
from utils.file_reader import read_file
from utils.search_engine import search_keywords, highlight_text

# 设置页面配置
st.set_page_config(page_title="文本资产快速定位与高亮工具", layout="wide")

# 自定义CSS样式
st.markdown("""
<style>
    .highlight-exact {
        background-color: yellow;
        font-weight: bold;
    }
    .highlight-fuzzy {
        background-color: orange;
        font-weight: bold;
    }
    .asset-item {
        cursor: pointer;
        padding: 8px;
        border-radius: 4px;
        margin-bottom: 4px;
    }
    .asset-item:hover {
        background-color: #f0f0f0;
    }
    .asset-item.selected {
        background-color: #e0f7fa;
    }
    .text-container {
        height: 700px;
        overflow-y: auto;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 4px;
    }
    .asset-container {
        height: 700px;
        overflow-y: auto;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 4px;
    }
    .nav-buttons {
        display: flex;
        gap: 10px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 应用标题
st.title("文本资产快速定位与高亮工具")

# 初始化会话状态
if 'text_content' not in st.session_state:
    st.session_state.text_content = ""
if 'df_assets' not in st.session_state:
    st.session_state.df_assets = None
if 'matches' not in st.session_state:
    st.session_state.matches = []
if 'keyword_counts' not in st.session_state:
    st.session_state.keyword_counts = {}
if 'selected_keyword' not in st.session_state:
    st.session_state.selected_keyword = None
if 'current_match_index' not in st.session_state:
    st.session_state.current_match_index = 0
if 'highlighted_text' not in st.session_state:
    st.session_state.highlighted_text = ""

# 文件上传区
col1, col2 = st.columns(2)

with col1:
    st.subheader("上传文稿")
    text_file = st.file_uploader("支持 .txt 或 .docx 格式", type=["txt", "docx"], key="text_uploader")

with col2:
    st.subheader("上传资产列表")
    asset_file = st.file_uploader("支持 .xlsx 或 .csv 格式", type=["xlsx", "csv"], key="asset_uploader")

# 处理文件上传
if text_file is not None:
    # 保存临时文件
    text_file_path = f"temp_{text_file.name}"
    with open(text_file_path, "wb") as f:
        f.write(text_file.getbuffer())
    
    try:
        # 读取文件内容
        st.session_state.text_content = read_file(text_file_path)
        st.success("文稿读取成功！")
    except Exception as e:
        st.error(f"读取文稿失败: {e}")
    finally:
        # 删除临时文件
        if os.path.exists(text_file_path):
            os.remove(text_file_path)

if asset_file is not None:
    # 保存临时文件
    asset_file_path = f"temp_{asset_file.name}"
    with open(asset_file_path, "wb") as f:
        f.write(asset_file.getbuffer())
    
    try:
        # 读取文件内容
        st.session_state.df_assets = read_file(asset_file_path)
        st.success("资产列表读取成功！")
    except Exception as e:
        st.error(f"读取资产列表失败: {e}")
    finally:
        # 删除临时文件
        if os.path.exists(asset_file_path):
            os.remove(asset_file_path)

# 搜索参数设置
if st.session_state.df_assets is not None:
    st.subheader("搜索参数设置")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # 选择关键词列
        keyword_columns = st.multiselect(
            "选择关键词列",
            options=st.session_state.df_assets.columns.tolist(),
            key="keyword_columns"
        )
    
    with col2:
        # 大小写敏感开关
        case_sensitive = st.checkbox("大小写敏感", value=False, key="case_sensitive")
    
    with col3:
        # 模糊匹配开关
        use_fuzzy = st.checkbox("启用模糊匹配", value=False, key="use_fuzzy")
    
    with col4:
        # 模糊匹配阈值
        if use_fuzzy:
            fuzzy_threshold = st.slider("模糊匹配阈值", min_value=50, max_value=100, value=80, key="fuzzy_threshold")
        else:
            fuzzy_threshold = 80
    
    # 搜索按钮
    if st.button("开始搜索", key="search_button"):
        if not keyword_columns:
            st.error("请选择至少一个关键词列")
        elif not st.session_state.text_content:
            st.error("请先上传文稿")
        else:
            with st.spinner("搜索中..."):
                # 提取关键词
                keywords = []
                for col in keyword_columns:
                    keywords.extend(st.session_state.df_assets[col].dropna().astype(str).tolist())
                
                # 去重
                keywords = list(set(keywords))
                
                # 搜索关键词
                matches, keyword_counts = search_keywords(
                    st.session_state.text_content,
                    keywords,
                    case_sensitive=case_sensitive,
                    use_fuzzy=use_fuzzy,
                    fuzzy_threshold=fuzzy_threshold
                )
                
                # 更新会话状态
                st.session_state.matches = matches
                st.session_state.keyword_counts = keyword_counts
                st.session_state.selected_keyword = None
                st.session_state.current_match_index = 0
                
                # 生成高亮文本
                st.session_state.highlighted_text = highlight_text(st.session_state.text_content, matches)
                
                st.success(f"搜索完成！找到 {len(matches)} 个匹配项")

# 结果展示区
if st.session_state.highlighted_text:
    st.subheader("搜索结果")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 原文（高亮显示）")
        
        # 文本容器
        text_container = st.container()
        with text_container:
            st.markdown(f'<div class="text-container">{st.session_state.highlighted_text}</div>', unsafe_allow_html=True)
        
        # 导航按钮
        with st.container():
            st.markdown("### 导航")
            nav_col1, nav_col2, nav_col3 = st.columns(3)
            
            with nav_col1:
                if st.button("上一个", key="prev_button"):
                    if st.session_state.current_match_index > 0:
                        st.session_state.current_match_index -= 1
            
            with nav_col2:
                if st.session_state.matches:
                    st.write(f"匹配项 {st.session_state.current_match_index + 1} / {len(st.session_state.matches)}")
            
            with nav_col3:
                if st.button("下一个", key="next_button"):
                    if st.session_state.current_match_index < len(st.session_state.matches) - 1:
                        st.session_state.current_match_index += 1
    
    with col2:
        st.markdown("### 资产列表")
        
        # 生成资产列表
        asset_list = []
        for keyword, count in st.session_state.keyword_counts.items():
            if count > 0:
                asset_list.append((keyword, count))
        
        # 按出现次数排序
        asset_list.sort(key=lambda x: x[1], reverse=True)
        
        # 显示资产列表
        asset_container = st.container()
        with asset_container:
            st.markdown('<div class="asset-container">', unsafe_allow_html=True)
            
            for i, (keyword, count) in enumerate(asset_list):
                # 检查是否为选中状态
                is_selected = keyword == st.session_state.selected_keyword
                
                # 创建资产项
                asset_html = f'<div class="asset-item {"selected" if is_selected else ""}" onclick="Streamlit.setComponentValue(\"selected_asset\", \"{keyword}\")">'
                asset_html += f'<strong>{keyword}</strong> (出现次数: {count})'
                asset_html += '</div>'
                
                st.markdown(asset_html, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 处理资产选择
        selected_asset = st.text_input("selected_asset", value="", key="selected_asset", label_visibility="hidden")
        
        if selected_asset and selected_asset != st.session_state.selected_keyword:
            st.session_state.selected_keyword = selected_asset
            
            # 找到该关键词的第一个匹配项
            for i, match in enumerate(st.session_state.matches):
                if match['keyword'] == selected_asset:
                    st.session_state.current_match_index = i
                    break

# 重置按钮
if st.button("重置", key="reset_button"):
    st.session_state.text_content = ""
    st.session_state.df_assets = None
    st.session_state.matches = []
    st.session_state.keyword_counts = {}
    st.session_state.selected_keyword = None
    st.session_state.current_match_index = 0
    st.session_state.highlighted_text = ""
    st.experimental_rerun()