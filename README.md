# 英语长难句智能解析系统 (Sentence Analyzer) v2.0 终极版

这是一个基于 Vue 3 和 Gemini 大模型的全栈应用。经过全新的 **v2.0 宏观与微观双核引擎 (Dual-Engine)** 架构升级，本作已经从单一的语法拆解工具，正式进化为**“全能型的 AI 英语阅读伴读导师”**。

该项目采用深色毛玻璃美学设计，支持通过 SSE（Server-Sent Events）实现丝滑的流式打字机输出效果，并提供了一套极致优化过的“资深英语教授级”提示词工程。

---

## ✨ v2.0 核心双擎特性

### 🚀 引擎 1：【篇章导读模式】 (宏观扫描)
适用于将几千字的外刊、文学巨著或者生涩论文“整篇丢入”。大模型会在几秒钟内为您生成一份高维度的预习报告：
- **核心主旨**：一针见血地提炼文章到底在讲什么，补充相关的历史背景或隐喻。
- **情绪与文风**：帮你领略作者字里行间的“言外之意”（如讽刺、沉重、欢快等）。
- **高频生词本**：提前扫除阅读路上的 5-10 个核心词汇绊脚石。
- **长难句雷达 🎯**：系统会像雷达一样，精准扫描出全篇最容易踩坑的 1-2 个长难句。

### 🔬 引擎 2：【长难句精读模式】 (微观死磕)
深入到细胞级别的语法拆解，结合了强制思维链 (CoT) 和小样本 (Few-Shot) 的五模块深度解析引擎：
- **多维度深度解析**：涵盖意译/直译、意群拆分、重点词汇、主干与修饰成分语法分析。
- **全景精读模式 (Context)**：支持粘贴长难句的段落上下文，大模型根据语境推断代词指代和感情色彩。
- **书籍排版解析支持**：支持原生 Markdown 标记输入（如 `*斜体*` 或 `**加粗**`），精准剖析原著作者使用排版以强调特定概念或语气的意图。
- **专有词汇表接口 (Vocabulary Bank)**：输入自创词/专业术语，大模型翻译和解析将严格遵守预设词库。

### ⚡️ 独创交互：雷达级联 (Radar Interaction)
在【篇章导读】扫出最难的长难句后，其旁会自动生成一个**「一键精读 🎯」**按钮。用户无需复制粘贴，**只需轻轻一点，系统瞬间切回【长难句精读】引擎**并直接对这句话开刀！形成**“先宏观预习 -> 发现难点 -> 一键微观死磕”**的完美沉浸式闭环。

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
│   ├── prompt_engine.py    # 提示词引擎：支持针对不同模式动态加载 system_prompt
│   ├── output_formatter.py # 格式化验证器：自动修复异常格式，兼容多套 Tabs 结构
│   ├── database.py         # 数据库访问层：基于 aiosqlite 管理历史记录
│   ├── utils.py            # 工具函数：如长难句主干提取、语言检测
│   ├── data/               # 存放 SQLite 数据库文件 (自动生成)
│   └── prompts/            # 提示词模板存放目录
│       ├── system_prompt.j2           # 微观精读引擎的系统指令 (严格的五模块约束)
│       ├── system_prompt_article.j2   # 宏观导读引擎的系统指令 (主旨、文风、雷达)
│       ├── task_standard.j2           # 微观精读任务提示词 (整合了上下文、思维链)
│       ├── task_article.j2            # 宏观导读任务提示词
│       └── few_shots.j2               # 满分范例题库，用于精读模式的 Few-Shot 对齐
│
└── frontend/               # Vue 3 + Vite 前端应用
    ├── index.html
    ├── package.json
    ├── src/
    │   ├── main.js         # 前端入口
    │   ├── App.vue         # 根组件：左右分栏布局
    │   ├── style.css       # 基础样式重置
    │   ├── assets/
    │   │   └── main.css    # 全局核心样式表（含双模切换、雷达按钮等科幻组件样式）
    │   ├── components/
    │   │   ├── HistoryPanel.vue # 左侧历史记录列表组件
    │   │   ├── InputPanel.vue   # 核心输入组件（包含双模切换 Segments 控制器）
    │   │   ├── OutputPanel.vue  # 解析结果展示与一键复制控制组件
    │   │   └── TabsRenderer.vue # 选项卡渲染核心组件（深度集成雷达点击事件捕获）
    │   ├── stores/
    │   │   └── analyzer.js      # Pinia 状态管理：维护双擎数据状态隔离及联动跳转
    │   └── utils/
    │       └── markdown-renderer.js # 深度定制的 Markdown 解析器（处理雷达级联按钮注入）
```

---

## 🚀 运行指南 (极速部署)

如果未来你需要在全新的电脑上运行此项目，请严格按照以下步骤操作：

### 0. 基础工具安装 (仅限全新 Mac)
MacOS 系统自带 Python 3.9+（可通过 `python3 -V` 检查），完美满足本项目要求，无需额外折腾安装 Python。

打开终端 (Terminal) 执行以下命令：
```bash
# 1. 安装 Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. 一键安装 Node.js (前端) 和 Poetry (后端包管理器)
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
echo "GEMINI_API_KEY=AIzaSyYourApiKeyHere..." > .env
```
*(注意：项目已配置 `.gitignore`，绝对不会将你的真实 API Key 上传到公网)*

### 3. 安装依赖
```bash
# 安装后端依赖
cd backend && poetry install && cd ..

# 安装前端依赖
cd frontend && npm install && cd ..
```

### 4. 一键启动
```bash
chmod +x start.sh
./start.sh
```
启动成功后，在浏览器访问 `http://localhost:5173/` 即可尽情使用！

---

## 🛠️ v2.0 技术进化史与踩坑指南 (备忘)

1. **雷达级联按钮的 DOM 注入与事件穿透**
   要在 Markdown-it 解析的 HTML 字符串中放入可点击的 `<button>` 并绑定 Vue 的 `pinia` 状态跳转，直接写 `@click` 是无效的（会被当做死文本）。
   **解决**：在 `markdown-renderer.js` 中使用正则替换注入 `<button class="radar-btn">`，然后在挂载了 `v-html` 的父组件 `TabsRenderer.vue` 中利用**事件委托 (Event Delegation)** 捕获 `e.target.closest('.radar-btn')` 的点击事件，从而跨越框架边界调用 `store.switchToSentence()`。

2. **多引擎下的状态隔离**
   在同一个输入面板中混合了长难句的输入框与篇章的巨型文本框，很容易互相污染数据。
   **解决**：在 `analyzer.js` 状态库中将 `inputSentence` 和 `inputArticle` 彻底解耦，再使用 `computed` 的 `canAnalyze` 智能判定当前模式是否满足发送要求，保证多引擎切换如丝般顺滑。

3. **大模型的“雷达制导”失控**
   让大模型挑出长难句时，它偶尔会混入无关的评论或使用错误的引用格式，导致前端正则提取按钮失败。
   **解决**：在 `system_prompt_article.j2` 中加入极度严格的标记指令：`必须严格遵守 > 【雷达提取】 句子 的特定块引用格式`。大模型对其的敏感度极高，做到了 100% 完美提取。

4. **强制思维链 (CoT) 无痕隐藏**
   要求大模型进行思考推导，可以极大提升解析倒装句和从句的正确率，但直接输出会毁掉极简的 UI。
   **解决**：在提示词中命令模型将推理过程写入 HTML 注释 `<!-- 思维推导：... -->` 中。后端拿到了满分的智力成果，前端展示依旧干净利落！
