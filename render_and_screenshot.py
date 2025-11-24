from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import tempfile
import os
from astrbot import logger

def render_and_screenshot(html_content, output_image_path):
    # 创建临时 HTML 文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as tmpfile:
        tmpfile.write(html_content)
        tmpfile_path = tmpfile.name

    driver = None
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  # 使用新版无头模式
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=775,2000")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--lang=zh-CN")
        chrome_options.add_argument("Accept-Language=zh-CN,zh;q=0.9")

        logger.info("正在启动 Chrome 浏览器...")
        # 使用 webdriver-manager 自动下载和管理 ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        logger.info("Chrome 浏览器启动成功")

        driver.get(f"file://{tmpfile_path}")
        logger.info("页面加载完成")

        # 删除旧截图
        if os.path.exists(output_image_path):
            os.remove(output_image_path)

        # 等待页面加载（body存在）
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # 等待 MathJax 渲染完成
        def mathjax_loaded(d):
            try:
                # 检查 MathJax 是否存在并完成渲染
                result = d.execute_script("""
                    if (typeof MathJax === 'undefined') return true;  // 没有 MathJax，直接通过
                    if (MathJax.Hub && MathJax.Hub.queue) {
                        return MathJax.Hub.queue.pending === 0;
                    }
                    if (MathJax.startup && MathJax.startup.promise) {
                        return true;  // MathJax 3.x
                    }
                    return true;
                """)
                return result
            except Exception:
                return True  # 出错就跳过等待

        WebDriverWait(driver, 15).until(mathjax_loaded)
        logger.info("MathJax 渲染完成")

        # 获取页面总高度
        fixed_width = 1150
        total_height = driver.execute_script("return document.body.scrollHeight")

        # 设置高清视口
        driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {
            'width': fixed_width,
            'height': total_height,
            'deviceScaleFactor': 2,
            'mobile': False,
        })

        # 截图并保存
        driver.save_screenshot(str(output_image_path))
        logger.info(f"截图已保存到: {output_image_path}")

    except Exception as e:
        logger.error(f"render_and_screenshot 错误: {e}")
        raise  # 重新抛出异常，让调用者知道失败了

    finally:
        if driver:
            driver.quit()
        if os.path.exists(tmpfile_path):
            os.unlink(tmpfile_path)
