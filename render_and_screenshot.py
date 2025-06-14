from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tempfile
import os

def render_and_screenshot(html_content, output_image_path):
    # 创建临时 HTML 文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as tmpfile:
        tmpfile.write(html_content)
        tmpfile_path = tmpfile.name
        
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # 使用新版无头模式
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=775,2000")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--lang=zh-CN")
    chrome_options.add_argument("Accept-Language=zh-CN,zh;q=0.9")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"file://{tmpfile_path}")
    
    try:
        # 删除旧截图
        if os.path.exists(output_image_path):
            os.remove(output_image_path)
    
        # 等待页面加载（body存在）
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    
        # 等待 MathJax 渲染完成（更可靠的条件）
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return MathJax?.hub?.queue?.length === 0") or
            EC.presence_of_element_located((By.CSS_SELECTOR, ".MathJax"))
        )
    
        # 获取页面总高度
        fixed_width = 1150
        total_height = driver.execute_script("return document.body.scrollHeight")
    
        # 设置高清视口（关键参数调整）
        driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {
            'width': fixed_width,
            'height': total_height,
            'deviceScaleFactor': 2,  # 2x 分辨率（注释中的3x是笔误）
            'mobile': False,
        })
    
        # 截图并保存
        driver.save_screenshot(output_image_path)
        
    except Exception as e:
        print(f"错误：{str(e)}，可能MathJax未加载完成")
    finally:
        driver.quit()
        os.unlink(tmpfile_path)
        
