from astrbot.api.star import Startools
from .markdown_to_html import convert_markdown_to_html
from .render_and_screenshot import render_and_screenshot
from astrbot import logger

def m2ipy(md_text):
    
    # 转换为 HTML
    html_content = convert_markdown_to_html(md_text)
    logger.info("转化成html成功")
    # 渲染并截图
    output_path = StarTools.get_data_dir('output.png')
    render_and_screenshot(html_content,output_path)

    logger.info("截图成功")
    return output_path
