# 文本资产快速定位与高亮工具

一个基于 Python + Streamlit 开发的文本资产快速定位与高亮工具，用于在文稿中快速定位和标记资产关键词。

## 功能特点

- **多格式支持**：支持 .txt、.docx 文稿格式，.xlsx、.csv 资产列表格式
- **精确匹配**：精确查找关键词在文稿中的位置
- **模糊匹配**：支持相似度 ≥ 80% 的模糊匹配
- **大小写控制**：可选择是否区分大小写
- **高亮显示**：匹配关键词自动高亮，不同类型使用不同颜色
- **快速导航**：点击资产列表自动定位，支持上一个/下一个导航
- **性能优化**：长文本分段加载，流畅不卡顿

## 在线使用

访问：[在线演示地址]（部署后填写）

## 本地运行

### 1. 克隆仓库

```bash
git clone https://github.com/你的用户名/text-asset-locator.git
cd text-asset-locator
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行应用

```bash
streamlit run app.py
```

## 使用说明

1. **上传文稿**：上传 .txt 或 .docx 格式的文稿文件
2. **上传资产列表**：上传 .xlsx 或 .csv 格式的资产列表
3. **选择关键词列**：从资产列表中选择包含关键词的列
4. **设置搜索参数**：
   - 大小写敏感：是否区分大小写
   - 模糊匹配：是否启用模糊匹配
   - 模糊阈值：设置模糊匹配的相似度阈值
5. **开始搜索**：点击"开始搜索"按钮
6. **查看结果**：
   - 左侧：原文高亮显示
   - 右侧：资产列表及出现次数
7. **导航定位**：
   - 点击资产列表项定位到对应位置
   - 使用"上一个/下一个"按钮导航

## 技术栈

- **前端框架**：Streamlit
- **数据处理**：Pandas
- **文档处理**：python-docx
- **模糊匹配**：fuzzywuzzy

## 项目结构

```
text-asset-locator/
├── app.py                 # 主应用文件
├── requirements.txt       # Python依赖
├── packages.txt          # 系统依赖
├── .streamlit/
│   └── config.toml       # Streamlit配置
└── utils/
    ├── file_reader.py    # 文件读取模块
    └── search_engine.py  # 搜索引擎模块
```

## 许可证

MIT License