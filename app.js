// 光影与信仰 — 渲染逻辑

const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));

function getAuthor(id) {
  return AUTHORS.find(a => a.id === id);
}
function filmsByAuthor(authorId) {
  return FILMS.filter(f => f.reviews.some(r => r.authorId === authorId));
}
function getFilm(id) {
  return FILMS.find(f => f.id === id);
}
function getParam(name) {
  return new URLSearchParams(window.location.search).get(name);
}

// 通用页头/页脚注入
function injectChrome(activePage) {
  const topbar = `
    <header class="topbar">
      <div class="container">
        <a href="index.html" class="brand"><span class="mark">✦</span>光影与信仰</a>
        <nav class="nav-links">
          <a href="index.html" class="${activePage === 'home' ? 'active' : ''}">首页</a>
          <a href="index.html#authors" class="${activePage === 'authors' ? 'active' : ''}">作者</a>
          <a href="index.html#featured" class="${activePage === 'films' ? 'active' : ''}">电影</a>
          <a href="index.html#disclaimer" class="${activePage === 'about' ? 'active' : ''}">关于</a>
        </nav>
      </div>
    </header>
  `;
  const footer = `
    <footer>
      <div class="container">
        <span class="mono">光影与信仰 · 导读索引站</span>
        <span class="mono">不搬运原文 · 仅作路标</span>
      </div>
    </footer>
  `;
  document.body.insertAdjacentHTML("afterbegin", topbar);
  document.body.insertAdjacentHTML("beforeend", footer);
}

// ========= 首页渲染 =========
function renderHome() {
  injectChrome("home");

  // 作者卡片
  const authorsGrid = $("#authors-grid");
  if (authorsGrid) {
    authorsGrid.innerHTML = AUTHORS.map((a, i) => `
      <a class="author-card reveal reveal-${i + 1}" href="author.html?id=${a.id}">
        <div class="initial">${a.name[0]}</div>
        <div class="name">${a.name}</div>
        ${a.penName ? `<div class="pen">笔名 · ${a.penName}</div>` : `<div class="pen">&nbsp;</div>`}
        <div class="field">${a.title}<br><span style="color:var(--muted);font-size:0.78rem">${a.field}</span></div>
        <span class="arrow">→</span>
      </a>
    `).join("");
  }

  // 精选电影
  const featuredRow = $("#featured-row");
  if (featuredRow) {
    featuredRow.innerHTML = FILMS.map((f, i) => `
      <a class="film-card reveal reveal-${(i % 4) + 1}" href="film.html?id=${f.id}">
        <div class="poster"></div>
        <div class="info">
          <div class="title">${f.title}</div>
          <div class="meta">${f.year} · ${f.director}</div>
          <div class="blurb">${f.summary}</div>
        </div>
      </a>
    `).join("");
  }

  // 统计数字
  const statAuthors = $("#stat-authors");
  const statFilms = $("#stat-films");
  if (statAuthors) statAuthors.textContent = AUTHORS.length;
  if (statFilms) statFilms.textContent = FILMS.length;
}

// ========= 作者页渲染 =========
function renderAuthor() {
  injectChrome("authors");
  const id = getParam("id");
  const author = getAuthor(id);
  if (!author) {
    $("#author-content").innerHTML = `<div class="container" style="padding:4rem 0"><p>未找到该作者。<a href="index.html">返回首页</a></p></div>`;
    return;
  }
  document.title = `${author.name} — 光影与信仰`;

  const films = filmsByAuthor(id);
  const content = $("#author-content");
  content.innerHTML = `
    <div class="container">
      <a href="index.html#authors" class="back-link">← 全部作者</a>
      <section class="author-hero reveal">
        <div class="name-block">
          <div class="glyph">${author.name[0]}</div>
          <div>
            <h1>${author.name}</h1>
            ${author.penName ? `<div class="penname">笔名 · ${author.penName}</div>` : `<div class="penname">${author.born ? "生于 " + author.born : ""}</div>`}
            <div class="title-line">${author.title}</div>
            <div class="field-line">研究领域：${author.field}</div>
          </div>
        </div>
      </section>

      <div class="author-body">
        <div class="author-bio reveal reveal-1">
          <div class="kicker">作者简介</div>
          <p>${author.bio}</p>
        </div>
        <div class="author-works reveal reveal-2">
          <h3>代表影评文集</h3>
          ${author.works.map(w => `
            <div class="work-item">
              <div class="wt">《${w.title}》</div>
              <div class="wm">${w.publisher ? w.publisher + " · " : ""}${w.year}${w.count ? " · " + w.count + " 篇" : ""}</div>
            </div>
          `).join("")}
        </div>
      </div>

      <section class="reveal reveal-3">
        <div class="section-head">
          <h2>评过的电影</h2>
          <span class="count">${films.length} 部</span>
        </div>
        <div class="film-list">
          ${films.map((f, i) => `
            <a class="row" href="film.html?id=${f.id}">
              <div class="num">${String(i + 1).padStart(2, "0")}</div>
              <div>
                <div class="ft">${f.title}<span class="en">${f.titleEn}</span></div>
                <div class="fd">${f.director} · ${f.country} · ${f.genre}</div>
              </div>
              <div class="year">${f.year}</div>
            </a>
          `).join("")}
        </div>
      </section>
    </div>
  `;
}

// ========= 电影详情页渲染 =========
function renderFilm() {
  injectChrome("films");
  const id = getParam("id");
  const film = getFilm(id);
  if (!film) {
    $("#film-content").innerHTML = `<div class="container" style="padding:4rem 0"><p>未找到该电影。<a href="index.html">返回首页</a></p></div>`;
    return;
  }
  document.title = `${film.title} — 光影与信仰`;

  const content = $("#film-content");
  const authorById = id_ => AUTHORS.find(a => a.id === id_);
  content.innerHTML = `
    <div class="container">
      <a href="${film.reviews[0] ? "author.html?id=" + film.reviews[0].authorId : "index.html#featured"}" class="back-link">← 返回</a>
    </div>

    <section class="film-hero reveal">
      <div class="poster-full"></div>
      <div class="container">
        <div class="title-block">
          <h1>${film.title}</h1>
          <div class="en-title">${film.titleEn}</div>
        </div>
      </div>
    </section>

    <div class="container">
      <div class="film-body">
        <div class="meta-table reveal reveal-1">
          <div class="row"><div class="k">年份</div><div class="v">${film.year}</div></div>
          <div class="row"><div class="k">导演</div><div class="v">${film.director}</div></div>
          <div class="row"><div class="k">国别</div><div class="v">${film.country}</div></div>
          <div class="row"><div class="k">类型</div><div class="v">${film.genre}</div></div>
        </div>
        <div class="summary-block reveal reveal-2">
          <div class="label">主题摘要 · 本站自撰</div>
          <p>${film.summary}</p>
        </div>
      </div>

      <section class="reviews-block reveal reveal-3">
        <h2>评论出处</h2>
        ${film.reviews.map(r => {
          const a = authorById(r.authorId);
          const isArticle = !!r.excerpt;
          return `
            <div class="review-item">
              <div class="who">
                ${a.name} <span class="work">${r.work}</span>
                ${r.section ? `<span class="section">${r.section}</span>` : ""}
              </div>
              ${r.excerpt ? `<blockquote class="excerpt">${r.excerpt}</blockquote>` : ""}
              <a class="go" href="${r.source}" target="_blank" rel="noopener">${isArticle ? "前往原文 →" : "查看书籍 →"}</a>
            </div>
          `;
        }).join("")}
        <p style="margin-top:1.5rem;font-size:0.8rem;color:var(--muted);line-height:1.7">
          本站为导读索引，不搬运原文。带摘录的条目来自作者公开网络文章，引用范围符合合理使用原则，点击"前往原文"阅读完整文章；其余条目为作者影评文集中的章节，点击"查看书籍"跳转豆瓣图书条目。
        </p>
      </section>
    </div>
  `;
}

// 路由
const page = document.body.dataset.page;
if (page === "home") renderHome();
else if (page === "author") renderAuthor();
else if (page === "film") renderFilm();
