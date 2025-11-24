import asyncio
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

    # 在线程池中运行阻塞的 Selenium 操作，避免阻塞事件循环
    await asyncio.to_thread(render_and_screenshot, html_content, output_path)

    logger.info("截图成功")
    return output_path
