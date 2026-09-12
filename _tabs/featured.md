---
layout: page
title: 精选
icon: fas fa-star
order: 2
permalink: /featured/
---

这里按主题整理了几篇相对完整的文章。如果你只有几分钟，建议从 **AI Agent** 部分开始。

## AI Agent

围绕 Agent 从 Demo 走向生产的工程问题：编排模式怎么选、状态怎么管、工具链怎么搭。

- **[多 Agent 系统架构设计：从单体模型到分布式协同的模式演进](/posts/multi-agent-architecture-patterns/)**
  梳理 Sequential、Worker-Orchestrator、Debate、Dynamic Handoff 四类主流编排模式，以及各自的适用边界与生产选型建议。

- **[从「黑盒」到「数字组织」：多 Agent 设计范式的横纵深度解析](/posts/multi-agent-design-paradigms-deep-dive/)**
  从横向协作拓扑与纵向控制层级两个维度拆解多 Agent 设计，讨论如何把「角色分工」落到可维护的系统结构上。

- **[深度研报：Harness Engineering 的演进与控制大模型的工程实践](/posts/harness-engineering-deep-dive/)**
  讨论 Harness 这一层如何约束与引导模型行为——为什么同一模型换个 Harness 效果差异巨大，以及工程上如何设计。

- **[Agent Skills 使用指南：为 AI 编程代理构建工程技能库](/posts/agent-skills-guide/)**
  一套覆盖「定义 → 计划 → 构建 → 验证 → 审查 → 发布」的技能库，以及在 Claude Code、Gemini CLI、Cursor 等工具中的接入方式。

## 工程实践

线上问题的定位方法论，以及大规模系统演进中的取舍。

- **[生产环境四大经典问题排查指南：死锁、GC、OOM 与连接池](/posts/production-troubleshooting-guide/)**
  四类高频线上问题的排查路径：从现象到根因的定位顺序、常用工具与典型误判。

- **[数据库重连失败问题定位分析](/posts/db-reconnect-failure/)**
  一次数据库连接重连失败的完整定位过程，包含排查思路与最终根因。

## AI 工具

工具选型与效率实践，尽量讲清楚各家的真实生态位而不是罗列功能。

- **[谁在制造 Vibe Coding 幻觉？四款热门 AI 编程工具的真实生态位](/posts/vibe-coding-tools-comparison/)**
  Cursor、Claude Code、Gemini CLI、Copilot 的实际差异与各自擅长的场景。

- **[OpenClaw：开箱即用的个人 AI 助手架构详解](/posts/20260324-openclaw--ai/)**
  拆解其架构设计与扩展方式。

- **[Gemini CLI 常用命令速查手册](/posts/gemini-cli-commands/)**
  日常高频命令与配置速查。

## 算法与基础

题解与模板归档，偏重「思路为什么成立」而非只给代码。

- **[算法核心之双指针：从 O(N²) 到 O(N) 的时空跳跃](/posts/mastering-two-pointers/)**
- **[算法专题：动态规划之子序列问题](/posts/dp-subsequence/)**
- **[核心算法模板与题解归档](/posts/algo-templates/)**
- **[剑指 offer：全系列算法题解大归档](/posts/jianzhi-offer-all-in-one/)**

---

如果想按时间顺序浏览，见 [归档](/archives/)；也可以直接按 [分类](/categories/) 或 [标签](/tags/) 检索。
