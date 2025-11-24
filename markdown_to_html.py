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
    # MathJax 本地文件路径
    mathjax_path = current_dir / "static" / "mathjax" / "tex-chtml.js"

    with open(template_path, "r", encoding="utf-8") as f:
        html_template = f.read()

    # 替换模板中的 body 内容
    full_html = html_template.replace("{{CONTENT}}", html_body)

    # 将相对路径替换为绝对路径（file:// 协议）
    # Windows 路径需要转换为 file:///C:/... 格式
    mathjax_url = mathjax_path.as_uri()
    full_html = full_html.replace("../static/mathjax/tex-chtml.js", mathjax_url)

    return full_html
