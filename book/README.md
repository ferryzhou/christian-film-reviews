# 把本站影评出版为电子书与纸质书（Amazon KDP · Lulu · IngramSpark）

`book/` 目录把 `original-reviews/` 下的自撰影评编成一本书——《光影与信仰：二十一部电影里的救赎》——并生成可直接上传 Amazon KDP（Kindle Direct Publishing）的文件、封面与上架文案。

## 先读这一段：KDP 对中文书的硬性规定

以 KDP 官方帮助页为准（2026 年 9 月核对）：

| 规定 | 出处 |
| --- | --- |
| 中文只支持 **繁体中文（Chinese (Traditional)，Beta）**，且**只能出电子书**，不能出纸质书 | [Book Supported Languages](https://kdp.amazon.com/en_US/help/topic/G200673300) |
| **不支持简体中文**电子书（"KDP doesn't support eBooks in Chinese (Simplified)"） | [Chinese (Traditional) (Beta)](https://kdp.amazon.com/en_US/help/topic/G27T64E65VM6JWKK) |
| 繁体中文书稿**只接受 Word 文件（DOC/DOCX）**，不接受 EPUB/KPF | 同上 |
| 必须横排、从左到右；书名与作者名在 KDP 表单里也须用繁体填写 | 同上 |

因此本流程的 Amazon 主产出是 **繁体中文 DOCX**：脚本用 OpenCC（`s2tw`，台湾标准字形）把简体影评逐字转换为繁体，并在每篇开头附上台湾通行译名（如《肖申克的救赎》→《刺激1995》）。简体版 DOCX/EPUB 同时生成，供 Word 校对或上架其他平台（见文末）。

## 一键生成

```bash
pip install python-docx ebooklib opencc-python-reimplemented
python3 book/build_book.py                # 全部产出 → book/dist/
python3 book/build_book.py --only docx-tw # 只重生成 KDP 用的繁体 DOCX
python3 book/build_book.py --with-images  # 额外生成内嵌剧照版 → book/dist/illustrated/（见"版权"）
```

封面渲染需要 `node` + `playwright` + Chromium（本仓库 `render_cover.js`），并建议安装 Noto Serif SC/TC 字体；缺失时脚本跳过封面并提示，其余产出不受影响。

| 产出（`book/dist/`） | 用途 |
| --- | --- |
| `光影与信仰-繁體.docx` | **上传 KDP 的书稿** |
| `cover-tw.jpg` | KDP 封面，1600×2560（1:1.6），JPEG，原创排版，不含影片素材 |
| `kdp-listing-tw.txt` | 上架表单文案：书名、副标题、简介、7 组关键词、3 个分类、章节一览 |
| `光影与信仰-繁體.epub` | Send to Kindle 自用、Apple Books / Google Play / Kobo 等其他平台 |
| `光影与信仰-简体.docx` / `.epub` / `cover-sc.jpg` / `kdp-listing-sc.txt` | 简体版，同上；**不能上传 KDP** |

书的结构：书名页 → 版权页 → 目录（带 Kindle 逻辑目录书签）→ 序 → 五辑二十一篇（每篇：标题、片名/原名/年份/导演、正文）→ 附录一 影片索引 → 附录二 经文索引（自动从正文抽取，按圣经卷序）→ 关于作者。

## 上架步骤（KDP）

1. **账号**：<https://kdp.amazon.com> 用 Amazon 账号登录，完成 Account 页的作者信息、收款银行、税务问卷（非美国居民填 W-8BEN；中国大陆/台湾/香港均可收款）。
2. **Create → Kindle eBook**。
3. **Kindle eBook Details**：
   - Language 选 **Chinese (Traditional)**。
   - Book Title / Subtitle / Author 按 `kdp-listing-tw.txt` 填（繁体）。
   - Description 粘贴文件中的简介（≤4000 字符）。
   - Publishing Rights 选 "I own the copyright…"。
   - Primary Audience：非成人内容；Reading age 留空。
   - Categories 选 3 个（文件中给了建议路径；KDP 的分类树会随时间变动，找不到时选最接近的）。
   - Keywords 7 格，逐组粘贴。
   - **AI-generated content**：KDP 自 2023 年起要求申报。本仓库的影评由 `.claude/skills/write-film-review` 生成，封面由脚本排版——请如实勾选 "Yes" 并填写文字（Text）与图片（Images）均为 AI-generated；繁体转换为程序转换（Translation 也勾选）。申报不影响上架，隐瞒被发现会下架并可能封号。
   - Pre-order：可不选。
4. **Kindle eBook Content**：
   - Manuscript 上传 `光影与信仰-繁體.docx`。
   - Cover 选 "Upload a cover you already have"，上传 `cover-tw.jpg`。
   - AI 内容申报如上一步未出现会在此处出现。
   - **Kindle eBook Preview**：务必用在线预览器（或下载 [Kindle Previewer](https://kdp.amazon.com/en_US/help/topic/G202131170)）翻一遍：目录能否跳转、各篇标题是否成章、繁体字有无明显错字（见下节）。
   - ISBN：电子书不需要。
5. **Kindle eBook Pricing**：
   - **KDP Select 不要勾选**——Select 要求电子书在其他任何地方（包括你自己的网站）都不得以数字形式免费或付费提供，而这些影评在 <https://ferryzhou.github.io/christian-film-reviews/> 与 WordPress 上公开可读，勾选即违约。
   - Territories：All territories。
   - 定价参考：US$4.99（可享 70% 版税档位 2.99–9.99）；其他市场按汇率自动换算即可。繁体读者主要在台湾/香港/海外华人，实际购买多经 Amazon.com。
6. **Publish**。审核通常 72 小时内（Beta 语言可能更久）。审核会核对 AI 申报、版权（见下节）与"内容是否在网上免费可得"——后者对版权所有者是允许的，如被问询，回复自己是网站作者并给出站点链接即可。

## 版权与配图：为什么默认纯文字

- **剧照**：站内影评的配图是低分辨率官方剧照，靠"评论目的 + 少量 + 低清 + 承诺下架"的合理使用（fair use）站在网站上。放进**付费出售**的书里，合理使用的四要素中"商业性"与"对市场的影响"都变得不利，而 KDP 的内容审核要求你对每张图片持有权利，被要求出示授权时无法提供。所以默认产出**不含剧照**。`--with-images` 仅供自用/印给朋友，或在你取得片方授权后使用；输出在 `dist/illustrated/`，不入库。
- **海报**同理不进书，封面为脚本排版的原创图（纸色底、金色胶片孔、隐秘的阳光），无第三方素材。
- **台词引用**：正文中的短句台词引用属于评论范畴，与出版影评集的行业惯例一致。
- **经文**：和合本 1919 年出版，已进入公有领域。
- **书名**："光影与信仰"沿用站名；副标题可在 `book.json` 改。

## 出版前检查清单

- [ ] 署名：`book.json` 的 `author`（周津）+ `authorSuffix`（著）出现在封面与书名页；`aiDisclosure` 印在版权页，序末也有写作方式的交代。KDP 后台仍须如实申报 AI-generated。
- [ ] 通读一遍 `光影与信仰-繁體.docx`。OpenCC 的字符级转换在少数一对多简繁字上会出错，重点扫：**发/髮·發、后/後·后、干/幹·乾、里/裡·里、面/麵·面、只/隻·只、系/係·繫、松/鬆·松、复/復·複**，人名与专名（"辛德勒""俊""宗灿"等）确认未被误转。改法：修 `original-reviews/*.md` 的原文不合适时，直接在 DOCX 里改。
- [ ] `titleTW`（台湾译名表）只覆盖了差异明显的 8 部，其余片名简繁转换后与台湾通行译名相同或相近；如发现不同，在 `book.json` 补充。
- [ ] Kindle 预览器里看目录跳转、五辑扉页、两个附录。
- [ ] 版权页年份、版本号（`book.json` 的 `year`、`edition`）。

## 简体读者怎么办

KDP 不收简体书，简体版可走：

- **Send to Kindle**（自用 / 送读者）：把 `光影与信仰-简体.epub` 发到 Kindle 邮箱，中文显示正常。
- **Google Play Books Partner Center**、**Apple Books**（需 Mac 或 aggregator）、**Kobo Writing Life**、**Draft2Digital**：都接受 EPUB 与简体中文，把 `简体.epub` + `cover-sc.jpg` + `kdp-listing-sc.txt` 的文案上传即可。
- 纸质书：见下一节"印刷与销售纸质书"。

## 印刷与销售纸质书（Lulu 直销 + IngramSpark 分销，两条线并行）

KDP 不接受任何中文纸质书，所以纸书走按需印刷（Print on Demand）。`build_print.py` 一次产出两个平台各自的文件：

```bash
pip install weasyprint python-barcode      # 另需 Ghostscript（apt install ghostscript）把 Ingram 封面转 CMYK
python3 book/build_print.py                 # → book/dist/print/
python3 book/build_print.py --spine 0.29 --platform ingram   # 平台模板给出的书脊与估算不同时，重做该平台封面
```

| 产出（简繁各一套） | 说明 |
| --- | --- |
| `光影与信仰-*-内文.pdf` | 5.5×8.5 in（Digest）开本，113 页；字体全部内嵌；正文 100% 黑（IngramSpark 要求）；半书名页、书名页、版权页、带页码目录、序、五辑扉页（起右页）、正文（页眉：左页书名 / 右页篇名）、两个附录（含页码）、关于作者 |
| `光影与信仰-*-封面-lulu.pdf` | Lulu 全包封面：书脊按 Lulu 官方公式 pages/444 + 0.06 in（113 页 → 0.317 in），RGB |
| `光影与信仰-*-封面-ingram.pdf` | IngramSpark 全包封面：书脊 = 页数 × 0.0025 in（cream 50# 纸，→ 0.285 in），Ghostscript 转 CMYK；条码区白底 2×1.2 in（Ingram 要求 ≥1.75×1 in） |
| `print-listing-*.txt` | 两个平台的上架文案：书名/英文书名、规格、书脊、Lulu 分类与关键词、Ingram 的 BISAC 三个类目、英文短简介、折扣与退货建议 |
| `cover-preview-*.png` | 封面预览 |

开本、纸张、出血、ISBN、定价、英文书名都在 `book.json` 的 `print` 段。**填入 `isbn` 后重跑**：封底右下角自动生成 EAN-13 条码，版权页与文案同步印上 ISBN。

### 两条线怎么并行

| | Lulu 书店直销 | IngramSpark 分销 |
| --- | --- | --- |
| 作用 | 最快开卖：自己的网站/朋友圈/教会直接卖，自己批量进书送人 | 上 Amazon、Barnes & Noble、全球书店与图书馆订购系统 |
| ISBN | 不需要（Lulu 书店内部销售） | **必须自有**：美国 Bowker 单个 $125 / 10 个 $295；台湾向国家图书馆 ISBN 中心免费申请；香港向公共图书馆申请 |
| 中文限制 | 书名、封面、元数据都可以中文 | 书名可中文，Ingram 建议同时给英文书名与英文简介（文案文件已备好）；书脊文字须拉丁字母时用英文书名 |
| 不要做 | 不勾 Lulu Global Distribution（要求书名与封面文字只能是拉丁字母，中文过不了） | 同一 ISBN 不要再在 Lulu 开分销，只在 Ingram 分销 |
| 收入 | Lulu 书店卖出：**80%** 的（定价 − 印刷成本）归你 | （定价 × (1 − 批发折扣)）− 印刷成本 |
| 印刷成本（估） | 113 页黑白 Digest，Lulu 计算器约 $4 上下 | Ingram 2026 小开本黑白约 $1.33 + $0.0146/页 ≈ $3 |
| 定价建议 | US$12.99：Lulu 净收约 $7 | US$12.99、55% 折扣：净收约 $2.8；40% 折扣：约 $4.8，但书店不进货，只剩 Amazon |

**本周可以做的（不需要 ISBN）：**

1. Lulu 注册（<https://www.lulu.com>）→ Create → Print Book → 上传 `内文.pdf` 与 `封面-lulu.pdf` → Digest 5.5×8.5 in、黑白、cream 纸、平装（Perfect Bound）、光面或哑面封面 → 在线预览翻一遍（目录页码、右页页眉、辑扉页在右页）→ 定价 → 只勾 "Lulu Bookstore" → 先**订一本样书**，到手确认后再公开。
2. 买 ISBN（Bowker 或所在地免费申请），填进 `book.json` 的 `print.isbn`，重跑 `build_print.py`。
3. IngramSpark 注册（<https://www.ingramspark.com>）→ Add a Title → 按 `print-listing-*.txt` 填：Language = Chinese，Title/Subtitle 中文，Contributor，Imprint，三个 BISAC，英文短简介 + 中文全简介，Keywords → 上传 `内文.pdf` 与 `封面-ingram.pdf`（先用 Ingram 的 Cover Template Generator 拿到该 ISBN/页数的书脊，与 0.285 不同就 `--spine` 重做）→ 定价：US/UK/EU/AU 各币种，Wholesale discount 55%，Returns = No → 提交。审核通过后 Amazon 通常 2–4 周自动出现纸质版页面。
4. 简体版与繁体版是两本书，各需自己的 ISBN；先只上一种也可以（简体版 Lulu 直销、繁体版走 Ingram 上 Amazon，与电子书的繁体版呼应，是一种省钱的组合）。

**印刷前检查：**

- [ ] 页数 ≥ 100 才印书脊文字（Lulu 规定；脚本按页数自动处理）。
- [ ] 书脊宽度用平台的模板/计算器核对；封面 PDF 总尺寸 = 2×5.5 + 书脊 + 2×0.125 in 宽、8.5 + 0.25 in 高。
- [ ] Ingram 封面必须有 ISBN 条码：填 `isbn` 重跑后确认封底右下角条码已出现。
- [ ] 平台预览器里翻一遍：目录页码、附录页码、右页页眉篇名、辑扉页是否在右页。
- [ ] 想要带图的印刷版可用 `--with-images`（输出到 `dist/print/illustrated/`），但站内剧照只有 ≤720 px，达不到印刷要求的 300 ppi，且商业销售的版权风险同前文，仅建议自印留念。
- [ ] 每个平台各订一本样书（proof）再开售。

## 维护

新写一篇影评并登记 `originals.js` 后，把它的 `filmId` 加进 `book.json` 的某一辑；忘了加的话脚本会自动归入末尾"余音"辑并在终端提醒。重跑 `python3 book/build_book.py`，把新的 DOCX 在 KDP 书页 "Edit eBook Content" 里重新上传，即为再版。
