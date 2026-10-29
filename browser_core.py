"""
浏览器自动化核心 —— 基于 Playwright 持久化上下文
作用：启动/接管一个本机 Chrome，登录态保存在 user_data 目录，可复用。
"""

import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

# 登录态保存目录（会保存 cookie、localStorage 等）
BASE_DIR = Path(__file__).resolve().parent
USER_DATA_DIR = BASE_DIR / "user_data"

# 系统 Chrome 路径（Windows 常见位置）
CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def _find_chrome() -> str:
    """找到本机已安装的 Chrome/Edge 可执行文件路径"""
    for p in CHROME_PATHS:
        if Path(p).exists():
            return p
    raise FileNotFoundError("未找到 Chrome/Edge，请手动指定浏览器路径")


def get_browser(playwright, headless: bool = False):
    """
    启动一个持久化浏览器（复用系统 Chrome/Edge 内核）。
    复用 user_data 目录，登录一次后，后续无需重复登录。
    """
    USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
    chrome_path = _find_chrome()

    context = playwright.chromium.launch_persistent_context(
        user_data_dir=str(USER_DATA_DIR),
        executable_path=chrome_path,   # 用系统已装浏览器，无需下载内核
        headless=headless,             # 有头模式：你能看到窗口，方便首次扫码登录
        viewport={"width": 1280, "height": 800},
        args=["--start-maximized"],
    )
    return context


def main():
    with sync_playwright() as p:
        context = get_browser(p, headless=False)
        page = context.pages[0] if context.pages else context.new_page()

        print("=" * 50)
        print("浏览器已启动（非无头模式，你能看到窗口）")
        print("请在窗口里完成登录（例如网易云扫码登录）")
        print("登录后，本脚本会等待 60 秒供你操作，然后关闭并保存登录态")
        print("=" * 50)

        page.goto("https://music.163.com")
        page.wait_for_timeout(60_000)  # 给你 60 秒完成登录

        context.close()


if __name__ == "__main__":
    main()
