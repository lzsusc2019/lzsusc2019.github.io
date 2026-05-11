# Agent Skills 使用指南

> 为 AI 编程代理打造的生产级工程技能库

## 项目简介

agent-skills 是一套生产级工程技能库，包含 **22 个技能**，涵盖了软件开发的完整生命周期：定义 → 计划 → 构建 → 验证 → 审查 → 发布。

这些技能将资深工程师的开发流程、质量门槛和最佳实践编码为结构化的工作流，让 AI 代理能够一致地遵循工程规范。

## 支持的 AI 工具

| 工具 | 安装方式 |
|------|----------|
| **Claude Code** (推荐) | `/plugin marketplace add addyosmani/agent-skills` |
| **Gemini CLI** | `gemini skills install ./agent-skills/skills/` |
| **Cursor** | 复制 SKILL.md 到 `.cursor/rules/` |
| **Windsurf** | 添加到 Windsurf rules 配置 |
| **OpenCode** | 通过 AGENTS.md 和 `skill` 工具使用 |
| **GitHub Copilot** | 使用 `agents/` 作为人物设定 |

## 7 个斜杠命令

命令对应开发生命周期的各个阶段：

```
DEFINE          PLAN           BUILD          VERIFY         REVIEW          SHIP
┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐
│ Idea │ ───▶ │ Spec │ ───▶ │ Code │ ───▶ │ Test │ ───▶ │  QA  │ ───▶ │  Go  │
└──────┘      └──────┘      └──────┘      └──────┘      └──────┘      └──────┘
 /spec        /plan          /build        /test         /review        /ship
```

| 命令 | 技能 | 关键原则 |
|------|------|----------|
| `/spec` | spec-driven-development | 先规范后代码 |
| `/plan` | planning-and-task-breakdown | 小而原子化的任务 |
| `/build` | incremental-implementation | 增量构建 |
| `/test` | test-driven-development | 测试即证明 |
| `/review` | code-review-and-quality | 改进代码健康度 |
| `/code-simplify` | code-simplification | 清晰优于巧妙 |
| `/ship` | shipping-and-launch | 更快即更安全 |

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/addyosmani/agent-skills.git
```

### 2. 选择技能

浏览 `skills/` 目录，每个子目录包含一个 `SKILL.md` 文件：

- **When to Use** — 触发条件
- **Process** — 分步工作流
- **Verification** — 如何确认工作完成
- **Common Rationalizations** — 常见的跳过步骤的借口
- **Red Flags** — 技能被违反的信号

### 3. 加载技能到你的代理

**方式一：系统提示词**
在会话开始时粘贴技能内容。

**方式二：规则文件**
将技能内容添加到项目的规则文件（CLAUDE.md, .cursorrules 等）。

**方式三：对话中引用**
"请使用 test-driven-development 流程来实现这个功能。"

### 4. 使用元技能发现

从 `using-agent-skills` 技能开始，它包含一个流程图，将任务类型映射到合适的技能。

## 推荐的技能组合

### 最小配置（推荐入门）

加载三个核心技能：

1. **spec-driven-development** — 定义要构建什么
2. **test-driven-development** — 证明它能工作
3. **code-review-and-quality** — 合并前的质量验证

### 完整生命周期

按阶段加载技能：

```
项目启动:  spec-driven-development → planning-and-task-breakdown
开发阶段:  incremental-implementation + test-driven-development
合并前:    code-review-and-quality + security-and-hardening
发布前:    shipping-and-launch
```

### 上下文感知加载

不要一次加载所有技能，按当前任务加载相关技能：

- 做 UI 工作？加载 `frontend-ui-engineering`
- 调试？加载 `debugging-and-error-recovery`
- 设置 CI？加载 `ci-cd-and-automation`

## 22 个技能一览

### 元技能 - 发现适合的技能

| 技能 | 用途 | 使用场景 |
|------|------|----------|
| using-agent-skills | 将任务映射到正确的技能工作流 | 开始会话或不确定使用哪个技能 |

### Define - 明确要构建什么

| 技能 | 用途 | 使用场景 |
|------|------|----------|
| idea-refine | 结构化发散/收敛思维，将模糊想法转化为具体提案 | 有需要探索的粗略概念 |
| spec-driven-development | 编写 PRD，覆盖目标、命令、结构、代码风格、测试和边界 | 启动新项目、功能或重大变更 |

### Plan - 分解任务

| 技能 | 用途 | 使用场景 |
|------|------|----------|
| planning-and-task-breakdown | 将规范分解为小、可验证的任务，包含验收标准和依赖排序 | 有规范但需要可执行的单元 |

### Build - 编写代码

| 技能 | 用途 | 使用场景 |
|------|------|----------|
| incremental-implementation | 薄垂直切片 - 实现、测试、验证、提交。特性开关、安全默认值、回滚友好变更 | 任何涉及多文件更改 |
| test-driven-development | 红-绿-重构，测试金字塔 (80/15/5)，DAMP 优于 DRY，Beyonce 规则 | 实现逻辑、修复 bug 或更改行为 |
| context-engineering | 在正确的时间给代理正确的信息 - 规则文件、上下文打包、MCP 集成 | 开始会话、切换任务或输出质量下降 |
| source-driven-development | 基于官方文档验证、引用来源、标记未验证项 | 任何框架或库的权威、来源引用的代码 |
| doubt-driven-development | 对每个非常规决策进行对抗性审查 - CLAIM → EXTRACT → DOUBT → RECONCILE → STOP | 高风险（生产、安全、不可逆）、在不熟悉的代码中工作、输出便宜现在验证比以后调试 |
| frontend-ui-engineering | 组件架构、设计系统、状态管理、响应式设计、WCAG 2.1 AA 可访问性 | 构建或修改用户界面 |
| api-and-interface-design | 契约优先设计、Hyrum's Law、One-Version Rule、错误语义、边界验证 | 设计 API、模块边界或公共接口 |

### Verify - 证明它能工作

| 技能 | 用途 | 使用场景 |
|------|------|----------|
| browser-testing-with-devtools | Chrome DevTools MCP 获取实时运行数据 - DOM 检查、控制台日志、网络追踪、性能分析 | 构建或调试任何在浏览器中运行的内容 |
| debugging-and-error-recovery | 五步分类：复现、定位、减少、修复、守卫。停止线规则、安全回退 | 测试失败、构建中断或行为异常 |

### Review - 合并前的质量门

| 技能 | 用途 | 使用场景 |
|------|------|----------|
| code-review-and-quality | 五轴审查，变更大小（约 100 行），严重性标签（Nit/Optional/FYI），审查速度规范 | 合并任何变更前 |
| code-simplification | Chesterton's Fence，500 规则，在保持完全行为的同时降低复杂度 | 代码能工作但比应有的更难阅读或维护 |
| security-and-hardening | OWASP Top 10 预防、认证模式、密钥管理、依赖审计、三层边界系统 | 处理用户输入、认证、数据存储或外部集成 |
| performance-optimization | 先测量方法 - Core Web Vitals 目标、性能分析工作流、包分析、反模式检测 | 存在性能要求或怀疑性能退化 |

### Ship - 自信发布

| 技能 | 用途 | 使用场景 |
|------|------|----------|
| git-workflow-and-versioning | 基于主干的开发、原子提交、变更大小（约 100 行）、提交作为保存点模式 | 进行任何代码变更（始终） |
| ci-cd-and-automation | 左移、更快即更安全、特性开关、质量门流水线、失败反馈循环 | 设置或修改构建和部署流水线 |
| deprecation-and-migration | 代码即负债心态、强制性与建议性弃用、迁移模式、僵尸代码移除 | 移除旧系统、迁移用户或 sunset 功能 |
| documentation-and-adrs | 架构决策记录、API 文档、内联文档标准 - 记录 *why* | 做架构决策、更改 API 或发布功能 |
| shipping-and-launch | 发布前清单、特性开关生命周期、分阶段发布、回滚程序、监控设置 | 准备部署到生产环境 |

## 代理人物设定

项目还包含 3 个预配置的专业代理人物设定：

| 代理 | 角色 | 视角 |
|------|------|------|
| code-reviewer | 高级 Staff 工程师 | 五轴代码审查，"Staff 工程师会批准这个吗？" 标准 |
| test-engineer | QA 专家 | 测试策略、覆盖率分析和 Prove-It 模式 |
| security-auditor | 安全工程师 | 漏洞检测、威胁建模、OWASP 评估 |

## 参考清单

`references/` 目录包含技能需要时加载的补充材料：

| 参考 | 配合技能 |
|------|----------|
| testing-patterns.md | test-driven-development |
| security-checklist.md | security-and-hardening |
| performance-checklist.md | performance-optimization |
| accessibility-checklist.md | frontend-ui-engineering |

## 技能结构

每个技能遵循一致的结构：

```
┌─────────────────────────────────────────────────┐
│  SKILL.md                                       │
│                                                 │
│  ┌─ YAML Frontmatter ─────────────────────────┐ │
│  │ name: lowercase-hyphen-name               │ │
│  │ description: Guides agents through [task].│ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  Overview        → 这个技能做什么               │
│  When to Use     → 触发条件                    │
│  Process         → 分步工作流                  │
│  Rationalizations → 借口 + 反驳                 │
│  Red Flags       → 出错的信号                  │
│  Verification    → 证据要求                    │
└─────────────────────────────────────────────────┘
```

## Claude Code 详细安装

```bash
# 通过市场安装
/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills

# 如果遇到 SSH 错误，使用 HTTPS
/plugin marketplace add https://github.com/addyosmani/agent-skills.git
/plugin install agent-skills@addy-agent-skills

# 本地/开发模式
git clone https://github.com/addyosmani/agent-skills.git
claude --plugin-dir /path/to/agent-skills
```

## Gemini CLI 安装

```bash
# 从仓库安装
gemini skills install https://github.com/addyosmani/agent-skills.git --path skills

# 从本地克隆安装
gemini skills install ./agent-skills/skills/
```

## Cursor 安装

将任何 `SKILL.md` 复制到 `.cursor/rules/`，或引用完整的 `skills/` 目录。

详细说明见 [docs/cursor-setup.md](docs/cursor-setup.md)

## 项目结构

```
agent-skills/
├── skills/                            # 22 个技能 (21 个生命周期 + 1 个元技能)
│   ├── idea-refine/                   #   Define
│   ├── spec-driven-development/       #   Define
│   ├── planning-and-task-breakdown/   #   Plan
│   ├── incremental-implementation/    #   Build
│   ├── context-engineering/           #   Build
│   ├── source-driven-development/     #   Build
│   ├── doubt-driven-development/      #   Build
│   ├── frontend-ui-engineering/       #   Build
│   ├── test-driven-development/       #   Build
│   ├── api-and-interface-design/      #   Build
│   ├── browser-testing-with-devtools/ #   Verify
│   ├── debugging-and-error-recovery/  #   Verify
│   ├── code-review-and-quality/       #   Review
│   ├── code-simplification/          #   Review
│   ├── security-and-hardening/        #   Review
│   ├── performance-optimization/      #   Review
│   ├── git-workflow-and-versioning/   #   Ship
│   ├── ci-cd-and-automation/         #   Ship
│   ├── deprecation-and-migration/    #   Ship
│   ├── documentation-and-adrs/       #   Ship
│   ├── shipping-and-launch/           #   Ship
│   └── using-agent-skills/            #   元技能
├── agents/                            # 3 个专业代理人物设定
├── references/                        # 4 个补充清单
├── hooks/                             # 会话生命周期钩子
├── .claude/commands/                  # 7 个斜杠命令 (Claude Code)
├── .gemini/commands/                  # 7 个斜杠命令 (Gemini CLI)
└── docs/                              # 各工具的设置指南
```

## 关键设计原则

1. **流程，而非文章** - 技能是代理遵循的工作流，不是参考文档
2. **反合理化** - 每个技能包含常见借口的表格及反驳论点
3. **验证不可或缺** - 每个技能以证据要求结束
4. **渐进披露** - `SKILL.md` 是入口，支持参考资料仅在需要时加载

## 提示

1. 对任何非平凡工作，从 `spec-driven-development` 开始
2. 编写代码时始终加载 `test-driven-development`
3. 不要跳过验证步骤 - 这是全部意义所在
4. 选择性加载技能 - 更多上下文并不总是更好
5. 使用代理进行审查 - 不同视角发现不同问题
