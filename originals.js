// 本站自撰影评注册表
// 正文存于 original-reviews/<filmId>.md（Markdown，YAML front matter），
// 此处仅登记元信息，供首页徽标与电影页"本站影评"板块同步渲染。
// 由 .claude/skills/write-film-review 在写完影评后维护，title 须与 md 文件内标题一致。

const ORIGINALS = {
  "zhiqingchun": {
    title: "我们都爱自己，胜过爱爱情",
    style: "文学随笔式",
    date: "2026-08-13"
  },
  "xiaoshenke-de-jiushu": {
    title: "得救之道，就在其中",
    style: "文学随笔式",
    date: "2026-08-19"
  },
  "miyang": {
    title: "你看见了吗",
    style: "文学随笔式",
    date: "2026-08-20"
  },
  "agan-zhengzhuan": {
    title: "他和上帝讲和了",
    style: "文学随笔式",
    date: "2026-08-21"
  },
  "twelve-angry-men": {
    title: "慢慢地动怒",
    style: "文学随笔式",
    date: "2026-08-21"
  },
  "xunmeng-huanyouji": {
    title: "请记得我",
    style: "文学随笔式",
    date: "2026-08-21"
  },
  "jianyuzhe": {
    title: "这是给我的",
    style: "文学随笔式",
    date: "2026-08-21"
  },
  "diqi-fengyin": {
    title: "我要知识，不是信仰",
    style: "文学随笔式",
    date: "2026-08-22"
  },
  "xinling-qilv": {
    title: "这就是海洋",
    style: "文学随笔式",
    date: "2026-08-22"
  }
};

if (typeof window !== "undefined") window.ORIGINALS = ORIGINALS;
