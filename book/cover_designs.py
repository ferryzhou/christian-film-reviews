"""封面正面的几套设计。每套是一个函数：(lang, x, y, w, h, bleed_right, ctx) -> HTML 片段。

ctx 里有：title / lines（书名按字数拆成 1–2 行）/ subtitle / author_line / kicker / ref / verse / en_title / ff（字体）。
坐标单位英寸；(x, y) 是封面正面左上角，w×h 是成品尺寸，bleed_right 是右侧出血（电子书为 0）。
每套设计附一个 palette：bg / fg / accent，供封底与书脊配色。

在 book.json 的 cover.design 里选用：fuse | paper | slab | door | frame | night | beam
"""

import html as H


def esc(s):
    return H.escape(str(s), quote=True)


def _holes_v(x, y, h, color, step=0.30, size=(0.09, 0.15), border=True):
    style = f"border:0.6pt solid {color}" if border else f"background:{color}"
    return "".join(
        f'<div style="position:absolute; left:{x:.3f}in; top:{y + 0.12 + i * step:.3f}in; width:{size[0]}in; height:{size[1]}in; {style}; border-radius:0.015in"></div>'
        for i in range(int((h - 0.2) / step)))


def _holes_h(x, y, w, color, step=0.30, size=(0.15, 0.09)):
    return "".join(
        f'<div style="position:absolute; left:{x + 0.12 + i * step:.3f}in; top:{y:.3f}in; width:{size[0]}in; height:{size[1]}in; background:{color}; border-radius:0.015in"></div>'
        for i in range(int((w - 0.2) / step)))


def _vertical(x, y, text, pt, color, extra="", gap=1.18):
    """竖排文字：逐字一行，从上到下；x,y 为左上角（英寸）。"""
    chars = "".join(f'<div style="line-height:{gap}">{esc(ch)}</div>' for ch in text if ch.strip())
    return f'<div style="position:absolute; left:{x:.3f}in; top:{y:.3f}in; width:{pt / 72 * 1.05:.3f}in; text-align:center; font-size:{pt}pt; color:{color}; {extra}">{chars}</div>'


def _abs(x, y, w, extra, inner):
    return f'<div style="position:absolute; left:{x:.3f}in; top:{y:.3f}in; width:{w:.3f}in; {extra}">{inner}</div>'


# ---------------------------------------------------------------- A 纸本竖排
def paper(lang, x, y, w, h, br, c):
    ink, cream, gold = "#1b1a17", "#f4eddc", "#b8933f"
    vt = "writing-mode: vertical-rl; text-orientation: upright;"
    out = [f'<div style="position:absolute; left:{x}in; top:{y}in; width:{w + br}in; height:{h}in; background:{cream}"></div>',
           # 淡金色日轮，在书名上端之后
           f'<div style="position:absolute; left:{x + w - 2.55:.3f}in; top:{y + 0.55:.3f}in; width:2.0in; height:2.0in; border-radius:50%; background:#e9d9a8; opacity:0.55"></div>',
           _holes_v(x + 0.10, y, h, "#d9cdb0"),
           # 书名竖排（逐字堆叠）
           _vertical(x + w - 1.75, y + 0.85, c["title"], 66, ink, "font-weight:700", gap=1.16),
           _vertical(x + w - 2.35, y + 1.0, c["subtitle"], 14, "#5a5040", gap=1.45),
           _vertical(x + w - 2.75, y + 1.0, c["kicker"], 8.5, gold, gap=1.7),
           # 左下：经文与作者
           _abs(x + 0.55, y + h - 2.35, 2.6, f"font-size:9pt; line-height:1.9; color:#5a5040", f'{esc(c["verse"])}<br><span style="color:{gold}; letter-spacing:0.15em">{esc(c["ref"])}</span>'),
           _abs(x + 0.55, y + h - 1.05, 3.0, f"font-size:13pt; letter-spacing:0.35em; color:{ink}", esc(c["author_line"])),
           _abs(x + 0.55, y + h - 0.68, 3.5, f"font-size:6.5pt; letter-spacing:0.1em; color:#8a7f6a", esc(c["en_title"]))]
    return "".join(out)


paper.palette = {"bg": "#f4eddc", "fg": "#1b1a17", "accent": "#b8933f", "muted": "#5a5040"}


# ---------------------------------------------------------------- B 黑底大字
def slab(lang, x, y, w, h, br, c):
    bg, cream, gold = "#0d0d10", "#f3ecdb", "#c9a35e"
    lines = "".join(f'<div style="line-height:1.1">{esc(l)}</div>' for l in c["lines"])
    pt = 88 if len(c["lines"]) > 1 else 72
    out = [f'<div style="position:absolute; left:{x}in; top:{y}in; width:{w + br}in; height:{h}in; background:{bg}"></div>',
           _abs(x + 0.6, y + 0.7, w - 1.2, f"font-size:8pt; letter-spacing:0.4em; color:{gold}", f'✦ {esc(c["kicker"])} ✦'),
           _abs(x + 0.6, y + 1.35, w - 1.0, f"font-size:{pt}pt; font-weight:700; letter-spacing:0.06em; color:{cream}", lines),
           # 一道从左射入的光缝
           f'<div style="position:absolute; left:{x - 0.2:.3f}in; top:{y + 4.55:.3f}in; width:{w + br + 0.2:.3f}in; height:0.5in; background:linear-gradient(90deg, rgba(246,220,156,0.28), rgba(246,220,156,0) 75%)"></div>',
           f'<div style="position:absolute; left:{x - 0.2:.3f}in; top:{y + 4.76:.3f}in; width:{w + br + 0.2:.3f}in; height:0.06in; background:linear-gradient(90deg, #f6dc9c, rgba(246,220,156,0) 85%)"></div>',
           _abs(x + 0.6, y + 5.1, w - 1.2, f"font-size:16pt; letter-spacing:0.2em; color:{cream}", esc(c["subtitle"])),
           _abs(x + 0.6, y + 5.55, w - 1.2, f"font-size:9pt; letter-spacing:0.2em; color:{gold}", esc(c["ref"])),
           _abs(x + 0.6, y + 5.85, w - 1.2, f"font-size:7pt; letter-spacing:0.1em; color:#8f8776", esc(c["en_title"])),
           _abs(x + 0.6, y + h - 1.05, w - 1.2, f"font-size:13pt; letter-spacing:0.35em; color:{cream}", esc(c["author_line"])),
           _holes_h(x, y + h - 0.32, w + br, "#2a2a30")]
    return "".join(out)


slab.palette = {"bg": "#0d0d10", "fg": "#f3ecdb", "accent": "#c9a35e", "muted": "#8f8776"}


# ---------------------------------------------------------------- C 门缝透光
def door(lang, x, y, w, h, br, c):
    dark, cream, ink, gold = "#0d0d10", "#f4eddc", "#1b1a17", "#b8933f"
    split = x + w * 0.64
    vt = "writing-mode: vertical-rl; text-orientation: upright;"
    lines = "".join(f'<div style="line-height:1.12">{esc(l)}</div>' for l in c["lines"])
    out = [f'<div style="position:absolute; left:{x}in; top:{y}in; width:{w + br}in; height:{h}in; background:{cream}"></div>',
           f'<div style="position:absolute; left:{x}in; top:{y}in; width:{split - x:.3f}in; height:{h}in; background:{dark}"></div>',
           # 门缝：暗部边缘一条渐亮的光
           f'<div style="position:absolute; left:{split - 0.55:.3f}in; top:{y}in; width:0.55in; height:{h}in; background:linear-gradient(90deg, rgba(246,220,156,0), rgba(246,220,156,0.55))"></div>',
           f'<div style="position:absolute; left:{split - 0.02:.3f}in; top:{y}in; width:0.05in; height:{h}in; background:#f6dc9c"></div>',
           f'<div style="position:absolute; left:{split:.3f}in; top:{y}in; width:1.2in; height:{h}in; background:linear-gradient(90deg, rgba(246,220,156,0.7), rgba(246,220,156,0))"></div>',
           _abs(x + 0.5, y + 0.7, split - x - 0.7, f"font-size:8pt; letter-spacing:0.35em; color:{gold}", f'✦ {esc(c["kicker"])} ✦'),
           _abs(x + 0.5, y + 1.35, split - x - 0.5, f"font-size:56pt; font-weight:700; letter-spacing:0.04em; color:{cream}", lines),
           _abs(x + 0.5, y + 4.6, split - x - 0.7, f"font-size:9pt; line-height:1.9; color:#cfc4a8", f'{esc(c["verse"])}<br><span style="color:{gold}; letter-spacing:0.15em">{esc(c["ref"])}</span>'),
           _abs(x + 0.5, y + h - 1.05, split - x - 0.7, f"font-size:13pt; letter-spacing:0.35em; color:{cream}", esc(c["author_line"])),
           # 亮部：竖排副标题（逐字堆叠）
           _vertical(split + 0.95, y + 0.95, c["subtitle"], 16, ink, gap=1.5),
           _abs(split + 0.35, y + h - 1.6, w - (split - x) - 0.7, f"font-size:6.5pt; line-height:1.6; letter-spacing:0.05em; color:#8a7f6a", esc(c["en_title"]))]
    return "".join(out)


door.palette = {"bg": "#0d0d10", "fg": "#f3ecdb", "accent": "#b8933f", "muted": "#cfc4a8"}


# ---------------------------------------------------------------- D 胶片格
def frame(lang, x, y, w, h, br, c):
    cream, ink, black, gold = "#f4eddc", "#1b1a17", "#111114", "#b8933f"
    top, bh = y + 2.35, 3.35
    lines = "".join(f'<div style="line-height:1.12">{esc(l)}</div>' for l in c["lines"])
    out = [f'<div style="position:absolute; left:{x}in; top:{y}in; width:{w + br}in; height:{h}in; background:{cream}"></div>',
           _abs(x, y + 0.75, w, f"text-align:center; font-size:8.5pt; letter-spacing:0.4em; color:{gold}", f'✦ {esc(c["kicker"])} ✦'),
           _abs(x, y + 1.25, w, f"text-align:center; font-size:9.5pt; line-height:1.9; color:#5a5040", f'{esc(c["verse"])}<br><span style="color:{gold}; letter-spacing:0.15em">{esc(c["ref"])}</span>'),
           # 一格 35mm 胶片
           f'<div style="position:absolute; left:{x - 0.2:.3f}in; top:{top:.3f}in; width:{w + br + 0.2:.3f}in; height:{bh}in; background:{black}"></div>',
           _holes_h(x - 0.2, top + 0.14, w + br + 0.2, cream, step=0.34, size=(0.2, 0.13)),
           _holes_h(x - 0.2, top + bh - 0.27, w + br + 0.2, cream, step=0.34, size=(0.2, 0.13)),
           _abs(x, top + 0.62, w, f"text-align:center; font-size:70pt; font-weight:700; letter-spacing:0.08em; color:{cream}", lines),
           _abs(x, top + bh + 0.55, w, f"text-align:center; font-size:16pt; letter-spacing:0.22em; color:{ink}", esc(c["subtitle"])),
           _abs(x, top + bh + 0.98, w, f"text-align:center; font-size:7pt; letter-spacing:0.1em; color:#8a7f6a", esc(c["en_title"])),
           _abs(x, y + h - 1.05, w, f"text-align:center; font-size:13pt; letter-spacing:0.35em; color:{ink}", esc(c["author_line"]))]
    return "".join(out)


frame.palette = {"bg": "#f4eddc", "fg": "#1b1a17", "accent": "#b8933f", "muted": "#5a5040"}


# ---------------------------------------------------------------- E 夜与一盏灯
def night(lang, x, y, w, h, br, c):
    import random
    navy, warm, gold = "#101626", "#f5efe0", "#e3c47a"
    rnd = random.Random(3)
    stars = "".join(f'<div style="position:absolute; left:{x + rnd.random() * (w + br):.3f}in; top:{y + rnd.random() * h * 0.62:.3f}in; width:{0.012 + rnd.random() * 0.02:.3f}in; height:{0.012 + rnd.random() * 0.02:.3f}in; border-radius:50%; background:{warm}; opacity:{0.25 + rnd.random() * 0.6:.2f}"></div>'
                    for _ in range(90))
    hz = y + h * 0.70
    lines = "".join(f'<div style="line-height:1.12">{esc(l)}</div>' for l in c["lines"])
    out = [f'<div style="position:absolute; left:{x}in; top:{y}in; width:{w + br}in; height:{h}in; background:linear-gradient(180deg, #0b1020 0%, {navy} 55%, #1a2440 100%)"></div>',
           stars,
           # 地平线与一扇亮着的窗
           f'<div style="position:absolute; left:{x}in; top:{hz:.3f}in; width:{w + br}in; height:{y + h - hz:.3f}in; background:#0a0d16"></div>',
           f'<div style="position:absolute; left:{x + w * 0.5 - 0.9:.3f}in; top:{hz - 0.9:.3f}in; width:1.8in; height:1.8in; border-radius:50%; background:radial-gradient(circle, rgba(246,220,156,0.55), rgba(246,220,156,0) 70%)"></div>',
           f'<div style="position:absolute; left:{x + w * 0.5 - 0.09:.3f}in; top:{hz - 0.22:.3f}in; width:0.18in; height:0.22in; background:{gold}"></div>',
           _abs(x, y + 0.75, w, f"text-align:center; font-size:8.5pt; letter-spacing:0.4em; color:{gold}", f'✦ {esc(c["kicker"])} ✦'),
           _abs(x, y + 1.35, w, f"text-align:center; font-size:72pt; font-weight:700; letter-spacing:0.08em; color:{warm}", lines),
           _abs(x + w / 2 - 0.35, y + 4.35, 0.7, f"height:1pt; background:{gold}", ""),
           _abs(x, y + 4.5, w, f"text-align:center; font-size:9pt; letter-spacing:0.25em; color:{gold}", esc(c["ref"])),
           _abs(x, hz + 0.45, w, f"text-align:center; font-size:15pt; letter-spacing:0.22em; color:{warm}", esc(c["subtitle"])),
           _abs(x, hz + 0.88, w, f"text-align:center; font-size:7pt; letter-spacing:0.1em; color:#8f93a3", esc(c["en_title"])),
           _abs(x, y + h - 0.95, w, f"text-align:center; font-size:13pt; letter-spacing:0.35em; color:{warm}", esc(c["author_line"]))]
    return "".join(out)


night.palette = {"bg": "#101626", "fg": "#f5efe0", "accent": "#e3c47a", "muted": "#8f93a3"}


# ---------------------------------------------------------------- F 导火线（慢慢地动怒）
def fuse(lang, x, y, w, h, br, c):
    import random
    bg, cream, amber, muted = "#14151a", "#f3ecdb", "#d9a441", "#9a9384"
    W = w + br
    lines = "".join(f'<div style="line-height:1.1">{esc(l)}</div>' for l in c["lines"])
    # 导火线：从右下角进入，蜿蜒到左侧中下部的火星；后面是烧过的灰痕
    sx, sy = 1.05, h - 2.55
    path = f"M {W:.2f},{h - 1.05:.2f} C {w * 0.72:.2f},{h - 1.05:.2f} {w * 0.58:.2f},{h - 2.15:.2f} {w * 0.40:.2f},{h - 2.25:.2f} S {sx + 0.6:.2f},{sy + 0.05:.2f} {sx:.2f},{sy:.2f}"
    ash = f"M {sx:.2f},{sy:.2f} C {sx - 0.35:.2f},{sy - 0.05:.2f} {0.55:.2f},{sy - 0.35:.2f} {0.35:.2f},{sy - 0.6:.2f}"
    rnd = random.Random(19)
    sparks = "".join(f'<circle cx="{sx + rnd.uniform(-0.28, 0.28):.3f}" cy="{sy + rnd.uniform(-0.3, 0.2):.3f}" r="{rnd.uniform(0.008, 0.022):.3f}" fill="#ffd27a" opacity="{rnd.uniform(0.35, 0.9):.2f}"/>'
                     for _ in range(14))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}in" height="{h}in" viewBox="0 0 {W} {h}" style="position:absolute; left:{x}in; top:{y}in">
  <defs>
    <radialGradient id="ember" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#fff1c4" stop-opacity="1"/><stop offset="0.25" stop-color="#ffb347" stop-opacity="0.85"/>
      <stop offset="0.6" stop-color="#c2542a" stop-opacity="0.25"/><stop offset="1" stop-color="#14151a" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="vig" cx="0.5" cy="0.45" r="0.75">
      <stop offset="0" stop-color="#1d1e25"/><stop offset="1" stop-color="{bg}"/>
    </radialGradient>
  </defs>
  <rect x="0" y="0" width="{W}" height="{h}" fill="url(#vig)"/>
  <path d="{path}" fill="none" stroke="#3a3b44" stroke-width="0.075" stroke-linecap="round"/>
  <path d="{path}" fill="none" stroke="#cdb98e" stroke-width="0.045" stroke-linecap="round"/>
  <path d="{ash}" fill="none" stroke="#4a4a50" stroke-width="0.04" stroke-linecap="round" stroke-dasharray="0.03 0.05"/>
  <circle cx="{sx:.3f}" cy="{sy:.3f}" r="0.55" fill="url(#ember)"/>
  <circle cx="{sx:.3f}" cy="{sy:.3f}" r="0.05" fill="#fff6d6"/>
  {sparks}
</svg>'''
    out = [svg,
           _abs(x + 0.6, y + 0.7, w - 1.2, f"font-size:8pt; letter-spacing:0.4em; color:{amber}", f'✦ {esc(c["kicker"])} ✦'),
           _abs(x + 0.6, y + 1.2, w - 1.0, f"font-size:84pt; font-weight:700; letter-spacing:0.05em; color:{cream}", lines),
           _abs(x + 0.62, y + 4.05, 0.7, f"height:1pt; background:{amber}", ""),
           _abs(x + 0.6, y + 4.2, w - 1.2, f"font-size:9pt; letter-spacing:0.25em; color:{amber}", esc(c["ref"])),
           _abs(x + 0.6, y + 4.55, w - 1.2, f"font-size:16pt; letter-spacing:0.2em; color:{cream}", esc(c["subtitle"])),
           _abs(x + 0.6, y + 4.98, w - 1.2, f"font-size:7pt; letter-spacing:0.1em; color:{muted}", esc(c["en_title"])),
           _abs(x + 0.6, y + h - 1.0, w - 1.2, f"font-size:13pt; letter-spacing:0.35em; color:{cream}", esc(c["author_line"]))]
    return "".join(out)


fuse.palette = {"bg": "#14151a", "fg": "#f3ecdb", "accent": "#d9a441", "muted": "#9a9384"}


# ================================================================ 浅色底系列（十选一）

def _base(x, y, w, h, br, bg, extra=""):
    return f'<div style="position:absolute; left:{x}in; top:{y}in; width:{w + br}in; height:{h}in; background:{bg}; {extra}"></div>'


def _stack(x, y, w, h, c, fg, accent, muted, title_pt=80, top=1.3, align="center", sub_gap=0.45):
    """居中/左对齐的通用文字堆：标签、书名两行、金线、经文出处、副标题、英文、作者。返回 (html, 书名底部 y)。"""
    lines = "".join(f'<div style="line-height:1.1">{esc(l)}</div>' for l in c["lines"])
    lx = x + 0.6
    ta = f"text-align:{align};"
    rule_left = x + w / 2 - 0.35 if align == "center" else lx
    tb = y + top + 1.1 * len(c["lines"]) * title_pt / 72
    html = "".join([
        _abs(lx, y + 0.7, w - 1.2, f"{ta} font-size:8pt; letter-spacing:0.4em; color:{accent}", f'✦ {esc(c["kicker"])} ✦'),
        _abs(lx, y + top, w - 1.2, f"{ta} font-size:{title_pt}pt; font-weight:700; letter-spacing:0.05em; color:{fg}", lines),
        _abs(rule_left, tb + 0.18, 0.7, f"height:1pt; background:{accent}", ""),
        _abs(lx, tb + 0.32, w - 1.2, f"{ta} font-size:9pt; letter-spacing:0.25em; color:{accent}", esc(c["ref"])),
        _abs(lx, tb + 0.32 + sub_gap, w - 1.2, f"{ta} font-size:16pt; letter-spacing:0.2em; color:{fg}", esc(c["subtitle"])),
        _abs(lx, tb + 0.32 + sub_gap + 0.42, w - 1.2, f"{ta} font-size:7pt; letter-spacing:0.1em; color:{muted}", esc(c["en_title"])),
        _abs(lx, y + h - 1.0, w - 1.2, f"{ta} font-size:13pt; letter-spacing:0.35em; color:{fg}", esc(c["author_line"])),
    ])
    return html, tb


# 1 米纸 · 导火线
def fuse_light(lang, x, y, w, h, br, c):
    import random
    bg, ink, amber, muted = "#f4eddc", "#1b1a17", "#b8862b", "#8a7f6a"
    W = w + br
    sx, sy = 1.05, h - 2.45
    path = f"M {W:.2f},{h - 1.0:.2f} C {w * 0.72:.2f},{h - 1.0:.2f} {w * 0.58:.2f},{h - 2.1:.2f} {w * 0.40:.2f},{h - 2.2:.2f} S {sx + 0.6:.2f},{sy + 0.05:.2f} {sx:.2f},{sy:.2f}"
    ash = f"M {sx:.2f},{sy:.2f} C {sx - 0.35:.2f},{sy - 0.05:.2f} 0.55,{sy - 0.35:.2f} 0.35,{sy - 0.6:.2f}"
    rnd = random.Random(19)
    sparks = "".join(f'<circle cx="{sx + rnd.uniform(-0.28, 0.28):.3f}" cy="{sy + rnd.uniform(-0.3, 0.2):.3f}" r="{rnd.uniform(0.008, 0.022):.3f}" fill="#e08a1e" opacity="{rnd.uniform(0.35, 0.9):.2f}"/>' for _ in range(14))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}in" height="{h}in" viewBox="0 0 {W} {h}" style="position:absolute; left:{x}in; top:{y}in">
  <defs><radialGradient id="emb" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#fff0c0"/><stop offset="0.3" stop-color="#f2a93b" stop-opacity="0.9"/><stop offset="0.65" stop-color="#e08a1e" stop-opacity="0.25"/><stop offset="1" stop-color="{bg}" stop-opacity="0"/></radialGradient></defs>
  <rect width="{W}" height="{h}" fill="{bg}"/>
  <path d="{path}" fill="none" stroke="#3a3328" stroke-width="0.05" stroke-linecap="round"/>
  <path d="{ash}" fill="none" stroke="#b8ae9c" stroke-width="0.04" stroke-linecap="round" stroke-dasharray="0.03 0.05"/>
  <circle cx="{sx}" cy="{sy}" r="0.5" fill="url(#emb)"/><circle cx="{sx}" cy="{sy}" r="0.045" fill="#fff6d6"/>{sparks}
</svg>'''
    html, _ = _stack(x, y, w, h, c, ink, amber, muted, title_pt=84, top=1.2, align="left")
    return svg + html


fuse_light.palette = {"bg": "#f4eddc", "fg": "#1b1a17", "accent": "#b8862b", "muted": "#8a7f6a"}


# 2 朱红圆 · 竖排
def seal(lang, x, y, w, h, br, c):
    bg, ink, red, gold = "#f5efe2", "#1b1a17", "#c0392b", "#b8933f"
    out = [_base(x, y, w, h, br, bg),
           f'<div style="position:absolute; left:{x + 0.5:.3f}in; top:{y + 0.9:.3f}in; width:2.7in; height:2.7in; border-radius:50%; background:{red}"></div>',
           _vertical(x + w - 1.55, y + 0.9, c["title"], 70, ink, "font-weight:700", gap=1.14),
           _vertical(x + w - 2.1, y + 1.0, c["subtitle"], 14, "#5a5040", gap=1.45),
           _abs(x + 0.5, y + 0.45, 3.0, f"font-size:8pt; letter-spacing:0.35em; color:{gold}", f'✦ {esc(c["kicker"])} ✦'),
           _abs(x + 0.55, y + h - 2.5, 2.8, f"font-size:9pt; line-height:1.9; color:#5a5040", f'{esc(c["verse"])}<br><span style="color:{gold}; letter-spacing:0.15em">{esc(c["ref"])}</span>'),
           _abs(x + 0.55, y + h - 1.05, 3.0, f"font-size:13pt; letter-spacing:0.35em; color:{ink}", esc(c["author_line"])),
           _abs(x + 0.55, y + h - 0.68, 3.6, f"font-size:6.5pt; letter-spacing:0.08em; color:#8a7f6a", esc(c["en_title"]))]
    return "".join(out)


seal.palette = {"bg": "#f5efe2", "fg": "#1b1a17", "accent": "#c0392b", "muted": "#5a5040"}


# 3 水面涟漪
def ripple(lang, x, y, w, h, br, c):
    bg, ink, accent, muted = "#e6ecec", "#1f2a33", "#7a8d92", "#6b7b80"
    W = w + br
    cx, cy = w / 2, h * 0.80
    rings = "".join(f'<circle cx="{cx}" cy="{cy}" r="{0.3 + i * 0.34:.2f}" fill="none" stroke="#9fb0b4" stroke-width="{0.012 if i else 0.02}" opacity="{max(0.15, 0.8 - i * 0.1):.2f}"/>' for i in range(6))
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}in" height="{h}in" viewBox="0 0 {W} {h}" style="position:absolute; left:{x}in; top:{y}in"><rect width="{W}" height="{h}" fill="{bg}"/>{rings}<circle cx="{cx}" cy="{cy}" r="0.05" fill="{ink}"/></svg>'
    html, _ = _stack(x, y, w, h, c, ink, accent, muted, title_pt=78, top=1.25)
    return svg + html


ripple.palette = {"bg": "#e6ecec", "fg": "#1f2a33", "accent": "#7a8d92", "muted": "#6b7b80"}


# 4 赭红底 · 米色大字
def terracotta(lang, x, y, w, h, br, c):
    bg, cream, gold, muted = "#b5563a", "#f6ecdc", "#f0cf85", "#eed3bd"
    html, _ = _stack(x, y, w, h, c, cream, gold, muted, title_pt=86, top=1.3)
    thin = f'<div style="position:absolute; left:{x + 0.45:.3f}in; top:{y + 0.45:.3f}in; width:{w - 0.9:.3f}in; height:{h - 0.9:.3f}in; border:1pt solid rgba(246,236,220,0.45)"></div>'
    return _base(x, y, w, h, br, bg) + thin + html


terracotta.palette = {"bg": "#b5563a", "fg": "#f6ecdc", "accent": "#f0cf85", "muted": "#eed3bd"}


# 5 灰绿底 · 一线金
def sage(lang, x, y, w, h, br, c):
    bg, cream, gold, muted = "#8c9a86", "#f6f2e8", "#e6c77a", "#e2e6dc"
    html, _ = _stack(x, y, w, h, c, cream, gold, muted, title_pt=84, top=1.35)
    line = f'<div style="position:absolute; left:{x}in; top:{y + h * 0.62:.3f}in; width:{w + br}in; height:1.5pt; background:{gold}; opacity:0.85"></div>'
    return _base(x, y, w, h, br, bg) + line + html


sage.palette = {"bg": "#8c9a86", "fg": "#f6f2e8", "accent": "#e6c77a", "muted": "#e2e6dc"}


# 6 赭黄底 · 胶片边
def ochre(lang, x, y, w, h, br, c):
    bg, brown, cream = "#d9a441", "#3b2a14", "#fbf3e2"
    html, _ = _stack(x, y, w, h, c, brown, brown, "#6b5535", title_pt=86, top=1.35)
    strip = (f'<div style="position:absolute; left:{x}in; top:{y + h - 1.75:.3f}in; width:{w + br}in; height:0.55in; background:{brown}"></div>'
             + _holes_h(x, y + h - 1.75 + 0.08, w + br, bg, step=0.34, size=(0.2, 0.11))
             + _holes_h(x, y + h - 1.75 + 0.36, w + br, bg, step=0.34, size=(0.2, 0.11)))
    return _base(x, y, w, h, br, bg) + strip + html.replace(f"top:{y + h - 1.0:.3f}in", f"top:{y + h - 0.95:.3f}in")


ochre.palette = {"bg": "#d9a441", "fg": "#3b2a14", "accent": "#3b2a14", "muted": "#6b5535"}


# 7 米纸 + 底部红带
def split_red(lang, x, y, w, h, br, c):
    cream, ink, red, gold = "#f4eddc", "#1b1a17", "#a63d2f", "#b8933f"
    band_top = y + h * 0.70
    lines = "".join(f'<div style="line-height:1.1">{esc(l)}</div>' for l in c["lines"])
    out = [_base(x, y, w, h, br, cream),
           f'<div style="position:absolute; left:{x}in; top:{band_top:.3f}in; width:{w + br}in; height:{y + h - band_top:.3f}in; background:{red}"></div>',
           _abs(x + 0.6, y + 0.7, w - 1.2, f"font-size:8pt; letter-spacing:0.4em; color:{gold}", f'✦ {esc(c["kicker"])} ✦'),
           _abs(x + 0.6, y + 1.25, w - 1.0, f"font-size:86pt; font-weight:700; letter-spacing:0.05em; color:{ink}", lines),
           _abs(x + 0.6, y + 4.35, w - 1.2, f"font-size:9pt; line-height:1.9; color:#5a5040", f'{esc(c["verse"])}<br><span style="color:{gold}; letter-spacing:0.15em">{esc(c["ref"])}</span>'),
           _abs(x + 0.6, band_top + 0.55, w - 1.2, f"font-size:17pt; letter-spacing:0.2em; color:#f6ecdc", esc(c["subtitle"])),
           _abs(x + 0.6, band_top + 1.0, w - 1.2, f"font-size:7pt; letter-spacing:0.1em; color:#eed3bd", esc(c["en_title"])),
           _abs(x + 0.6, y + h - 0.95, w - 1.2, f"font-size:13pt; letter-spacing:0.35em; color:#f6ecdc", esc(c["author_line"]))]
    return "".join(out)


split_red.palette = {"bg": "#f4eddc", "fg": "#1b1a17", "accent": "#a63d2f", "muted": "#5a5040"}


# 8 灰蓝底 · 一点余烬
def dusk(lang, x, y, w, h, br, c):
    bg, cream, gold, muted = "#4f6274", "#f5efe0", "#e3c47a", "#c9d2da"
    W = w + br
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}in" height="{h}in" viewBox="0 0 {W} {h}" style="position:absolute; left:{x}in; top:{y}in">
  <defs><linearGradient id="dk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5b6f82"/><stop offset="1" stop-color="#3f5163"/></linearGradient>
  <radialGradient id="em2" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#fff0c0"/><stop offset="0.35" stop-color="#f2a93b" stop-opacity="0.8"/><stop offset="1" stop-color="#3f5163" stop-opacity="0"/></radialGradient></defs>
  <rect width="{W}" height="{h}" fill="url(#dk)"/>
  <circle cx="{w / 2}" cy="{h * 0.70}" r="0.7" fill="url(#em2)"/><circle cx="{w / 2}" cy="{h * 0.70}" r="0.06" fill="#fff6d6"/>
</svg>'''
    html, _ = _stack(x, y, w, h, c, cream, gold, muted, title_pt=82, top=1.3)
    return svg + html


dusk.palette = {"bg": "#4f6274", "fg": "#f5efe0", "accent": "#e3c47a", "muted": "#c9d2da"}


# 9 水印大字 · 竖排
def watermark(lang, x, y, w, h, br, c):
    bg, ink, gold = "#f7f3ea", "#1b1a17", "#b8933f"
    big = c["title"][-1]  # 最后一个字（怒）作淡水印
    out = [_base(x, y, w, h, br, bg),
           _abs(x - 0.3, y + 1.6, w + 0.6, f"text-align:center; font-size:300pt; font-weight:700; color:#e9e2d2; line-height:1", esc(big)),
           _vertical(x + w / 2 - 0.5, y + 1.15, c["title"], 68, ink, "font-weight:700", gap=1.14),
           _abs(x, y + 0.7, w, f"text-align:center; font-size:8pt; letter-spacing:0.4em; color:{gold}", f'✦ {esc(c["kicker"])} ✦'),
           _abs(x, y + h - 2.2, w, f"text-align:center; font-size:9pt; letter-spacing:0.25em; color:{gold}", esc(c["ref"])),
           _abs(x, y + h - 1.85, w, f"text-align:center; font-size:15pt; letter-spacing:0.22em; color:{ink}", esc(c["subtitle"])),
           _abs(x, y + h - 1.45, w, f"text-align:center; font-size:7pt; letter-spacing:0.1em; color:#8a7f6a", esc(c["en_title"])),
           _abs(x, y + h - 0.95, w, f"text-align:center; font-size:13pt; letter-spacing:0.35em; color:{ink}", esc(c["author_line"]))]
    return "".join(out)


watermark.palette = {"bg": "#f7f3ea", "fg": "#1b1a17", "accent": "#b8933f", "muted": "#8a7f6a"}


# 10 暖白 · 沙漏细线
def hourglass(lang, x, y, w, h, br, c):
    bg, ink, gold, muted = "#faf6ee", "#1b1a17", "#b8933f", "#8a7f6a"
    W = w + br
    cx, top, bh = w / 2, h * 0.60, 1.9
    hw = 0.75
    # 沙漏轮廓 + 上半沙面（还剩很多）+ 下半一小堆 + 细流
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}in" height="{h}in" viewBox="0 0 {W} {h}" style="position:absolute; left:{x}in; top:{y}in">
  <rect width="{W}" height="{h}" fill="{bg}"/>
  <path d="M {cx - hw},{top} L {cx + hw},{top} L {cx + 0.06},{top + bh / 2} L {cx + hw},{top + bh} L {cx - hw},{top + bh} L {cx - 0.06},{top + bh / 2} Z" fill="none" stroke="{ink}" stroke-width="0.022" stroke-linejoin="round"/>
  <line x1="{cx - hw - 0.15}" y1="{top}" x2="{cx + hw + 0.15}" y2="{top}" stroke="{ink}" stroke-width="0.035"/>
  <line x1="{cx - hw - 0.15}" y1="{top + bh}" x2="{cx + hw + 0.15}" y2="{top + bh}" stroke="{ink}" stroke-width="0.035"/>
  <path d="M {cx - hw + 0.28},{top + 0.55} Q {cx},{top + 0.42} {cx + hw - 0.28},{top + 0.55} L {cx + 0.05},{top + bh / 2 - 0.04} L {cx - 0.05},{top + bh / 2 - 0.04} Z" fill="{gold}" opacity="0.85"/>
  <line x1="{cx}" y1="{top + bh / 2}" x2="{cx}" y2="{top + bh - 0.22}" stroke="{gold}" stroke-width="0.02" stroke-dasharray="0.03 0.04"/>
  <path d="M {cx - 0.3},{top + bh - 0.02} Q {cx},{top + bh - 0.32} {cx + 0.3},{top + bh - 0.02} Z" fill="{gold}" opacity="0.85"/>
</svg>'''
    html, _ = _stack(x, y, w, h, c, ink, gold, muted, title_pt=80, top=1.25)
    return svg + html


hourglass.palette = {"bg": "#faf6ee", "fg": "#1b1a17", "accent": "#b8933f", "muted": "#8a7f6a"}


DESIGNS = {
    "fuse_light": ("米纸导火线", fuse_light),
    "seal": ("朱红圆竖排", seal),
    "ripple": ("水面涟漪", ripple),
    "terracotta": ("赭红底", terracotta),
    "sage": ("灰绿底", sage),
    "ochre": ("赭黄胶片边", ochre),
    "split_red": ("米纸红带", split_red),
    "dusk": ("灰蓝余烬", dusk),
    "watermark": ("水印竖排", watermark),
    "hourglass": ("沙漏", hourglass),
    "fuse": ("导火线", fuse),
    "paper": ("纸本竖排", paper),
    "slab": ("黑底大字", slab),
    "door": ("门缝透光", door),
    "frame": ("胶片格", frame),
    "night": ("夜与一盏灯", night),
}
