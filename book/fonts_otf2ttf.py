#!/usr/bin/env python3
"""把 CFF 轮廓的 OpenType 字体（.otf）转成 TrueType（.ttf），字体名不变。

Lulu 的 PDF 预检只接受 TrueType 轮廓，思源宋体（Noto Serif CJK）官方只提供 CFF 版；
把 ~/.fonts 里的 .otf 转成 .ttf 并替换后重跑 build_print.py，WeasyPrint 就会嵌入 TrueType。

用法：python3 fonts_otf2ttf.py [字体目录，默认 ~/.fonts]
"""
import os, sys, glob, time
from concurrent.futures import ProcessPoolExecutor

MAX_ERR = 1.0  # 曲线拟合误差（字体单位，1000 upm 下 1 单位肉眼不可见）


def otf2ttf(src):
    import traceback
    try:
        return _otf2ttf(src)
    except Exception:
        return f"{src} 失败：\n" + traceback.format_exc()


def _otf2ttf(src):
    from fontTools.ttLib import TTFont, newTable
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    from fontTools.pens.cu2quPen import Cu2QuPen
    t0 = time.time()
    f = TTFont(src)
    if "CFF " not in f:
        return f"{src}: 不是 CFF 字体，跳过"
    glyph_set = f.getGlyphSet()
    glyf = newTable("glyf")
    glyf.glyphOrder = f.getGlyphOrder()
    glyf.glyphs = {}
    for name in glyf.glyphOrder:
        pen = TTGlyphPen(glyph_set)
        glyph_set[name].draw(Cu2QuPen(pen, MAX_ERR, reverse_direction=True))
        glyf.glyphs[name] = pen.glyph()
    f["glyf"] = glyf
    f["loca"] = newTable("loca")
    maxp = f["maxp"] = newTable("maxp")
    maxp.tableVersion = 0x00010000
    maxp.maxZones = 1
    maxp.maxTwilightPoints = maxp.maxStorage = maxp.maxFunctionDefs = 0
    maxp.maxInstructionDefs = maxp.maxStackElements = maxp.maxSizeOfInstructions = 0
    maxp.maxComponentElements = max(len(getattr(g, "components", [])) for g in glyf.glyphs.values())
    # post 表改为 3.0（不带字形名；CJK 字体 6 万多字形，2.0 的 16 位名字索引会溢出），head 的 glyphDataFormat 置 0
    f["post"].formatType = 3.0
    for attr in ("extraNames", "mapping", "glyphOrder"):
        if hasattr(f["post"], attr):
            delattr(f["post"], attr)
    f["head"].glyphDataFormat = 0
    for tag in ("CFF ", "VORG"):
        if tag in f:
            del f[tag]
    f.sfntVersion = "\x00\x01\x00\x00"
    f.recalcBBoxes = True
    dst = os.path.splitext(src)[0] + ".ttf"
    f.save(dst)
    return f"{os.path.basename(src)} -> {os.path.basename(dst)}  {len(glyf.glyphOrder)} 字形，{time.time() - t0:.0f}s"


def main():
    d = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "~/.fonts")
    srcs = sorted(glob.glob(os.path.join(d, "*.otf")))
    if not srcs:
        print("没有 .otf 文件：", d); return
    with ProcessPoolExecutor() as ex:
        for msg in ex.map(otf2ttf, srcs):
            print(msg, flush=True)
    if not all(os.path.exists(os.path.splitext(s)[0] + ".ttf") for s in srcs):
        print("有文件未转换成功，未替换"); sys.exit(1)
    bak = os.path.join(os.path.dirname(d.rstrip("/")), "fonts-otf-backup")
    os.makedirs(bak, exist_ok=True)
    for s in srcs:  # 原件移出字体目录：fontconfig 按内容识别字体，留在原目录（哪怕改名 .bak）仍会被选中
        os.replace(s, os.path.join(bak, os.path.basename(s)))
    os.system("fc-cache -f >/dev/null 2>&1")
    print(f"已替换为 TTF；原 .otf 移到 {bak}")


if __name__ == "__main__":
    main()
