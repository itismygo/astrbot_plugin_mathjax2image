
from .markdown_to_html import convert_markdown_to_html
from .render_and_screenshot import render_and_screenshot
from astrbot import logger

def m2ipy(md_text):
    
    # 转换为 HTML
    html_content = convert_markdown_to_html(md_text)
    logger.info("转化成html成功")
    # 渲染并截图
    
    render_and_screenshot(html_content,'output.png')
    logger.info("截图成功")


if __name__ == "__main__":
    # 读取 Markdown 文件
    with open("input.md", "r") as f:
        md_text = f.read()
    html_content = convert_markdown_to_html(md_text)

    # 渲染并截图
    render_and_screenshot(html_content, "test.png")
