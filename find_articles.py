#!/usr/bin/env python3
"""
基督教电影评论文章搜索工具
用于持续更新 trae-films / christian-film-reviews 网站

用法:
  python3 find_articles.py search "电影名"          # 搜索某部电影的评论
  python3 find_articles.py search "电影名" --author shihengtan  # 限定作者来源
  python3 find_articles.py list-sources               # 列出所有已知来源
  python3 find_articles.py verify "https://..."       # 验证 URL 是否可访问并提取摘录
  python3 find_articles.py scan ebaomonthly           # 扫描某个来源的全部文章
  python3 find_articles.py generate                   # 交互式生成 data.js 条目
"""

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
import ssl

# ============================================================
# 已知文章来源
# ============================================================
SOURCES = {
    "ebaomonthly": {
        "name": "翼报",
        "base_url": "https://chs.ebaomonthly.com",
        "author_id": "shihengtan",
        "author_name": "石衡潭",
        "search_url": "https://chs.ebaomonthly.com/ebao/searchebao.php?q={query}",
        "url_pattern": r"ebaomonthly\.com/ebao/(?:read|print)ebao\.php\?a=\d+",
        "notes": "石衡潭在翼报'艺文走廊'专栏的影评文章，URL格式: ebaomonthly.com/ebao/readebao.php?a=YYYYMMDD"
    },
    "christiantimes": {
        "name": "基督时报",
        "base_url": "https://www.chinachristiantimes.com",
        "author_id": "christiantimes",
        "author_name": "基督时报福音影评",
        "search_url": "https://www.chinachristiantimes.com/search?q={query}",
        "url_pattern": r"chinachristiantimes\.com/news/\d+",
        "notes": "基督时报'福音影评'专栏，多位作者，URL格式: chinachristiantimes.com/news/编号"
    },
    "sina": {
        "name": "新浪",
        "base_url": "https://news.sina.com.cn",
        "author_id": "wangshuya",
        "author_name": "王书亚",
        "search_url": "https://search.sina.com.cn/?q={query}+电光倒影",
        "url_pattern": r"(?:sina\.cn|sina\.com\.cn)/.*detail-|news\.sina\.com\.cn/.+\.shtml",
        "notes": "王书亚'电光倒影'专栏，南方人物周刊授权新浪转载"
    },
    "sohu": {
        "name": "搜狐",
        "base_url": "https://www.sohu.com",
        "author_id": "wangshuya",
        "author_name": "王书亚",
        "search_url": "https://search.sohu.com/?keyword={query}+电光倒影",
        "url_pattern": r"sohu\.com/\d+/n\d+\.shtml",
        "notes": "王书亚'电光倒影'专栏，南方人物周刊授权搜狐转载"
    },
    "douban": {
        "name": "豆瓣",
        "base_url": "https://book.douban.com",
        "author_id": None,
        "author_name": "书籍引用",
        "search_url": "https://search.douban.com/book/subject_search?search_text={query}",
        "url_pattern": r"book\.douban\.com/subject/\d+",
        "notes": "豆瓣图书页面，用于书籍引用链接（非在线文章）"
    }
}

# 作者 ID -> 中文名 映射
AUTHOR_MAP = {
    "qihongwei": "齐宏伟",
    "shihengtan": "石衡潭",
    "wangshuya": "王书亚",
    "liuxiaofeng": "刘小枫",
    "christiantimes": "基督时报",
}

# 已收录的电影标题列表（用于去重）
EXISTING_FILMS = [
    "海上钢琴师", "密阳", "盗梦空间", "黑客帝国", "悲惨世界",
    "唐山大地震", "肖申克的救赎", "少年派的奇幻漂流", "找死专卖店", "赵氏孤儿",
    "深河", "300", "血色将至", "天狗", "树先生",
    "疯狂的石头", "致我们终将逝去的青春", "车票", "千里走单骑",
    "搜索", "云图", "阿米什的恩典", "母亲",
    "血战钢锯岭", "火星救援", "魔鬼代言人", "小萝莉的猴神大叔",
    "哪吒2", "默杀", "第二十条",
]

# ============================================================
# 工具函数
# ============================================================

def create_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def fetch_url(url, timeout=15):
    """获取 URL 内容，返回 HTML 文本"""
    ctx = create_ssl_context()
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            return resp.read().decode(charset, errors="replace")
    except Exception as e:
        return None

def verify_url(url):
    """验证 URL 是否可访问，返回 (状态码, 内容长度)"""
    ctx = create_ssl_context()
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    })
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            content = resp.read()
            return resp.status, len(content), content.decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, 0, ""
    except Exception as e:
        return 0, 0, str(e)

def extract_excerpt(html, max_len=300):
    """从 HTML 中提取文章摘录"""
    if not html:
        return ""
    # 移除 script 和 style
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    # 移除 HTML 标签
    text = re.sub(r'<[^>]+>', ' ', html)
    # 清理空白
    text = re.sub(r'\s+', ' ', text).strip()
    # 尝试找到正文内容（简单启发式：找最长的中文段落）
    paragraphs = re.split(r'[。！？\n]', text)
    best = ""
    for p in paragraphs:
        p = p.strip()
        if len(p) > len(best) and len(p) > 50:
            best = p
    if best:
        return best[:max_len] + ("..." if len(best) > max_len else "")
    return text[:max_len]

def extract_title(html):
    """从 HTML 中提取标题"""
    if not html:
        return ""
    m = re.search(r'<title>([^<]+)</title>', html)
    if m:
        title = m.group(1).strip()
        # 清理常见后缀
        for suffix in [" - 翼报", " - 基督时报", "_新浪", "_搜狐", " | ", "- 南方人物周刊"]:
            if suffix in title:
                title = title.split(suffix)[0].strip()
        return title
    return ""

def extract_urls_from_html(html, pattern):
    """从 HTML 中按正则提取 URL"""
    if not html:
        return []
    urls = re.findall(pattern, html)
    # 补全为完整 URL
    full_urls = []
    for u in urls:
        if u.startswith("http"):
            full_urls.append(u)
        else:
            full_urls.append("https://" + u)
    return list(set(full_urls))

# ============================================================
# 命令处理
# ============================================================

def cmd_list_sources():
    """列出所有已知来源"""
    print("=" * 60)
    print("已知文章来源")
    print("=" * 60)
    for key, src in SOURCES.items():
        print(f"\n  [{key}] {src['name']} — {src['author_name']}")
        print(f"    URL: {src['base_url']}")
        print(f"    说明: {src['notes']}")
    print(f"\n  已收录电影 ({len(EXISTING_FILMS)} 部):")
    for i, f in enumerate(EXISTING_FILMS):
        print(f"    {i+1}. {f}", end="")
        if (i + 1) % 5 == 0:
            print()
    print()

def cmd_search(query, author=None):
    """搜索文章"""
    print(f"\n搜索: '{query}'")
    if author:
        src = SOURCES.get(author)
        if not src:
            print(f"  未知来源: {author}")
            print(f"  可用来源: {', '.join(SOURCES.keys())}")
            return
        sources_to_search = {author: src}
    else:
        sources_to_search = SOURCES

    results = []
    for key, src in sources_to_search.items():
        if not src.get("search_url"):
            continue
        search_url = src["search_url"].format(query=urllib.parse.quote(query))
        print(f"\n  [{src['name']}] 搜索中... {search_url}")
        html = fetch_url(search_url)
        if not html:
            print(f"    无法获取页面")
            continue
        # 提取 URL
        pattern = src.get("url_pattern", "")
        if pattern:
            urls = extract_urls_from_html(html, pattern)
            print(f"    找到 {len(urls)} 个候选链接")
            for url in urls[:10]:
                print(f"      {url}")
                results.append({
                    "source": key,
                    "source_name": src["name"],
                    "author_id": src["author_id"],
                    "author_name": src["author_name"],
                    "url": url,
                })
        else:
            print(f"    无 URL 匹配模式")

    if not results:
        print("\n  未找到结果。可以尝试:")
        print("    1. 使用不同的关键词")
        print("    2. 直接访问网站搜索")
        for key, src in sources_to_search.items():
            if src.get("search_url"):
                print(f"       {src['name']}: {src['search_url'].format(query=urllib.parse.quote(query))}")
    else:
        print(f"\n  共找到 {len(results)} 个候选链接")
        print(f"  使用 'python3 find_articles.py verify <URL>' 验证并提取摘录")

    return results

def cmd_verify(url):
    """验证 URL 并提取摘录"""
    print(f"\n验证 URL: {url}")
    status, length, html = verify_url(url)
    print(f"  状态码: {status}")
    print(f"  内容长度: {length} bytes")

    if status == 200 and html:
        title = extract_title(html)
        excerpt = extract_excerpt(html)
        print(f"\n  标题: {title}")
        print(f"\n  摘录 ({len(excerpt)} 字):")
        print(f"  {excerpt[:500]}")

        # 尝试判断来源
        for key, src in SOURCES.items():
            if src["base_url"] in url or key in url:
                print(f"\n  来源: {src['name']} ({src['author_name']})")
                break

        # 生成 data.js 条目片段
        print(f"\n  --- data.js 条目模板 ---")
        print(f'  source: "{url}",')
        if excerpt:
            # 转义引号
            safe_excerpt = excerpt.replace('"', '\\"').replace('\n', ' ')[:200]
            print(f'  excerpt: "{safe_excerpt}",')
        return {"title": title, "excerpt": excerpt, "url": url, "status": status}
    else:
        print(f"  URL 不可访问或内容为空")
        return None

def cmd_scan(source_key):
    """扫描某个来源的全部文章"""
    src = SOURCES.get(source_key)
    if not src:
        print(f"未知来源: {source_key}")
        print(f"可用来源: {', '.join(SOURCES.keys())}")
        return

    print(f"\n扫描来源: {src['name']} ({source_key})")
    print(f"  基础 URL: {src['base_url']}")

    # 尝试访问专栏页面
    if source_key == "ebaomonthly":
        # 翼报艺文走廊
        urls_to_try = [
            "https://chs.ebaomonthly.com/ebao/categorylist.php?cat=12",
            "https://chs.ebaomonthly.com/ebao/searchebao.php?q=电影",
            "https://chs.ebaomonthly.com/ebao/searchebao.php?q=影评",
        ]
    elif source_key == "christiantimes":
        urls_to_try = [
            "https://www.chinachristiantimes.com/category/111/影视",
            "https://www.chinachristiantimes.com/search?q=影评",
            "https://www.chinachristiantimes.com/search?q=电影+信仰",
        ]
    elif source_key == "sina":
        urls_to_try = [
            "https://search.sina.com.cn/?q=王书亚+电光倒影",
            "https://search.sina.com.cn/?q=电光倒影+电影",
        ]
    elif source_key == "sohu":
        urls_to_try = [
            "https://search.sohu.com/?keyword=王书亚+电光倒影",
        ]
    else:
        urls_to_try = [src["base_url"]]

    all_urls = []
    for url in urls_to_try:
        print(f"\n  扫描: {url}")
        html = fetch_url(url)
        if not html:
            print(f"    无法获取")
            continue
        pattern = src.get("url_pattern", "")
        if pattern:
            found = extract_urls_from_html(html, pattern)
            print(f"    找到 {len(found)} 个链接")
            for u in found:
                if u not in all_urls:
                    all_urls.append(u)
        else:
            print(f"    无匹配模式")

    # 过滤掉已收录的
    print(f"\n  共发现 {len(all_urls)} 个唯一 URL")
    print(f"\n  可逐一验证:")
    for u in all_urls[:30]:
        print(f"    python3 find_articles.py verify '{u}'")

    return all_urls

def cmd_generate():
    """交互式生成 data.js 电影条目"""
    print("\n=== 生成 data.js 电影条目 ===\n")

    film = {}
    film["id"] = input("电影 ID (拼音，如 haishang-piano): ").strip()
    film["title"] = input("中文片名: ").strip()
    film["titleEn"] = input("英文片名: ").strip()
    film["year"] = input("年份: ").strip()
    film["director"] = input("导演: ").strip()
    film["country"] = input("国家: ").strip()
    film["genre"] = input("类型 (如 剧情 / 战争): ").strip()
    film["summary"] = input("剧情+评论摘要 (1-2句): ").strip()

    print("\n--- 添加评论 ---")
    reviews = []
    while True:
        review = {}
        print(f"\n评论 #{len(reviews) + 1}:")
        print("  作者ID可选: " + ", ".join(f"{k}({v})" for k, v in AUTHOR_MAP.items()))
        review["authorId"] = input("  作者 ID: ").strip()
        review["work"] = input("  出处 (如 翼报·艺文走廊): ").strip()
        review["section"] = input("  文章标题: ").strip()
        review["source"] = input("  文章 URL: ").strip()
        excerpt = input("  摘录 (1-2段，回车结束): ").strip()
        if excerpt:
            review["excerpt"] = excerpt
        reviews.append(review)

        more = input("\n  继续添加评论? (y/n): ").strip().lower()
        if more != "y":
            break

    film["reviews"] = reviews

    # 生成 JS 代码
    print("\n\n=== 生成的 data.js 条目 ===\n")
    print("  {")
    print(f'    id: "{film["id"]}",')
    print(f'    title: "{film["title"]}",')
    print(f'    titleEn: "{film["titleEn"]}",')
    print(f'    year: {film["year"]},')
    print(f'    director: "{film["director"]}",')
    print(f'    country: "{film["country"]}",')
    print(f'    genre: "{film["genre"]}",')
    print(f'    summary: "{film["summary"]}",')
    print(f'    reviews: [')

    for i, r in enumerate(reviews):
        print("      {")
        print(f'        authorId: "{r["authorId"]}",')
        print(f'        work: "{r["work"]}",')
        print(f'        section: "{r["section"]}",')
        print(f'        source: "{r["source"]}",')
        if "excerpt" in r:
            safe = r["excerpt"].replace('"', '\\"').replace('\n', ' ')
            print(f'        excerpt: "{safe}"')
        print("      }" + ("," if i < len(reviews) - 1 else ""))

    print("    ]")
    print("  },")

    print(f"\n将以上条目插入 data.js 的 FILMS 数组末尾（最后一个 ] 之前）。")

# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="基督教电影评论文章搜索工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s list-sources                    # 列出所有已知来源
  %(prog)s search "血战钢锯岭"              # 搜索某部电影
  %(prog)s search "云图" --author ebaomonthly  # 限定来源搜索
  %(prog)s verify "https://chs.ebaomonthly.com/ebao/readebao.php?a=20130501"  # 验证URL
  %(prog)s scan ebaomonthly                # 扫描翼报全部文章
  %(prog)s generate                        # 交互式生成data.js条目
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="命令")

    # list-sources
    subparsers.add_parser("list-sources", help="列出所有已知文章来源")

    # search
    sp_search = subparsers.add_parser("search", help="搜索电影评论文章")
    sp_search.add_argument("query", help="搜索关键词（电影名等）")
    sp_search.add_argument("--author", "-a", choices=list(SOURCES.keys()),
                          help="限定搜索来源")

    # verify
    sp_verify = subparsers.add_parser("verify", help="验证 URL 并提取摘录")
    sp_verify.add_argument("url", help="要验证的 URL")

    # scan
    sp_scan = subparsers.add_parser("scan", help="扫描某个来源的全部文章")
    sp_scan.add_argument("source", choices=list(SOURCES.keys()),
                        help="来源名称")

    # generate
    subparsers.add_parser("generate", help="交互式生成 data.js 电影条目")

    args = parser.parse_args()

    if args.command == "list-sources":
        cmd_list_sources()
    elif args.command == "search":
        cmd_search(args.query, args.author)
    elif args.command == "verify":
        cmd_verify(args.url)
    elif args.command == "scan":
        cmd_scan(args.source)
    elif args.command == "generate":
        cmd_generate()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
