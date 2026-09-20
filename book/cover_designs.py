"""封面正面的几套设计。每套是一个函数：(lang, x, y, w, h, bleed_right, ctx) -> HTML 片段。

ctx 里有：title / lines（书名按字数拆成 1–2 行）/ subtitle / author_line / kicker / ref / verse / en_title / ff（字体）。
坐标单位英寸；(x, y) 是封面正面左上角，w×h 是成品尺寸，bleed_right 是右侧出血（电子书为 0）。
每套设计附一个 palette：bg / fg / accent，供封底与书脊配色。

在 book.json 的 cover.design 里选用：paper | slab | door | frame | night | beam
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


DESIGNS = {
    "paper": ("纸本竖排", paper),
    "slab": ("黑底大字", slab),
    "door": ("门缝透光", door),
    "frame": ("胶片格", frame),
    "night": ("夜与一盏灯", night),
}
