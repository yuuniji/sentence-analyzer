# 英语长难句智能解析系统 (Sentence Analyzer)

这是一个基于 Vue 3 和 Gemini 大模型的全栈应用，专门用于深度拆解、翻译和分析英语长难句。

该项目采用深色毛玻璃美学设计，支持通过 SSE（Server-Sent Events）实现丝滑的流式打字机输出效果，并提供了专门针对语法解析优化的 Markdown 渲染体验。

## ✨ 核心特性

- **多维度深度解析**：涵盖意译/直译、意群拆分、重点词汇、主干与修饰成分语法分析。
- **高颜值深色 UI**：采用现代化的 Glassmorphism（毛玻璃）设计，视觉体验极佳。
- **SSE 流式输出**：接入 Gemini 大模型，实现实时逐字输出，告别漫长等待。
- **精美 Markdown 渲染**：深度定制了 `markdown-it` 解析器，完美支持复杂的嵌套 Tabs 选项卡和表格渲染。
- **一键复制分享**：内置“一键复制 Markdown”功能，完美保留所有格式，方便一键粘贴到博客或笔记软件（如 Obsidian, Notion）。
- **历史记录管理**：支持历史解析记录的本地持久化保存和分页查看。
- **动态模型切换**：实时拉取当前 API 密钥支持的可用模型列表（如 Gemini 2.5 Pro / Flash）进行自由切换。

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
│       └── task_standard.j2    # 具体任务分析提示词
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
    │   │   ├── InputPanel.vue   # 句子输入与模型控制组件
    │   │   ├── OutputPanel.vue  # 解析结果展示与一键复制控制组件
    │   │   └── TabsRenderer.vue # 选项卡渲染核心组件
    │   ├── stores/
    │   │   └── analyzer.js      # Pinia 状态管理：处理核心 SSE 数据流、记录刷新等
    │   └── utils/
    │       └── markdown-renderer.js # 自定义 Markdown 解析逻辑（解决大模型 Tabs 嵌套渲染等疑难杂症）
```

---

## 🚀 运行指南

### 1. 环境准备
- 后端需要 **Python 3.9+** 及 **Poetry** 包管理器。
- 前端需要 **Node.js 18+**。

### 2. 配置 API Key
在项目根目录下创建一个 `.env` 文件（如果没有的话），并填入你的 Google Gemini API Key：
```env
GEMINI_API_KEY=AIzaSyYourApiKeyHere...
```

### 3. 安装依赖
由于包含前后端两个项目，第一次运行前需分别安装依赖：
```bash
# 后端安装
cd backend
poetry install

# 前端安装
cd ../frontend
npm install
```

### 4. 一键启动
回到项目根目录，运行启动脚本即可：
```bash
chmod +x start.sh
./start.sh
```
该脚本会自动在后台启动 FastAPI (端口 8000) 和 Vite (端口 5173)。启动后直接在浏览器中访问 `http://localhost:5173/` 即可使用。

*停止服务只需在终端按下 `Ctrl+C`。*

---

## 🛠️ 技术原理与踩坑指南 (备忘)

1. **Jinja2 模板与 Vue/Gemini 语法的冲突**
   在 `system_prompt.j2` 中编写提示词时，如果提示词内包含 `{{...}}` 这种大模型指令或示范，会和 Jinja2 的变量插值语法冲突导致 `TemplateSyntaxError`。
   **解决**：使用 `{% raw %}` 和 `{% endraw %}` 将纯文本模板包裹起来。

2. **Python SSE 流式传输 `\n` 丢失问题**
   原生的 SSE 协议以及基于 `sse_starlette` 的 `yield chunk` 如果遇到刚好以换行符结尾的片段，换行符会在内部的 `splitlines()` 处理中被丢弃，导致前端收到的 Markdown 失去换行排版能力（特别是表格会变成单行乱码）。
   **解决**：将每个 chunk 用 JSON 对象包裹：`yield {"event": "chunk", "data": json.dumps({"text": chunk})}`，前端 `JSON.parse` 提取，确保换行符绝对安全。

3. **Markdown-it 渲染原生 HTML 与嵌套 Tabs**
   如果前端直接使用原生的 HTML 标签 `<details>` 包裹 Markdown-it 的 `::: tabs` 容器，必须保证 `<summary>` 之后有一个**空行**，否则 `markdown-it` 会判定其为整块 HTML 代码而放弃渲染内部的 Markdown 语法。
   同时，嵌套结构中，外部容器必须使用 4 个冒号 `:::: tabs`，内部子选项卡使用 3 个冒号 `::: tabpane`，否则渲染器层级识别会错乱导致一片空白。
   **解决**：在 `markdown-renderer.js` 中做了正则表达式预处理，强制补齐空行并区分冒号数量层级，完美渲染。

4. **Vue 的 v-html 与手动挂载 DOM 冲突**
   在 `TabsRenderer.vue` 中，用原生 JS `querySelectorAll` 去挂载选项卡按钮。这必须在 Vue 完成 `v-html` 的 DOM 更新后进行。
   **解决**：使用 `watch(..., { immediate: true })` 并在 `nextTick` 中调用挂载函数，确保无论是流式加载过程还是初始化历史记录回显，都能正确激活选项卡按钮。

---

## 📦 生产部署建议

如果未来需要将其部署到服务器面向外部使用：
1. 前端使用 `npm run build` 打包出静态文件，丢给 Nginx 代理。
2. 后端丢弃 `--reload`，使用 `gunicorn -k uvicorn.workers.UvicornWorker main:app` 进行生产级别的高并发部署。
3. 如果国内服务器无法直接访问 Google API，需在后端服务器配置代理，或者在后端代码的 `GeminiClient` 中配置反向代理（如通过 Cloudflare Worker）。
