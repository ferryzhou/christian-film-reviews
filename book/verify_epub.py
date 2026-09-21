#!/usr/bin/env python3
"""用 Chromium（Playwright）逐章渲染 dist/*.epub，核对每张图：图片是否加载、图注与下一段的间距。

用法：pip install playwright pillow && python3 verify_epub.py [--shots]
（若未下载浏览器：playwright install chromium；或设 CHROME=/path/to/chromium）
--shots 会把每张图附近截图拼成对比图，写到 dist/verify/。
"""
import glob, io, json, os, sys, zipfile, tempfile
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "dist")
JS = """() => {
  const fs = parseFloat(getComputedStyle(document.body).fontSize);
  const figs = [...document.querySelectorAll('figure')].map((f, i) => {
    const img = f.querySelector('img'), cap = f.querySelector('figcaption'), nxt = f.nextElementSibling;
    const r = {i, img_ok: !!(img && img.complete && img.naturalWidth > 0), next: nxt ? nxt.tagName : '', gap_em: null,
               top: cap ? cap.getBoundingClientRect().top + scrollY : 0, bottom: cap ? cap.getBoundingClientRect().bottom + scrollY : 0};
    if (cap && nxt) r.gap_em = +((nxt.getBoundingClientRect().top - cap.getBoundingClientRect().bottom) / fs).toFixed(2);
    return r;
  });
  const bad = [...document.images].filter(i => !(i.complete && i.naturalWidth > 0)).map(i => i.getAttribute('src'));
  return {figs, bad};
}"""


def main():
    shots = "--shots" in sys.argv
    exe = os.environ.get("CHROME") or ("/opt/pw-browsers/chromium" if os.path.exists("/opt/pw-browsers/chromium") else None)
    ok = True
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=exe) if exe else pw.chromium.launch()
        for epub in sorted(glob.glob(os.path.join(DIST, "*.epub"))):
            name = os.path.basename(epub)
            with tempfile.TemporaryDirectory() as x:
                zipfile.ZipFile(epub).extractall(x)
                files = sorted(glob.glob(os.path.join(x, "EPUB", "*.xhtml")))
                pg = b.new_page(viewport={"width": 450, "height": 900})
                nfig, bad, gaps, gaps_reset, crops = 0, [], [], [], []
                for f in files:
                    pg.goto("file://" + f); pg.wait_for_load_state("load")
                    r = pg.evaluate(JS)
                    bad += [(os.path.basename(f), s) for s in r["bad"]]
                    if shots and r["figs"]:
                        from PIL import Image
                        full = Image.open(io.BytesIO(pg.screenshot(full_page=True)))
                    for fg in r["figs"]:
                        nfig += 1
                        if fg["gap_em"] is not None: gaps.append(fg["gap_em"])
                        if shots: crops.append(full.crop((0, int(fg["top"]) - 70, 450, int(fg["bottom"]) + 110)))
                    # 模拟把 figure 外边距清零的阅读器
                    pg.add_style_tag(content="figure{margin:0 !important} p{margin-top:0 !important}")
                    gaps_reset += [fg["gap_em"] for fg in pg.evaluate(JS)["figs"] if fg["gap_em"] is not None]
                pg.close()
            print(f"== {name}: {len(files)} 个页面文件，{nfig} 张图，加载失败 {len(bad)}")
            if gaps:
                print(f"   图注→下一段间距：{min(gaps)}–{max(gaps)} em；阅读器清零 figure 边距后：{min(gaps_reset)}–{max(gaps_reset)} em")
            if bad or (gaps and min(gaps_reset) < 0.8):
                ok = False; print("   !! 有问题：", bad[:5])
            if shots and crops:
                from PIL import Image
                out = os.path.join(DIST, "verify"); os.makedirs(out, exist_ok=True)
                per, W, H = 18, 450, max(c.size[1] for c in crops)
                for si in range(0, len(crops), per):
                    sheet = Image.new("RGB", (W * 3 + 20, ((per + 2) // 3) * (H + 6)), "white")
                    for k, c in enumerate(crops[si:si + per]):
                        sheet.paste(c, ((k % 3) * (W + 10), (k // 3) * (H + 6)))
                    sheet.save(os.path.join(out, f"{name[:-5]}-figs-{si // per + 1:02d}.png"))
                print(f"   对比图 -> {out}/")
        b.close()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
