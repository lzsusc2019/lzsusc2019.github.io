---
layout: post
title: "Gemini CLI 内部命令详解"
date: 2026-05-08
description: "全面介绍 Gemini CLI 内部的常用命令，包括 /resume、/quit、/help 等核心操作"
tags: [AI, CLI]
permalink: /posts/20260508-gemini-cli-commands/
---

## 前言

Gemini CLI 启动后，在交互界面中输入 `/` 开头的命令来控制对话、管理文件、调用工具。

---

## 一、退出与停止

### 退出 CLI

```
/quit
```

或直接输入：

```
/exit
```

### 停止当前生成

```
Ctrl + C
```

当 AI 正在输出时，按此组合键立即中断。

---

## 二、恢复与切换会话

### 恢复上一个会话

```
/resume
```

### 恢复指定会话

```
/sessions
```

先查看所有会话，找到 `session-id`：

```
/resume def456
```

### 切换会话

```
/switch
```

交互式选择切换到其他历史会话。

### 新建会话

```
/new
```

---

## 三、文件操作

### 读取文件

```
/read <file-path>
```

栗子：

```
/read README.md
/read src/main.java
```

### 写入文件

```
/write <file-path>
```

进入多行模式，输入完成后按 `Ctrl + D` 保存。

```
/write output.txt
# 输入内容...
# Ctrl + D 保存
```

### 编辑文件

```
/edit <file-path>
```

---

## 四、工具管理

### 查看工具列表

```
/tools
```

### 启用工具

```
/tools enable web_search
/tools enable web_fetch
```

### 禁用工具

```
/tools disable web_search
```

### 查看工具状态

```
/tools status
```

---

## 五、配置相关

### 查看当前配置

```
/config
```

### 切换模型

```
/model gemini-2.5-pro
```

常用模型：

| 模型 | 场景 |
|------|------|
| `gemini-2.5-pro` | 复杂推理 |
| `gemini-2.0-flash` | 快速响应 |

### 设置温度

```
/temperature 0.7
```

### 设置系统指令

```
/system 你是一个代码审查专家
```

---

## 六、信息查询

| 命令 | 功能 |
|------|------|
| `/help` | 显示帮助 |
| `/history` | 查看消息历史 |
| `/tokens` | 查看 Token 使用量 |
| `/session` | 查看当前会话信息 |

---

## 七、其他命令

| 命令 | 功能 |
|------|------|
| `/clear` | 清屏 |
| `/retry` | 重发上一条消息 |
| `/think` | 开启深度思考 |
| `/export` | 导出对话为 Markdown |
| `/doctor` | 健康检查 |

---

## 八、典型场景

### 场景一：续上昨天的对话

```
$ gemini
> /sessions
> /resume def456
```

### 场景二：读取代码并审查

```
> /read src/service/UserService.java
> 这段代码有什么问题？
```

### 场景三：保存输出到文件

```
> /write result.json
> { "status": "ok" }
> Ctrl + D
```

---

## 九、命令速查

```
退出相关：    /quit, /exit, Ctrl+C
会话管理：    /resume, /sessions, /switch, /new
文件操作：    /read, /write, /edit
工具管理：    /tools, /tools enable/disable
配置相关：    /config, /model, /temperature, /system
信息查询：    /help, /history, /tokens, /session
其他：        /clear, /retry, /think, /export, /doctor
```

---

## 参考资料

- [Gemini CLI 官方文档](https://ai.google.dev/gemini-api/docs)
