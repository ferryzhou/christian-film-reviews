# 道影 · 光影与信仰 (daoying.org)

**在线访问：<https://ferryzhou.github.io/christian-film-reviews/>**（正式域名 `daoying.org` 配置中，见下方"部署"）

华人基督徒影评导读索引站。收录齐宏伟、石衡潭、王书亚、刘小枫及基督时报"福音影评"专栏作者的电影评论线索：谁评过哪部电影，从什么角度切入，原文在哪里。

**本站做路标，不做搬运** —— 站内只有事实信息与本站自撰的主题摘要，所有"前往阅读"链接指向作者原著或公开原文页面。

## 网站结构

纯静态站点，无构建步骤，无任何外部依赖。字体使用系统字体栈（宋体系 + Georgia + 等宽），不加载 Google Fonts —— fonts.googleapis.com 在中国大陆被墙，外链字体会让大陆访客首屏卡顿甚至超时。

| 文件 | 作用 |
| --- | --- |
| `index.html` | 首页：作者卡片 + 电影索引（搜索 / 按作者筛选 / 按年份排序） |
| `author.html` | 作者页（`?id=<authorId>`）：简介、文集、评过的电影 |
| `film.html` | 电影页（`?id=<filmId>`）：元信息、主题摘要、本站影评入口、评论出处 |
| `review.html` | 本站影评阅读页（`?id=<filmId>`）：运行时 fetch 并渲染 `original-reviews/<filmId>.md` |
| `data.js` | 全部数据：`AUTHORS` 与 `FILMS` 两个数组 |
| `app.js` | 渲染逻辑：按 `<body data-page>` 路由到对应页面的渲染函数 |
| `styles.css` | 共享样式（米色纸质底 + 金色点缀的版式风格） |
| `find-articles.skill.md` | 找文章的方法论手册：来源、URL 模式、验证与收录规范 |
| `find_articles.py` | 辅助脚本：按手册批量查找 / 验证文章链接 |
| `.claude/skills/write-film-review/` | 自撰影评 skill：以基督信仰视角为电影写原创影评（引经文、指向救赎、挖细节、全角色群像，四种可选文风） |
| `original-reviews/` | 本站自撰的原创影评（Markdown，由上述 skill 生成，`review.html` 直接渲染） |
| `originals.js` | 自撰影评注册表（filmId → 标题/风格/日期），供首页徽标与电影页入口同步渲染 |
| `stills/` | 自撰影评配图（低分辨率剧照 / 自由授权取景地照片，按 filmId 分目录，版权归属见文内图注） |

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

- **GitHub Pages**：<https://ferryzhou.github.io/christian-film-reviews/>，由 `main` 分支自动发布。
- **surge.sh**：另有一份通过本地 `deploy-films.py` 脚本手动部署的副本（脚本与凭据不入库，见 `.gitignore`），合并到 `main` 不会自动更新该副本。

### 正式域名：daoying.org（面向大陆访客）

目标：大陆访客可直接访问。`*.github.io` / `*.surge.sh` 等平台共享域名在大陆被墙或不稳定，自有域名是第一前提。

上线步骤（按顺序）：

1. **购买域名**：在 Porkbun（或 Cloudflare Registrar）注册 `daoying.org`，开启免费 WHOIS 隐私保护。
2. **选择托管**（二选一）：
   - **阿里云 OSS 或腾讯云 COS 香港区**（推荐）：静态网站模式 + 绑定自定义域名 + 开启 HTTPS。香港节点对大陆延迟低、IP 段较少被墙，且境外托管无需 ICP 备案。
   - **GitHub Pages + 自定义域名**（零成本过渡方案）：仓库 Settings → Pages 填入 `daoying.org`，DNS 加 CNAME 记录指向 `ferryzhou.github.io`，勾选 Enforce HTTPS。注意：`CNAME` 文件须在域名 DNS 生效后再提交，否则现有 github.io 地址会指向尚未生效的域名。
3. **验证大陆可达性**：用 17ce.com 或 boce.com 从多省份测试；此后定期复测。

注意：不考虑大陆境内托管 —— 需要 ICP 备案，且宗教类内容还需《互联网宗教信息服务许可证》，个人与境外主体实际无法取得。境外托管 + 自有域名是合规且现实的方案。

## 版权说明

本站不收录任何作者的影评原文。各作者文章版权归作者本人与原出版社所有；站内摘录仅限作者公开网络文章的短引用，符合合理使用原则。详见站内"版权与说明"一节。
