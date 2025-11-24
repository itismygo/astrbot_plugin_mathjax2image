"""
自动下载 MathJax 离线包到插件目录
"""
import urllib.request
import os
from pathlib import Path

def download_mathjax():
    """下载 MathJax 核心文件"""

    # 获取当前脚本目录
    current_dir = Path(__file__).resolve().parent
    mathjax_dir = current_dir / "static" / "mathjax"

    # 创建目录
    mathjax_dir.mkdir(parents=True, exist_ok=True)

    # MathJax 核心文件（单文件版本，包含所有功能）
    mathjax_url = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"
    mathjax_file = mathjax_dir / "tex-chtml.js"

    if mathjax_file.exists():
        print(f"MathJax 已存在: {mathjax_file}")
        return

    print(f"正在下载 MathJax 到 {mathjax_file}...")

    try:
        # 下载文件
        urllib.request.urlretrieve(mathjax_url, mathjax_file)
        print(f"下载成功: {mathjax_file}")
        print(f"文件大小: {mathjax_file.stat().st_size / 1024:.2f} KB")
    except Exception as e:
        print(f"下载失败: {e}")
        print("请手动下载 https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js")
        print(f"并保存到: {mathjax_file}")
        raise

if __name__ == "__main__":
    download_mathjax()
