# 英语长难句与口语智能解析评估平台 (Sentence & Spoken Analyzer) v3.0 终极版

这是一个基于 Vue 3 和 Gemini 大模型的全栈应用。经过全新的 **v3.0 宏观、微观与口语三核引擎 (Triple-Engine)** 架构升级，本作已经从最初的语法拆解工具，正式进化为 **“全能型的 AI 英语伴读与口语评估导师”** 。

该项目采用深色毛玻璃美学设计，支持通过 SSE（Server-Sent Events）实现长难句与篇章的流式打字机输出效果，并提供了一套极致优化过的“资深英语教授级”提示词工程和结构化 JSON 纠错模型。

---

## v3.0 核心三核引擎特性

### 引擎 1：【篇章导读模式】 (宏观扫描)
适用于将几千字的外刊、文学巨著或者生涩论文“整篇丢入”。大模型会在几秒钟内为您生成一份高维度的预习报告：
- **核心主旨** ：一针见血地提炼文章到底在讲什么，补充相关的历史背景或隐喻。
- **情绪与文风** ：帮你领略作者字里行间的“言外之意”（如讽刺、沉重、欢快等）。
- **高频生词本** ：提前扫除阅读路上的 5-10 个核心词汇绊脚石。
- **长难句雷达** ：系统会像雷达一样，精准扫描出全篇最容易踩坑的 1-2 个长难句。

### 引擎 2：【长难句精读模式】 (微观死磕)
深入到细胞级别的语法拆解，结合了强制思维链 (CoT) 和小样本 (Few-Shot) 的五模块深度解析引擎：
- **多维度深度解析** ：涵盖意译/直译、意群拆分、重点词汇、主干与修饰成分语法分析。
- **全景精读模式 (Context)** ：支持粘贴长难句的段落上下文，大模型根据语境推断代词指代和感情色彩。
- **书籍排版解析支持** ：支持原生 Markdown 标记输入（如 `*斜体*` 或 `**加粗**` ），精准剖析原著作者使用排版以强调特定概念或语气的意图。
- **专有词汇表接口 (Vocabulary Bank)** ：输入自创词/专业术语，大模型翻译和解析将严格遵守预设词库。

### 引擎 3：【口语语法与发音评估】 (口语纠错)
面向英语学习者的口语发音与语法纠错引擎，支持网页端一键录音和智能打分剖析：
- **细粒度单词纠错** ：支持识别发音问题（Pronunciation）、语法错误（Grammar）、词汇不当（Vocabulary）、多余重复词（Deleted）、遗漏词补全（Insertion）、语气停顿词（Filler）和长停顿（Pause）。
- **单词级高亮呈现** ：前端使用不同颜色的高亮标签和删除线，将口语中的毛病和正确的修改建议一一对照呈现。
- **口语深度句法剖析** ：提供修正后文本的自然翻译（信达雅）、意群拆分、重点词汇精讲、语法主干/修饰枝叶解析。
- **导师综合点评** ：针对学习者的口语表现提供温暖且专业的改进小结。

### 独创交互：雷达级联 (Radar Interaction)
在【篇章导读】扫出最难的长难句后，其旁会自动生成一个 **「一键精读」** 按钮。用户无需复制粘贴， **只需轻轻一点，系统瞬间切回【长难句精读】引擎** 并直接对这句话开刀！形成 **“先宏观预习 -> 发现难点 -> 一键微观死磕”** 的完美沉浸式闭环。

---

## 项目结构

项目分为前端 (`frontend`) 和后端 (`backend`) 两个独立的子目录：

```text
sentence-analyzer/
├── start.sh                # 全局一键启动脚本
├── .env                    # 系统环境变量配置文件 (存放 GEMINI_API_KEY)
│
├── backend/                # FastAPI 后端服务
│   ├── main.py             # 入口文件：定义 API 路由和 SSE 接口（含口语上传接口）
│   ├── gemini_client.py    # 大模型服务层：封装流式 Gemini API 及结构化口语 JSON 分析
│   ├── prompt_engine.py    # 提示词引擎：支持针对不同模式动态加载 system_prompt
│   ├── output_formatter.py # 格式化验证器：自动修复异常格式，兼容多套 Tabs 结构
│   ├── database.py         # 数据库访问层：基于 aiosqlite 管理历史记录（支持 spoken 模式）
│   ├── utils.py            # 工具函数：如长难句主干提取、语言检测
│   ├── data/               # 存放 SQLite 数据库文件 (自动生成)
│   └── prompts/            # 提示词模板存放目录
│       ├── system_prompt.j2           # 微观精读引擎的系统指令 (严格的五模块约束)
│       ├── system_prompt_article.j2   # 宏观导读引擎的系统指令 (主旨、文风、雷达)
│       ├── task_standard.j2           # 微观精读任务提示词 (整合了上下文、思维链)
│       ├── task_article.j2            # 宏观导读任务提示词
│       └── few_shots.j2               # 满分范例题库，用于精读模式 of Few-Shot 对齐
│
└── frontend/               # Vue 3 + Vite 前端应用
    ├── index.html
    ├── package.json
    ├── src/
    │   ├── main.js         # 前端入口
    │   ├── App.vue         # 根组件：浮动导航，支持三模切换
    │   ├── style.css       # 基础样式重置
    │   ├── assets/
    │   │   └── main.css    # 全局核心样式表（含双模切换、录音面板、高亮标签等样式）
    │   ├── components/
    │   │   ├── HistoryPanel.vue # 左侧历史记录列表组件
    │   │   ├── InputPanel.vue   # 核心输入组件（包含长难句、篇章及口语录音面板）
    │   │   ├── OutputPanel.vue  # 解析结果展示与一键复制控制组件
    │   │   ├── SpokenFeedback.vue # 口语纠错与深度句法剖析渲染组件
    │   │   └── TabsRenderer.vue # 选项卡渲染核心组件（深度集成雷达点击事件捕获）
    │   ├── stores/
    │   │   └── analyzer.js      # Pinia 状态管理：维护三核引擎数据状态隔离及联动跳转
    │   └── utils/
    │       └── markdown-renderer.js # 深度定制的 Markdown 解析器（处理雷达级联按钮注入）
```

---

## 多平台部署与运行指南 (适合新生)

为了能让新加入项目的同学在自己的电脑上快速运行起来，请根据你的操作系统（ **macOS** / **Windows** / **Linux** ）按照以下对应指南安装基础环境，然后执行通用配置。

---

### 1. 基础开发环境安装

根据你的操作系统，选择以下 **任意一种** 方式配置环境：

#### 方式 A：macOS 部署指南
macOS 默认自带 Python 3.9+，建议使用包管理器 `Homebrew` 一键完成其余依赖安装：
1. **安装 Homebrew** (如已安装可跳过):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. **一键安装 Node.js、Poetry 包管理器与 Git**:
   ```bash
   brew install node poetry git
   ```

#### 方式 B：Windows 部署指南 (极简/避坑版)
Windows 新手最容易在 Python 环境变量配置上踩坑（如输入 `python` 却跳转到微软应用商店）。建议使用以下标准步骤：
1. **安装 Python 3 & Node.js** (推荐使用 Windows 11 内置的命令行包管理器):
   * 打开 **PowerShell** (以管理员身份运行) 并分别执行以下命令：
     ```powershell
     # 安装 Python 3 (安装完后关闭并重新打开窗口以使环境变量生效)
     winget install Python.Python.3.11
     
     # 安装 Node.js
     winget install OpenJS.NodeJS
     
     # 安装 Git
     winget install Git.Git
     ```
   * *注：如果没有 winget，也可以直接前往 [Node.js 官网](https://nodejs.org/) 和 [Python 官网](https://www.python.org/) 下载 `.msi` / `.exe` 手动安装， **安装时务必勾选 "Add to PATH"** 。*
2. **验证安装成功**:
   * 重启命令行，输入 `python --version` 和 `node --version`，如果输出了版本号，说明环境变量配置正确。
3. **安装 Poetry** (后端包管理器):
   * 在 PowerShell 中输入以下命令安装：
     ```powershell
     pip install poetry
     ```
   * 验证安装：输入 `poetry --version`。

#### 方式 C：Linux (Ubuntu/Debian) 部署指南
1. **更新系统源并安装 Python 和 Git**:
   ```bash
   sudo apt update
   sudo apt install -y git curl python3 python3-pip python3-venv
   ```
2. **安装 Node.js** (使用 NodeSource 安装最新 LTS 版本):
   ```bash
   curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
   sudo apt install -y nodejs
   ```
3. **安装 Poetry**:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   # 确保 ~/.local/bin 在你的环境变量中
   export PATH="$HOME/.local/bin:$PATH"
   ```

---

### 2. 通用初始化步骤 (三端一致)

基础环境搞定后，打开终端（Windows 下可使用 PowerShell 或 Git Bash），依次执行：

#### 步骤 2.1：克隆项目代码到本地
```bash
git clone https://github.com/yuuniji/sentence-analyzer.git
cd sentence-analyzer
```

#### 步骤 2.2：配置 API 凭证与网络代理 (重要)
在项目根目录创建一个 `.env` 文件，并填入您的 Google Gemini API Key：
```bash
# 创建并写入配置文件
echo "GEMINI_API_KEY=AIzaSyYourApiKeyHere..." > .env
```
> [!IMPORTANT]
> **网络访问提示** ：由于 Gemini API 在中国大陆境内无法直接连接，你需要确保本地开发环境开启了科学上网代理（TUN 虚拟网卡模式或全局代理模式）。后端服务会自动读取系统环境变量中的代理配置（HTTP_PROXY/HTTPS_PROXY）。

#### 步骤 2.3：安装前后端项目依赖
在项目根目录 `sentence-analyzer` 下分别执行：
1. **安装后端 Python 依赖**:
   ```bash
   cd backend
   poetry install
   cd ..
   ```
2. **安装前端 Node 依赖**:
   ```bash
   cd frontend
   npm install
   cd ..
   ```

---

### 3. 启动运行

#### macOS / Linux 启动
直接在项目根目录运行一键启动脚本：
```bash
# 赋予执行权限
chmod +x start.sh
# 运行启动脚本
./start.sh
```

#### Windows 启动
由于 Windows 原生不支持 `.sh` 脚本，有以下两种非常简单的启动方法：
* **方法 A (极力推荐：双终端独立运行)** ：
  1. 打开 **终端 1** ，启动后端服务：
     ```powershell
     cd backend
     poetry run uvicorn main:app --reload --host 127.0.0.1 --port 8000
     ```
  2. 打开 **终端 2** ，启动前端服务：
     ```powershell
     cd frontend
     npm run dev
     ```
* **方法 B (使用 Git Bash)** ：
  如果您在安装 Git 时附带安装了 Git Bash，在项目根目录下鼠标右键选择 **"Git Bash Here"** ，可以直接运行：
  ```bash
  ./start.sh
  ```

运行成功后，直接在浏览器中访问 **`http://localhost:5173/`** 即可打开平台，开始分析长难句与录制口语评估！

---

## 技术进化史与踩坑指南 (备忘)

### 1. Gemini 3.1 JSON Schema 中 Pydantic Default 参数冲突
在 v3.0 的口语评估中，我们使用 `google-generativeai` SDK 传入 `response_schema` 约束大模型返回结构化的 JSON 数据。
* **报错** ：`ValueError: Unknown field for Schema: default`
* **踩坑原因** ：Gemini 官方 Python SDK 在生成 Schema 时，遇到 Pydantic 模型的 Field 包含默认值（如 `default=None` 或 `= None` 等）时会抛出异常。
* **解决** ：将 Pydantic 定义中的所有默认值移除，对可选字段使用 `Optional[T]` 声明但不赋任何默认值。

### 2. 多媒体直传与格式解耦
在处理口语录音时，原本打算在后端使用 `ffmpeg` 将用户的 WebM 音频流转码为标准 WAV，但这会极大增加后端对宿主机环境的依赖。
* **解决** ：Gemini 3.1 Pro 具备原生多模态理解能力。我们直接将前端录制的 `audio/webm` (或 Safari 生成的 `audio/mp4`) 字节流，伴随正确的 MIME 类型直传给大模型。大模型在云端即可完美解码并提取极高精度的转写文本（STT），实现了零依赖轻量化后端架构。

### 3. 雷达级联按钮 of DOM 注入与事件穿透
要在 Markdown-it 解析的 HTML 字符串中放入可点击 of `<button>` 并绑定 Vue 的 `pinia` 状态跳转，直接写 `@click` 是无效的（会被当做死文本）。
* **解决** ：在 `markdown-renderer.js` 中使用正则替换注入 `<button class="radar-btn">`，然后在挂载了 `v-html` 的父组件 `TabsRenderer.vue` 中利用 **事件委托 (Event Delegation)** 捕获 `e.target.closest('.radar-btn')` 的点击事件，从而跨越框架边界调用 `store.switchToSentence()`。

### 4. 多引擎下的状态隔离
在同一个输入面板中混合了长难句的输入框与篇章的巨型文本框，很容易互相污染数据。
* **解决** ：在 `analyzer.js` 状态库中将 `inputSentence`、`inputArticle` 和 `spokenResult` 彻底解耦，再使用 `computed` 的 `canAnalyze` 智能判定当前模式是否满足发送要求，保证多引擎切换如丝般顺滑。

### 5. 大模型的“雷达制导”失控
让大模型挑出长难句时，它偶尔会混入无关的评论或使用错误的引用格式，导致前端正则提取按钮失败。
* **解决** ：在 `system_prompt_article.j2` 中加入极度严格的标记指令：`必须严格遵守 > 【雷达提取】 句子 的特定块引用格式`。大模型对其的敏感度极高，做到了 100% 完美提取。

### 6. 强制思维链 (CoT) 无痕隐藏
要求大模型进行思考推导，可以极大提升解析倒装句和从句的正确率，但直接输出会毁掉极简的 UI。
* **解决** ：在提示词中命令模型将推理过程写入 HTML 注释 `<!-- 思维推导：... -->` 中。后端拿到了满分的智力成果，前端展示依旧干净利落！

### 7. 模型默认升级到 `gemini-3.1-pro-preview`
长难句精读与口语微观分析极度考验模型的句法推理和指令遵循。升级到 3.1 Pro 旗舰版后，不仅语法拆解更精准地道，且能完美遵循各种复杂的 Markdown 与 JSON Schema 约束，彻底告别格式崩溃现象。

### 8. 预览折叠扁平化优化
原先在渲染时使用 `<details>/<summary>` 双层折叠，用户输入句子后仍需点击数次才能阅读，交互繁琐。前端重构了渲染逻辑，在 Markdown 渲染阶段通过正则彻底剥离折叠标签，直接将胶囊选项卡与解析结果平铺呈现，直达内容，体验更为极致清爽。
