# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/6/6 11:26
# Desc  : 通过UI形式写入数据库信息
# 打包: pyinstaller.exe -F --distpath ./ -n phds_export_tools.exe ./phds_export_ui.py
# PySimpleGUI教程: https://zhuanlan.zhihu.com/p/397542578
import PySimpleGUI as sg

# 定义布局
from phds_export_data import connect_databases


def phds_export_gui():
    layout = [

        [sg.Text("请输入数据库的基本信息", font='Red 12')],

        [sg.Text(" ")],

        [sg.Text("数据库地址")],
        [sg.InputText(key='-ip-', size=(200, 200))],
        [sg.Text("数据库端口")],
        [sg.InputText('1433', key='-port-', size=(200, 200))],
        [sg.Text("数据库账户名")],
        [sg.InputText(key='-user-', size=(200, 200))],
        [sg.Text("数据库密码")],
        [sg.InputText(key='-pwd-', password_char='*', size=(200, 200))],
        [sg.Text("数据库名称")],
        [sg.InputText('hydee', key='-database-', size=(200, 200))],

        # [sg.Text("可选天数")],
        # [sg.InputText('180', key='-days-', size=(200, 200))],

        [sg.B("确定", key="ok"), sg.B("取消", key="Exit")],

    ]

    # 创建窗口
    window = sg.Window("PHDS导出工具", layout, size=(400, 450))

    # 事件循环
    while True:
        # 窗口的读取，有两个返回值（1、事件，2、值）
        event, values = window.read()

        if event in ("Exit", None):
            sg.Popup("是否退出程序")
            break

        if event == "ok":
            # values['-ip-'], values['-port-'], values['-user-'], values['-pwd-'], values['-database-'] = 'xxxx', '11118', 'root', 'root', 'hydee'
            # values['-ip-'], values['-port-'], values['-user-'], values['-pwd-'], values['-database-'] = '113.240.228.87', '2433', 'hydee', 'lk@2018!', 'hydee'
            # sg.Popup("您执行了确定任务")
            if values['-ip-'] != '' and values['-port-'] != '' and values['-user-'] != '' and values['-pwd-'] != '' and values['-database-'] != '':
                print("连接数据库, 准备导出数据 【期间请勿关闭窗口耐心等待】...")
                is_flag = True
                export_flag = connect_databases(values['-ip-'], values['-port-'], values['-user-'], values['-pwd-'], values['-database-'], is_flag)
                if export_flag:
                    sg.Popup("数据导出完毕, 请在本地查看文件")
                    break
                else:
                    sg.Popup("数据导出失败, 请检查数据库登录信息或查看相关报错信息")
            else:
                sg.Popup("请填写完所有信息")

    # 关闭窗口
    window.close()


if __name__ == '__main__':
    print("version: v1.9")
    phds_export_gui()
