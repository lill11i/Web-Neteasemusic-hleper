# PC 操作 Agent 使用说明

这是一个跑在**你本机**的浏览器自动化 Agent，能替你操作网页（以你本人身份、复用你的登录态）。

## 目录结构

```
pc-agent/
├── browser_core.py      # 核心：启动持久化 Chrome，保存/复用登录态
├── netease_play.py      # 动作示例：网易云搜歌并播放
├── user_data/           # （自动生成）登录态保存目录
└── README.md            # 本说明
```

## 环境准备（一次性）

```bash
# 1. 安装 playwright（用你系统里的 Python，例如 Anaconda）
pip install playwright
```

> 无需下载 Chromium —— 脚本会直接复用你本机已安装的 Chrome/Edge 内核。

## 第一步：先登录一次（保存登录态）

```bash
python browser_core.py
```

- 会弹出一个 Chrome 窗口，自动打开网易云。
- 在这个窗口里**扫码/账密登录**你的网易云账号。
- 脚本等待 60 秒后自动关闭，登录态已保存到 `user_data/`。
- 以后就不用再登录了。

## 第二步：让 Agent 帮你搜歌播放

```bash
python netease_play.py "Kanye Only One"
```

- 会用已登录的身份打开网易云，搜索并尝试点击播放。

## 怎么扩展新的「动作」

复制 `netease_play.py`，改成你想操作的网站，套路都是：

1. `get_browser(p, headless=False)` 拿到浏览器（带登录态）
2. `page.goto("目标网址")`
3. 用 `page.locator("选择器")` 定位元素并 `.click()` / `.fill()`

## 重要提醒

- **登录态 = 你的账号**。`user_data/` 目录包含 cookie，请勿分享给别人。
- 首次登录建议用**非无头模式**（能看到窗口），扫码更自然。
- 本 Agent 只能操作**网页版**；纯客户端（网易云 PC 客户端、微信朋友圈）无法覆盖。
- **运行前请先关闭你本机的 Chrome**：如果 Chrome 已在运行，Playwright 会复用你日常的浏览器，登录态可能不一致；建议关闭 Chrome 后再跑脚本，让脚本用独立的 `user_data` 配置启动。

## 定位元素的小技巧

如果不知道按钮的选择器，可以在浏览器里右键元素 →「检查」，拿到 CSS 选择器后填进脚本。
