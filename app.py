import streamlit as st
import pandas as pd
import os
from utils.file_reader import read_file, read_file_from_upload
from utils.search_engine import search_keywords, highlight_text

# 设置页面配置
st.set_page_config(page_title="文本资产快速定位与高亮工具", layout="wide")

# 自定义CSS样式和JavaScript
st.markdown("""
<style>
    /* 基础高亮样式 */
    .highlight-exact {
        background-color: yellow;
        font-weight: bold;
    }
    .highlight-fuzzy {
        background-color: orange;
        font-weight: bold;
    }
    
    /* 点击资产时的高亮为蓝色 */
    .highlight-exact.clicked,
    .highlight-fuzzy.clicked {
        background-color: #2196F3 !important;
        box-shadow: 0 0 0 2px #0d47a1;
        animation: blue-pulse 0.8s ease-in-out;
    }
    @keyframes blue-pulse {
        0% { box-shadow: 0 0 0 0 rgba(33, 150, 243, 0.7); }
        70% { box-shadow: 0 0 0 6px rgba(33, 150, 243, 0); }
        100% { box-shadow: 0 0 0 0 rgba(33, 150, 243, 0); }
    }
    
    /* 左侧文本容器 */
    .text-container {
        height: 700px;
        overflow-y: auto;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 4px;
    }
    
    /* 高亮当前选中的匹配项 */
    .highlight-exact.active,
    .highlight-fuzzy.active {
        box-shadow: 0 0 0 2px blue;
        animation: pulse 1s ease-in-out;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(0, 0, 255, 0.7); }
        70% { box-shadow: 0 0 0 5px rgba(0, 0, 255, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 0, 255, 0); }
    }
    
    /* 重构后的右侧资产列表样式 */
    /* 1. 完整资产容器 - 占满右侧整个区域 */
    .asset-full-container {
        height: 700px;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        border: 1px solid #ddd;
        border-radius: 4px;
        background-color: white;
    }
    
    /* 2. 标题样式 */
    .asset-full-container h3 {
        margin: 0;
        padding: 10px;
        background-color: #f8f9fa;
        border-bottom: 1px solid #ddd;
        font-size: 18px;
        font-weight: 600;
    }
    
    /* 3. 当前高亮信息区域 */
    .current-highlight {
        padding: 15px;
        background-color: #f0f8ff;
        border-bottom: 1px solid #ddd;
        margin: 0;
    }
    
    .current-highlight h4 {
        margin: 0 0 8px 0;
        color: #4682b4;
        font-size: 16px;
    }
    
    .current-highlight p {
        margin: 5px 0;
        font-size: 14px;
    }
    
    /* 4. 资产列表区域 - 核心样式：占满剩余空间，只在内部滚动 */
    .asset-list {
        flex: 1;
        overflow-y: auto;
        overflow-x: hidden;
        padding: 10px;
        word-break: break-word;
        white-space: normal;
    }
    
    /* 5. 资产项样式 */
    .asset-item {
        cursor: pointer;
        padding: 8px;
        border-radius: 4px;
        margin-bottom: 4px;
        word-break: break-word;
        white-space: normal;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        transition: background-color 0.2s ease;
    }
    
    .asset-item:hover {
        background-color: #f0f0f0;
    }
    
    .asset-item.selected {
        background-color: #e0f7fa;
        border-left: 3px solid #4682b4;
    }
    
    /* 6. 确保列布局正确 */
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 50% !important;
    }
    
    /* 7. 移除默认的Streamlit边距 */
    .stMarkdown {
        margin: 0 !important;
        padding: 0 !important;
    }
</style>

<script>
// 滚动到指定锚点并添加绿色高亮效果
function scrollToAnchor(anchorId) {
    setTimeout(function() {
        const element = document.getElementById(anchorId);
        if (element) {
            // 移除之前的所有高亮类
            document.querySelectorAll('.highlight-exact.active, .highlight-fuzzy.active, .highlight-exact.clicked, .highlight-fuzzy.clicked').forEach(el => {
                el.classList.remove('active', 'clicked');
            });
            // 滚动到元素位置，上方留100px边距
            element.scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });
            // 添加clicked类（绿色高亮）
            element.classList.add('clicked');
            // 1秒后移除clicked类，恢复原高亮
            setTimeout(function() {
                element.classList.remove('clicked');
                // 保留active类（蓝色边框）
                element.classList.add('active');
            }, 800);
        }
    }, 100);
}

// 监听URL变化，处理导航
window.addEventListener('hashchange', function() {
    const hash = window.location.hash;
    if (hash.startsWith('#match_')) {
        scrollToAnchor(hash.substring(1));
    }
});

// 页面加载时检查hash
if (window.location.hash.startsWith('#match_')) {
    scrollToAnchor(window.location.hash.substring(1));
}
</script>
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
    try:
        # 直接从上传文件读取内容，无需创建临时文件
        st.session_state.text_content = read_file_from_upload(text_file)
        st.success("文稿读取成功！")
    except Exception as e:
        st.error(f"读取文稿失败: {e}")

if asset_file is not None:
    try:
        # 直接从上传文件读取内容，无需创建临时文件
        st.session_state.df_assets = read_file_from_upload(asset_file)
        st.success("资产列表读取成功！")
    except Exception as e:
        st.error(f"读取资产列表失败: {e}")

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
                if st.button("上一个 ⬆️", key="prev_button"):
                    if st.session_state.current_match_index > 0:
                        st.session_state.current_match_index -= 1
                        st.rerun()
            
            with nav_col2:
                if st.session_state.matches:
                    st.write(f"匹配项 {st.session_state.current_match_index + 1} / {len(st.session_state.matches)}")
            
            with nav_col3:
                if st.button("下一个 ⬇️", key="next_button"):
                    if st.session_state.current_match_index < len(st.session_state.matches) - 1:
                        st.session_state.current_match_index += 1
                        st.rerun()
        
        # 添加JavaScript实现滚动到当前匹配项并触发蓝色高亮
        if st.session_state.matches:
            current_match_id = f"match_{st.session_state.current_match_index}"
            st.markdown(f"""
            <script>
                setTimeout(function() {{
                    var element = document.getElementById('{current_match_id}');
                    if (element) {{
                        // 移除之前的高亮类
                        document.querySelectorAll('.highlight-exact.active, .highlight-fuzzy.active, .highlight-exact.clicked, .highlight-fuzzy.clicked').forEach(function(el) {{
                            el.classList.remove('active', 'clicked');
                        }});
                        // 滚动到位置
                        element.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                        // 添加蓝色高亮
                        element.classList.add('clicked');
                        // 1秒后保留蓝色边框
                        setTimeout(function() {{
                            element.classList.remove('clicked');
                            element.classList.add('active');
                        }}, 1000);
                    }}
                }}, 200);
            </script>
            """, unsafe_allow_html=True)
    
    with col2:
        # 使用Streamlit原生组件展示资产列表
        st.markdown("### 资产列表")
        
        # 提取并排序资产
        asset_list = []
        for keyword, count in st.session_state.keyword_counts.items():
            if count > 0:
                asset_list.append((keyword, count))
        asset_list.sort(key=lambda x: x[1], reverse=True)
        
        # 显示当前高亮资产信息
        if st.session_state.matches and 0 <= st.session_state.current_match_index < len(st.session_state.matches):
            current_match = st.session_state.matches[st.session_state.current_match_index]
            current_keyword = current_match['keyword']
            current_count = st.session_state.keyword_counts.get(current_keyword, 0)
            
            st.info(f"📌 当前高亮：**{current_keyword}** (出现 {current_count} 次)")
        
        # 使用selectbox展示资产列表
        asset_options = [f"{keyword} (出现 {count} 次)" for keyword, count in asset_list]
        
        if asset_options:
            selected_asset = st.selectbox(
                "选择资产查看位置",
                options=asset_options,
                key="asset_selector"
            )
            
            if selected_asset:
                selected_keyword = selected_asset.split(" (出现")[0]
                
                if selected_keyword != st.session_state.selected_keyword:
                    st.session_state.selected_keyword = selected_keyword
                    
                    for i, match in enumerate(st.session_state.matches):
                        if match['keyword'] == selected_keyword:
                            st.session_state.current_match_index = i
                            break
                    
                    st.rerun()
        
        # 在selectbox下方显示可点击的资产列表
        st.markdown("#### 点击资产查看位置")
        for i, (keyword, count) in enumerate(asset_list):
            if st.button(f"📍 {keyword} ({count}次)", key=f"asset_btn_{i}"):
                st.session_state.selected_keyword = keyword
                for j, match in enumerate(st.session_state.matches):
                    if match['keyword'] == keyword:
                        st.session_state.current_match_index = j
                        break
                st.rerun()
        
        # 显示资产统计信息
        st.markdown("---")
        st.markdown(f"**资产总数：** {len(asset_list)}")
        st.markdown(f"**匹配总数：** {sum(count for _, count in asset_list)}")

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