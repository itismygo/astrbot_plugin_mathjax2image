from playwright.async_api import async_playwright
import tempfile
import os
from astrbot import logger

async def render_and_screenshot(html_content, output_image_path):
    """使用 Playwright 渲染 HTML 并截图（异步版本）"""

    # 创建临时 HTML 文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as tmpfile:
        tmpfile.write(html_content)
        tmpfile_path = tmpfile.name

    try:
        logger.info("正在启动 Playwright 浏览器...")

        async with async_playwright() as p:
            # 启动 Chromium 浏览器（Playwright 自带，无需额外安装）
            browser = await p.chromium.launch(headless=True)
            logger.info("浏览器启动成功")

            page = await browser.new_page(viewport={'width': 1150, 'height': 2000})

            # 加载页面（使用 domcontentloaded 避免等待外部 CDN 超时）
            await page.goto(f"file://{tmpfile_path}", wait_until='domcontentloaded', timeout=60000)
            logger.info("页面加载完成")

            # 等待 MathJax 加载和渲染完成
            try:
                # 先等待 MathJax 脚本加载（最多 30 秒）
                await page.wait_for_function("""
                    () => typeof MathJax !== 'undefined' && MathJax.startup
                """, timeout=30000)
                logger.info("MathJax 脚本已加载")

                # 等待 MathJax 渲染完成
                await page.wait_for_function("""
                    () => {
                        if (MathJax.startup && MathJax.startup.promise) {
                            return MathJax.startup.promise.then(() => true).catch(() => true);
                        }
                        return true;
                    }
                """, timeout=15000)
                # 额外等待确保渲染完成
                await page.wait_for_timeout(1000)
                logger.info("MathJax 渲染完成")
            except Exception as e:
                logger.warning(f"MathJax 等待超时或加载失败，继续截图: {e}")

            # 删除旧截图
            if os.path.exists(output_image_path):
                os.remove(output_image_path)

            # 获取页面高度并截图
            height = await page.evaluate("document.body.scrollHeight")
            await page.set_viewport_size({'width': 1150, 'height': height})

            # 截图
            await page.screenshot(path=str(output_image_path), full_page=True, scale='device')
            logger.info(f"截图已保存到: {output_image_path}")

            await browser.close()

    except Exception as e:
        logger.error(f"render_and_screenshot 错误: {e}")
        raise

    finally:
        if os.path.exists(tmpfile_path):
            os.unlink(tmpfile_path)
