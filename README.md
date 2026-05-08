# 个人技术博客

基于 [Jekyll Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy) 主题构建的极简、高性能技术博客。

## 🎯 核心理念 (Philosophy)
本项目遵循 **“快速回想 (Quick Recall)”** 风格：
- **高效检索**：侧边栏精准分类（AI、Java、中间件、算法）。
- **去冗余化**：文章开篇即核心模板与操作口诀。
- **视觉驱动**：精美代码高亮与层次分明的标题设计。

## 🛠️ 技术栈
- **主题**: Jekyll-Theme-Chirpy (Remote Theme 模式)
- **渲染引擎**: GitHub Actions (自动构建与部署)
- **语法高亮**: Rouge
- **增强功能**: Jekyll Spaceship (数学公式、流程图、表格增强)

## 💻 本地启动 (Local Development)

由于 Chirpy 主题对 Ruby 版本有严格要求 (>= 3.1)，推荐使用以下一键启动命令：

```bash
# 进入项目目录并自动配置环境、安装依赖、启动预览
cd lzsusc2019.github.io/ && \
export PATH="$(brew --prefix ruby@3.3)/bin:$PATH" && \
bundle install && \
bundle exec jekyll serve
```
访问地址: `http://127.0.0.1:4000`

## 🌐 远端配置 (Deployment)

### 1. 自动部署
项目已接入 **GitHub Actions**。每当您执行 `git push` 到 `main` 分支时，系统会自动执行：
- 环境校验 -> 静态资源编译 -> 部署至 `gh-pages` 分支。

### 2. 关键配置
所有的站点参数均在 `_config.yml` 中定义，包括：
- `remote_theme`: 确保云端 Layout 渲染正常。
- `permalink`: 解决了中文路径导致的 404 问题。

---
*更多开发规范详见项目根目录下的 [GEMINI.md](./GEMINI.md)*
