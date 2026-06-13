# 英语长难句智能解析系统 (Sentence Analyzer)

这是一个基于 Vue 3 和 Gemini 大模型的全栈应用，专门用于深度拆解、翻译和分析英语长难句。

该项目采用深色毛玻璃美学设计，支持通过 SSE（Server-Sent Events）实现丝滑的流式打字机输出效果，并提供了一套极致优化过的“资深英语教授级”提示词工程。

## ✨ 核心特性

- **多维度深度解析**：涵盖意译/直译、意群拆分、重点词汇、主干与修饰成分语法分析。
- **全景精读模式 (Context Mode)**：支持粘贴长难句的段落上下文。大模型不仅能准确解析句法，还能根据语境推断代词指代和感情色彩。
- **书籍排版解析支持**：支持原生 Markdown 标记输入（如 `*斜体*` 或 `**加粗**`），精准剖析原著作者使用排版以强调特定概念或语气的意图。
- **资深教授级提示词系统 (Advanced Prompt Engineering)**：
  - **强制思维链推导 (CoT)**：在后台使用不可见的 HTML 注释强制大模型进行（主干寻找 -> 枝叶拆解 -> 逻辑推理）步骤，大幅提升复杂从句和倒装句的分析准确率。
  - **内置满分语料库 (Few-Shot)**：内置教科书级别的“简·奥斯汀长难句”解析示范，强制锁定大模型的排版、语调和专业水准。
- **专有词汇表接口 (Vocabulary Bank)**：供用户在阅读奇幻小说或专业文献时输入自创词/专业术语，大模型翻译和解析将严格遵守预设词库。
- **高颜值深色 UI**：采用现代化的 Glassmorphism（毛玻璃）设计，视觉体验极佳。
- **SSE 流式输出与 Markdown 渲染**：接入 Gemini 大模型实现实时逐字输出。深度定制的 `markdown-it` 解析器完美支持复杂的嵌套 Tabs 选项卡和表格渲染。
- **一键复制分享**：完美保留所有格式，方便一键粘贴到博客或笔记软件（如 Obsidian, Notion）。
- **历史记录管理**：支持历史解析记录的本地持久化保存和分页查看。

---

## 📁 项目结构

项目分为前端 (`frontend`) 和后端 (`backend`) 两个独立的子目录：

```text
sentence-analyzer/
├── start.sh                # 全局一键启动脚本
├── .env                    # 系统环境变量配置文件 (存放 GEMINI_API_KEY)
│
├── backend/                # FastAPI 后端服务
│   ├── main.py             # 入口文件：定义 API 路由和 SSE 接口
│   ├── gemini_client.py    # 大模型服务层：封装流式和非流式 Gemini API 调用
│   ├── prompt_engine.py    # 提示词引擎：负责加载和渲染 Jinja2 模板
│   ├── output_formatter.py # 格式化验证器：自动尝试修复 LLM 返回的不规范格式
│   ├── database.py         # 数据库访问层：基于 aiosqlite 管理历史记录
│   ├── utils.py            # 工具函数：如长难句主干提取、语言检测
│   ├── data/               # 存放 SQLite 数据库文件 (自动生成)
│   └── prompts/            # 提示词模板存放目录
│       ├── system_prompt.j2    # 系统人设与严苛的 Markdown 格式输出规范
│       ├── task_standard.j2    # 具体任务分析提示词 (整合了上下文、自定义术语及思维链指引)
│       └── few_shots.j2        # 满分范例题库，用于大模型 Few-Shot 对齐
│
└── frontend/               # Vue 3 + Vite 前端应用
    ├── index.html
    ├── package.json
    ├── src/
    │   ├── main.js         # 前端入口
    │   ├── App.vue         # 根组件：左右分栏布局
    │   ├── style.css       # 基础样式重置
    │   ├── assets/
    │   │   └── main.css    # 全局核心样式表（含毛玻璃、主题色、自定义 Markdown 样式）
    │   ├── components/
    │   │   ├── HistoryPanel.vue # 左侧历史记录列表组件
    │   │   ├── InputPanel.vue   # 句子输入、上下文、专有词汇与模型控制组件
    │   │   ├── OutputPanel.vue  # 解析结果展示与一键复制控制组件
    │   │   └── TabsRenderer.vue # 选项卡渲染核心组件
    │   ├── stores/
    │   │   └── analyzer.js      # Pinia 状态管理：处理核心 SSE 数据流、记录刷新等
    │   └── utils/
    │       └── markdown-renderer.js # 自定义 Markdown 解析逻辑（解决大模型 Tabs 嵌套渲染等疑难杂症）
```

---

## 🚀 运行指南 (全新环境极速部署)

如果未来你换了新的 MacBook，或者需要在全新的电脑上运行此项目，请严格按照以下步骤操作：

### 0. 基础工具安装 (仅限全新 Mac)
MacOS 系统通常已经自带了 Python 3.9+（可通过 `python3 -V` 检查，如 `Python 3.9.6`），这已经完美满足本项目的运行要求，无需额外折腾安装 Python！

如果你的新电脑还没安装基础开发工具，请打开终端 (Terminal) 执行以下命令：

```bash
# 1. 安装 Homebrew (Mac 必备包管理器)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. 通过 Homebrew 一键安装 Node.js (前端) 和 Poetry (后端包管理器)
brew install node poetry
```

### 1. 克隆项目到本地
```bash
git clone https://github.com/yuuniji/sentence-analyzer.git
cd sentence-analyzer
```

### 2. 配置 API Key
在项目根目录创建一个 `.env` 文件，并填入你的 Google Gemini API Key：
```bash
# 在终端中快速创建
echo "GEMINI_API_KEY=AIzaSyYourApiKeyHere..." > .env
```
*(注意：千万不要把真实的 API Key 提交到 GitHub！项目中已经配置了 `.gitignore` 来忽略 `.env`)*

### 3. 安装依赖

**安装后端依赖：**
```bash
cd backend
# 直接使用系统自带的 Python 安装依赖
poetry install
cd ..
```

**安装前端依赖：**
```bash
cd frontend
# 安装 Vue 及其相关前端依赖
npm install
cd ..
```

### 4. 一键启动
回到项目根目录（`sentence-analyzer/`），赋予启动脚本执行权限并运行：
```bash
# 赋予执行权限 (仅需执行一次)
chmod +x start.sh

# 一键启动前后端服务
./start.sh
```
启动成功后，终端会打印出前后端的 PID。直接在浏览器中访问 `http://localhost:5173/` 即可尽情使用！

*如需停止服务，直接在当前终端按下 `Ctrl+C` 即可自动关闭所有关联进程。如果遇到端口被占用的报错（`Address already in use`），可以运行 `lsof -ti :8000 | xargs kill -9` 和 `lsof -ti :5173 | xargs kill -9` 强行清理残留进程。*

---

## 🛠️ 技术原理与踩坑指南 (备忘)

1. **CSS Flex 布局与 Markdown 解析冲突**
   如果标题 `<summary>` 内存在 HTML 标签（如将 `*斜体*` 转换为 `<em>斜体</em>` 后），`justify-content: space-between` 布局会将标签和普通文本无情拉开，产生巨大空隙。
   **解决**：在前端 Markdown 渲染器解析 `<summary>` 时，务必在内容外层包裹一个透明的 `<span>` 容器，强制将其视为单一的 flex 元素。

2. **Jinja2 模板与 Vue/Gemini 语法的冲突**
   在 `system_prompt.j2` 中编写提示词时，如果提示词内包含 `{{...}}` 这种大模型指令或示范，会和 Jinja2 的变量插值语法冲突导致 `TemplateSyntaxError`。
   **解决**：使用 `{% raw %}` 和 `{% endraw %}` 将纯文本模板包裹起来。

3. **Python SSE 流式传输 `\n` 丢失问题**
   原生的 SSE 协议以及基于 `sse_starlette` 的 `yield chunk` 如果遇到刚好以换行符结尾的片段，换行符会在内部的 `splitlines()` 处理中被丢弃，导致前端收到的 Markdown 失去换行排版能力（特别是表格会变成单行乱码）。
   **解决**：将每个 chunk 用 JSON 对象包裹：`yield {"event": "chunk", "data": json.dumps({"text": chunk})}`，前端 `JSON.parse` 提取，确保换行符绝对安全。

4. **Markdown-it 渲染原生 HTML 与嵌套 Tabs**
   如果前端直接使用原生的 HTML 标签 `<details>` 包裹 Markdown-it 的 `::: tabs` 容器，必须保证 `<summary>` 之后有一个**空行**，否则 `markdown-it` 会判定其为整块 HTML 代码而放弃渲染内部的 Markdown 语法。
   同时，嵌套结构中，外部容器必须使用 4 个冒号 `:::: tabs`，内部子选项卡使用 3 个冒号 `::: tabpane`，否则渲染器层级识别会错乱导致一片空白。
   **解决**：在 `markdown-renderer.js` 中做了正则表达式预处理，强制补齐空行并区分冒号数量层级，完美渲染。

5. **大模型的注意力偏移陷阱**
   当给大模型提供长篇上下文（Context）用于辅助解析特定句子时，大模型经常会“自作主张”去解析整个上下文段落。
   **解决**：在提示词中必须使用最强烈的词汇进行限制（如 `⚠️【核心警告】你必须且只能对上方的【待解析句子】进行拆解和翻译！绝对不要去解析【上下文参考】中的其他句子`）。

---

## 📦 生产部署建议

如果未来需要将其部署到服务器面向外部使用：
1. 前端使用 `npm run build` 打包出静态文件，丢给 Nginx 代理。
2. 后端丢弃 `--reload`，使用 `gunicorn -k uvicorn.workers.UvicornWorker main:app` 进行生产级别的高并发部署。
3. 如果国内服务器无法直接访问 Google API，需在后端服务器配置代理，或者在后端代码的 `GeminiClient` 中配置反向代理（如通过 Cloudflare Worker）。
