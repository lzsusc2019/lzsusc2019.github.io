# Blog 开发与维护规约

## 🛠 核心技术准则 (Avoid Errors)
1. **数据安全第一**：在执行任何批量 `sed` 或 `python` 脚本处理 `_posts` 目录前，必须进行二次校验，确保正文（Body）不被误删。
2. **字符洁净度**：严禁在文件开头引入不可见字符（如 `\x01`）。Front Matter 必须从文件的第 1 行第 1 列开始。
3. **路径稳定性**：由于 GitHub Pages 对中文 URL 支持不佳，所有文章必须在 Front Matter 中显式定义 `permalink`，格式为 `/posts/YYYYMMDD-title-in-english/`。

## ✍️ 文章风格规范 (Article Style)
1. **分类限制**：仅限 `[AI]`, `[Java]`, `[中间件]` 三大类，默认归入 `[Tech]`。
2. **代码高亮**：
   - 所有的 Java 代码片段必须使用 \` \` \`java 标识。
   - 禁止使用无标注的裸代码块。
3. **元数据要求**：
   - `layout: post` 必须存在。
   - `tags` 必须使用数组格式，例如 `tags: [Java, Spring]`。

## 📦 推送流程
1. 在执行 `git push` 前，必须向用户展示修改摘要。
2. 必须在用户回复确认后方可执行推送。
