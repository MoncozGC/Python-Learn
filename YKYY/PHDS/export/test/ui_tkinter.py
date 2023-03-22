# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/6/6 11:00
# Desc  : 界面输入
from tkinter import *  # 引入tkinter包
from tkinter import messagebox  # 引入对话框包

app = Tk()  # 定义一个界面
app.title(string='Alan.hsiang>>>系统登录')  # 设置标题
app.geometry('400x300+300+400')  # 大小坐标设置格式 =widthxheight+x+y
name_label = Label(master=app, text='用户名')  # Label用于显示文本内容，且用户无法修改
pwd_label = Label(master=app, text='密码')  # master 用于表示对象属于哪个容器

name_entry = Entry(master=app)  # 文本框，用户可以进行输入
pwd_entry = Entry(master=app, show='*')  # 密码框，显示密文，以*代替


# 因为python是顺序执行，所以login函数定义必须在绑定事件前面
def login():
    name = name_entry.get()
    pwd = pwd_entry.get()
    if name == '' or pwd == '':
        messagebox.showerror(title='错误', message='用户名和密码都不能为空！！！')
    # else:
    #     if name == 'admin' and pwd == '123':
    #         messagebox.showinfo(title='成功', message='登录成功')
    #     else:
    #         messagebox.showerror(title='错误', message='用户名和密码错误！！！')
    print(name)
    print(pwd)


login_btn = Button(master=app, text='登录', width=8, command=login)  # 登录按钮

# name_label.pack(anchor=W) # pack 方式布局，默认为居中 ，一个元素一行 anchor用于设置对齐方式
# name_entry.pack(anchor=W)
# pwd_label.pack(anchor=W)
# pwd_entry.pack(anchor=W)
# login_btn.pack(anchor=W)

name_label.grid(row=0, column=0, padx=20, pady=20)  # grid 方式布局，通过设置行列的方式布局，从0开始
name_entry.grid(row=0, column=1)
pwd_label.grid(row=1, column=0)
pwd_entry.grid(row=1, column=1)
login_btn.grid(row=2, column=1, pady=20, stick=E)  # stick表示靠哪边对齐，通过N（北）S（南）W（西）E（东）来表示

login_btn.bind('<Button-1>', func=login)  # 绑定事件

app.mainloop()

if __name__ == '__main__':
    print("执行程序")
