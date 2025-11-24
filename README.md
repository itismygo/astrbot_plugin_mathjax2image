# Mathjax2image

/mj2i 调用llm来生成支持mathjax的文章，并渲染为图片


/m2i 将带有数学公式的输入转化为输出（最后输出的都是和数学相关的）


/wz 调用llm生成文章（输出不一定是和数学相关的，不支持mathjax）

推荐使用deepseekv3_0324模型

## 安装说明

### 1. 安装依赖
```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. MathJax 自动安装 ✨

**插件会在首次加载时自动下载 MathJax 离线包，无需手动操作！**

- 首次启动时会自动检测 MathJax 是否存在
- 如果不存在会自动从 CDN 下载（约 1.1MB）
- 下载完成后即可正常使用

如果自动下载失败，可以手动运行：
```bash
python install_mathjax.py
```

或手动下载：
1. 下载 https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js
2. 保存到 `static/mathjax/tex-chtml.js`

### 3. 启动使用
安装依赖后直接使用即可，MathJax 会自动安装。

## 特性

- ✅ **自动安装** - 首次使用自动下载 MathJax
- ✅ **完全离线** - 无需访问外部 CDN
- ✅ **零配置** - 开箱即用
- ✅ 自动处理 MathJax 渲染
- ✅ 支持 Markdown 和数学公式
- ✅ 自动管理浏览器驱动

# 支持

[帮助文档](https://astrbot.app)
