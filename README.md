# 光影与信仰 · Christian Film Reviews

**在线访问：<https://daoying.org>**

华人基督徒影评导读索引站。收录齐宏伟、石衡潭、王书亚、刘小枫及基督时报"福音影评"专栏作者的电影评论线索：谁评过哪部电影，从什么角度切入，原文在哪里。

**本站做路标，不做搬运** —— 站内只有事实信息与本站自撰的主题摘要，所有"前往阅读"链接指向作者原著或公开原文页面。

## 网站结构

纯静态站点，无构建步骤，无外部依赖（仅 Google Fonts）。

| 文件 | 作用 |
| --- | --- |
| `index.html` | 首页：作者卡片 + 电影索引（搜索 / 按作者筛选 / 按年份排序） |
| `author.html` | 作者页（`?id=<authorId>`）：简介、文集、评过的电影 |
| `film.html` | 电影页（`?id=<filmId>`）：元信息、主题摘要、本站影评入口、评论出处 |
| `originals.html` | 本站原创影评列表页（署名"道影"，按发表日期倒序，最新在前） |
| `review.html` | 本站影评阅读页（`?id=<filmId>`）：运行时 fetch 并渲染 `original-reviews/<filmId>.md` |
| `review/<filmId>.html` | 预渲染的静态影评页（`build_review_pages.py` 生成）：自带 og meta，供微信等分享爬虫抓取标题/描述/海报；站内入口指向此处，`review.html?id=` 旧链接仍可用 |
| `data.js` | 全部数据：`AUTHORS` 与 `FILMS` 两个数组 |
| `app.js` | 渲染逻辑：按 `<body data-page>` 路由到对应页面的渲染函数 |
| `styles.css` | 共享样式（米色纸质底 + 金色点缀的版式风格） |
| `find-articles.skill.md` | 找文章的方法论手册：来源、URL 模式、验证与收录规范 |
| `find_articles.py` | 辅助脚本：按手册批量查找 / 验证文章链接 |
| `.claude/skills/write-film-review/` | 自撰影评 skill：以基督信仰视角为电影写原创影评（引经文、指向救赎、挖细节、全角色群像，四种可选文风） |
| `original-reviews/` | 本站自撰的原创影评（Markdown，由上述 skill 生成，`review.html` 直接渲染） |
| `originals.js` | 自撰影评注册表（filmId → 标题/风格/日期），供首页徽标与电影页入口同步渲染 |
| `stills/` | 自撰影评配图（低分辨率剧照 / 自由授权取景地照片，按 filmId 分目录，版权归属见文内图注） |
| `publish_wordpress.py` | 自撰影评同步到 WordPress.com：`WP_SITE=站点 WP_TOKEN=令牌 python3 publish_wordpress.py`（`--dry-run` 本地预览；`wp-sync.json` 记录文章映射，更新旧文不重复发布） |
| `book/` | 出版为 Amazon Kindle 电子书：`python3 book/build_book.py` 把全部自撰影评编成《慢慢地动怒：二十一部电影里的救赎》，产出 KDP 上传用的繁体 DOCX、简繁 EPUB、电子书封面与上架文案；`book/build_print.py` 产出 Lulu / IngramSpark 按需印刷用的内文与全包封面 PDF（中文规则、上架与印刷步骤见 `book/README.md`） |

## 本地预览

```bash
python3 -m http.server 8000
# 打开 http://localhost:8000
```

## 数据模型

`data.js` 中每部电影的结构：

```js
{
  id: "miyang",              // 用于 film.html?id=… 的短标识
  title: "密阳",
  titleEn: "Secret Sunshine",
  year: 2007,
  director: "李沧东",
  country: "韩国",
  genre: "剧情",
  summary: "……",             // 本站自撰摘要，不复制原文
  reviews: [
    {
      authorId: "wangshuya", // 对应 AUTHORS 中的 id
      work: "……",            // 出处（书名或专栏）
      section: "……",         // 章节 / 文章标题（可选）
      excerpt: "……",         // 合理使用范围内的短摘录（仅公开网络文章，可选）
      source: "https://…"    // 指向原文或豆瓣图书页
    }
  ]
}
```

新增电影或作者时的收录规范、来源渠道与去重清单见 `find-articles.skill.md`。

## 部署

- **GitHub Pages + 自定义域名**：<https://daoying.org>，由 `main` 分支自动发布。根目录 `CNAME` 文件声明域名（勿删）；旧地址 <https://ferryzhou.github.io/christian-film-reviews/> 由 GitHub 自动 301 跳转到新域名。DNS（在域名注册商处设置）：根域 `daoying.org` 四条 A 记录 `185.199.108.153` / `185.199.109.153` / `185.199.110.153` / `185.199.111.153`（可选 AAAA `2606:50c0:8000::153` / `8001::153` / `8002::153` / `8003::153`），`www` 一条 CNAME → `ferryzhou.github.io`；仓库 Settings → Pages 填 `daoying.org` 并勾选 Enforce HTTPS。
- **surge.sh**：另有一份手动部署的副本 <https://daoying.surge.sh>，合并到 `main` 不会自动更新。同步流程：先 `SITE_URL=https://daoying.surge.sh python3 build_review_pages.py` 重生成静态影评页（og:image/og:url 指向 surge 域，GitHub Pages 在中国大陆被屏蔽，分享用 surge 链接）；再 `SURGE_LOGIN=<邮箱> SURGE_TOKEN=<令牌> npx -y surge ./ daoying.surge.sh`；最后 `python3 build_review_pages.py` 恢复 daoying.org 版本再提交（凭据不入库；`.surgeignore` 排除非站点文件，包括 `CNAME`——该文件属于 GitHub Pages，surge 部署务必显式写出 `daoying.surge.sh`）。

## 版权说明

本站不收录任何作者的影评原文。各作者文章版权归作者本人与原出版社所有；站内摘录仅限作者公开网络文章的短引用，符合合理使用原则。详见站内"版权与说明"一节。
