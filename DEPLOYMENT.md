# 部署指南 - Streamlit Cloud

本指南将帮助你将文本资产快速定位与高亮工具部署到 Streamlit Cloud，让其他人也能在线使用。

## 前提条件

- 一个 GitHub 账号（如果没有，请先注册：https://github.com）
- 项目代码已准备好

## 部署步骤

### 第一步：创建 GitHub 仓库

1. 登录 GitHub：https://github.com
2. 点击右上角的 "+" 按钮，选择 "New repository"
3. 填写仓库信息：
   - Repository name: `text-asset-locator`（或其他你喜欢的名字）
   - Description: 文本资产快速定位与高亮工具
   - 选择 "Public"（公开仓库）
   - 勾选 "Add a README file"
4. 点击 "Create repository" 创建仓库

### 第二步：上传代码到 GitHub

#### 方法一：使用 Git 命令行（推荐）

1. 在项目目录打开终端
2. 初始化 Git 仓库：
   ```bash
   git init
   git add .
   git commit -m "Initial commit: 文本资产快速定位与高亮工具"
   ```

3. 关联远程仓库：
   ```bash
   git remote add origin https://github.com/你的用户名/text-asset-locator.git
   git branch -M main
   git push -u origin main
   ```

#### 方法二：使用 GitHub Desktop

1. 下载并安装 GitHub Desktop：https://desktop.github.com
2. 打开 GitHub Desktop，登录你的 GitHub 账号
3. File → Add local repository → 选择项目目录
4. 点击 "Publish repository" 上传到 GitHub

#### 方法三：网页上传

1. 在 GitHub 仓库页面点击 "uploading an existing file"
2. 将项目文件拖拽到上传区域
3. 填写 commit 信息，点击 "Commit changes"

### 第三步：部署到 Streamlit Cloud

1. 访问 Streamlit Cloud：https://streamlit.io/cloud
2. 点击 "Sign up" 或 "Log in"（可以使用 GitHub 账号登录）
3. 登录后，点击 "New app"
4. 填写部署信息：
   - Repository: 选择你的 GitHub 仓库 `text-asset-locator`
   - Branch: `main`
   - Main file path: `app.py`
   - App URL (可选): 自定义应用名称
5. 点击 "Deploy!" 开始部署
6. 等待几分钟，部署完成后会自动打开应用页面

### 第四步：分享应用

部署成功后，你会获得一个类似这样的网址：
```
https://你的应用名称.streamlit.app
```

你可以：
- 直接分享这个链接给其他人使用
- 在 README.md 中添加这个链接
- 嵌入到网站或文档中

## 常见问题

### Q: 部署失败怎么办？

A: 检查以下几点：
1. `requirements.txt` 文件是否正确
2. 所有依赖包是否都已列出
3. 查看 Streamlit Cloud 的日志信息

### Q: 应用运行缓慢？

A: 可能的原因：
1. Streamlit Cloud 免费版资源有限
2. 处理大文件时需要更多时间
3. 建议文件大小不超过 10MB

### Q: 如何更新应用？

A: 
1. 修改代码后提交到 GitHub
2. Streamlit Cloud 会自动检测并重新部署
3. 或者在 Streamlit Cloud 控制台点击 "Reboot"

### Q: 如何查看应用日志？

A: 
1. 登录 Streamlit Cloud
2. 进入你的应用
3. 点击右下角的 "Manage app"
4. 选择 "Logs" 查看运行日志

## 其他部署选项

除了 Streamlit Cloud，你还可以考虑：

### 1. Heroku
- 支持更多自定义配置
- 有免费额度（有限制）

### 2. Railway
- 简单易用
- 提供免费额度

### 3. 自己的服务器
- 完全控制
- 需要自己维护

## 需要帮助？

如果遇到问题，可以：
1. 查看 Streamlit 官方文档：https://docs.streamlit.io
2. 在 GitHub 上提问
3. 查看 Streamlit 社区论坛：https://discuss.streamlit.io