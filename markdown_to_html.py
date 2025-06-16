import markdown
from pathlib import Path
from astrbot import logger



def convert_markdown_to_html(md_text):
    # 转换 Markdown 为 HTML
    html_body = markdown.markdown(md_text, extensions=['fenced_code', 'tables'])

    # 获取当前脚本所在目录
    current_dir = Path(__file__).resolve().parent
    # 构建模板文件路径
    template_path = current_dir / "templates" / "template.html"

    with open(template_path, "r", encoding="utf-8") as f:
        html_template = f.read()    

    # 替换模板中的 body 内容
    full_html = html_template.replace("{{CONTENT}}", html_body)


    return full_html
