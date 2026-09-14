# QithYang

A lightweight, local-only viewer for Claude conversation exports. It renders the `conversations.json` file exported from Claude as a clean chat interface. Everything is processed in your browser; nothing is uploaded anywhere.

[Live demo →](https://qithyang.github.io/QithYang/) · [中文说明](#中文说明)

![QithYang showing the bundled sample conversation](assets/screenshot.jpg)

*The interface is in Chinese. The screenshot shows the bundled sample conversation, not real data.*

## Features

- **Conversation list**: sorted by last update, with title search and delete (local soft delete)
- **Message rendering**: Markdown (bold, italic, lists, code blocks, quotes, links), attachments, image placeholders
- **Thinking chains**: a collapsible pill button that expands into a block marked by a left rule
- **Bookmarks**: hover a message to reveal ☆ and bookmark it; the Bookmarks tab groups them by conversation
- **Timeline**: month calendar view with conversation days highlighted
- **Search**: current conversation or all conversations, with highlighting and next/previous jumps
- **Merge multiple imports**: the sidebar `+` button imports another export, de-duplicated by conversation uuid
- **Export**: back up your data as JSON, or export a self-contained HTML file that opens on its own

## Usage

### Online (recommended)

Open <https://qithyang.github.io/QithYang/>

- With no data loaded, a sample conversation is shown
- To view your own data, drag the `conversations.json` exported from Claude onto the upload box

### Local

```bash
git clone https://github.com/QithYang/QithYang.git
cd QithYang
python -m http.server 8765
```

Then open `http://localhost:8765/` in your browser.

## Data and privacy

Imported conversations are stored in your browser (IndexedDB). The page makes no network requests with your data; it only loads its own local files.

## Tech

A single-file front end (HTML + CSS + JavaScript) with no framework and no build step.

## Project structure

```
.
├── index.html               # the whole app (HTML + CSS + JS in one file)
├── assets/                  # icons and screenshot
├── fonts/                   # fonts
├── demo-conversations.json  # sample data
├── LICENSE
└── .gitignore
```

## How it was built

Built with AI coding tools. I specified the features and the privacy model (fully client-side; no data leaves the browser) and verified the behaviour through browser testing.

## License

[MIT](LICENSE)

---

## 中文说明

轻量、本地的 Claude 对话查看器 —— 把 Claude 导出的 `conversations.json` 渲染成清晰的聊天界面。所有数据在浏览器本地处理，不上传任何东西。

[在线体验 →](https://qithyang.github.io/QithYang/)

![QithYang 示例对话界面](assets/screenshot.jpg)

### 功能

- **对话列表** — 按最近更新排序，支持标题搜索、删除（本地软删除）
- **消息渲染** — Markdown（加粗/斜体/列表/代码块/引用/链接）、附件、图片占位
- **思考链** — 药丸折叠按钮 + 左侧竖线展开块
- **收藏** — hover 消息显示 ☆，点击收藏。「收藏」标签页按对话分组浏览
- **时间轴** — 月历视图，有对话的日期高亮
- **搜索** — 当前对话 / 全部对话两种范围，支持高亮、上下跳转
- **多次导入合并** — 侧边栏 `+` 按钮，按 uuid 去重
- **导出** — 导出 JSON 备份，或导出可单独打开的独立 HTML 文件

### 使用

#### 在线（推荐）

打开 <https://qithyang.github.io/QithYang/>

- 没有数据时会展示一份示例对话
- 想看自己的数据：把从 Claude 导出的 `conversations.json` 拖进上传框

#### 本地

```bash
git clone https://github.com/QithYang/QithYang.git
cd QithYang
python -m http.server 8765
```

浏览器访问 `http://localhost:8765/`。

### 数据与隐私

导入的对话保存在浏览器本地（IndexedDB）。页面不会把你的数据发往任何服务器，只加载自身的本地文件。

### 文件结构

```
.
├── index.html               # 整个应用（HTML + CSS + JS 单文件）
├── assets/                  # 图标与截图
├── fonts/                   # 字体
├── demo-conversations.json  # 演示数据
├── LICENSE
└── .gitignore
```

### 开发方式

借助 AI 编程工具完成：功能与隐私模型（完全在浏览器本地运行，数据不外传）由我定义，行为经我在浏览器中测试验证。

### 许可证

[MIT](LICENSE)
