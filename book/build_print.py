#!/usr/bin/env python3
"""印刷版：生成按需印刷（Lulu / IngramSpark）所需的内文 PDF 与全包封面 PDF。

用法：
  python3 book/build_print.py                 # 简体 + 繁体，含灰度剧照 → book/dist/print/
  python3 book/build_print.py --no-images     # 纯文字版 → book/dist/print/text-only/
  python3 book/build_print.py --lang tw       # 只做一种语言
  python3 book/build_print.py --spine 0.31 --platform ingram   # 用平台封面计算器给出的书脊宽度重做该平台封面

产出（每种语言）：
  <书名>-<语言>-内文.pdf   内文，开本/边距见 book.json 的 print 段，字体全部内嵌，页码与页眉齐全
  <书名>-<语言>-封面-lulu.pdf     Lulu 用全包封面（封底+书脊+封面，含出血，Lulu 书脊公式，RGB）
  <书名>-<语言>-封面-ingram.pdf   IngramSpark 用全包封面（Ingram 书脊公式，Ghostscript 转 CMYK）
  cover-preview-<语言>-<平台>.png 封面预览图；print-listing-<语言>.txt 两个平台的上架文案

排版引擎：WeasyPrint（pip install weasyprint）。条码：pip install python-barcode（填了 ISBN 才需要）。
"""

import argparse
import base64
import html as H
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build_book as B  # noqa: E402

CONFIG = B.CONFIG
PRINT = {
    "trim": [5.5, 8.5], "bleed": 0.125, "paper": "cream",
    "isbn": "", "price": "", "titleEn": "", "subtitleEn": "", "font_pt": 10.5,
}
PRINT.update(CONFIG.get("print", {}))
# 各平台书脊公式（英寸）；最终以平台自己的封面模板/计算器为准，不一致用 --spine 覆盖
PAPER_THICKNESS = {"cream": 0.0025, "white": 0.002252}   # IngramSpark 50# 纸每页厚度
PLATFORMS = {
    # Lulu 官方：spine = pages / 444 + 0.06（help.api.lulu.com "How is spine width calculated?"）
    "lulu": {"label": "Lulu", "spine": lambda pages: pages / 444 + 0.06, "cmyk": False},
    # IngramSpark：pages × 纸厚；封面要求 CMYK、300ppi、条码区 ≥1.75×1 in 白底
    "ingram": {"label": "IngramSpark", "spine": lambda pages: pages * PAPER_THICKNESS.get(PRINT["paper"], 0.0025), "cmyk": True},
}


def esc(s):
    return H.escape(str(s), quote=True)


def isbn_for(lang):
    """print.isbn 可以是一个字符串（两版共用，不推荐）或 {"tw": ..., "sc": ...}；简繁纸书是两本书，各需一个 ISBN。"""
    v = PRINT.get("isbn") or ""
    return (v.get(lang.code, "") if isinstance(v, dict) else v).strip()


def inline(text):
    out = ""
    for t, b, i in B.inline_runs(text):
        t = esc(t)
        if b:
            t = f"<strong>{t}</strong>"
        if i:
            t = f"<em>{t}</em>"
        out += t
    return out


def font_family(lang):
    return '"Noto Serif CJK TC", "Noto Serif TC", "Noto Serif CJK SC", "Noto Serif SC", "Songti TC", "PMingLiU", serif' \
        if lang.code == "tw" else '"Noto Serif CJK SC", "Noto Serif SC", "Songti SC", "SimSun", serif'


# ---------------------------------------------------------------- 内文

def print_image(rel, outdir):
    """印刷内文用灰度剧照（黑白内页；IngramSpark 要求黑白书的图片为灰度）。缓存在 outdir/.cache/。"""
    from PIL import Image, ImageEnhance
    fp = os.path.join(B.ROOT, rel)
    if not os.path.exists(fp):
        return None
    cache = os.path.join(outdir, ".cache")
    os.makedirs(cache, exist_ok=True)
    out = os.path.join(cache, os.path.splitext(rel.replace("/", "_"))[0] + ".jpg")
    if not os.path.exists(out) or os.path.getmtime(out) < os.path.getmtime(fp):
        im = Image.open(fp).convert("L")
        im = ImageEnhance.Contrast(im).enhance(1.08)
        im.save(out, "JPEG", quality=90, optimize=True)
    return out


def interior_css(lang):
    w, h = PRINT["trim"]
    fs = PRINT["font_pt"]
    return f"""
@page {{ size: {w}in {h}in; margin: 0.75in 0.55in 0.7in 0.55in;
  @bottom-center {{ content: counter(page); font-family: {font_family(lang)}; font-size: 8.5pt; color: #000; }} }}
@page :left {{ margin-left: 0.55in; margin-right: 0.8in;
  @top-left {{ content: string(booktitle); font-family: {font_family(lang)}; font-size: 7.5pt; letter-spacing: 0.2em; color: #000; }} }}
@page :right {{ margin-left: 0.8in; margin-right: 0.55in;
  @top-right {{ content: string(chaptitle); font-family: {font_family(lang)}; font-size: 7.5pt; letter-spacing: 0.1em; color: #000; }} }}
@page :blank {{ @top-left {{ content: none }} @top-right {{ content: none }} @bottom-center {{ content: none }} }}
@page plain {{ @top-left {{ content: none }} @top-right {{ content: none }} @bottom-center {{ content: none }} }}

html {{ font-family: {font_family(lang)}; font-size: {fs}pt; line-height: 1.72; color: #000; }}
body {{ margin: 0; }}
p {{ margin: 0; text-indent: 2em; text-align: justify; orphans: 2; widows: 2; hyphens: none; }}
p.noindent {{ text-indent: 0; }}
strong {{ font-weight: 700; }}

.plain {{ page: plain; }}
.recto {{ break-before: right; }}
.page {{ break-before: page; }}

.halftitle {{ text-align: center; padding-top: 2.6in; font-size: 16pt; letter-spacing: 0.3em; }}
.titlepage {{ text-align: center; padding-top: 2in; }}
.titlepage .title {{ font-size: 30pt; font-weight: 700; letter-spacing: 0.15em; text-indent: 0; line-height: 1.3; }}
.titlepage .subtitle {{ font-size: 13pt; letter-spacing: 0.15em; color: #000; margin-top: 0.4in; text-indent: 0; }}
.titlepage .en {{ font-size: 8.5pt; letter-spacing: 0.06em; color: #000; margin-top: 0.15in; text-indent: 0; }}
.titlepage .author {{ font-size: 12pt; letter-spacing: 0.3em; margin-top: 1.6in; text-indent: 0; }}
.titlepage .publisher {{ font-size: 9pt; letter-spacing: 0.2em; color: #000; margin-top: 0.15in; text-indent: 0; }}
.copyright {{ padding-top: 3.5in; font-size: 8pt; line-height: 1.6; color: #000; }}
.copyright p {{ text-indent: 0; margin-bottom: 0.35em; }}
.epigraph {{ text-align: center; padding-top: 3in; font-size: 12pt; letter-spacing: 0.08em; }}
.epigraph .ref {{ font-size: 9pt; margin-top: 0.25in; }}

h1.section {{ font-size: 17pt; font-weight: 700; letter-spacing: 0.15em; margin: 0.4in 0 0.35in; text-align: left; string-set: chaptitle content(); }}
.toc p {{ text-indent: 0; margin: 0.12em 0; text-align: left; }}
.toc p.part {{ margin-top: 0.9em; font-weight: 700; }}
.toc p.ch {{ margin-left: 1.4em; }}
.toc p.ch .film {{ color: #000; font-size: 0.9em; }}
.toc a {{ text-decoration: none; color: inherit; }}
.toc a::after {{ content: leader(".") target-counter(attr(href), page); font-weight: 400; color: #000; }}

.partpage {{ text-align: center; padding-top: 2.8in; }}
.partpage .num {{ font-size: 10pt; letter-spacing: 0.4em; color: #000; text-indent: 0; }}
.partpage .name {{ font-size: 26pt; font-weight: 700; letter-spacing: 0.25em; margin-top: 0.2in; text-indent: 0; }}
.partpage .theme {{ font-size: 11pt; letter-spacing: 0.2em; color: #000; margin-top: 0.35in; text-indent: 0; }}

.chapter h2 {{ font-size: 19pt; font-weight: 700; line-height: 1.35; margin: 0.9in 0 0.12in; text-align: left; string-set: chaptitle content(); }}
.chapter h3.film {{ font-size: 8.5pt; font-weight: 400; color: #000; letter-spacing: 0.05em; margin: 0 0 0.45in; text-align: left; }}
.chapter h3 {{ font-size: 11.5pt; font-weight: 700; margin: 1.2em 0 0.4em; }}
figure {{ margin: 0.9em 0 1.1em; text-align: center; break-inside: avoid; }}
figure img {{ max-width: 100%; max-height: 3.4in; }}
figcaption {{ font-size: 8pt; line-height: 1.5; color: #000; margin-top: 0.3em; text-align: center; }}

.appendix table {{ border-collapse: collapse; width: 100%; font-size: 8.5pt; line-height: 1.45; margin-top: 0.2in; }}
.appendix th, .appendix td {{ border-bottom: 0.5pt solid #bbb; padding: 0.35em 0.25em; text-align: left; vertical-align: top; }}
.appendix th {{ font-weight: 700; border-bottom: 1pt solid #111; }}
.scripture p {{ text-indent: 0; margin-bottom: 0.45em; font-size: 9pt; line-height: 1.6; }}
.scripture strong {{ letter-spacing: 0.05em; }}
.lead {{ text-indent: 0; font-size: 9pt; color: #000; margin-bottom: 0.25in; }}
.about p.site {{ text-indent: 0; margin-top: 0.3in; font-size: 9pt; color: #000; }}
"""


def interior_html(parts, lang, with_images, outdir):
    T = lang.T
    c = CONFIG
    title, subtitle = T(c["title"]), T(c["subtitle"])
    pre_title, pre_blocks = B.preface_blocks()
    out = [f'<!DOCTYPE html><html lang="{lang.bcp47}"><head><meta charset="utf-8"><title>{esc(title)}</title>'
           f"<style>{interior_css(lang)}</style></head><body>"]

    # 前页：半书名页 → 书名页（右页）→ 版权页（左页）
    out.append(f'<div class="plain"><p class="halftitle noindent" style="string-set: booktitle \'{esc(title)}\'">{esc(title)}</p></div>')
    en_line = " · ".join(x for x in [PRINT.get("titleEn"), PRINT.get("subtitleEn")] if x)
    out.append(f'<div class="plain recto titlepage"><p class="title">{esc(title)}</p><p class="subtitle">{esc(subtitle)}</p>'
               + (f'<p class="en">{esc(en_line)}</p>' if en_line else "")
               + f'<p class="author">{esc(B.author_line(lang))}</p><p class="publisher">{esc(T(c["publisher"]))}</p></div>')
    cr = [f"<p>{esc(x)}</p>" for x in B.copyright_lines(lang)]
    if isbn_for(lang):
        cr.insert(3, f"<p>ISBN {esc(isbn_for(lang))}</p>")
    cr.append(f"<p>{esc(T('印装：按需印刷（Print on Demand）'))}</p>")
    out.append(f'<div class="plain page copyright">{"".join(cr)}</div>')

    # 题记（右页）
    if c.get("epigraph"):
        out.append(f'<div class="plain recto epigraph"><p class="noindent">{esc(T(c["epigraph"]["text"]))}</p>'
                   f'<p class="noindent ref">——{esc(T(c["epigraph"]["ref"]))}</p></div>')

    # 目录
    out.append(f'<div class="recto opener toc"><h1 class="section">{esc(T("目录"))}</h1>')
    out.append(f'<p><a href="#preface">{esc(T(pre_title))}</a></p>')
    for part in parts:
        ptitle, theme = B.part_heading(part, lang)
        out.append(f'<p class="part"><a href="#part{part["no"]}">{esc(ptitle)}　{esc(theme)}</a></p>')
        for ch in part["chapters"]:
            out.append(f'<p class="ch"><a href="#{ch["anchor"]}">{esc(T(ch["title"]))}　<span class="film">《{esc(T(ch["film"]))}》</span></a></p>')
    out.append(f'<p class="part"><a href="#app-films">{esc(T("附录一　影片索引"))}</a></p>')
    out.append(f'<p class="part"><a href="#app-scripture">{esc(T("附录二　经文索引"))}</a></p>')
    out.append(f'<p class="part"><a href="#about">{esc(T("关于作者"))}</a></p></div>')

    # 序
    out.append(f'<div class="recto opener"><h1 class="section" id="preface">{esc(T(pre_title))}</h1>')
    out += [f"<p>{inline(T(b[1]))}</p>" for b in pre_blocks if b[0] == "p"]
    out.append("</div>")

    # 正文
    for part in parts:
        ptitle, theme = B.part_heading(part, lang)
        num, name = ptitle.split("　", 1) if "　" in ptitle else (ptitle, "")
        out.append(f'<div class="recto plain partpage" id="part{part["no"]}"><p class="num">{esc(num)}</p>'
                   f'<p class="name">{esc(name)}</p><p class="theme">{esc(theme)}</p></div>')
        for ch in part["chapters"]:
            out.append(f'<div class="page opener chapter"><h2 id="{ch["anchor"]}">{esc(T(ch["title"]))}</h2>'
                       f'<h3 class="film">{esc(B.chapter_subtitle(ch, lang))}</h3>')
            for b in ch["blocks"]:
                if b[0] == "p":
                    out.append(f"<p>{inline(T(b[1]))}</p>")
                elif b[0] == "h":
                    out.append(f"<h3>{inline(T(b[1]))}</h3>")
                elif b[0] == "img" and with_images:
                    fp = print_image(b[2], outdir)
                    if fp:
                        out.append(f'<figure><img src="file://{esc(fp)}" alt="{esc(T(b[1]))}"><figcaption>{inline(T(b[1]))}</figcaption></figure>')
            out.append("</div>")

    # 附录一
    rows = sorted((ch for part in parts for ch in part["chapters"]), key=lambda c: int(c["year"] or 0))
    out.append(f'<div class="recto opener appendix"><h1 class="section" id="app-films">{esc(T("附录一　影片索引"))}</h1>'
               f'<table><tr><th>{esc(T("片名"))}</th><th>{esc(T("原名"))}</th><th>{esc(T("年份 · 导演"))}</th><th>{esc(T("本书篇目"))}</th><th>{esc(T("页"))}</th></tr>')
    for ch in rows:
        out.append(f'<tr><td>{esc(T(ch["film"]))}</td><td>{esc(ch["filmEn"])}</td><td>{esc(ch["year"])} · {esc(T(ch["director"]))}</td>'
                   f'<td>{esc(T(ch["title"]))}</td><td><a href="#{ch["anchor"]}" class="pg"></a></td></tr>')
    out.append("</table></div>")

    # 附录二
    out.append(f'<div class="recto opener appendix scripture"><h1 class="section" id="app-scripture">{esc(T("附录二　经文索引"))}</h1>'
               f'<p class="lead">{esc(T("以下为各篇正文中引用的和合本经文，按圣经卷序排列；括号内为所在篇目与页码。"))}</p>')
    for bk, items in B.scripture_index(parts):
        refs = "；".join(f'{esc(ref)}（{esc(T(ch["title"]))}，<a href="#{ch["anchor"]}" class="pg"></a>）' for ch, ref in items)
        out.append(f"<p><strong>{esc(T(bk))}</strong>　{refs}</p>")
    out.append("</div>")

    # 关于作者
    out.append(f'<div class="recto opener about"><h1 class="section" id="about">{esc(T("关于作者"))}</h1>'
               f'<p>{esc(T(c["authorBio"]))}</p><p class="site">{esc(c["site"])}</p></div>')
    out.append("</body></html>")
    html = "\n".join(out)
    # 附录里的页码：a.pg 用 target-counter 取章首页码
    return html.replace("</style>", 'a.pg::after { content: target-counter(attr(href), page); } a.pg { text-decoration: none; color: inherit; }</style>', 1)


def build_interior(parts, lang, with_images, outdir):
    from weasyprint import HTML
    out = os.path.join(outdir, f"{CONFIG['title']}-{lang.file_tag}-内文.pdf")
    doc = HTML(string=interior_html(parts, lang, with_images, outdir), base_url=B.ROOT).render()
    doc.write_pdf(out)
    return out, len(doc.pages)


# ---------------------------------------------------------------- 全包封面

def spine_width(pages, platform, override=None):
    if override:
        return float(override)
    pages += pages % 2  # 按需印刷按偶数页装订
    return round(PLATFORMS[platform]["spine"](pages), 3)


def to_cmyk(pdf_path):
    """用 Ghostscript 把封面 PDF 转成 CMYK（IngramSpark 要求）；没有 gs 就原样保留并提示。"""
    import shutil, subprocess
    if not shutil.which("gs"):
        print("!! 未找到 Ghostscript，封面保持 RGB；IngramSpark 会自行转换，色彩可能略有偏差")
        return False
    tmp = pdf_path + ".cmyk.pdf"
    subprocess.run(["gs", "-q", "-o", tmp, "-sDEVICE=pdfwrite", "-dPDFSETTINGS=/prepress",
                    "-sColorConversionStrategy=CMYK", "-dProcessColorModel=/DeviceCMYK",
                    "-dEmbedAllFonts=true", "-dSubsetFonts=true", pdf_path], check=True)
    os.replace(tmp, pdf_path)
    return True


def barcode_data_uri(isbn):
    try:
        import barcode
        from barcode.writer import SVGWriter
    except ImportError:
        return None
    digits = isbn.replace("-", "").replace(" ", "")
    if len(digits) != 13 or not digits.isdigit():
        return None
    buf = io.BytesIO()
    barcode.get("ean13", digits, writer=SVGWriter()).write(buf, {"module_height": 12, "font_size": 8, "text_distance": 3, "quiet_zone": 2})
    return "data:image/svg+xml;base64," + base64.b64encode(buf.getvalue()).decode()


def isbn_check(isbn):
    """校验 ISBN-13 校验位；返回 (是否有效, 规范化 13 位)。"""
    d = isbn.replace("-", "").replace(" ", "")
    if len(d) != 13 or not d.isdigit():
        return False, d
    total = sum(int(ch) * (1 if i % 2 == 0 else 3) for i, ch in enumerate(d[:12]))
    return (10 - total % 10) % 10 == int(d[12]), d


def _dust(seed, n, x0, y0, x1, y1):
    """确定性的“光束里的尘埃”：在给定矩形内撒 n 个小圆点（英寸坐标）。"""
    import random
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = x0 + rnd.random() * (x1 - x0), y0 + rnd.random() * (y1 - y0)
        # 只保留落在光束（从左上光源向右下展开的锥形）里的点
        t = (y - y0) / max(0.01, (y1 - y0))
        left = x0 + 0.9 * (1 - t) + 0.2 * t
        if x < left:
            continue
        r = 0.006 + rnd.random() * 0.02
        out.append(f'<circle cx="{x:.3f}in" cy="{y:.3f}in" r="{r:.3f}in" fill="#f6e3b4" opacity="{0.25 + rnd.random() * 0.5:.2f}"/>')
    return "".join(out)


def _front_html(lang, x, y, w, h, bleed_right):
    """封面正面（一块 w×h 英寸的区域，左上角在 (x, y)）：深色底 + 放映机光束 + 书名。"""
    T = lang.T
    c = CONFIG
    title, subtitle = T(c["title"]), T(c["subtitle"])
    n = len(title)
    lines = [title] if n <= 4 else [title[: (n + 1) // 2], title[(n + 1) // 2:]]
    en_title = " · ".join(v for v in [PRINT.get("titleEn"), PRINT.get("subtitleEn")] if v)
    ref = T(c.get("epigraph", {}).get("ref", ""))
    kicker = T("电影随笔集")
    # 光源与光束（SVG，Chromium 与 WeasyPrint 都能画）
    sx, sy = x + 0.55, y + 0.75
    bx1 = x + w + bleed_right
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w + bleed_right}in" height="{h}in" viewBox="0 0 {w + bleed_right} {h}"
  style="position:absolute; left:{x}in; top:{y}in" preserveAspectRatio="none">
  <defs>
    <radialGradient id="glow" cx="{(sx - x) / (w + bleed_right):.4f}" cy="{(sy - y) / h:.4f}" r="0.55">
      <stop offset="0" stop-color="#ffe9b8" stop-opacity="0.95"/><stop offset="0.12" stop-color="#f0cf85" stop-opacity="0.55"/>
      <stop offset="0.45" stop-color="#8a6a2a" stop-opacity="0.12"/><stop offset="1" stop-color="#0b0c10" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="beam" x1="{sx - x:.3f}" y1="{sy - y:.3f}" x2="{w * 0.85:.3f}" y2="{h:.3f}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#f6dc9c" stop-opacity="0.62"/><stop offset="0.35" stop-color="#e2c27a" stop-opacity="0.26"/>
      <stop offset="1" stop-color="#e2c27a" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="{w + bleed_right}" height="{h}" fill="#0b0c10"/>
  <polygon points="{sx - x:.3f},{sy - y:.3f} {w + bleed_right:.3f},{h * 0.30:.3f} {w + bleed_right:.3f},{h:.3f} {w * 0.05:.3f},{h:.3f}" fill="url(#beam)" opacity="0.35"/>
  <polygon points="{sx - x:.3f},{sy - y:.3f} {w + bleed_right:.3f},{h * 0.38:.3f} {w + bleed_right:.3f},{h:.3f} {w * 0.22:.3f},{h:.3f}" fill="url(#beam)" opacity="0.55"/>
  <polygon points="{sx - x:.3f},{sy - y:.3f} {w + bleed_right:.3f},{h * 0.46:.3f} {w + bleed_right:.3f},{h:.3f} {w * 0.40:.3f},{h:.3f}" fill="url(#beam)"/>
  <rect x="0" y="0" width="{w + bleed_right}" height="{h}" fill="url(#glow)"/>
  <g transform="translate({-x},{-y})">{_dust(7, 260, x + 0.3, y + 0.9, x + w + bleed_right, y + h)}</g>
</svg>'''
    # 左缘一条隐约的胶片齿孔
    holes = "".join(f'<div style="position:absolute; left:{x + 0.09:.3f}in; top:{y + 0.12 + i * 0.30:.3f}in; width:0.09in; height:0.15in; border:0.6pt solid #2a2b32; border-radius:0.015in"></div>'
                    for i in range(int((h - 0.2) / 0.30)))
    title_pt = min(64, 250 / max(3, len(lines[0])))
    title_html = "".join(f'<div style="line-height:1.12">{esc(l)}</div>' for l in lines)
    return f'''{svg}{holes}
<div class="abs" style="left:{x}in; width:{w}in; top:{y + 0.62}in; text-align:center; font-size:8pt; letter-spacing:0.38em; color:#c9a35e">✦ {esc(kicker)} ✦</div>
<div class="abs" style="left:{x}in; width:{w}in; top:{y + 1.25}in; text-align:center; font-size:{title_pt:.0f}pt; font-weight:700; letter-spacing:0.10em; color:#f5ead3">{title_html}</div>
<div class="abs" style="left:{x + w / 2 - 0.35}in; width:0.7in; top:{y + 1.25 + 1.12 * len(lines) * title_pt / 72 + 0.28:.3f}in; height:1pt; background:#c9a35e"></div>
<div class="abs" style="left:{x}in; width:{w}in; top:{y + 1.25 + 1.12 * len(lines) * title_pt / 72 + 0.40:.3f}in; text-align:center; font-size:8.5pt; letter-spacing:0.25em; color:#c9a35e">{esc(ref)}</div>
<div class="abs" style="left:{x}in; width:{w}in; top:{y + h * 0.66}in; text-align:center; font-size:15pt; letter-spacing:0.22em; color:#e9dcc0">{esc(subtitle)}</div>
{f'<div class="abs" style="left:{x}in; width:{w}in; top:{y + h * 0.66 + 0.36}in; text-align:center; font-size:7pt; letter-spacing:0.14em; color:#a89f8c">{esc(en_title)}</div>' if en_title else ''}
<div class="abs" style="left:{x}in; width:{w}in; top:{y + h - 0.95}in; text-align:center; font-size:12.5pt; letter-spacing:0.35em; color:#f5ead3">{esc(B.author_line(lang))}</div>
'''


def cover_ctx(lang):
    """各套封面设计共用的文字素材。"""
    T = lang.T
    c = CONFIG
    title = T(c["title"])
    n = len(title)
    return {
        "title": title, "lines": [title] if n <= 4 else [title[: (n + 1) // 2], title[(n + 1) // 2:]],
        "subtitle": T(c["subtitle"]), "author_line": B.author_line(lang), "author": T(c["author"]),
        "kicker": T("电影随笔集"),
        "ref": T(c.get("epigraph", {}).get("ref", "")), "verse": T(c.get("epigraph", {}).get("text", "")),
        "en_title": " · ".join(v for v in [PRINT.get("titleEn"), PRINT.get("subtitleEn")] if v),
        "ff": font_family(lang),
    }


BEAM_PALETTE = {"bg": "#0b0c10", "fg": "#f5ead3", "accent": "#c9a35e", "muted": "#a89f8c"}


def cover_design(design=None):
    """返回 (正面渲染函数, 配色)。design 取自 book.json 的 cover.design，默认 beam。"""
    from cover_designs import DESIGNS
    design = design or CONFIG.get("cover", {}).get("design", "beam")
    if design == "beam":
        return (lambda lang, x, y, w, h, br, ctx: _front_html(lang, x, y, w, h, br)), BEAM_PALETTE
    if design not in DESIGNS:
        sys.exit(f"未知封面设计 {design}，可选：beam, " + ", ".join(DESIGNS))
    fn = DESIGNS[design][1]
    return fn, fn.palette


def cover_html(lang, pages, spine, front_only=False, trim=None, design=None):
    """全包封面（封底 | 书脊 | 封面）或仅封面（电子书）。正面样式见 cover_designs.py。"""
    T = lang.T
    c = CONFIG
    w, h = trim or PRINT["trim"]
    bleed = 0 if front_only else PRINT["bleed"]
    W, Hh = (w, h) if front_only else (2 * w + spine + 2 * bleed, h + 2 * bleed)
    front, pal = cover_design(design)
    ff = font_family(lang)
    back_x, spine_x, front_x = bleed, bleed + w, (0 if front_only else bleed + w + spine)
    safe = 0.4
    show_spine_text = pages >= 100
    title, subtitle, author = T(c["title"]), T(c["subtitle"]), T(c["author"])
    parts = [f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@page {{ size: {W}in {Hh}in; margin: 0; }}
html, body {{ margin: 0; padding: 0; }}
body {{ width: {W}in; height: {Hh}in; position: relative; overflow: hidden; font-family: {ff}; color: {pal["fg"]}; background: {pal["bg"]}; }}
.abs {{ position: absolute; }}
.v {{ position: absolute; left: 0; width: {spine}in; text-align: center; writing-mode: vertical-rl; text-orientation: upright; letter-spacing: 0.12em; color: {pal["fg"]}; }}
.back-blurb p {{ margin: 0 0 0.6em; text-indent: 2em; }}
</style></head><body>''']
    if not front_only:
        bc = barcode_data_uri(isbn_for(lang)) if isbn_for(lang) else None
        blurb = [p for p in T(c["description"]).split("\n") if p.strip()]
        parts.append(f'''
<div class="abs" style="left:{back_x + safe}in; width:{w - 2 * safe}in; top:{bleed + 0.75}in; font-size:13.5pt; font-weight:700; letter-spacing:0.1em; color:{pal["fg"]}">{esc(title)}　<span style="font-weight:400; font-size:10.5pt; color:{pal["accent"]}">{esc(subtitle)}</span></div>
<div class="abs" style="left:{back_x + safe}in; width:{w - 2 * safe}in; top:{bleed + 1.15}in; height:1pt; background:{pal["accent"]}; opacity:0.7"></div>
<div class="abs back-blurb" style="left:{back_x + safe}in; width:{w - 2 * safe}in; top:{bleed + 1.4}in; font-size:8.6pt; line-height:1.8; text-align:justify; color:{pal["fg"]}">{"".join(f"<p>{esc(p)}</p>" for p in blurb)}</div>
<div class="abs" style="left:{back_x + safe}in; width:{w - 2 * safe - 2.2}in; top:{bleed + h - 1.35}in; font-size:7.5pt; line-height:1.6; color:{pal["muted"]}">{esc(T("文章网络版可免费阅读："))}<br>{esc(c["site"])}{('<br>' + esc(T('定价：')) + esc(PRINT['price'])) if PRINT.get('price') else ''}</div>
<div class="abs" style="left:{back_x + w - safe - 2.0}in; top:{bleed + h - safe - 1.2}in; width:2.0in; height:1.2in; background:#fff">{f'<img src="{bc}" style="width:2.0in; height:1.2in">' if bc else f'<div style="font-size:6.5pt; color:#999; text-align:center; padding-top:0.5in">{esc(T("ISBN 条码位置（book.json 填入 isbn 后自动生成）"))}</div>'}</div>
<div class="abs" style="left:{spine_x}in; top:0; width:{spine}in; height:{Hh}in; background:{pal["bg"]}"></div>
''')
        if show_spine_text:
            # 书脊：单列逐字竖排。书名尽量大（两侧各留 ≥0.0625in 安全边，Ingram 规定），副标题小字紧随其后，作者在底部
            usable = max(0.15, spine - 0.14)
            tpt = max(9, min(24, usable * 72 * 0.92))
            spt = max(6.5, min(9.5, tpt * 0.42))
            stack = lambda text, pt, color, weight="400", gap=1.22: "".join(
                f'<div style="line-height:{gap}; font-size:{pt:.1f}pt; font-weight:{weight}; color:{color}; text-align:center">{esc(ch)}</div>' for ch in text if ch.strip())
            parts.append(f'''<div class="abs" style="left:{spine_x}in; top:{bleed + 0.55}in; width:{spine}in">{stack(title, tpt, pal["fg"], "700", 1.18)}
<div style="height:0.22in"></div>{stack(subtitle, spt, pal["fg"], "400", 1.3)}</div>
<div class="abs" style="left:{spine_x}in; bottom:{bleed + 0.55}in; width:{spine}in">{stack(author, min(9, spt + 1), pal["accent"])}</div>''')
    parts.append(front(lang, front_x, 0 if front_only else bleed, w, h, 0 if front_only else bleed, cover_ctx(lang)))
    parts.append("</body></html>")
    return "".join(parts)


def build_cover(lang, pages, outdir, platform, spine_override=None):
    from weasyprint import HTML
    import pymupdf
    spine = spine_width(pages, platform, spine_override)
    out = os.path.join(outdir, f"{CONFIG['title']}-{lang.file_tag}-封面-{platform}.pdf")
    HTML(string=cover_html(lang, pages, spine)).write_pdf(out)
    if PLATFORMS[platform]["cmyk"]:
        to_cmyk(out)
    prev = os.path.join(outdir, f"cover-preview-{lang.code}-{platform}.png")
    pymupdf.open(out)[0].get_pixmap(dpi=72).save(prev)
    return out, spine


EN_DESCRIPTION = (
    f"{PRINT.get('titleEn') or 'This book'}: {PRINT.get('subtitleEn', '')} is a collection of twenty-one original essays, written in Chinese, "
    "that reread landmark films through the eyes of Christian faith: from Bergman's The Seventh Seal and Lee Chang-dong's Secret Sunshine "
    "to Schindler's List, Life Is Beautiful, Dying to Survive and Pixar's Soul. Each essay starts from a line of dialogue, a prop or an "
    "echoing shot, sketches a portrait of every character, faces the human predicament the film exposes, and walks toward the gospel. "
    "Arranged in five parts (Questions in Suffering; Freedom and Redemption; Sacrifice and Justice; Memory, Identity and Homecoming; "
    "Youth and Education), with an index of films and an index of Scripture references. For film lovers, and for anyone lingering at the door of faith."
)
BISAC = [
    "REL012000  RELIGION / Christian Living / General",
    "PER004030  PERFORMING ARTS / Film / History & Criticism",
    "LCO010000  LITERARY COLLECTIONS / Essays",
]


def write_print_listing(lang, pages, spines, outdir):
    T = lang.T
    c = CONFIG
    w, h = PRINT["trim"]
    variant = "Traditional Chinese" if lang.code == "tw" else "Simplified Chinese"
    en_title = PRINT.get("titleEn", ""); en_sub = PRINT.get("subtitleEn", "")
    lines = [
        f"=== 纸质书上架文案（{lang.label}）===", "",
        f"书名：{T(c['title'])}    副标题：{T(c['subtitle'])}    作者：{T(c['author'])}",
        f"English title: {en_title}: {en_sub}    ({variant} edition)",
        f"规格：{w} × {h} in · 平装 · 黑白内文 · {PRINT['paper']} 纸 · {pages} 页（装订按 {pages + pages % 2} 页）",
        f"ISBN：{isbn_for(lang) or '（未填，book.json print.isbn）'}    定价：{PRINT.get('price') or '（未填，book.json print.price）'}", "",
        "--- Lulu（Create → Print Book；只勾 Lulu Bookstore，不勾 Global Distribution）---",
        f"Spine width: {spines['lulu']:.3f} in（pages/444 + 0.06）",
        "Category: Religion & Spirituality > Christianity   |   Keywords: " + "、".join(T(k) for k in c["keywords"][:5]),
        "Description:", T(c["description"]), "",
        "--- Bowker My Identifiers（数据库只收 Latin-1，中文会变问号；用拼音 + 英文登记，不影响 Ingram/Amazon 显示中文）---",
        f"Title: {PRINT.get('titleRoman', '')} ({en_title})",
        f"Subtitle: {en_sub} ({variant} Edition)",
        f"Author: {PRINT.get('authorRoman', 'Zhou, Jin')}    Publisher: {c.get('publisherEn', '')}    Language: Chinese    Format: Paperback    Pages: {pages + pages % 2}",
        "Description: 用下方 IngramSpark 的英文短简介", "",
        "--- IngramSpark（Add a Title；需自有 ISBN）---",
        f"Spine width: {spines['ingram']:.3f} in（pages × {PAPER_THICKNESS.get(PRINT['paper'])}，最终以 Cover Template Generator 为准）",
        f"Language: Chinese    Title: {T(c['title'])}    Subtitle: {T(c['subtitle'])}",
        f"Contributor: {T(c['author'])} (Author)    Imprint: {c.get('publisherEn', c['publisher'])}（须与 Bowker 登记的 Publisher 一字不差）",
        "BISAC subjects（下拉框按名称选，最多 3 个）:", *[f"  {b}" for b in BISAC],
        "Keywords: Christian film criticism; Chinese essays; faith and cinema; " + "; ".join(T(k) for k in c["keywords"][:4]),
        "Short description (English, for retailers):", EN_DESCRIPTION, "",
        "Full description (Chinese):", T(c["description"]), "",
        "Wholesale discount: 55%（Amazon/书店标准；40% 利润更高但书店不进货）    Returns: No    Print on demand: Yes",
        "Markets: US / UK / EU / AU / Global Connect 全选    Publication date: 上传后 2–4 周", "",
        "=== 章节一览 ===",
    ]
    for part in B.load_book():
        ptitle, theme = B.part_heading(part, lang)
        lines.append(f"{ptitle}　{theme}")
        for ch in part["chapters"]:
            lines.append(f"  {ch['no']:>2}. {T(ch['title'])}　《{T(ch['film'])}》 {ch['filmEn']} ({ch['year']})")
    out = os.path.join(outdir, f"print-listing-{lang.code}.txt")
    open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return out


def build_all(parts, langs, with_images, outdir, platforms, spine_override=None):
    os.makedirs(outdir, exist_ok=True)
    w, h = PRINT["trim"]
    for lang in langs:
        if isbn_for(lang):
            ok, _ = isbn_check(isbn_for(lang))
            if not ok:
                sys.exit(f"{lang.label} 的 ISBN {isbn_for(lang)} 校验位不对，请核对 book.json")
        interior, pages = build_interior(parts, lang, with_images, outdir)
        print(f"印刷版 {lang.label}：{pages} 页 · 开本 {w}×{h} in")
        print("  内文 ->", interior)
        spines = {}
        for platform in platforms:
            cover, spine = build_cover(lang, pages, outdir, platform, spine_override)
            spines[platform] = spine
            print(f"  封面（{PLATFORMS[platform]['label']}，书脊 {spine:.3f} in{'，命令行覆盖' if spine_override else ''}） ->", cover,
                  "" if pages >= 100 else "（不足 100 页，书脊未印文字）")
        print(f"  ISBN：{isbn_for(lang) or '无（未填）'}")
        if len(platforms) == 2:
            print("  上架文案 ->", write_print_listing(lang, pages, spines, outdir))
    if with_images:
        print("!! 剧照原图 ≤720px，按 4.2in 宽排版约 170ppi，低于平台建议的 300ppi，印出来会略软；平台一般只警告不拒收。")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-images", action="store_true", help="不嵌剧照，输出到 dist/print/text-only/")
    ap.add_argument("--lang", choices=["sc", "tw"])
    ap.add_argument("--spine", type=float, help="书脊宽度（英寸），覆盖估算")
    ap.add_argument("--platform", choices=["lulu", "ingram", "all"], default="all", help="只出某个平台的封面")
    args = ap.parse_args()
    parts = B.load_book()
    langs = [B.Lang(args.lang)] if args.lang else [B.Lang("tw"), B.Lang("sc")]
    platforms = ["lulu", "ingram"] if args.platform == "all" else [args.platform]
    outdir = os.path.join(B.DIST, "print", "text-only") if args.no_images else os.path.join(B.DIST, "print")
    build_all(parts, langs, not args.no_images, outdir, platforms, args.spine)


if __name__ == "__main__":
    main()
