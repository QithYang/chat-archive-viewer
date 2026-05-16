# QithYang

轻量、本地的 Claude 对话查看器 —— 把 Claude 导出的 `conversations.json` 渲染成清晰的聊天界面。所有数据在浏览器本地处理，不上传任何东西。

[在线体验 →](https://qithyang.github.io/QithYang/)

## 功能

- **对话列表** — 按最近更新排序，支持标题搜索、删除（本地软删除）
- **消息渲染** — Markdown（加粗/斜体/列表/代码块/引用/链接）、附件、图片占位
- **思考链** — 药丸折叠按钮 + 左侧竖线展开块
- **收藏** — hover 消息显示 ☆，点击收藏。「收藏」标签页按对话分组浏览
- **时间轴** — 月历视图，有对话的日期高亮
- **搜索** — 当前对话 / 全部对话两种范围，支持高亮、上下跳转
- **多次导入合并** — 侧边栏 `+` 按钮，按 uuid 去重

## 使用

### 在线（推荐）

打开 <https://qithyang.github.io/QithYang/>

- 没有数据时会展示一份示例对话
- 想看自己的数据：把从 Claude 导出的 `conversations.json` 拖进上传框

### 本地

```bash
git clone https://github.com/QithYang/QithYang.git
cd QithYang
python -m http.server 8765
```

浏览器访问 `http://localhost:8765/`。

## 文件结构

```
.
├── index.html               # 整个应用（HTML + CSS + JS 单文件）
├── assets/                  # 图标
├── fonts/                   # 字体
├── demo-conversations.json  # 演示数据
└── .gitignore
```
