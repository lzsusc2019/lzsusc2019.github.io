---
title: "Gemini CLI 常用命令速查手册"
date: 2026-05-08 10:00:00 +0800
categories: [AI工具,CLI]
tags: [AI, CLI, Productivity]
permalink: /posts/gemini-cli-commands/
layout: post
---

> **快速回想**：Gemini CLI 启动后，所有以 `/` 开头的指令都是内部控制命令。记住 `/help` 是你最好的朋友。
{: .prompt-info }

## 一、 会话控制 (Session Management)

### 1. 恢复与切换
- **列出所有历史会话**：
  ```bash
  /sessions
  ```
- **恢复指定会话**（支持 ID 简写）：
  ```bash
  /resume [session-id]
  ```
- **开启全新对话**：
  ```bash
  /new
  ```

### 2. 退出与中断
- **退出程序**：`/quit` 或 `/exit`
- **强行中断生成**：`Ctrl + C`
{: .prompt-warning }

---

## 二、 文件与代码操作 (File I/O)

### 1. 读取代码
> 将外部文件内容喂给 AI 的最快方式。
```bash
/read src/main/java/UserService.java
```

### 2. 快速写入
> 进入多行模式，输入内容后按 **Ctrl + D** 保存退出。
```bash
/write config.json
## ... 编辑内容 ...
## [Ctrl + D]
```
{: .prompt-tip }

---

## 三、 配置与模型切换 (Configuration)

### 1. 切换大脑 (Model)
根据任务复杂度选择模型：
```bash
/model gemini-2.5-pro   # 处理复杂架构与逻辑
/model gemini-2.0-flash # 追求极致响应速度
```

### 2. 状态检查
- **查看当前所有配置**：`/config`
- **查看 Token 消耗**：`/tokens`
- **对话健康检查**：`/doctor`

---

## 四、 核心工具管理 (Toolbelt)

### 1. 插件开关
```bash
/tools status           # 查看当前插件状态
/tools enable web_search # 开启联网搜索
/tools disable web_fetch # 关闭网页抓取
```

---

## 五、 常用命令汇总表

| 命令 | 分类 | 功能描述 |
| :--- | :--- | :--- |
| `/resume` | 会话 | 恢复上一次对话进度 |
| `/clear` | 界面 | 清理当前屏幕缓存 |
| `/history` | 记录 | 回溯本次对话的所有消息 |
| `/retry` | 纠错 | 让 AI 重新回答上一个问题 |
| `/think` | 模式 | 开启 Chain-of-Thought 深度思考 |
| `/export` | 导出 | 将对话保存为 .md 文件 |

---

## 💡 典型工作流示例

### 场景：代码审查并导出建议
1. **读取代码**：`/read Controller.java`
2. **发起提问**：`请分析这段代码的并发安全问题。`
3. **开启思考**：`/think` (如果需要更深度的回答)
4. **导出记录**：`/export review_result.md`
