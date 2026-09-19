#!/usr/bin/env python3
"""预渲染本站影评为静态页 review/<film-id>.html。

用途：微信等分享爬虫不执行 JS，review.html?id=xx 的标题/海报/描述抓不到；
静态页自带 <title>、description、og:title/og:description/og:image 与完整正文，
分享卡片即可显示标题、副标题与海报图，同时对搜索引擎友好。

用法：python3 build_review_pages.py          # 重新生成全部
每写完一篇新影评（登记 originals.js 之后）运行一次即可；
review.html?id=xx 旧链接保持可用，站内入口链接指向静态页。
"""

import html, os, re

from publish_wordpress import load_registry, load_posters, parse_front_matter

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://ferryzhou.github.io/christian-film-reviews"
OUT_DIR = os.path.join(ROOT, "review")


def load_films():
    """从 data.js 提取每部影片的元信息（够静态页用即可）。"""
    src = open(os.path.join(ROOT, "data.js"), encoding="utf-8").read()
    films = {}
    for m in re.finditer(r'\{\s*id:\s*"([\w-]+)"(.*?)\n  \}', src, re.S):
        fid, body = m.group(1), m.group(2)
        def field(name):
            fm = re.search(rf'{name}:\s*"((?:[^"\\]|\\.)*)"', body)
            return fm.group(1).replace('\\"', '"') if fm else ""
        ym = re.search(r'year:\s*(\d+)', body)
        films[fid] = {
            "title": field("title"), "titleEn": field("titleEn"),
            "year": ym.group(1) if ym else "", "director": field("director"),
        }
    return films


def esc(s):
    return html.escape(s, quote=False)


def md_inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)
    return s


def md_to_html(md):
    """与 app.js mdToHtml 输出同构；相对资源路径补 ../（页面在 review/ 下）。"""
    out = []
    for b in (x.strip() for x in re.split(r"\n{2,}", md)):
        if not b or b.startswith("# "):
            continue
        if b.startswith("## "):
            out.append(f"<h2>{md_inline(b[3:])}</h2>")
            continue
        if b.startswith(">"):
            out.append(f"<blockquote>{md_inline(re.sub(r'^> ?', '', b, flags=re.M))}</blockquote>")
            continue
        m = re.match(r"^!\[([^\]]*)\]\(([^)\s]+)\)$", b)
        if m and not re.match(r"^(javascript|data):", m.group(2), re.I):
            cap, src = m.group(1), m.group(2)
            if not src.startswith(("http://", "https://")):
                src = "../" + src
            fig = f'<figure><img src="{html.escape(src)}" alt="{html.escape(cap)}" loading="lazy" />'
            if cap:
                fig += f"<figcaption>{md_inline(cap)}</figcaption>"
            out.append(fig + "</figure>")
            continue
        out.append(f"<p>{md_inline(b)}</p>")
    return "\n".join(out)


PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — 光影与信仰</title>
  <meta name="description" content="{desc}" />
  <meta property="og:type" content="article" />
  <meta property="og:locale" content="zh_CN" />
  <meta property="og:site_name" content="光影与信仰" />
  <meta property="og:title" content="{title} — 光影与信仰" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{url}" />
{og_image}  <link rel="canonical" href="{url}" />
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ctext x='16' y='24' font-size='24' text-anchor='middle' fill='%239a7320'%3E%E2%9C%A6%3C/text%3E%3C/svg%3E" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;500&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../styles.css" />
</head>
<body data-page="review-static">
  <header class="topbar">
    <div class="container">
      <a href="../index.html" class="brand"><span class="mark">✦</span>光影与信仰</a>
      <nav class="nav-links">
        <a href="../index.html">首页</a>
        <a href="../index.html#featured" class="active">电影</a>
        <a href="../index.html#authors">作者</a>
        <a href="../books.html">文集</a>
        <a href="../index.html#disclaimer">关于</a>
      </nav>
    </div>
  </header>
  <main>
    <div class="container">
      <a href="../film.html?id={fid}" class="back-link">← 《{film}》</a>
    </div>
    <section class="film-hero reveal">
      <div class="container">
        <div class="title-block">
          <h1>{title}</h1>
          <div class="en-title">《{film}》{en_suffix}</div>
        </div>
      </div>
    </section>
    <div class="container">
      <article class="review-article reveal reveal-1">
        {poster_tag}<div class="review-meta mono">{meta_line} · 本站原创</div>
{body}
        <div class="review-footnote">
          本文为"光影与信仰"原创影评，以基督信仰的眼光读电影。所引圣经经文采用和合本。
          {figure_note}欢迎链接分享；转载请注明出处。
          <a href="../film.html?id={fid}">← 返回《{film}》影片页</a>
        </div>
      </article>
    </div>
  </main>
  <footer>
    <div class="container">
      <span class="mono">光影与信仰 · 导读索引站</span>
      <span class="mono">不搬运原文 · 仅作路标</span>
    </div>
  </footer>
</body>
</html>
"""


def main():
    registry = load_registry()
    posters = load_posters()
    films = load_films()
    os.makedirs(OUT_DIR, exist_ok=True)
    for fid, meta in registry.items():
        film = films.get(fid)
        if not film:
            print(f"!! data.js 中无 {fid}，跳过")
            continue
        raw = open(os.path.join(ROOT, "original-reviews", f"{fid}.md"), encoding="utf-8").read()
        fm, body = parse_front_matter(raw)
        title = meta["title"]
        first_para = next((b.strip() for b in re.split(r"\n{2,}", body)
                           if b.strip() and not b.strip().startswith(("#", "!["))), "")
        sub = " · ".join(x for x in [film["titleEn"], film["year"], film["director"]] if x)
        desc = html.escape(f"《{film['title']}》（{sub}）本站原创影评：{first_para[:90]}…", quote=True)
        url = f"{SITE_URL}/review/{fid}.html"
        og_image = ""
        if posters.get(fid):
            og_image = (f'  <meta property="og:image" content="{SITE_URL}/posters/{posters[fid]}" />\n'
                        f'  <meta name="twitter:card" content="summary" />\n')
        poster_tag = ""
        if posters.get(fid):
            poster_tag = (f'<img class="review-poster" src="../posters/{posters[fid]}" '
                          f'alt="《{esc(film["title"])}》海报（低分辨率，仅作影片标识）" />\n        ')
        body_html = md_to_html(body)
        figure_note = ("文中配图为低分辨率剧照或取景地照片，仅作评论配图（合理使用），版权归属见各图注；"
                       "如权利方提出异议，本站将及时移除。\n          " if "<figure>" in body_html else "")
        meta_line = " · ".join(x for x in [film["year"], film["director"],
                                           fm.get("style") or meta.get("style"),
                                           fm.get("date") or meta.get("date")] if x)
        page = PAGE.format(
            title=esc(title), desc=desc, url=url, og_image=og_image, fid=fid,
            film=esc(film["title"]),
            en_suffix=f" · {esc(film['titleEn'])}" if film["titleEn"] else "",
            poster_tag=poster_tag, meta_line=esc(meta_line),
            body=body_html, figure_note=figure_note,
        )
        out = os.path.join(OUT_DIR, f"{fid}.html")
        open(out, "w", encoding="utf-8").write(page)
        print(f"生成 review/{fid}.html")
    print(f"完成，共 {len(registry)} 篇。")


if __name__ == "__main__":
    main()
