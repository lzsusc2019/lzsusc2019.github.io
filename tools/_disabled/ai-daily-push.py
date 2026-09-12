#!/usr/bin/env python3
"""
AI 日报推送器 - 使用 GitHub REST API 直接上传文件
绕过 git push 的代理/凭证问题
"""

import subprocess
import os
import base64
import json
import time
from datetime import datetime

BLOG_DIR = "/Users/taozi/Documents/personal/blog/lzsusc2019.github.io"
POSTS_DIR = os.path.join(BLOG_DIR, "_posts")
GITHUB_PAT = os.environ.get("GITHUB_TOKEN", "")
REPO_OWNER = "lzsusc2019"
REPO_NAME = "lzsusc2019.github.io"
BRANCH = "main"
GITHUB_API = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"


def curl_api(method, endpoint, data=None, token=None):
    """通过 curl 调用 GitHub API"""
    import subprocess

    url = f"https://api.github.com{endpoint}"
    cmd = [
        "curl", "-s", "--max-time", "20", "-L",
        "-X", method,
        "-H", f"Authorization: Bearer {token}",
        "-H", "Accept: application/vnd.github+json",
        "-H", "X-GitHub-Api-Version: 2022-11-28",
        "-H", "Content-Type: application/json",
    ]
    if data:
        cmd.extend(["-d", json.dumps(data)])

    cmd.append(url)
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
    try:
        return json.loads(result.stdout) if result.stdout else {}
    except:
        return {"raw": result.stdout[:200]}


def get_file_sha(path):
    """获取仓库中已存在文件的 SHA"""
    import subprocess
    cmd = [
        "curl", "-s", "--max-time", "15",
        "-H", f"Authorization: Bearer {GITHUB_PAT}",
        "-H", "Accept: application/vnd.github+json",
        f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
    try:
        data = json.loads(result.stdout)
        return data.get("sha")
    except:
        return None


def upsert_file(path, content, message, sha=None):
    """创建或更新仓库中的文件"""
    import subprocess

    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}"
    data = {
        "message": message,
        "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
        "branch": BRANCH,
    }
    if sha:
        data["sha"] = sha

    json_data = json.dumps(data).replace('"', '"')
    cmd = [
        "curl", "-s", "--max-time", "20", "-L",
        "-X", "PUT",
        "-H", f"Authorization: Bearer {GITHUB_PAT}",
        "-H", "Accept: application/vnd.github+json",
        "-H", "X-GitHub-Api-Version: 2022-11-28",
        "-H", "Content-Type: application/json",
        "-d", json_data,
        url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
    try:
        resp = json.loads(result.stdout)
        if "content" in resp or "sha" in resp:
            return True, resp.get("commit", {}).get("sha", "")
        else:
            return False, resp.get("message", result.stdout[:200])
    except:
        return False, result.stdout[:200]


def git_push(filename):
    """git add + commit + 用 GitHub API push 代替 git push"""
    filepath = os.path.join(POSTS_DIR, filename)
    if not os.path.exists(filepath):
        print(f"[ERROR] 文件不存在: {filepath}")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    date_part = filename[:10]  # 2026-05-21
    commit_msg = f"docs: add AI daily report {date_part}"
    gh_path = f"_posts/{filename}"

    # 检查是否已存在（需要 SHA 来更新）
    sha = get_file_sha(gh_path)
    if sha:
        print(f"[INFO] 文件已存在，SHS: {sha[:8]}...")

    # 上传文件
    success, result = upsert_file(gh_path, content, commit_msg, sha=sha)
    if success:
        print(f"[OK] 已推送: {filename}")
        return True
    else:
        print(f"[ERROR] 推送失败: {result}")
        return False


def main():
    import subprocess
    # 取消代理环境变量
    env = os.environ.copy()
    for k in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"]:
        env.pop(k, None)
    subprocess.run(["git", "config", "--global", "--unset", "https.proxy"],
                   env=env, capture_output=True)

    date_today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_today}-ai-daily-{date_today.replace('-', '')}.md"
    filepath = os.path.join(POSTS_DIR, filename)

    if not os.path.exists(filepath):
        print(f"[SKIP] 本地文件不存在: {filename}")
        return

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] 开始推送: {filename}")
    git_push(filename)


if __name__ == "__main__":
    main()
