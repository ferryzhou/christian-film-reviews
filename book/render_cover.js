// 用 Chromium 把 cover.html 渲染成 1600×2560 JPEG（KDP 电子书封面规格）。
// 由 build_book.py 调用：node render_cover.js '{"title":..,"subtitle":..,"author":..,"tagline":..,"out":..}'
// 依赖全局或本地安装的 playwright（NODE_PATH 由 build_book.py 设置）。
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const opts = JSON.parse(process.argv[2]);
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");
const kicker = /[與體]/.test(opts.title + opts.subtitle) ? "✦ 電影隨筆集 ✦" : "✦ 电影随笔集 ✦";
let html = fs.readFileSync(path.join(__dirname, "cover.html"), "utf8")
  .replace(/\{\{HOLES\}\}/g, "<span></span>".repeat(30))
  .replace("{{TITLE}}", esc(opts.title))
  .replace("{{SUBTITLE}}", esc(opts.subtitle))
  .replace("{{TAGLINE}}", esc(opts.tagline))
  .replace("{{AUTHOR}}", esc(opts.author))
  .replace("✦ 电影随笔集 ✦", kicker);

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1600, height: 2560 }, deviceScaleFactor: 1 });
  await page.setContent(html, { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: opts.out, type: "jpeg", quality: 92, fullPage: false });
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
