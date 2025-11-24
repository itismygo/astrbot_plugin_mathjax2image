from astrbot.api.star import StarTools
from .markdown_to_html import convert_markdown_to_html
from .render_and_screenshot import render_and_screenshot
from astrbot import logger

async def m2ipy(md_text):

    # 转换为 HTML
    html_content = convert_markdown_to_html(md_text)
    logger.info("转化成html成功")
    # 渲染并截图
    output_dir = StarTools.get_data_dir('astrbot_plugin_mathjax2image')
    output_path = output_dir / "output.png"

    # Playwright 原生异步，直接 await
    await render_and_screenshot(html_content, output_path)

    logger.info("截图成功")
    return output_path
