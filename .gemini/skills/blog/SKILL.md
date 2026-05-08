---
name: blog
description: 博客文章写作技能。当用户要写博客文章、发布文章、修改文章时激活。融合 GEMINI.md 写作规范与 Prospero 四阶段写作流程。
---

# 博客写作 Skill

## 写作哲学

**第一要义：博客是服务于"我"的。**
- 所有的内容必须以"快速回想"为终极目标。
- 拒绝废话，直击痛点。
- 看到标题和第一段，必须能立即唤起当时的解题思路或操作场景。

---

## 四阶段写作流程

### 阶段一：追问 (Interrogate)

通过苏格拉底追问，提炼文章骨架。

**核心问题**：
1. **论点**：核心观点是什么？一句话能说清吗？
2. **反驳**：最强反驳是什么？谁会反对？为什么？
3. **证据**：证据在哪？什么会让怀疑者改变想法？
4. **意义**：为什么读者应该关心？（So What?）

**输出格式**：
```markdown
# <标题>

## Thesis
<1-3句话核心论点>

## Antithesis
<最强反驳版本（smart, good-faith disagreer 会怎么想）>

## Synthesis
<综合后的结论>

## Entry Point
<切入点：故事、观察、历史案例>

## Sections
### <章节标题>
- **Claim**: 本节论点
- **Evidence**: 支撑（经验、数据、引用）
- **Objection**: 怀疑者会说什么
- **Resolution**: 如何回应

## So What?
<为什么读者应该关心？>

## Open Questions
<未解决的问题>
```

### 阶段二：批评 (Critique)

对立审查阶段。

**任务**：
1. 先读 `research.md` 已有研究
2. 检查论点是否严密
3. 补充分ounterarguments
4. 追加到 `research.md`

**检查清单**：
- [ ] Thesis 是否清晰？能否被一句话概括？
- [ ] Antithesis 是否是真实反驳，不是稻草人？
- [ ] 证据是否充分？是否有 thin evidence？
- [ ] "So What?" 是否有说服力？
- [ ] 各章节是否推进论点？

### 阶段三：创作 (Author)

根据提纲创作初稿。

**前置检查**：
- [ ] 已定义文风规则（参考 GEMINI.md）
- [ ] 已定义目标读者
- [ ] 有完整 outline

**写作规范**（来自 GEMINI.md）：

1. **标题层级**：
   - 禁止使用 `#`（H1）
   - 所有顶级章节使用 `##`
   - 标题前后必须保留空行

2. **Quick Recall 模块**：
   - 每篇文章开头使用 `{: .prompt-info }` 或 `{: .prompt-tip }` 总结核心要点
   - 算法类文章需在标题下标注时间/空间复杂度

3. **代码块**：
   - 必须标注语言（`java`, `bash`, `sql` 等）
   - 复杂代码块首行使用 `// filepath: ...` 标注
   - 关键行需添加简短中文注释

4. **视觉增强**：
   - 首次出现的关键术语使用 **加粗** 或 `行内代码`
   - Chirpy Callouts：
     - 提示：`{: .prompt-tip }`
     - 警告：`{: .prompt-warning }`
     - 关键点：`{: .prompt-info }`

5. **Chirpy Frontmatter**：
```yaml
---
layout: post
title: "<标题>"
date: YYYY-MM-DD
description: "<描述>"
tags: [标签1, 标签2]
categories: [父分类, 子分类]
permalink: /posts/YYYYMMDD-title/
---
```

### 阶段四：修订 (Revise)

修订润色阶段。

**循环**：`/blog revise` → 检查 → 修改，可多次迭代。

**修订检查点**：
- [ ] 每个章节是否都有意义？（不推进论点的删掉）
- [ ] 过渡是否自然？（不是简单的"接下来..."）
- [ ] 开头是否在两句话内钩住读者？
- [ ] 结尾是否有力量？（不模糊地暗示未来）
- [ ] voice.md 规则是否都遵守了？

---

## Skill 使用方式

### `/blog start [标题]`
开始新文章，进入追问阶段。

### `/blog write [slug]`
根据草稿创作初稿，进入创作阶段。

### `/blog revise [slug]`
修订已有草稿，进入修订阶段。

### `/blog critique [slug]`
批评审查草稿，进入批评阶段。

### `/blog list`
列出所有草稿。

### `/blog show [slug]`
显示草稿内容。

---

## 草稿存储

草稿存储在 `.gemini/skills/blog/drafts/<slug>/` 目录：

```
<slug>/
├── outline.md     # 大纲
├── research.md   # 研究资料
└── draft.md      # 初稿（如有）
```

---

## 与 GEMINI.md 的关系

本 Skill 继承并引用 GEMINI.md 中的所有写作规范：

- **排版风格**：标题层级、代码块、Chirpy Callouts
- **技术维护**：数据原子性、字符洁净度、路径稳定性
- **血泪教训**：禁止过度精简、严禁破坏索引

GEMINI.md 是长期生效的上下文，Skill 提供的是**写作流程框架**。
