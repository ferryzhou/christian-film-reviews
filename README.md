# 光影与信仰 · Christian Film Reviews

**在线访问：<https://ferryzhou.github.io/christian-film-reviews/>**

华人基督徒影评导读索引站。收录齐宏伟、石衡潭、王书亚、刘小枫及基督时报"福音影评"专栏作者的电影评论线索：谁评过哪部电影，从什么角度切入，原文在哪里。

**本站做路标，不做搬运** —— 站内只有事实信息与本站自撰的主题摘要，所有"前往阅读"链接指向作者原著或公开原文页面。

## 网站结构

纯静态站点，无构建步骤，无外部依赖（仅 Google Fonts）。

| 文件 | 作用 |
| --- | --- |
| `index.html` | 首页：作者卡片 + 电影索引（搜索 / 按作者筛选 / 按年份排序） |
| `author.html` | 作者页（`?id=<authorId>`）：简介、文集、评过的电影 |
| `film.html` | 电影页（`?id=<filmId>`）：元信息、主题摘要、评论出处 |
| `data.js` | 全部数据：`AUTHORS` 与 `FILMS` 两个数组 |
| `app.js` | 渲染逻辑：按 `<body data-page>` 路由到对应页面的渲染函数 |
| `styles.css` | 共享样式（米色纸质底 + 金色点缀的版式风格） |
| `find-articles.skill.md` | 找文章的方法论手册：来源、URL 模式、验证与收录规范 |
| `find_articles.py` | 辅助脚本：按手册批量查找 / 验证文章链接 |

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

## 版权说明

本站不收录任何作者的影评原文。各作者文章版权归作者本人与原出版社所有；站内摘录仅限作者公开网络文章的短引用，符合合理使用原则。详见站内"版权与说明"一节。
