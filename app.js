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
// 至少有一条评论带全文摘录（即存在公开网络原文）
function hasWebText(f) {
  return f.reviews.some(r => r.excerpt);
}
// 本站自撰影评（originals.js 注册表）
function getOriginal(filmId) {
  return typeof ORIGINALS !== "undefined" ? ORIGINALS[filmId] : undefined;
}
function setMetaDescription(text) {
  let m = document.querySelector('meta[name="description"]');
  if (!m) {
    m = document.createElement("meta");
    m.setAttribute("name", "description");
    document.head.appendChild(m);
  }
  m.setAttribute("content", text);
}

// 通用页头/页脚注入
function injectChrome(activePage) {
  const topbar = `
    <header class="topbar">
      <div class="container">
        <a href="index.html" class="brand"><span class="mark">✦</span>道影</a>
        <nav class="nav-links">
          <a href="index.html" class="${activePage === 'home' ? 'active' : ''}">首页</a>
          <a href="index.html#featured" class="${activePage === 'films' ? 'active' : ''}">电影</a>
          <a href="index.html#authors" class="${activePage === 'authors' ? 'active' : ''}">作者</a>
          <a href="books.html" class="${activePage === 'books' ? 'active' : ''}">文集</a>
          <a href="index.html#disclaimer" class="${activePage === 'about' ? 'active' : ''}">关于</a>
        </nav>
      </div>
    </header>
  `;
  const footer = `
    <footer>
      <div class="container">
        <span class="mono">道影 daoying.org · 光影与信仰导读索引站</span>
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
      <a class="author-card reveal reveal-${Math.min(i + 1, 4)}" href="author.html?id=${a.id}">
        <div class="initial">${a.name[0]}</div>
        <div class="name">${a.name}</div>
        ${a.penName ? `<div class="pen">笔名 · ${a.penName}</div>` : `<div class="pen">&nbsp;</div>`}
        <div class="field">${a.title}<br><span style="color:var(--muted);font-size:0.78rem">${a.field}</span></div>
        <span class="arrow">→</span>
      </a>
    `).join("");
  }

  // 电影索引：搜索 + 按作者筛选
  const featuredRow = $("#featured-row");
  const searchInput = $("#film-search");
  const chipsWrap = $("#filter-chips");
  const filmsCount = $("#films-count");
  const sortSelect = $("#film-sort");
  const state = { q: "", authorId: "", sort: "year-desc" };
  // 首页索引：有公开网络原文，或有本站自撰影评
  const WEB_FILMS = FILMS.filter(f => hasWebText(f) || getOriginal(f.id));

  function matchingFilms() {
    const q = state.q.trim().toLowerCase();
    const films = WEB_FILMS.filter(f => {
      if (state.authorId && !f.reviews.some(r => r.authorId === state.authorId)) return false;
      if (!q) return true;
      return [f.title, f.titleEn, f.director, String(f.year), f.country, f.genre]
        .some(v => v && v.toLowerCase().includes(q));
    });
    if (state.sort === "year-desc") films.sort((a, b) => b.year - a.year);
    else if (state.sort === "year-asc") films.sort((a, b) => a.year - b.year);
    return films;
  }

  function reviewerNames(f) {
    return [...new Set(f.reviews.map(r => getAuthor(r.authorId)?.name).filter(Boolean))];
  }

  function renderFilms() {
    const films = matchingFilms();
    if (filmsCount) {
      filmsCount.textContent = films.length === WEB_FILMS.length
        ? `共 ${WEB_FILMS.length} 部 · 点击查看导读与出处`
        : `${films.length} / ${WEB_FILMS.length} 部`;
    }
    if (!films.length) {
      featuredRow.innerHTML = `<p class="no-results">没有匹配的电影。换个关键词，或清除筛选试试。</p>`;
      return;
    }
    const hasPosters = typeof POSTERS !== "undefined";
    featuredRow.innerHTML = films.map((f, i) => `
      <a class="film-card reveal reveal-${(i % 4) + 1}" href="film.html?id=${f.id}">
        ${hasPosters && POSTERS[f.id]
          ? `<img class="card-poster" src="posters/${POSTERS[f.id]}" alt="《${f.title}》海报" loading="lazy" />`
          : `<div class="card-poster card-poster-empty">✦</div>`}
        <div class="info">
          <div class="title">${f.title}</div>
          <div class="meta">${[f.year, f.director].filter(Boolean).join(" · ")}</div>
          <div class="blurb">${f.summary}</div>
          <div class="reviewers">评 · ${[...reviewerNames(f), ...(getOriginal(f.id) ? ['<span class="orig-flag">✦ 本站影评</span>'] : [])].join(" / ")}</div>
        </div>
      </a>
    `).join("");
  }

  if (featuredRow) {
    if (chipsWrap) {
      chipsWrap.innerHTML = [{ id: "", name: "全部" }, ...AUTHORS].map(a => `
        <button type="button" class="chip${a.id === state.authorId ? " active" : ""}" data-author="${a.id}">${a.name}</button>
      `).join("");
      chipsWrap.addEventListener("click", e => {
        const chip = e.target.closest(".chip");
        if (!chip) return;
        state.authorId = chip.dataset.author;
        $$(".chip", chipsWrap).forEach(c => c.classList.toggle("active", c === chip));
        renderFilms();
      });
    }
    if (searchInput) {
      searchInput.addEventListener("input", () => {
        state.q = searchInput.value;
        renderFilms();
      });
    }
    if (sortSelect) {
      sortSelect.addEventListener("change", () => {
        state.sort = sortSelect.value;
        renderFilms();
      });
    }
    renderFilms();
  }

  // 统计数字
  const statAuthors = $("#stat-authors");
  const statFilms = $("#stat-films");
  const authorsCount = $("#authors-count");
  if (statAuthors) statAuthors.textContent = AUTHORS.length;
  if (statFilms) statFilms.textContent = WEB_FILMS.length;
  if (authorsCount) authorsCount.textContent = `共 ${AUTHORS.length} 位 · 点击进入作者页`;

  const booksLink = $("#books-link");
  const bookOnly = FILMS.length - WEB_FILMS.length;
  if (booksLink && bookOnly > 0) {
    booksLink.innerHTML = `另有 ${bookOnly} 部影片的评论仅见于纸质文集（暂无网络全文）→ <a href="books.html">文集篇目</a>`;
  }
}

// ========= 文集篇目页渲染 =========
function renderBooks() {
  injectChrome("books");
  const films = FILMS.filter(f => !hasWebText(f));
  const hasPosters = typeof POSTERS !== "undefined";
  const authorById = id_ => AUTHORS.find(a => a.id === id_);
  $("#books-content").innerHTML = `
    <div class="container">
      <a href="index.html#featured" class="back-link">← 电影索引</a>
      <div class="section-head">
        <h2>文集篇目</h2>
        <span class="count">共 ${films.length} 部</span>
      </div>
      <p style="margin-bottom:2rem;font-size:0.9rem;color:var(--ink-dim);line-height:1.8">
        以下影片的评论仅收录于作者的纸质影评文集，暂无公开网络全文。点击卡片查看本站自撰导读与书籍出处（豆瓣图书页）。
      </p>
      <div class="featured-row">
        ${films.map((f, i) => `
          <a class="film-card reveal reveal-${(i % 4) + 1}" href="film.html?id=${f.id}">
            ${hasPosters && POSTERS[f.id]
              ? `<img class="card-poster" src="posters/${POSTERS[f.id]}" alt="《${f.title}》海报" loading="lazy" />`
              : `<div class="card-poster card-poster-empty">✦</div>`}
            <div class="info">
              <div class="title">${f.title}</div>
              <div class="meta">${[f.year, f.director].filter(Boolean).join(" · ")}</div>
              <div class="blurb">${f.summary}</div>
              <div class="reviewers">评 · ${[...new Set(f.reviews.map(r => authorById(r.authorId)?.name).filter(Boolean))].join(" / ")} · 见文集</div>
            </div>
          </a>
        `).join("")}
      </div>
    </div>
  `;
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
  document.title = `${author.name} — 道影`;

  const films = filmsByAuthor(id);
  setMetaDescription(`${author.name}（${author.title}）的影评导读：共评过 ${films.length} 部电影。研究领域：${author.field}。`);
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
                <div class="ft">${f.title}${f.titleEn ? `<span class="en">${f.titleEn}</span>` : ""}</div>
                <div class="fd">${[f.director, f.country, f.genre].filter(Boolean).join(" · ")}</div>
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
  document.title = `${film.title} — 道影`;
  setMetaDescription(`${film.title}（${film.titleEn}，${film.year}）影评导读。${film.summary.slice(0, 120)}…`);

  const content = $("#film-content");
  const authorById = id_ => AUTHORS.find(a => a.id === id_);
  // 有全文摘录的评论（公开网络原文）排在书籍引用之前
  const reviews = [...film.reviews].sort((a, b) => (b.excerpt ? 1 : 0) - (a.excerpt ? 1 : 0));
  content.innerHTML = `
    <div class="container">
      <a href="${reviews[0] ? "author.html?id=" + reviews[0].authorId : "index.html#featured"}" class="back-link">← 返回</a>
    </div>

    <section class="film-hero reveal">
      <div class="container">
        <div class="title-block">
          <h1>${film.title}</h1>
          ${film.titleEn ? `<div class="en-title">${film.titleEn}</div>` : ""}
        </div>
      </div>
    </section>

    <div class="container">
      <div class="film-body">
        <div class="reveal reveal-1">
          ${typeof POSTERS !== "undefined" && POSTERS[film.id]
            ? `<img class="poster-thumb" src="posters/${POSTERS[film.id]}" alt="《${film.title}》海报（低分辨率，仅作影片标识）" loading="lazy" />`
            : ""}
          <div class="meta-table">
          ${[["年份", film.year], ["导演", film.director], ["国别", film.country], ["类型", film.genre]]
            .filter(([, v]) => v)
            .map(([k, v]) => `<div class="row"><div class="k">${k}</div><div class="v">${v}</div></div>`).join("")}
          </div>
        </div>
        <div class="summary-block reveal reveal-2">
          <div class="label">主题摘要 · 本站自撰</div>
          <p>${film.summary}</p>
        </div>
      </div>

      ${getOriginal(film.id) ? `
      <section class="original-block reveal reveal-3">
        <h2>本站影评</h2>
        <a class="orig-card" href="review.html?id=${film.id}">
          <div class="orig-kicker">原创 · ${getOriginal(film.id).style}</div>
          <div class="orig-title">${getOriginal(film.id).title}</div>
          <span class="go">阅读全文 →</span>
        </a>
      </section>` : ""}

      <section class="reviews-block reveal reveal-3">
        <h2>评论出处</h2>
        ${reviews.map(r => {
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
          本站为导读索引，不搬运原文。带摘录的条目来自作者公开网络文章，引用范围符合合理使用原则，点击"前往原文"阅读完整文章；其余条目为作者影评文集中的章节，点击"查看书籍"跳转豆瓣图书条目。页面中的电影海报为低分辨率缩略图，仅用于标识所评影片，版权归属各制片方；如权利方提出异议，本站将及时移除。
        </p>
      </section>
    </div>
  `;
}

// ========= 本站影评阅读页渲染 =========
// original-reviews/<id>.md 是正文唯一来源：YAML front matter + Markdown。
// 这里只实现影评实际用到的 Markdown 子集（段落 / 二级标题 / 引用 / 粗斜体），保持零依赖。
function parseFrontMatter(text) {
  if (text.startsWith("---")) {
    const end = text.indexOf("\n---", 3);
    if (end !== -1) {
      const fm = {};
      text.slice(3, end).split("\n").forEach(line => {
        const i = line.indexOf(":");
        if (i > 0) fm[line.slice(0, i).trim()] = line.slice(i + 1).trim();
      });
      return { fm, body: text.slice(end + 4) };
    }
  }
  return { fm: {}, body: text };
}
function mdEscape(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
function mdInline(s) {
  return s.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>").replace(/\*([^*]+)\*/g, "<em>$1</em>");
}
function mdToHtml(md) {
  return md.split(/\n{2,}/).map(b => b.trim()).filter(Boolean).map(b => {
    if (b.startsWith("# ")) return ""; // 一级标题由页头渲染，不重复
    if (b.startsWith("## ")) return `<h2>${mdInline(mdEscape(b.slice(3)))}</h2>`;
    if (b.startsWith(">")) return `<blockquote>${mdInline(mdEscape(b.replace(/^> ?/gm, "")))}</blockquote>`;
    return `<p>${mdInline(mdEscape(b))}</p>`;
  }).join("\n");
}

function renderReview() {
  injectChrome("films");
  const content = $("#review-content");
  const id = (getParam("id") || "").replace(/[^a-z0-9-]/g, "");
  const film = getFilm(id);
  const orig = getOriginal(id);
  const notFound = msg => {
    content.innerHTML = `<div class="container" style="padding:4rem 0"><p>${msg}<a href="index.html">返回首页</a></p></div>`;
  };
  if (!film || !orig) return notFound("未找到该影评。");

  fetch(`original-reviews/${id}.md`)
    .then(res => { if (!res.ok) throw new Error(res.status); return res.text(); })
    .then(text => {
      const { fm, body } = parseFrontMatter(text);
      const title = orig.title || fm.film;
      document.title = `${title} — 光影与信仰`;
      const firstPara = body.split(/\n{2,}/).map(b => b.trim()).find(b => b && !b.startsWith("#")) || "";
      setMetaDescription(`《${film.title}》本站原创影评：${firstPara.slice(0, 110)}…`);
      content.innerHTML = `
        <div class="container">
          <a href="film.html?id=${id}" class="back-link">← 《${film.title}》</a>
        </div>

        <section class="film-hero reveal">
          <div class="container">
            <div class="title-block">
              <h1>${title}</h1>
              <div class="en-title">《${film.title}》${film.titleEn ? " · " + film.titleEn : ""}</div>
            </div>
          </div>
        </section>

        <div class="container">
          <article class="review-article reveal reveal-1">
            <div class="review-meta mono">
              ${[film.year, film.director, fm.style || orig.style, (fm.date || orig.date)].filter(Boolean).join(" · ")} · 本站原创
            </div>
            ${mdToHtml(body)}
            <div class="review-footnote">
              本文为"光影与信仰"原创影评，以基督信仰的眼光读电影。所引圣经经文采用和合本。
              欢迎链接分享；转载请注明出处。
              <a href="film.html?id=${id}">← 返回《${film.title}》影片页</a>
            </div>
          </article>
        </div>
      `;
    })
    .catch(() => notFound("影评加载失败。"));
}

// 路由
const page = document.body.dataset.page;
if (page === "home") renderHome();
else if (page === "author") renderAuthor();
else if (page === "film") renderFilm();
else if (page === "books") renderBooks();
else if (page === "review") renderReview();
