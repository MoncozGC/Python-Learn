import os
import random
import subprocess
import time

# 随机播放视频目录文件, 并且平铺到显示器, 再关闭某一个视频时再补充


# --- 基础配置 ---
VIDEO_DIR = r'F:\F-Data Files\Images\data'  # 视频目录
MPV_PATH = r'D:\Software\Other Software\mpv-x86_64-20260303-git-c55bdc3\mpv.exe'  # mpv.exe 路径
SCREEN_WIDTH = 3840  # 4K 显示器宽度
SCREEN_HEIGHT = 2100  # 4K 显示器高度
ROWS = 2
COLS = 3
TOTAL = (ROWS * COLS) + 1

WIN_WIDTH = SCREEN_WIDTH // COLS
WIN_HEIGHT = SCREEN_HEIGHT // ROWS

# --- 核心设置：指定必播视频及其位置 ---
# 键 (Key) 是位置编号：1, 2, 3 (第一行) | 4, 5, 6 (第二行)
# 值 (Value) 是视频文件名
# 如果不想指定，留空即可，例如：SPECIFIED_VIDEOS = {}
SPECIFIED_VIDEOS = {
    2: "1102787.mp4",  # 在左上角第一个位置播放
    5: "1003837.mp4"  # 在第二行中间位置播放
}


def get_all_videos():
    extensions = ('.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv')
    return [f for f in os.listdir(VIDEO_DIR) if f.lower().endswith(extensions)]


def start_mpv(video_file, x, y):
    video_path = os.path.join(VIDEO_DIR, video_file)
    cmd = [
        MPV_PATH,
        video_path,
        f"--geometry={WIN_WIDTH}x{WIN_HEIGHT}+{x}+{y}",
        f"--autofit={WIN_WIDTH}x{WIN_HEIGHT}",
        "--no-border",  # 无边框平铺
        "--loop-file=inf",  # 单个视频无限循环播放
        "--osd-level=1",  # 允许显示进度条
        "--osd-bar=yes",  # 强制显示一个更直观的进度条（适应有黑边的环境）
        "--mute=no",  # 开启声音
        "--volume=60"  # 初始音量
    ]
    return subprocess.Popen(cmd)


def run_video_wall():
    all_videos = get_all_videos()
    if len(all_videos) < TOTAL:
        print("警告：视频文件不足 6 个。")

    # 1. 确定初始 6 个位置播放什么
    # slots_data 存储每个位置的信息
    slots = {}

    # 记录哪些视频已经被占用了，防止随机填充时重复
    used_files = set(SPECIFIED_VIDEOS.values())

    # 准备随机池（排除掉已经指定的）
    random_pool = [f for f in all_videos if f not in used_files]
    random.shuffle(random_pool)

    for i in range(1, TOTAL):  # 位置 1 到 6
        index_zero = i - 1
        row, col = index_zero // COLS, index_zero % COLS
        x, y = col * WIN_WIDTH, row * WIN_HEIGHT

        # 判断当前位置是否有指定视频
        if i in SPECIFIED_VIDEOS:
            target_file = SPECIFIED_VIDEOS[i]
        else:
            # 如果没有指定，从随机池取一个
            if random_pool:
                target_file = random_pool.pop(0)
            else:
                target_file = random.choice(all_videos)  # 实在没了就随便选

        print(f"位置 {i} 启动: {target_file}")
        proc = start_mpv(target_file, x, y)

        slots[i] = {
            "process": proc,
            "x": x,
            "y": y,
            "current_file": target_file,
            "is_specified": i in SPECIFIED_VIDEOS  # 记录这是否是一个“固定位”
        }
        time.sleep(0.3)

    print("\n[监控运行中] ------------------------------------")
    print(f"当前排版：")
    for k, v in SPECIFIED_VIDEOS.items():
        print(f"  位置 {k} 已锁定为: {v}")
    print("操作：关闭任意窗口将随机补位（固定位关闭后也会随机补位）。")
    print("--------------------------------------------------")

    try:
        while True:
            for i in range(1, TOTAL):
                if slots[i]["process"].poll() is not None:
                    # 重新获取当前所有视频，排除正在播放的
                    current_videos = get_all_videos()
                    playing_now = [slots[s]["current_file"] for s in slots]
                    available = [f for f in current_videos if f not in playing_now]

                    if not available: available = current_videos

                    new_file = random.choice(available)
                    print(f"检测到位置 {i} 已关闭。补位新视频: {new_file}")

                    new_proc = start_mpv(new_file, slots[i]["x"], slots[i]["y"])
                    slots[i]["process"] = new_proc
                    slots[i]["current_file"] = new_file

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n停止监控...")
        for i in range(1, TOTAL):
            slots[i]["process"].terminate()


if __name__ == "__main__":
    run_video_wall()
