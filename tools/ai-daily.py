#!/usr/bin/env python3
"""
AI 日报生成器
每天抓取 AIBase 最新 AI 日报，生成博客文章并推送到 GitHub
"""

import subprocess
import os
import re
import html
from datetime import datetime

BLOG_DIR = "/Users/taozi/Documents/personal/blog/lzsusc2019.github.io"
POSTS_DIR = os.path.join(BLOG_DIR, "_posts")


def curl_get(url, referer=""):
    """用 curl 获取页面内容，绕过反爬"""
    cmd = [
        "curl", "-s", "--max-time", "15",
        "-L",
        "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
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


def get_latest_daily_id():
    """获取最新日报 ID"""
    html_content = curl_get("https://news.aibase.com/zh/daily")
    if not html_content:
        return None
    matches = re.findall(r'/zh/daily/(\d+)', html_content)
    if matches:
        ids = sorted(set(int(m) for m in matches), reverse=True)
        return str(ids[0])
    return None


def fetch_daily_content(daily_id):
    """抓取指定日报的完整内容"""
    url = f"https://news.aibase.com/zh/daily/{daily_id}"
    html_content = curl_get(url)
    return html_content, url


def parse_aibase_daily(html_content, url):
    """解析 AIBase 日报 HTML，提取结构化数据"""

    # 提取标题
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content, re.DOTALL)
    title = ""
    if title_match:
        title = html.unescape(re.sub(r'<[^>]+>', '', title_match.group(1)).strip())

    # 提取发布时间
    date_match = re.search(
        r'(\d{4})年(\d{1,2})月(\d{1,2})号?\s*(\d{1,2}):(\d{2})',
        html_content
    )
    pub_date = datetime.now().strftime("%Y-%m-%d")
    if date_match:
        pub_date = (
            f"{date_match.group(1)}-"
            f"{date_match.group(2).zfill(2)}- "
            f"{date_match.group(3).zfill(2)}"
        )

    # 提取推荐区条目
    items = []
    article_blocks = re.findall(
        r'<h2[^>]*>(.*?)</h2>.*?<p[^>]*>(.*?)</p>',
        html_content, re.DOTALL
    )
    for title_raw, summary_raw in article_blocks[:8]:
        item_title = html.unescape(re.sub(r'<[^>]+>', '', title_raw).strip())
        item_summary = html.unescape(re.sub(r'<[^>]+>', '', summary_raw).strip())
        if item_title and item_summary and len(item_summary) > 30:
            items.append({
                "title": item_title,
                "summary": item_summary[:300]
            })

    # 如果没解析到，尝试提取链接文本
    if not items:
        text_blocks = re.findall(r'>([^<]{30,150})<', html_content)
        for block in text_blocks[:5]:
            clean = html.unescape(block.strip())
            if clean:
                items.append({
                    "title": clean[:60],
                    "summary": clean
                })

    return {
        "title": title or "AI 日报",
        "date": pub_date,
        "items": items,
        "url": url
    }


def generate_md(data, daily_id):
    """生成 Jekyll 博客 Markdown 文件"""
    date_str = data["date"]
    filename = f"{date_str}-ai-daily-{date_str.replace('-', '')}.md"
    filepath = os.path.join(POSTS_DIR, filename)

    # 周末跳过
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    if dt.weekday() >= 5:
        print(f"[SKIP] 周末不生成日报: {date_str}")
        return None

    # 构建详情
    items_md = ""
    for i, item in enumerate(data["items"][:6], 1):
        items_md += f"""
### {i}. {item['title']}

{item['summary']}

> 🔗 来源：[AIBase]({data['url']})
"""

    read_min = max(3, len(data["items"]) // 2 + 2)
    today_str = datetime.now().strftime('%Y-%m-%d %H:%M')

    items_brief = '\n\n'.join(
        f'**{i}. {item["title"]}**\n{item["summary"][:80]}...'
        for i, item in enumerate(data["items"][:6], 1)
    )

    content = f"""---
title: "{data['title']}"
date: {data['date']} 08:00:00 +0800
categories: [AI资讯]
tags: [AI, 大模型, 行业动态, 日报]
---

> **📅 日期**：{data['date']}  
> **⏱ 阅读时长**：约 {read_min} 分钟  
> **🤖 自动生成**：每日 AI 行业速览，上班前 10 分钟了解行业动态  
> **🔗 原文链接**：[AIBase 日报]({data['url']})

---

## 📰 今日要点

{items_brief}

---

## 🔥 详细速览

{items_md}

---

## 💬 今日思考

> AI 行业日新月异，每天花 10 分钟了解行业动态，保持对技术的敏感度。  
> 持续关注：大模型能力边界扩展、Coding Agent 落地进展、AI 基础设施演进。

---

*🕐 自动更新于 {today_str} · 数据来源：AIBase*
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[OK] 生成日报: {filename}")
    return filename


def git_push(filename):
    """Git add → commit → push"""
    subprocess.run(["git", "add", f"_posts/{filename}"],
                   cwd=BLOG_DIR, capture_output=True)
    msg = f"docs: add AI daily report {filename[:10]}"
    subprocess.run(["git", "commit", "-m", msg],
                   cwd=BLOG_DIR, capture_output=True)
    result = subprocess.run(["git", "push", "origin", "main"],
                           cwd=BLOG_DIR, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[WARN] push 输出: {result.stderr}")
    print(f"[OK] 已推送: {filename}")


def main():
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    print(f"[{now}] AI 日报生成器启动")

    # 1. 获取最新日报 ID
    daily_id = get_latest_daily_id()
    if not daily_id:
        print("[ERROR] 无法获取日报 ID")
        return
    print(f"[INFO] 最新日报 ID: {daily_id}")

    # 2. 检查是否已生成
    date_today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_today}-ai-daily-{date_today.replace('-', '')}.md"
    filepath = os.path.join(POSTS_DIR, filename)

    if os.path.exists(filepath):
        print(f"[SKIP] 今日已生成: {filename}")
        return

    # 3. 抓取并解析
    html_content, url = fetch_daily_content(daily_id)
    if not html_content:
        print("[ERROR] 抓取内容失败")
        return

    data = parse_aibase_daily(html_content, url)
    print(f"[INFO] 解析到 {len(data['items'])} 条内容: {data['title']}")

    # 4. 生成 MD
    md_file = generate_md(data, daily_id)
    if not md_file:
        return

    # 5. 推送
    git_push(md_file)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] 完成！")


if __name__ == "__main__":
    main()
