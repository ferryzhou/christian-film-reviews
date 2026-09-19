#!/usr/bin/env python3
"""印刷版：生成按需印刷（Lulu / IngramSpark）所需的内文 PDF 与全包封面 PDF。

用法：
  python3 book/build_print.py                 # 简体 + 繁体，纯文字 → book/dist/print/
  python3 book/build_print.py --with-images   # 内嵌剧照版 → book/dist/print/illustrated/（剧照仅 ≤720px，达不到 300ppi）
  python3 book/build_print.py --lang tw       # 只做一种语言
  python3 book/build_print.py --spine 0.31    # 用平台封面计算器给出的书脊宽度（英寸）覆盖估算值

产出（每种语言）：
  <书名>-<语言>-内文.pdf   内文，开本/边距见 book.json 的 print 段，字体全部内嵌，页码与页眉齐全
  <书名>-<语言>-封面.pdf   封底 + 书脊 + 封面全包一页，含出血；书脊宽按页数估算（见终端输出）
  cover-preview-<语言>.png 封面预览图

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
    "trim": [5.5, 8.5], "bleed": 0.125, "paper": "cream", "platform": "lulu",
    "isbn": "", "price": "", "titleEn": "", "subtitleEn": "", "font_pt": 10.5,
}
PRINT.update(CONFIG.get("print", {}))
# 每页纸厚（英寸）与平台封面板补偿；最终以平台的封面计算器为准
PAPER_THICKNESS = {"cream": 0.0025, "white": 0.002252}
PLATFORM_ALLOWANCE = {"lulu": 0.06, "ingram": 0.03, "none": 0.0}


def esc(s):
    return H.escape(str(s), quote=True)


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

def interior_css(lang):
    w, h = PRINT["trim"]
    fs = PRINT["font_pt"]
    return f"""
@page {{ size: {w}in {h}in; margin: 0.75in 0.55in 0.7in 0.55in;
  @bottom-center {{ content: counter(page); font-family: {font_family(lang)}; font-size: 8.5pt; color: #444; }} }}
@page :left {{ margin-left: 0.55in; margin-right: 0.8in;
  @top-left {{ content: string(booktitle); font-family: {font_family(lang)}; font-size: 7.5pt; letter-spacing: 0.2em; color: #666; }} }}
@page :right {{ margin-left: 0.8in; margin-right: 0.55in;
  @top-right {{ content: string(chaptitle); font-family: {font_family(lang)}; font-size: 7.5pt; letter-spacing: 0.1em; color: #666; }} }}
@page :blank {{ @top-left {{ content: none }} @top-right {{ content: none }} @bottom-center {{ content: none }} }}
@page plain {{ @top-left {{ content: none }} @top-right {{ content: none }} @bottom-center {{ content: none }} }}

html {{ font-family: {font_family(lang)}; font-size: {fs}pt; line-height: 1.72; color: #111; }}
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
.titlepage .subtitle {{ font-size: 13pt; letter-spacing: 0.15em; color: #444; margin-top: 0.4in; text-indent: 0; }}
.titlepage .en {{ font-size: 8.5pt; letter-spacing: 0.06em; color: #666; margin-top: 0.15in; text-indent: 0; }}
.titlepage .author {{ font-size: 12pt; letter-spacing: 0.3em; margin-top: 1.6in; text-indent: 0; }}
.titlepage .publisher {{ font-size: 9pt; letter-spacing: 0.2em; color: #666; margin-top: 0.15in; text-indent: 0; }}
.copyright {{ padding-top: 4.2in; font-size: 8pt; line-height: 1.6; color: #333; }}
.copyright p {{ text-indent: 0; margin-bottom: 0.35em; }}

h1.section {{ font-size: 17pt; font-weight: 700; letter-spacing: 0.15em; margin: 0.4in 0 0.35in; text-align: left; string-set: chaptitle content(); }}
.toc p {{ text-indent: 0; margin: 0.12em 0; text-align: left; }}
.toc p.part {{ margin-top: 0.9em; font-weight: 700; }}
.toc p.ch {{ margin-left: 1.4em; }}
.toc p.ch .film {{ color: #555; font-size: 0.9em; }}
.toc a {{ text-decoration: none; color: inherit; }}
.toc a::after {{ content: leader(".") target-counter(attr(href), page); font-weight: 400; color: #444; }}

.partpage {{ text-align: center; padding-top: 2.8in; }}
.partpage .num {{ font-size: 10pt; letter-spacing: 0.4em; color: #666; text-indent: 0; }}
.partpage .name {{ font-size: 26pt; font-weight: 700; letter-spacing: 0.25em; margin-top: 0.2in; text-indent: 0; }}
.partpage .theme {{ font-size: 11pt; letter-spacing: 0.2em; color: #444; margin-top: 0.35in; text-indent: 0; }}

.chapter h2 {{ font-size: 19pt; font-weight: 700; line-height: 1.35; margin: 0.9in 0 0.12in; text-align: left; string-set: chaptitle content(); }}
.chapter h3.film {{ font-size: 8.5pt; font-weight: 400; color: #555; letter-spacing: 0.05em; margin: 0 0 0.45in; text-align: left; }}
.chapter h3 {{ font-size: 11.5pt; font-weight: 700; margin: 1.2em 0 0.4em; }}
figure {{ margin: 0.9em 0 1.1em; text-align: center; break-inside: avoid; }}
figure img {{ max-width: 100%; max-height: 3.4in; }}
figcaption {{ font-size: 8pt; line-height: 1.5; color: #444; margin-top: 0.3em; text-align: center; }}

.appendix table {{ border-collapse: collapse; width: 100%; font-size: 8.5pt; line-height: 1.45; margin-top: 0.2in; }}
.appendix th, .appendix td {{ border-bottom: 0.5pt solid #bbb; padding: 0.35em 0.25em; text-align: left; vertical-align: top; }}
.appendix th {{ font-weight: 700; border-bottom: 1pt solid #111; }}
.scripture p {{ text-indent: 0; margin-bottom: 0.45em; font-size: 9pt; line-height: 1.6; }}
.scripture strong {{ letter-spacing: 0.05em; }}
.lead {{ text-indent: 0; font-size: 9pt; color: #444; margin-bottom: 0.25in; }}
.about p.site {{ text-indent: 0; margin-top: 0.3in; font-size: 9pt; color: #444; }}
"""


def interior_html(parts, lang, with_images):
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
               + f'<p class="author">{esc(T(c["author"]))}</p><p class="publisher">{esc(T(c["publisher"]))}</p></div>')
    cr = [f"<p>{esc(x)}</p>" for x in B.copyright_lines(lang)]
    if PRINT.get("isbn"):
        cr.insert(3, f"<p>ISBN {esc(PRINT['isbn'])}</p>")
    cr.append(f"<p>{esc(T('印装：按需印刷（Print on Demand）'))}</p>")
    out.append(f'<div class="plain page copyright">{"".join(cr)}</div>')

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
                    fp = os.path.join(B.ROOT, b[2])
                    if os.path.exists(fp):
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
    doc = HTML(string=interior_html(parts, lang, with_images), base_url=B.ROOT).render()
    doc.write_pdf(out)
    return out, len(doc.pages)


# ---------------------------------------------------------------- 全包封面

def spine_width(pages, override=None):
    if override:
        return float(override)
    return round(pages * PAPER_THICKNESS.get(PRINT["paper"], 0.0025) + PLATFORM_ALLOWANCE.get(PRINT["platform"], 0.0), 3)


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


def cover_html(lang, pages, spine):
    T = lang.T
    c = CONFIG
    w, h = PRINT["trim"]
    bleed = PRINT["bleed"]
    W, Hh = 2 * w + spine + 2 * bleed, h + 2 * bleed
    title, subtitle = T(c["title"]), T(c["subtitle"])
    author = T(c["author"])
    kicker = T("电影随笔集")
    tagline = T("二十一篇以基督信仰为眼光的电影随笔")
    en_title = " · ".join(x for x in [PRINT.get("titleEn"), PRINT.get("subtitleEn")] if x)
    blurb_paras = [p for p in T(c["description"]).split("\n") if p.strip()]
    bc = barcode_data_uri(PRINT["isbn"]) if PRINT.get("isbn") else None
    show_spine_text = pages >= 100  # Lulu：不足 100 页不得印书脊文字；Ingram 下限 48 页
    ff = font_family(lang)
    # 各区域的 x 坐标（英寸）：封底 | 书脊 | 封面
    back_x, spine_x, front_x = bleed, bleed + w, bleed + w + spine
    safe = 0.375  # 安全区：距裁切线 ≥ 0.25in，这里留更宽
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@page {{ size: {W}in {Hh}in; margin: 0; }}
html, body {{ margin: 0; padding: 0; }}
body {{ width: {W}in; height: {Hh}in; position: relative; overflow: hidden; font-family: {ff}; color: #2a2418;
  background: #f1e7d0; }}
.abs {{ position: absolute; }}
.paper {{ left: 0; top: 0; width: {W}in; height: {Hh}in;
  background-image: radial-gradient(ellipse 5in 4in at {front_x + w / 2}in 22%, rgba(255,248,228,0.95), rgba(241,231,208,0) 70%); }}
.strip {{ top: 0; height: {Hh}in; width: 0.2in; background: #2a2418; }}
.hole {{ position: absolute; left: 0.062in; width: 0.076in; height: 0.13in; background: #f1e7d0; border-radius: 0.012in; }}
.frame {{ border: 1.5pt solid #9a7320; }}
.frame2 {{ border: 0.5pt solid rgba(154,115,32,0.55); }}
.spine {{ left: {spine_x}in; top: 0; width: {spine}in; height: {Hh}in; background: #2a2418; }}
.spine-text {{ left: {spine_x}in; top: 0; width: {spine}in; height: {Hh}in; color: #e9d7a6; }}
.spine-text .v {{ position: absolute; left: 0; width: {spine}in; text-align: center; writing-mode: vertical-rl; text-orientation: upright;
  letter-spacing: 0.12em; font-size: {min(13, max(7, spine * 30)):.1f}pt; }}
.front-kicker {{ left: {front_x}in; width: {w}in; top: {bleed + 0.85}in; text-align: center; font-size: 8pt; letter-spacing: 0.35em; color: #9a7320; }}
.front-title {{ left: {front_x}in; width: {w}in; top: {bleed + 1.25}in; text-align: center; font-size: 52pt; font-weight: 700; letter-spacing: 0.08em; line-height: 1.15; }}
.front-rule {{ left: {front_x + w / 2 - 0.4}in; width: 0.8in; top: {bleed + 3.55}in; height: 1.5pt; background: #9a7320; }}
.front-sub {{ left: {front_x}in; width: {w}in; top: {bleed + 3.75}in; text-align: center; font-size: 17pt; letter-spacing: 0.18em; color: #5a5040; }}
.front-en {{ left: {front_x}in; width: {w}in; top: {bleed + 4.2}in; text-align: center; font-size: 7.5pt; letter-spacing: 0.12em; color: #7a6a4a; }}
.sun {{ left: {front_x + w / 2 - 0.85}in; top: {bleed + 4.75}in; width: 1.7in; height: 1.7in; border-radius: 50%;
  background: radial-gradient(circle at 50% 45%, #f6d98a 0%, #d9ad4c 55%, #9a7320 100%); }}
.horizon {{ left: {front_x + safe}in; width: {w - 2 * safe}in; top: {bleed + 5.6}in; height: 1.55in; background: #2a2418; border-top: 2pt solid #c9a35e; }}
.front-tag {{ left: {front_x + safe}in; width: {w - 2 * safe}in; top: {bleed + 6.25}in; text-align: center; font-size: 9.5pt; letter-spacing: 0.15em; color: #e9d7a6; }}
.front-author {{ left: {front_x}in; width: {w}in; top: {bleed + h - 0.95}in; text-align: center; font-size: 13pt; letter-spacing: 0.35em; }}
.back-title {{ left: {back_x + safe}in; width: {w - 2 * safe}in; top: {bleed + 0.7}in; font-size: 14pt; font-weight: 700; letter-spacing: 0.1em; }}
.back-blurb {{ left: {back_x + safe}in; width: {w - 2 * safe}in; top: {bleed + 1.25}in; font-size: 8.6pt; line-height: 1.75; text-align: justify; }}
.back-blurb p {{ margin: 0 0 0.6em; text-indent: 2em; }}
.back-site {{ left: {back_x + safe}in; width: {w - 2 * safe - 2.2}in; top: {bleed + h - 1.35}in; font-size: 7.5pt; color: #5a5040; line-height: 1.6; }}
.barcode {{ left: {back_x + w - safe - 2.0}in; top: {bleed + h - safe - 1.2}in; width: 2.0in; height: 1.2in; background: #fff; }}
.barcode img {{ width: 2.0in; height: 1.2in; }}
.barcode .ph {{ font-size: 6.5pt; color: #999; text-align: center; padding-top: 0.5in; }}
</style></head><body>
<div class="abs paper"></div>
<div class="abs strip" style="left:{back_x - bleed}in">{"".join(f'<div class="hole" style="top:{0.15 + i * 0.28}in"></div>' for i in range(int(Hh / 0.28)))}</div>
<div class="abs strip" style="left:{front_x + w + bleed - 0.2}in">{"".join(f'<div class="hole" style="top:{0.15 + i * 0.28}in"></div>' for i in range(int(Hh / 0.28)))}</div>
<div class="abs frame" style="left:{front_x + 0.3}in; top:{bleed + 0.3}in; width:{w - 0.6}in; height:{h - 0.6}in"></div>
<div class="abs frame2" style="left:{front_x + 0.36}in; top:{bleed + 0.36}in; width:{w - 0.72}in; height:{h - 0.72}in"></div>
<div class="abs frame" style="left:{back_x + 0.3}in; top:{bleed + 0.3}in; width:{w - 0.6}in; height:{h - 0.6}in"></div>
<div class="abs spine"></div>
{f'<div class="abs spine-text"><div class="v" style="top:{bleed + 0.6}in">{esc(title)}　{esc(subtitle)}</div><div class="v" style="bottom:{bleed + 0.6}in; top:auto; font-size:7pt; letter-spacing:0.2em">{esc(author)}</div></div>' if show_spine_text else ''}
<div class="abs front-kicker">✦ {esc(kicker)} ✦</div>
<div class="abs front-title">{esc(title)}</div>
<div class="abs front-rule"></div>
<div class="abs front-sub">{esc(subtitle)}</div>
{f'<div class="abs front-en">{esc(en_title)}</div>' if en_title else ''}
<div class="abs sun"></div>
<div class="abs horizon"></div>
<div class="abs front-tag">{esc(tagline)}</div>
<div class="abs front-author">{esc(author)}</div>
<div class="abs back-title">{esc(title)}　{esc(subtitle)}</div>
<div class="abs back-blurb">{"".join(f"<p>{esc(p)}</p>" for p in blurb_paras)}</div>
<div class="abs back-site">{esc(T("文章网络版可免费阅读："))}<br>{esc(c["site"])}{('<br>' + esc(T('定价：')) + esc(PRINT['price'])) if PRINT.get('price') else ''}</div>
<div class="abs barcode">{f'<img src="{bc}">' if bc else f'<div class="ph">{esc(T("ISBN 条码位置（book.json 填入 isbn 后自动生成）"))}</div>'}</div>
</body></html>"""


def build_cover(lang, pages, outdir, spine_override=None):
    from weasyprint import HTML
    import pymupdf
    spine = spine_width(pages, spine_override)
    out = os.path.join(outdir, f"{CONFIG['title']}-{lang.file_tag}-封面.pdf")
    HTML(string=cover_html(lang, pages, spine)).write_pdf(out)
    prev = os.path.join(outdir, f"cover-preview-{lang.code}.png")
    pymupdf.open(out)[0].get_pixmap(dpi=72).save(prev)
    return out, spine


def build_all(parts, langs, with_images, outdir, spine_override=None):
    os.makedirs(outdir, exist_ok=True)
    w, h = PRINT["trim"]
    results = []
    for lang in langs:
        interior, pages = build_interior(parts, lang, with_images, outdir)
        cover, spine = build_cover(lang, pages, outdir, spine_override)
        print(f"印刷版 {lang.label}：{pages} 页 · 开本 {w}×{h} in · 书脊 {spine:.3f} in（{PRINT['paper']} 纸，{PRINT['platform']} 补偿"
              f"{'，命令行覆盖' if spine_override else '，估算值，最终以平台封面计算器为准'}）")
        print("  内文 ->", interior)
        print("  封面 ->", cover, "" if pages >= 100 else "（不足 100 页，书脊未印文字）")
        results.append((interior, cover))
    if with_images:
        print("!! 剧照为 ≤720px 低清图，印刷会偏软；按需印刷平台要求图片 300ppi，仅供自印留念。")
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--with-images", action="store_true")
    ap.add_argument("--lang", choices=["sc", "tw"])
    ap.add_argument("--spine", type=float, help="书脊宽度（英寸），覆盖估算")
    args = ap.parse_args()
    parts = B.load_book()
    langs = [B.Lang(args.lang)] if args.lang else [B.Lang("tw"), B.Lang("sc")]
    outdir = os.path.join(B.DIST, "print", "illustrated") if args.with_images else os.path.join(B.DIST, "print")
    build_all(parts, langs, args.with_images, outdir, args.spine)


if __name__ == "__main__":
    main()
