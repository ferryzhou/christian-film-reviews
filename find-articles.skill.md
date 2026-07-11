# Skill: 查找基督教电影评论文章

> 面向 agent 的策略手册。用于为 `data.js` 持续发现可公开访问的基督教电影评论全文，并按规范收录。
> 配套工具脚本：[find_articles.py](file:///workspace/films/find_articles.py)

## 何时使用

- 用户说"继续寻找""再找一些""扩充影评"等，且当前目标是丰富本站影评库时。
- 需要为已有电影补充第二条评论，或为未收录电影新增条目时。
- 部署前核对 `EXISTING_FILMS` 与 `data.js` 是否同步时。

## 核心方法论：从书到文章到全文站

用户早期明确提出的搜索方法论，是本 skill 的基础：

1. **先找到一本书** — 确认一位作者的影评集及其完整目录（篇名 + 对应电影）。
2. **逐篇搜索文章标题** — 用文章标题 + 电影名 + 作者名作为关键词，在多个站点搜索。
3. **找到全文网站后深入挖掘归档** — 一旦在某站发现一篇全文，立即用 `site:` 搜索该站，挖掘同一作者/专栏的其余文章。
4. **验证 URL 可访问** — WebFetch 实际访问，确认返回的是全文而非付费墙/目录页。
5. **提取 fair-use 摘录** — 1-2 段，不复制全文，附原文链接。

> 关键直觉：一篇全文的发现往往意味着同站还有数十篇。不要只搜一篇文章就停。

## 已知来源与 URL 模式

| 来源 key | 站点 | 作者 | URL 模式 | 备注 |
|---|---|---|---|---|
| `ebaomonthly` | 翼报 chs.ebaomonthly.com | 石衡潭 | `ebaomonthly.com/ebao/(read\|print)ebao.php?a=YYYYMMDD` | 早期文章用 `readebao.php?eID=eNNNNN`；主域名 `ebaomonthly.com` 文章为繁体 |
| `christiantimes` | 基督时报 chinachristiantimes.com | 福音影评专栏（多作者） | `chinachristiantimes.com/news/编号/标题` | 站点间歇性 `ERR_CONNECTION_CLOSED`；WebSearch `site:` 常能取到全文快照 |
| `sina` | 新浪 news.sina.cn | 王书亚 电光倒影 | `news.sina.cn/sa/YYYY-MM-DD/detail-XXXXX.d.html` | 南方人物周刊授权转载 |
| `sohu` | 搜狐 sohu.com | 王书亚 电光倒影 | `sohu.com/数字/n数字.shtml` | 同上 |
| `100md` | 百拇医药网 100md.com | 王书亚（南方人物周刊全期刊） | `100md.com/html/paper/1672-8335/年/期/页.htm` | 收录纸刊全期刊，是电光倒影专栏的宝库 |
| `kongfz` | 孔夫子旧书网 | — | `kongfz.com/数字/数字` | 仅用于获取旧书完整目录，非全文 |
| `douban` | 豆瓣图书 | — | `book.douban.com/subject/数字` | 用于书籍引用链接（非在线文章） |
| `docin` | 豆丁网 docin.com | 王书亚等 | `docin.com/touch_new/preview_new.do?id=数字` | 偶有全文扫描，可作补充 |

## 作者与其影评集（已知目录规模）

| 作者 ID | 作者 | 影评集 | 篇数 | 在线全文情况 |
|---|---|---|---|---|
| `qihongwei` | 齐宏伟 | 《牛人看电影·齐宏伟篇》(2018) + 《寻找感动力》(2020) | 35 + 25 | 基本无免费在线全文，仅付费电子书；以豆瓣图书页作引用 |
| `shihengtan` | 石衡潭 | 《光影中的信望爱》(2013) + 《电影之于人生二集》 | ~40 + ~30 | 翼报有大量全文；基督时报有部分转载 |
| `wangshuya` | 王书亚 | 《天堂沉默了半小时》(2008) | ~30 | 新浪/搜狐/百拇有部分全文；目录约220部推荐电影 |
| `liuxiaofeng` | 刘小枫 | 《拯救与逍遥》 | — | 非影评集，学界讨论坐标，仅书籍引用 |
| `christiantimes` | 基督时报 | 福音影评专栏（多作者） | — | 王新毅、肖朋、沐风、李道南、溪君、絮语、李纯、吴晏、李哈拿、王璐德等 |

## 搜索策略（按优先级）

### 策略 A：翼报系统扫描（石衡潭，高产全文）

1. WebSearch `石衡潭 影评 site:ebaomonthly.com`
2. WebSearch `石衡潭 电影 site:ebaomonthly.com`
3. 对发现的每个 URL，WebFetch 验证并提取标题/摘录。
4. 翼报 URL 含日期，可顺日期前后试探相邻文章（如发现 `a=20120701`，可试 `a=20120601`、`a=20120801`）。
5. 翼报搜索页 `searchebao.php?q=` 偶尔返回 404，不要依赖它，靠搜索引擎 `site:` 取代。

### 策略 B：从书目录反查全文

1. 在孔夫子/豆瓣找到影评集详情页，获取完整目录（篇名 + 电影名）。
2. 对目录中每部电影，WebSearch `电影名 作者名 影评` + `电影名 电光倒影/艺文走廊`。
3. 命中全文站后，立即转策略 D 深挖该站。

### 策略 C：基督时报福音影评扫描

1. WebSearch `site:chinachristiantimes.com 电影名 福音影评 作者名`。
2. 站点直连常 `ERR_CONNECTION_CLOSED`，但 WebSearch 的 `site:` 结果通常含正文快照，可直接取摘录。
3. 验证 URL 时若 WebFetch 失败，改用 WebSearch 快照作为来源依据，URL 仍记原始 news 链接。

### 策略 D：全文站深挖（单点突破）

发现任一全文后：

1. WebSearch `site:<该域名> 作者名 影评`
2. WebSearch `site:<该域名> 作者名 专栏名`
3. 对每条新 URL 走验证流程。
4. 同站文章常有统一的日期/编号规律，总结规律后可批量构造候选 URL 验证。

### 策略 E：其他平台横向搜索

当主来源枯竭时，搜索以下平台：
- 福音时报、基督日报等同类媒体
- 微信公众号（"今日佳音""橡果"等）— 通过 WebSearch `电影名 基督教 影评 公众号`
- 知乎/豆瓣基督徒影评作者
- 教会网站电影评论文章
- 王怡、余杰、北村、范学德等基督徒知识分子的影评

## 验证流程（每条 URL 必过）

1. **WebFetch 实际访问**，确认 HTTP 200 且返回全文（非付费墙/目录/404）。
2. **提取标题**：`<title>` 清理常见后缀（`- 翼报`、`- 基督时报`、`_新浪` 等）。
3. **提取摘录**：取最有信息量的 1-2 段中文（150-300 字），反映作者信仰视角的论点，不要纯剧情复述。
4. **记录四元组**：电影名 / 文章标题 / URL / 摘录。
5. **去重检查**：对照下方去重清单，避免重复收录。

> 持久化提示：子代理 Task 中 WebFetch 的大文件输出存于 `/tmp/trae/toolcall-output/`，但在主会话中**不可跨上下文访问**。子代理应直接在返回结果中带回标题+摘录，不要依赖主会话去读临时文件。

## 收录规范（写入 data.js）

### 新电影条目

```javascript
{
  id: "pinyin-slug",          // 拼音短横线，如 zhongguo-hehuoren
  title: "中文片名",
  titleEn: "English Title",
  year: 2013,
  director: "导演",
  country: "国家",
  genre: "剧情 / 战争",
  summary: "本站自撰的1-2句概括，结合剧情与作者评论切入点，不复制原文。",
  reviews: [
    {
      authorId: "shihengtan",           // 见 AUTHORS 数组
      work: "翼报 · 艺文走廊",            // 出处
      section: "向谁要尊严？",            // 文章标题
      source: "https://...",             // 全文 URL
      excerpt: "1-2段摘录，fair-use。"   // 必须有
    }
  ]
}
```

### 为已有电影补充评论

在对应电影的 `reviews` 数组追加一个对象即可。注意 `id` 不要改。

### 作者条目

- 新作者（如基督时报的独立作者）需在 `AUTHORS` 数组新增条目，含 `id`/`name`/`title`/`field`/`bio`/`works`/`source`。
- 基督时报的多作者统一归到 `christiantimes` 平台条目下，`bio` 中列出作者群。

## 去重检查清单

每次添加前：

1. 运行 `node -e "..."` 在沙箱中 eval `data.js`，打印 `FILMS.length` 和所有 `id`/`title`，确认无重复。
2. 对照 `find_articles.py` 的 `EXISTING_FILMS` 列表，确认新片名不在其中。
3. 同一电影已有同一作者评论时，确认是不同文章（不同 `source`）才追加。
4. 历史已修复的重复：`窃听风暴`（`qieting-fengbao` 与 `jianyuzhe` 重复，保留 `jianyuzhe`）、`致青春`（`zhi-qing-chun` 与 `zhiqingchun` 重复，保留 `zhiqingchun`）。

## 同步与部署

收录完成后：

1. **更新 `find_articles.py` 的 `EXISTING_FILMS`**，加入新电影标题，保持与 `data.js` 同步。
2. **语法验证**：`node -e` 沙箱 eval，确认 `FILMS`/`AUTHORS` 完整、无重复。
3. **部署**：`python3 deploy-films.py`（需先 `pip install pexpect`，每个新终端会话都要重装）→ surge.sh。
4. **GitHub**：`git add films/ && git commit && git push`。

## 常见坑

- **pexpect 每个新终端会话都丢失**：`python3 -m pip install --quiet pexpect` 重装。
- **基督时报间歇性连接中断**：用 WebSearch `site:` 快照代替直连。
- **翼报 searchebao.php 偶尔 404**：改用搜索引擎 `site:ebaomonthly.com`。
- **临时文件不可跨上下文**：子代理必须把摘录写进返回结果，不要只存临时文件。
- **王书亚/齐宏伟多数篇目无免费在线全文**：不要浪费时间反复搜，以豆瓣图书页作书籍引用即可，把精力集中在翼报和基督时报两座全文矿。

## 验证用 Node 片段

```bash
node -e '
const fs = require("fs");
const vm = require("vm");
const code = fs.readFileSync("films/data.js","utf8");
const ctx = { window: {} };
vm.runInNewContext(code, ctx);
const films = ctx.window.FILMS;
const ids = films.map(f => f.id);
const dupIds = ids.filter((id,i) => ids.indexOf(id) !== i);
const titles = films.map(f => f.title);
const dupTitles = titles.filter((t,i) => titles.indexOf(t) !== i);
const withFullText = films.filter(f => f.reviews.some(r => r.excerpt)).length;
console.log("FILMS count:", films.length);
console.log("AUTHORS count:", ctx.window.AUTHORS.length);
console.log("Duplicate ids:", dupIds);
console.log("Duplicate titles:", dupTitles);
console.log("Films with full-text excerpts:", withFullText);
'
```
