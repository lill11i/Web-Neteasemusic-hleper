"""
网易云音乐 —— 搜索并播放指定歌曲（网页版 music.163.com）
前提：已通过 browser_core.py 登录过网易云（登录态保存在 user_data 目录）

用法：
    python netease_play.py "Kanye Only One"
"""

import sys

from browser_core import get_browser
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout


def search_and_play(song_name: str):
    with sync_playwright() as p:
        context = get_browser(p, headless=False)
        page = context.pages[0] if context.pages else context.new_page()

        # 1. 打开网易云
        page.goto("https://music.163.com", wait_until="domcontentloaded")

        # 2. 定位搜索框并输入歌名
        # 网易云首页顶部有搜索输入框
        search_box = page.locator("input#srch, input[type='text']").first
        search_box.wait_for(state="visible", timeout=10_000)
        search_box.fill(song_name)
        search_box.press("Enter")

        # 3. 等待搜索结果页
        page.wait_for_timeout(3_000)

        # 4. 点击第一条「播放」按钮
        # 网易云搜索结果里，每首歌有播放图标。这里尝试多个可能的选择器
        play_selectors = [
            "a[data-res-action='play']",      # 搜索结果播放按钮
            ".ply",                            # 播放图标
            ".btn-play",                       # 播放按钮
        ]
        clicked = False
        for sel in play_selectors:
            try:
                btn = page.locator(sel).first
                if btn.is_visible():
                    btn.click()
                    clicked = True
                    print(f"[OK] 已点击播放按钮（选择器：{sel}）")
                    break
            except Exception:
                continue

        if not clicked:
            print("[提示] 未自动找到播放按钮，已停在搜索结果页，请手动点击播放。")
            print("        （网易云页面结构可能变化，这里保留窗口供你手动操作）")

        # 5. 保持窗口，让你确认
        print("窗口保持打开 30 秒，你可以确认播放效果……")
        page.wait_for_timeout(30_000)

        context.close()


if __name__ == "__main__":
    song = sys.argv[1] if len(sys.argv) > 1 else "Kanye Only One"
    search_and_play(song)
