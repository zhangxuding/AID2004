"""
ftp文件服务
多线程并发和套接字训练
"""

from socket import *
from threading import Thread
import sys,os
import time

# 全局变量
HOST = "0.0.0.0"
PORT = 8999
ADDR = (HOST, PORT)

FTP = "/home/tarena/FTP/" # 文件库位置


# 满足具体的客户端请求
class FTPServer(Thread):
    def __init__(self, connfd):
        self.connfd = connfd
        super().__init__()

    # 处理客户端请求文件列表
    def do_list(self):
        # 判断文件库是否为空
        file_list = os.listdir(FTP)
        if not file_list:
            self.connfd.send(b"FAIL") # 列表为空
            return
        else:
            self.connfd.send(b"OK")
            time.sleep(0.1)
            data = "\n".join(file_list) # 将文件拼接
            self.connfd.send(data.encode())
            time.sleep(0.1)
            self.connfd.send(b"##")

    def do_get(self,name):
        file_list = os.listdir(FTP)
        if name not in file_list:
            self.connfd.send(b"FAIL")
        else:
            fr = open(FTP+name,"rb")
            while True:
                data = fr.read(1024)
                if not data:
                    break
                self.connfd.send(data.decode())
            time.sleep(0.1)
            self.connfd.send(b"##")
            fr.close()



    # 线程函数  接收各种客户端请求，根据请求分配处理方法
    def run(self):
        while True:
            # 某一个客户端发来的各种请求
            data = self.connfd.recv(1024).decode()
            if data == "LIST":
                self.do_list()
            elif data[:3] == "GET":
                name = data.split(" ")[-1]
                self.do_get(name)


# 网络并发结构搭建
def main():
    # 创建tcp套接字
    sock = socket()
    sock.bind(ADDR)
    sock.listen(5)

    print("Listen the port %d" % PORT)

    # 循环接收客户端连接
    while True:
        try:
            connfd, addr = sock.accept()
            print("客户端地址:", addr)
        except KeyboardInterrupt:
            sock.close()
            sys.exit("服务端退出")

        # 有客户端连接进来，创建新的线程
        t = FTPServer(connfd)  # 使用自定义线程类
        t.start()

if __name__ == '__main__':
    main()
