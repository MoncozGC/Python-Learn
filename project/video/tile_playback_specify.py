import os
import random
import subprocess
import time
# 随机播放视频目录文件, 并且平铺到显示器, 再关闭某一个视频时再补充

# --- 配置参数 ---
VIDEO_DIR = r'F:\F-Data Files\Images\data'  # 视频目录
MPV_PATH = r'D:\Software\Other Software\mpv-x86_64-20260303-git-c55bdc3\mpv.exe'  # mpv.exe 路径
SCREEN_WIDTH = 3840  # 4K 显示器宽度
SCREEN_HEIGHT = 2160  # 4K 显示器高度
ROWS = 2
COLS = 3

WIN_WIDTH = SCREEN_WIDTH // COLS
WIN_HEIGHT = SCREEN_HEIGHT // ROWS


def get_all_videos():
    """获取目录下所有视频文件列表"""
    extensions = ('.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv')
    return [f for f in os.listdir(VIDEO_DIR) if f.lower().endswith(extensions)]


def start_mpv(video_file, x, y):
    """在指定位置启动一个 mpv 进程，设置为完整画面、单个循环且不置顶"""
    video_path = os.path.join(VIDEO_DIR, video_file)

    cmd = [
        MPV_PATH,
        video_path,
        f"--geometry={WIN_WIDTH}x{WIN_HEIGHT}+{x}+{y}",
        f"--autofit={WIN_WIDTH}x{WIN_HEIGHT}",
        "--no-border",  # 无边框平铺
        # "--ontop",           # 不再强制置顶
        "--loop-file=inf",  # 单个视频无限循环播放

        # --- 核心修改：恢复完整画面 ---
        # 删除 "--panscan=1.0"
        # 默认模式下，mpv 会自动在上下或左右添加黑边，以保证视频画面完整且不变形。

        # 界面优化
        "--osd-level=1",  # 允许显示进度条
        "--osd-bar=yes",  # 强制显示一个更直观的进度条（适应有黑边的环境）
        "--mute=no",  # 开启声音
        "--volume=40"  # 初始音量
    ]
    return subprocess.Popen(cmd)


def run_video_wall_with_replacement(must_play=None):
    if must_play is None: must_play = []

    all_videos = get_all_videos()
    if len(all_videos) < 6:
        print(f"警告：目录下只有 {len(all_videos)} 个视频，不足 6 个，将允许重复播放。")

    # 初始选择视频
    pool = [f for f in all_videos if f not in must_play]
    # 如果 pool 加上 must_play 还是不够 6 个，就从 all_videos 里随便凑
    if len(must_play) + len(pool) < 6:
        initial_selected = (must_play + pool + random.choices(all_videos, k=6))[:6]
    else:
        initial_selected = must_play + random.sample(pool, 6 - len(must_play))

    random.shuffle(initial_selected)

    # 初始化 6 个槽位
    slots = []
    for i in range(6):
        row, col = i // COLS, i % COLS
        x, y = col * WIN_WIDTH, row * WIN_HEIGHT

        proc = start_mpv(initial_selected[i], x, y)
        slots.append({
            "process": proc,
            "x": x,
            "y": y,
            "current_file": initial_selected[i]
        })
        print(f"槽位 {i + 1} 启动: {initial_selected[i]}")
        time.sleep(0.3)

    print("\n[监控运行中] ------------------------------------")
    print("1. 视频现在会【完整显示】，可能会有上下黑边。")
    print("2. 视频【单个循环播放】，【不置顶】。")
    print("3. 如果你【关闭】某个窗口，脚本会自动随机补位一个新视频。")
    print("--------------------------------------------------")

    try:
        while True:
            for i in range(6):
                # 检查进程是否被用户手动关闭
                if slots[i]["process"].poll() is not None:
                    old_file = slots[i]["current_file"]

                    # 重新扫描目录并剔除当前正在播放的文件，避免重复
                    current_videos = get_all_videos()
                    playing_now = [s["current_file"] for s in slots]
                    available = [f for f in current_videos if f not in playing_now]

                    if not available:
                        available = current_videos  # 实在没得选了就全选

                    new_file = random.choice(available)
                    print(f"检测到槽位 {i + 1} 已手动关闭。正在补位: {new_file}")

                    # 在原坐标重新启动
                    new_proc = start_mpv(new_file, slots[i]["x"], slots[i]["y"])
                    slots[i]["process"] = new_proc
                    slots[i]["current_file"] = new_file

            time.sleep(1)  # 每秒检查一次进程状态

    except KeyboardInterrupt:
        print("\n正在退出，清理所有播放窗口...")
        for s in slots:
            s["process"].terminate()


if __name__ == "__main__":
    # 指定必播视频（如果没有则留空）
    must_list = ["1102787.mp4", 'seg_867151760.mp4', '']
    run_video_wall_with_replacement(must_list)