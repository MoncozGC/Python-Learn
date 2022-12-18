import socket
import time
from json import dumps
from socket import SOL_SOCKET, SO_REUSEADDR

sk = socket.socket()  # 创建服务器的套接字
sk.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sk.bind(('127.0.0.1', 8080))  # 把地址绑定到套接字
sk.listen()  # 监听链接
conn, addr = sk.accept()  # 接收到客户端的连接和地址

while 1:
    ret = conn.recv(1024).decode('utf-8')  # 接收客户端信息
    if ret.strip() == 'bye' or ret.strip() == 'bye'.capitalize():  # 跳出循环的条件
        conn.send(b'bye')  # 发送bytes类型的Bye
        print('Client has disconnected!')
        break
    print(time.asctime(time.localtime(time.time())) + ' ' + dumps(addr) + ':' + ret)  # 格式化打印客户端发来的消息
    sendInfo = input(time.asctime(time.localtime(time.time())) + ' <<<')
    conn.send(sendInfo.encode('utf-8'))  # 向客户端发送信息

conn.close()  # 关闭客户端的连接
sk.close()  # 关闭服务器套接字
