#!/usr/bin/env python3
"""把 original-reviews/*.md 同步到 WordPress.com 站点。

用法：
  WP_SITE=yourname.wordpress.com WP_TOKEN=xxx python3 publish_wordpress.py [film-id ...]
  python3 publish_wordpress.py --dry-run [film-id ...]   # 只生成 HTML 到 wp-preview/，不上传

行为：
  - 读取 originals.js 注册表；不带参数时同步全部，带 film-id 时只同步指定几篇
  - Markdown（front matter + 本站子集）转 HTML；海报与剧照上传到 WP 媒体库
  - 按 wp-sync.json 记录的 post_id 更新旧文，否则新建（slug = film-id）
  - 文末附"原载于 光影与信仰"回链；令牌只从环境变量读取，不落盘
"""

import json, os, re, sys, mimetypes, urllib.request, uuid, html

ROOT = os.path.dirname(os.path.abspath(__file__))
API = "https://public-api.wordpress.com/rest/v1.1/sites/{site}/{path}"
SITE_URL = "https://ferryzhou.github.io/christian-film-reviews"
SYNC_FILE = os.path.join(ROOT, "wp-sync.json")


def load_registry():
    src = open(os.path.join(ROOT, "originals.js"), encoding="utf-8").read()
    body = src[src.index("{", src.index("ORIGINALS")):src.index("};") + 1]
    body = re.sub(r"//[^\n]*", "", body)
    body = re.sub(r"(\w+):", r'"\1":', body)          # 键加引号（本文件的键无特殊字符）
    body = re.sub(r",\s*}", "}", body)
    return json.loads(body)


def load_posters():
    src = open(os.path.join(ROOT, "posters.js"), encoding="utf-8").read()
    return dict(re.findall(r'"([\w-]+)"\s*:\s*"([^"]+)"', src))


def parse_front_matter(text):
    fm = {}
    if text.startswith("---"):
        end = text.index("\n---", 3)
        for line in text[3:end].strip().splitlines():
            k, _, v = line.partition(":")
            if _:
                fm[k.strip()] = v.strip()
        text = text[end + 4:]
    return fm, text


def md_inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)
    return s


def md_to_html(md, img_url):
    """img_url: 本地相对路径 -> 已上传的媒体 URL 的映射函数"""
    out = []
    for block in re.split(r"\n{2,}", md):
        b = block.strip()
        if not b:
            continue
        if b.startswith("# "):
            continue  # 一级标题作为文章标题，由调用方使用
        if b.startswith("## "):
            out.append(f"<h2>{md_inline(b[3:])}</h2>")
            continue
        m = re.match(r"^!\[([^\]]*)\]\(([^)\s]+)\)$", b)
        if m:
            cap, src = m.group(1), m.group(2)
            url = img_url(src)
            fig = f'<figure><img src="{url}" alt="{html.escape(cap)}" />'
            if cap:
                fig += f"<figcaption>{md_inline(cap)}</figcaption>"
            out.append(fig + "</figure>")
            continue
        if b.startswith(">"):
            text = re.sub(r"^> ?", "", b, flags=re.M)
            out.append(f"<blockquote>{md_inline(text)}</blockquote>")
            continue
        out.append(f"<p>{md_inline(b)}</p>")
    return "\n".join(out)


def api_request(site, token, path, data=None, files=None):
    url = API.format(site=site, path=path)
    headers = {"Authorization": f"Bearer {token}"}
    if files:  # multipart 上传
        boundary = uuid.uuid4().hex
        body = b""
        for name, fname, blob in files:
            ctype = mimetypes.guess_type(fname)[0] or "application/octet-stream"
            body += (f"--{boundary}\r\nContent-Disposition: form-data; "
                     f'name="{name}"; filename="{fname}"\r\n'
                     f"Content-Type: {ctype}\r\n\r\n").encode() + blob + b"\r\n"
        for k, v in (data or {}).items():
            body += (f"--{boundary}\r\nContent-Disposition: form-data; "
                     f'name="{k}"\r\n\r\n{v}\r\n').encode()
        body += f"--{boundary}--\r\n".encode()
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
        req = urllib.request.Request(url, data=body, headers=headers)
    elif data is not None:
        headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers)
    else:
        req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    registry = load_registry()
    posters = load_posters()
    targets = args or list(registry)

    site = os.environ.get("WP_SITE", "")
    token = os.environ.get("WP_TOKEN", "")
    if not dry and (not site or not token):
        sys.exit("请设置 WP_SITE 与 WP_TOKEN 环境变量，或用 --dry-run 预览。")

    sync = json.load(open(SYNC_FILE)) if os.path.exists(SYNC_FILE) else {}
    media_cache = sync.setdefault("_media", {})

    for fid in targets:
        meta = registry.get(fid)
        if not meta:
            print(f"!! 注册表中无 {fid}，跳过"); continue
        path = os.path.join(ROOT, "original-reviews", f"{fid}.md")
        fm, body = parse_front_matter(open(path, encoding="utf-8").read())

        def img_url(rel):
            if dry:
                return f"{SITE_URL}/{rel}"
            if rel not in media_cache:
                fp = os.path.join(ROOT, rel)
                resp = api_request(site, token, "media/new",
                                   files=[("media[]", os.path.basename(fp), open(fp, "rb").read())])
                media_cache[rel] = resp["media"][0]["URL"]
                print(f"   上传图片 {rel}")
            return media_cache[rel]

        parts = []
        poster = posters.get(fid)
        if poster:
            parts.append(f'<figure class="wp-poster"><img src="{img_url("posters/" + poster)}" '
                         f'alt="《{fm.get("film", fid)}》海报" style="max-width:280px" /></figure>')
        sub = " · ".join(x for x in [fm.get("film") and f"《{fm['film']}》",
                                     fm.get("filmEn"), fm.get("year"), fm.get("director")] if x)
        parts.append(f"<p><em>{html.escape(sub)}</em></p>")
        parts.append(md_to_html(body, img_url))
        parts.append(f'<hr /><p><em>本文为"光影与信仰"原创影评，'
                     f'原载于 <a href="{SITE_URL}/review.html?id={fid}">光影与信仰 · 本站影评</a>。'
                     f"所引圣经经文采用和合本；文中配图为低分辨率剧照，仅作评论配图，版权归属见图注。</em></p>")
        content = "\n".join(parts)

        if dry:
            os.makedirs(os.path.join(ROOT, "wp-preview"), exist_ok=True)
            out = os.path.join(ROOT, "wp-preview", f"{fid}.html")
            open(out, "w", encoding="utf-8").write(
                f"<h1>{html.escape(meta['title'])}</h1>\n{content}")
            print(f"-- dry-run 生成 {out}")
            continue

        payload = {
            "title": meta["title"],
            "content": content,
            "slug": fid,
            "date": meta.get("date", "") + "T12:00:00",
            "categories": "影评",
            "tags": ",".join(x for x in [fm.get("film"), meta.get("style")] if x),
            "status": "publish",
        }
        if fid in sync:
            resp = api_request(site, token, f"posts/{sync[fid]}", data=payload)
            print(f"更新 {fid} -> {resp.get('URL')}")
        else:
            resp = api_request(site, token, "posts/new", data=payload)
            sync[fid] = resp["ID"]
            print(f"发布 {fid} -> {resp.get('URL')}")
        json.dump(sync, open(SYNC_FILE, "w"), ensure_ascii=False, indent=2)

    if not dry:
        json.dump(sync, open(SYNC_FILE, "w"), ensure_ascii=False, indent=2)
        print("完成。post 映射已存入 wp-sync.json")


if __name__ == "__main__":
    main()
