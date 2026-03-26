import re
import markdown

# ファイル名設定
INPUT_MD = 'TravelToShikoku.md'
OUTPUT_HTML = 'index.html'

# 1. 埋め込むCSS（ここにお気に入りのUI成分をすべて入れます）
CSS_STYLE = """
:root {
    --primary: #007aff; --accent: #ff9500; --bg: #f2f2f7;
    --card: #ffffff; --text: #1c1c1e; --border: #d1d1d6;
}
body {
    font-family: -apple-system, sans-serif; line-height: 1.6;
    background-color: var(--bg); color: var(--text); margin: 0;
    -webkit-text-size-adjust: 100%;
}
header {
    background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px); position: sticky; top: 0;
    z-index: 1000; padding: 16px 0; text-align: center; border-bottom: 0.5px solid var(--border);
}
h1 { margin: 0; font-size: 17px; font-weight: 600; }
nav {
    display: flex; overflow-x: auto; background: #fff; padding: 10px; gap: 8px;
    position: sticky; top: 51px; z-index: 999; border-bottom: 0.5px solid var(--border);
}
nav a {
    flex: 0 0 auto; padding: 6px 14px; background: #e5e5ea; border-radius: 10px;
    text-decoration: none; color: var(--text); font-size: 13px; font-weight: 500;
}
.container { padding: 16px; padding-bottom: 100px; }
section {
    background: var(--card); border-radius: 12px; padding: 20px;
    margin-bottom: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
h2 { font-size: 20px; color: var(--primary); margin: 0 0 16px 0; border-bottom: 2px solid var(--primary); padding-bottom: 8px; }
h3 { font-size: 15px; color: #8e8e93; margin: 20px 0 8px 0; text-transform: uppercase; }
p, li { white-space: pre-wrap; margin: 8px 0; font-size: 15px; }

/* リンクを大きなボタンに自動変換 */
section a[href^="http"] {
    display: block;
    background: #f0f7ff;
    padding: 14px;
    border-radius: 10px;
    margin: 2px 0; /* 上下の隙間を大幅にカット */
    padding: 10px; /* ついでにボタン内の上下幅も少し詰めるとさらにスッキリします */
    text-align: center;
    font-weight: 600;
    border: 1px solid rgba(0,122,255,0.1);
}
.time-tag {
    background: var(--accent); color: white; padding: 2px 6px;
    border-radius: 4px; font-weight: bold; margin-right: 6px; font-size: 13px;
}
"""

# 2. スムーズスクロール用のJavaScript
JS_SCRIPT = """
document.querySelectorAll('nav a').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);
        const offset = 110; 
        const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - offset;
        window.scrollTo({ top: targetPosition, behavior: 'smooth' });
    });
});
"""

def generate_shiori():
    # Markdownの読み込み（linkタグなどは削除しておくのが無難です）
    with open(INPUT_MD, 'r', encoding='utf-8') as f:
        raw_md = f.read()
    
    # 既存のCSSリンクタグなどを除去（もしあれば）
    clean_md = re.sub(r'<link.*?>', '', raw_md)

    # 日程ごとにセクションを分割 (## で始まる行を基準にする)
    parts = re.split(r'\n## ', clean_md)
    
    nav_links = []
    sections_html = []

    for i, part in enumerate(parts):
        if not part.strip(): continue
        
        lines = part.strip().split('\n')
        title = lines[0].replace('#', '').strip()
        body_md = '\n'.join(lines[1:])
        
        section_id = f"day-{i}"
        
        # ナビゲーション用：タイトルの日付部分だけ抽出（例: 3/28）
        nav_label = title.split(' ')[0]
        nav_links.append(f'<a href="#{section_id}">{nav_label}</a>')
        
        # MarkdownをHTMLに変換
        body_html = markdown.markdown(body_md)
        
        # セクションの組み立て
        sections_html.append(f"""
        <section id="{section_id}">
            <h2>{title}</h2>
            {body_html}
        </section>
        """)

    # 全体を1つのHTMLとして組み立て
    html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>四国旅行計画 2026</title>
    <style>{CSS_STYLE}</style>
</head>
<body>
    <header><h1>四国旅行計画 2026</h1></header>
    <nav>{ "".join(nav_links) }</nav>
    <div class="container">
        { "".join(sections_html) }
    </div>
    <script>{JS_SCRIPT}</script>
</body>
</html>
"""

    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✅ 生成完了: {OUTPUT_HTML}")

if __name__ == "__main__":
    generate_shiori()