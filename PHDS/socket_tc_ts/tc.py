import socket
import time
sk = socket.socket()                                                                #创建客户端的套接字
sk.connect(('127.0.0.1',8080))                                                      #尝试连接服务器

while 1:
    sendInfo = input(time.asctime(time.localtime(time.time())) + ' <<<')
    sk.send(sendInfo.encode('utf-8'))                                               #向服务器发送消息
    ret = sk.recv(1024).decode('utf-8')                                             #接收服务器发送的消息
    if ret.strip() == 'bye' or ret.strip() == 'bye'.capitalize():                   #跳出循环的条件
        sk.send(b'bye')                                                             #发送bytes类型的Bye
        print('Sever has disconnected!')
        break
    print(time.asctime(time.localtime(time.time())) + ' ["127.0.0.1", 8080]:' + ret)#格式化打印服务器发来的消息

sk.close()                                                                          #关闭客户端的套接字