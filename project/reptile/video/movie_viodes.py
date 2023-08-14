# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023-08-13
# Desc  : 将视频文件根据十分钟进行分割 and .ts小文件进行合并为一个文件
import glob
import os

from moviepy.video.io.VideoFileClip import VideoFileClip
from natsort import natsorted


def split_long_videos(input_dir, output_dir, max_duration=600):
    """
    将大于等于10分钟的视频进行分割
    :param input_dir: 输入视频文件夹路径
    :param output_dir: 输出分割后的视频文件夹路径
    :param max_duration: 最大分割时长（默认为600秒，即10分钟）
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    video_files = [f for f in os.listdir(input_dir) if f.endswith('.mp4')]

    for video_file in video_files:
        video_path = os.path.join(input_dir, video_file)
        video_clip = VideoFileClip(video_path)
        video_duration = video_clip.duration

        if video_duration >= max_duration:
            num_segments = int(video_duration // max_duration) + 1

            for segment_index in range(num_segments):
                start_time = segment_index * max_duration
                end_time = min((segment_index + 1) * max_duration, video_duration)

                segment_clip = video_clip.subclip(start_time, end_time)
                segment_output_path = os.path.join(output_dir, f"{os.path.splitext(video_file)[0]}_{segment_index + 1}.mp4")
                segment_clip.write_videofile(segment_output_path, codec='libx264')

        video_clip.close()


import subprocess


def merge_ts_to_mp4(ts_files, output_file):
    """
    合并多个.ts文件为一个.mp4文件
    :param ts_files: 要合并的.ts文件列表
    :param output_file: 输出的.mp4文件路径
    """
    concat_list = "|".join(ts_files)
    cmd = ['ffmpeg', '-i', f'concat:{concat_list}', '-c', 'copy', output_file]
    subprocess.run(cmd)


if __name__ == '__main__':
    # 示例用法 将.ts文件合并成MP4文件
    ts_dir = 'data\\video\DLEAgqxM'
    ts_files = natsorted(glob.glob(os.path.join(ts_dir, '*.ts')))
    output_file = 'DLEAgqxM.mp4'
    merge_ts_to_mp4(ts_files, output_file)

    # 示例用法 根据视频时长十分钟拆分成一个视频, 使用v2sub的免费版本生成字幕
    # 之后可以再将生成的字幕视频合并成一个, 但是需要解决字幕的时间问题
    input_folder = "data/output_videos"
    output_folder = "data/output_videos2.ts"
    split_long_videos(input_folder, output_folder, max_duration=600)
