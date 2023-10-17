# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023-10-17
# Desc  : 调用CMD, 输出目录结构
import subprocess


def run_tree_command(directory):
    try:
        # 运行 'tree' 命令并捕获输出
        result = subprocess.run(['cmd.exe', '/c', 'tree', '/F'], capture_output=True, text=True, check=True, cwd=directory)

        # 打印命令的标准输出
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        # 如果命令执行失败，打印错误信息
        print(f"An error occurred: {e}")


# 指定目录运行
filename = "c://Temp"
# 调用函数
run_tree_command(filename)
