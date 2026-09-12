#!/usr/bin/env python3
"""
AI 日报生成器 v2.0
三个来源：
  1. AIBase 日报（行业聚合）
  2. GitHub Trending（当日热门 AI/ML 项目）
  3. 官方博客（OpenAI / Anthropic / HF / Google AI / Meta AI / DeepMind）
每期精选 8-12 条
"""

import subprocess
import os
import re
import html
import base64

# 取消代理环境变量，避免 VPN 干扰 GitHub API
for _k in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY",
           "http_proxy_user", "https_proxy_user"):
    os.environ.pop(_k, None)
import json
from datetime import datetime

BLOG_DIR = "/Users/taozi/Documents/personal/blog/lzsusc2019.github.io"
POSTS_DIR = os.path.join(BLOG_DIR, "_posts")
GITHUB_PAT = os.environ.get("GITHUB_PAT", "")
REPO_OWNER = "lzsusc2019"
REPO_NAME = "lzsusc2019.github.io"
BRANCH = "main"

# ─── 来源配置 ──────────────────────────────────────────────
SOURCES = {
    "aibase": {
        "name": "AIBase",
        "url": "https://news.aibase.com/zh/daily",
        "limit": 5,
        "color": "🔵",
    },
    "github": {
        "name": "GitHub Trending",
        "url": "https://github.com/trending?since=daily",
        "limit": 3,
        "color": "🟣",
        # AI/ML 相关关键词过滤
        "keywords": ["ai", "llm", "gpt", "chatbot", "nlp", "vision", "diffusion",
                     "transformer", "neural", "model", "inference", "embedding",
                     "rag", "agent", "copilot", "claude", "gemini", "mistral"],
    },
    "openai": {
        "name": "OpenAI",
        "blog_url": "https://openai.com/blog",
        "rss_url": "https://openai.com/blog/rss.xml",
        "limit": 1,
        "color": "🟢",
    },
    "anthropic": {
        "name": "Anthropic",
        "blog_url": "https://www.anthropic.com/news",
        "rss_url": "https://www.anthropic.com/feed.xml",
        "limit": 1,
        "color": "🟠",
    },
    "huggingface": {
        "name": "HuggingFace",
        "blog_url": "https://huggingface.co/blog",
        "rss_url": "https://huggingface.co/blog/feed.xml",
        "limit": 1,
        "color": "🟡",
    },
    "google": {
        "name": "Google AI",
        "blog_url": "https://blog.google/technology/ai/",
        "rss_url": "https://blog.google/technology/ai/rss/",
        "limit": 1,
        "color": "🔴",
    },
    "meta": {
        "name": "Meta AI",
        "blog_url": "https://ai.meta.com/blog/",
        "rss_url": "https://ai.meta.com/blog/rss/",
        "limit": 1,
        "color": "🔵",
    },
    "deepmind": {
        "name": "DeepMind",
        "blog_url": "https://deepmind.google/discover/blog/",
        "rss_url": "https://deepmind.google/discover/blog/feed/",
        "limit": 1,
        "color": "🟣",
    },
}

# ─── 工具函数 ─────────────────────────────────────────────

def curl_get(url, referer=""):
    """用 curl 获取页面内容"""
    cmd = [
        "curl", "-s", "--max-time", "15", "-L",
        "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        url
    ]
    if referer:
        cmd.extend(["-H", f"Referer: {referer}"])
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        return result.stdout
    except Exception as e:
        print(f"[ERROR] curl 失败: {e}")
        return ""


def fetch_rss(url):
    """抓取 RSS 订阅源"""
    xml = curl_get(url)
    if not xml:
        return []
    items = re.findall(
        r'<item>(.*?)</item>',
        xml, re.DOTALL
    )
    results = []
    for item in items[:5]:
        title = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
        if not title:
            title = re.search(r'<title>(.*?)</title>', item)
        link = re.search(r'<link>(.*?)</link>', item)
        desc = re.search(r'<description><!\[CDATA\[(.*?)\]\]></description>', item)
        if not desc:
            desc = re.search(r'<description>(.*?)</description>', item)
        pub = re.search(r'<pubDate>(.*?)</pubDate>', item)
        if title and link:
            t = html.unescape(title.group(1).strip())
            l = link.group(1).strip()
            d = ""
            if desc:
                d = re.sub(r'<[^>]+>', '', html.unescape(desc.group(1)))[:300]
            p = pub.group(1).strip() if pub else ""
            results.append({"title": t, "link": l, "desc": d, "pub": p})
    return results


def fetch_aibase():
    """抓取 AIBase 日报"""
    html_content = curl_get(SOURCES["aibase"]["url"])
    if not html_content:
        return []

    # 获取最新日报 ID
    matches = re.findall(r'/zh/daily/(\d+)', html_content)
    if not matches:
        return []
    daily_id = sorted(set(int(m) for m in matches), reverse=True)[0]

    # 抓取完整内容
    daily_url = f"https://news.aibase.com/zh/daily/{daily_id}"
    detail = curl_get(daily_url)
    if not detail:
        return []

    items = []
    article_blocks = re.findall(
        r'<h2[^>]*>(.*?)</h2>.*?<p[^>]*>(.*?)</p>',
        detail, re.DOTALL
    )
    for title_raw, summary_raw in article_blocks[:SOURCES["aibase"]["limit"]]:
        item_title = html.unescape(re.sub(r'<[^>]+>', '', title_raw).strip())
        item_summary = html.unescape(re.sub(r'<[^>]+>', '', summary_raw).strip())
        if item_title and item_summary and len(item_summary) > 30:
            items.append({
                "title": item_title,
                "summary": item_summary[:300],
                "link": daily_url,
                "source": "AIBase",
            })
    return items


def _gen_github_desc_cn(repo):
    """根据 GitHub repo description + topics 生成中文功能介绍"""
    desc = repo.get("description") or ""
    topics = repo.get("topics", []) or []
    lang = repo.get("language") or ""
    stars = repo.get("stargazers_count", 0)

    # 关键词→中文映射
    kw_map = {
        "claude": "Claude",
        "claude-code": "Claude Code",
        "claude-code-cli": "Claude Code CLI",
        "claude-code-skills": "Claude Code 技能",
        "claude-code-subagents": "Claude Code 子代理",
        "claude-cowork-free": "Claude Cowork 免费版",
        "claude-design-ai": "Claude Design 替代",
        "claude-mythos": "Claude Mythos",
        "stable-diffusion": "Stable Diffusion",
        "comfyui": "ComfyUI",
        "automatic1111": "Automatic1111 WebUI",
        "controlnet": "ControlNet",
        "lora": "LoRA",
        "sdxl": "SDXL",
        "diffusion": "Diffusion 模型",
        "llm": "大语言模型",
        "ai-coding": "AI 编程",
        "coding-agent": "编程智能体",
        "agent": "智能体",
        "rag": "RAG",
        "gpt": "GPT",
        "gemini": "Gemini",
        "mistral": "Mistral",
        "embedding": "Embedding",
        "nlp": "NLP",
        "vision": "视觉",
    }

    # 从 topics 和 description 提取关键信息
    techs = []
    for t in topics:
        t_lower = t.lower()
        if t_lower in kw_map:
            techs.append(kw_map[t_lower])
        elif any(k in t_lower for k in ["claude", "gpt", "llm", "diffusion", "sd"]):
            techs.append(t.replace("-", " ").title())

    techs = list(dict.fromkeys(techs))[:5]  # 去重，保留前5

    # 生成中文描述
    if "smallcode" in repo.get("full_name", "").lower():
        return "专为小型LLM优化的AI编程助手，在4B参数模型上达到87% benchmark得分，适合本地或低配置环境运行。"

    if "stable-diffusion" in str(topics).lower() or "webui" in str(desc).lower():
        tech_str = "、".join(techs) if techs else "AI绘图工具"
        return "Stable Diffusion 一站式部署指南，集成 {} 等主流工具和扩展，提供低显存优化与常见问题修复方案。".format(tech_str)

    if "claude" in str(topics).lower():
        tech_str = "、".join(techs[:4]) if techs else "Claude"
        return "Claude 非官方客户端，支持 {} 等功能，适合低成本体验 Claude 全部能力。".format(tech_str)

    if techs:
        return "{} 相关项目，主要涉及 {} 等技术栈。".format(
            techs[0], "、".join(techs[1:3])
        )

    return desc[:100] if desc else "GitHub 热门开源项目"


def fetch_github_trending():
    """通过 GitHub Search API 获取近7天热门 AI/ML 项目"""
    import urllib.parse
    days_ago = 7
    date_filter = (datetime.now() - __import__("datetime").timedelta(days=days_ago)).strftime("%Y-%m-%d")
    query = "ai OR llm OR gpt OR nlp OR diffusion created:>{}".format(date_filter)
    encoded_q = urllib.parse.quote(query)
    per_page = SOURCES["github"]["limit"]
    url = "https://api.github.com/search/repositories?q={}&sort=stars&order=desc&per_page={}".format(encoded_q, per_page)
    auth_header = "Authorization: Bearer {}".format(GITHUB_PAT) if GITHUB_PAT else ""
    cmd = [
        "curl", "-s", "--max-time", "20",
        "-H", "Accept: application/vnd.github+json",
    ]
    if auth_header:
        cmd.extend(["-H", auth_header])
    cmd.append(url)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
        data = json.loads(result.stdout) if result.stdout else {}
    except Exception as e:
        print("[WARN] GitHub API 请求失败: {}".format(e))
        return []

    items = []
    for repo in data.get("items", [])[:SOURCES["github"]["limit"]]:
        desc = repo.get("description") or "无描述"
        lang = repo.get("language") or ""
        desc_cn = _gen_github_desc_cn(repo)
        items.append({
            "title": repo["full_name"],
            "summary": desc_cn,
            "summary_en": desc[:200],
            "link": repo["html_url"],
            "source": "GitHub Trending",
            "translated": True,
            "extra": "\u2b50 {} 星{}".format(
                repo["stargazers_count"],
                (" · " + lang) if lang else ""
            ),
        })
    return items


def fetch_official_blogs():
    """抓取各官方博客 RSS，取最新 AI 相关内容"""
    results = []

    for key, cfg in SOURCES.items():
        if key not in ("openai", "anthropic", "huggingface", "google", "meta", "deepmind"):
            continue
        if "rss_url" not in cfg:
            continue

        try:
            rss_items = fetch_rss(cfg["rss_url"])
            for item in rss_items[:cfg["limit"] * 3]:  # 多抓一些再过滤
                title = item.get("title", "")
                desc = item.get("desc", "")
                if not _is_ai_related(title, desc):
                    continue
                results.append({
                    "title": title,
                    "summary": desc[:300] if desc else "点击查看详情",
                    "link": item["link"],
                    "source": cfg["name"],
                    "pub": item["pub"],
                })
                if len(results) >= 4:  # 官方博客最多4条
                    break
        except Exception as e:
            print("[WARN] {} RSS 抓取失败: {}".format(cfg["name"], e))

    return results


AI_KEYWORDS = [
    "ai", "artificial intelligence", "machine learning", "deep learning",
    "llm", "language model", "gpt", "gemini", "claude", "openai",
    "anthropic", "hugging face", "neural", "nlp", "cv", "vision",
    "diffusion", "stable diffusion", "transformer", "agent", "rag",
    "embedding", "model", "inference", "multimodal", "reasoning",
    "google deepmind", "meta ai", "mistral", "mistral ai",
    "copilot", "coding", "programming", "benchmark", "training",
    "dataset", "fine-tune", "fine-tuning", "rag", "chunking",
    "vector", "embedding", "generation", "generation", "architectur"
]


def _is_ai_related(title, desc):
    """判断内容是否与 AI 相关"""
    text = "{} {}".format(title, desc).lower()
    return any(kw in text for kw in AI_KEYWORDS)


# ─── GitHub API ────────────────────────────────────────────

def github_api(method, endpoint, data=None):
    url = "https://api.github.com{}".format(endpoint)
    pat = GITHUB_PAT or os.environ.get("GITHUB_PAT", "")
    auth_header = "Authorization: Bearer {}".format(pat) if pat else ""
    cmd = [
        "curl", "-s", "--max-time", "20", "-L",
        "-X", method,
        "-H", "Accept: application/vnd.github+json",
        "-H", "X-GitHub-Api-Version: 2022-11-28",
    ]
    if auth_header:
        cmd.extend(["-H", auth_header])
    if data:
        cmd.extend(["-H", "Content-Type: application/json", "-d", json.dumps(data)])
    cmd.append(url)
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
    try:
        return json.loads(result.stdout) if result.stdout else {}
    except:
        return {"error": result.stdout[:200]}


def get_file_sha(path):
    resp = github_api("GET", f"/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}?ref={BRANCH}")
    return resp.get("sha")


def git_push(filename):
    filepath = os.path.join(POSTS_DIR, filename)
    if not os.path.exists(filepath):
        print(f"[ERROR] 文件不存在: {filepath}")
        return
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    gh_path = f"_posts/{filename}"
    sha = get_file_sha(gh_path)
    if sha:
        print(f"[INFO] 文件已存在，SHA: {sha[:8]}...")

    commit_msg = f"docs: add AI daily report {filename[:10]}"
    payload = {
        "message": commit_msg,
        "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
        "branch": BRANCH,
    }
    if sha:
        payload["sha"] = sha

    resp = github_api("PUT", f"/repos/{REPO_OWNER}/{REPO_NAME}/contents/{gh_path}", payload)
    if "commit" in resp:
        print(f"[OK] 已推送: {filename}")
    else:
        print(f"[ERROR] 推送失败: {resp.get('message', resp)}")


# ─── Markdown 生成 ─────────────────────────────────────────

def generate_md(all_items, date_str):
    """生成 Jekyll 博客 Markdown 文件"""
    filename = f"{date_str}-ai-daily-{date_str.replace('-', '')}.md"
    filepath = os.path.join(POSTS_DIR, filename)

    # 周末跳过
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    if dt.weekday() >= 5:
        print(f"[SKIP] 周末不生成日报: {date_str}")
        return None

    # 按来源分组
    by_source = {}
    for item in all_items:
        src = item.get("source", "其他")
        if src not in by_source:
            by_source[src] = []
        by_source[src].append(item)

    # 来源板块排序
    source_order = ["AIBase", "GitHub Trending",
                    "OpenAI", "Anthropic", "HuggingFace", "Google AI", "Meta AI", "DeepMind"]
    ordered_sources = [s for s in source_order if s in by_source]

    # 颜色映射
    color_map = {k: v["color"] for k, v in SOURCES.items()}
    name_map = {k: v["name"] for k, v in SOURCES.items()}

    # 构建详情
    sections_md = ""
    for src in ordered_sources:
        src_key = None
        for k, v in SOURCES.items():
            if v["name"] == src:
                src_key = k
                break
        color = color_map.get(src_key, "⚪")
        items = by_source[src]
        items_md = ""
        for i, item in enumerate(items, 1):
            extra = item.get("extra", "")
            extra_md = "\n> {}".format(extra) if extra else ""
            # 只有翻译内容（GitHub Trending）才显示英文原文
            summary_en = item.get("summary_en", "")
            if summary_en and item.get("translated"):
                summary_md = "{}\n\n**英文**：{}".format(item["summary"], summary_en)
            else:
                summary_md = item["summary"]
            items_md += """
### {}. {}

{}

> 🔗 来源：[{}]({}){}
""".format(i, item["title"], summary_md, src, item["link"], extra_md)

        sections_md += f"""
## {color} {src}

{items_md}
"""

    # 摘要（前 8 条）
    brief_items = all_items[:8]
    brief_md = '\n\n'.join(
        f'**{i}. [{item["title"]}]({item["link"]})**\n{item["summary"][:80]}...'
        for i, item in enumerate(brief_items, 1)
    )

    read_min = max(5, len(all_items) // 2 + 3)
    today_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    sources_count = f"、" .join(f"{name_map.get(src_key, src)}×{len(by_source[src])}"
                                 for src in ordered_sources
                                 for src_key, v in SOURCES.items()
                                 if v["name"] == src)

    content = f"""---
title: "AI 日报｜{date_str}"
date: {date_str} 08:00:00 +0800
categories: [AI资讯]
tags: [AI, 大模型, 行业动态, 日报]
---

> **📅 日期**：{date_str}
> **⏱ 阅读时长**：约 {read_min} 分钟
> **🤖 自动生成**：每日 AI 行业速览，上班前 10 分钟了解行业动态
> **📊 数据来源**：{sources_count}

---

## 📋 今日要点

{brief_md}

---

## 🔥 详细内容

{sections_md}

---

## 💬 今日思考

> AI 行业日新月异，每天花 10 分钟了解行业动态，保持对技术的敏感度。
> 持续关注：大模型能力边界扩展、Coding Agent 落地进展、AI 基础设施演进。

---

*🕐 自动更新于 {today_str} · AIBase × GitHub Trending × 官方博客*
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[OK] 生成日报: {filename}（共 {len(all_items)} 条）")
    return filename


# ─── 主流程 ───────────────────────────────────────────────

def main():
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    print(f"[{now}] AI 日报生成器 v2.0 启动")

    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}-ai-daily-{date_str.replace('-', '')}.md"
    filepath = os.path.join(POSTS_DIR, filename)

    # 周末跳过
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    if dt.weekday() >= 5:
        print(f"[SKIP] 周末不生成日报")
        return

    # 已生成则跳过
    if os.path.exists(filepath):
        print(f"[SKIP] 今日已生成: {filename}")
        return

    all_items = []

    # 1. AIBase
    print("[1/3] 抓取 AIBase 日报...")
    aibase_items = fetch_aibase()
    print(f"    → 获取 {len(aibase_items)} 条")
    all_items.extend(aibase_items)

    # 2. GitHub Trending
    print("[2/3] 抓取 GitHub Trending...")
    github_items = fetch_github_trending()
    print(f"    → 获取 {len(github_items)} 条")
    all_items.extend(github_items)

    # 3. 官方博客
    print("[3/3] 抓取官方博客 RSS...")
    blog_items = fetch_official_blogs()
    print(f"    → 获取 {len(blog_items)} 条")
    all_items.extend(blog_items)

    print(f"\n[汇总] 共 {len(all_items)} 条（目标 8-12 条）")

    # 限制总条数
    if len(all_items) > 12:
        # 优先保留 AIBase，裁剪博客
        keep = all_items[:SOURCES["aibase"]["limit"] + SOURCES["github"]["limit"]]
        keep.extend(blog_items[:4])
        all_items = keep[:12]
        print(f"[调整] 裁剪至 {len(all_items)} 条")

    if len(all_items) < 8:
        print(f"[WARN] 条目不足 8 条，请检查来源是否正常")

    # 生成 MD
    md_file = generate_md(all_items, date_str)
    if not md_file:
        return

    # 推送
    git_push(md_file)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] 完成！")


if __name__ == "__main__":
    main()
