// 道影的纸质书：首页、本站影评页、作者页与静态影评页的购买入口共用此处。
// build_review_pages.py 也读取本文件（"const BOOK =" 之后须为合法 JSON），改完链接后重跑一次该脚本。
const BOOK = {
  "title": "慢慢地动怒",
  "subtitle": "二十一部电影里的救赎",
  "blurb": "本站二十一篇原创影评结集成书，以基督信仰的眼光重读二十一部华语与世界影史名作。",
  "cover": "book-cover.jpg",
  "buy": [
    { "label": "在 Lulu 购买纸质书", "url": "LULU_URL" }
  ]
};
