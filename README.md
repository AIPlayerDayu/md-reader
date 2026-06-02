# MD 阅读器

一个简单的本地 Markdown 阅读器，**完全离线**、无需联网、无需安装运行环境。

提供两种使用方式：

1. **macOS 原生程序（`MD阅读器.app`）** —— 双击任意 `.md` 文件即可用它打开渲染好的页面。
2. **单文件网页版（`MD 阅读器.html`）** —— 双击在浏览器里打开，可拖拽文件 / 打开整个文件夹（带目录树）。

渲染基于内嵌的 [marked](https://github.com/markedjs/marked) + [highlight.js](https://github.com/highlightjs/highlight.js)，支持 GFM 表格、任务列表、代码高亮，以及 🌓 浅色 / 深色主题切换。

---

## 方式一：macOS App（双击 .md 直接打开）

### 直接使用
仓库内已包含构建好的 `MD阅读器.app`：

1. 把 `MD阅读器.app` 拖到「应用程序」文件夹（或任意位置）。
2. 首次打开若提示「无法验证开发者」：右键 App → **打开** → 确认一次即可（自签名应用的正常一次性提示）。
3. 右键任意 `.md` 文件 → **显示简介** → 「打开方式」选 `MD阅读器` → **全部更改**，即可把它设为默认程序。

### 设为默认打开程序（命令行，可选）
```bash
brew install duti
for ext in md markdown mdown mkd; do duti -s com.local.mdreader .$ext all; done
```

### 自行构建
```bash
./build.sh
```
脚本会用 `osacompile` 编译 `src/main.applescript`，注入资源、写入 `Info.plist` 文档类型、签名并注册到 Launch Services。

**工作原理**：双击 `.md` → Finder 调用 App → App 用内嵌的 `render.py` 把 Markdown 渲染成自包含 HTML → 默认浏览器打开。

---

## 方式二：网页版（任意平台）

双击 `MD 阅读器.html` 在浏览器中打开，然后：

- 点「打开文件」选单个 `.md`
- 点「打开文件夹」→ 左侧显示目录树，点击切换
- 直接把 `.md` 文件拖进窗口

单个 HTML 文件，库已全部内嵌，可离线使用，也可放到任意机器（Windows / Linux）上用。

---

## 目录结构

```
.
├── MD阅读器.app/        # 构建好的 macOS 程序
├── MD 阅读器.html        # 单文件网页版
├── build.sh             # 构建 .app 的脚本
├── src/
│   ├── main.applescript # App 的 on open / on run 逻辑
│   ├── render.py        # Markdown → 自包含 HTML 渲染器
│   └── lib/             # marked / highlight.js / 样式
└── 示例.md              # 测试文档
```

## 依赖

- macOS（App 方式）；网页版任意平台
- `python3`（App 渲染用，macOS 自带或通过 Homebrew 安装）
- 构建工具 `osacompile`、`PlistBuddy` 均为 macOS 自带

## 隐私与安全

- 完全在本地运行，**不联网、不上传任何数据**，不收集任何信息。
- 渲染用的 marked / highlight.js 已内嵌，运行时不请求任何远程资源。
- App 的 `Info.plist` 不申请相机、通讯录、照片等任何系统权限。

## License

[MIT](LICENSE)
