from socket import *

# 服务器地址
ADDR = ("127.0.0.1",8888)

# 将具体发送请求的方法封装在类中
class FTPClient:
    def __init__(self,sock):
        self.sock = sock

    # 请求文件列表
    def do_list(self):
        self.sock.send(b"LIST") # 发送请求
        result = self.sock.recv(128).decode() # 等待回复
        if result == 'OK':
            # 接收文件列表
            while True:
                file = self.sock.recv(1024).decode()
                if file == "##":
                    break
                print(file)
        else:
            # 结束
            print("文件库为空")

    def do_get(self,filename):
        msg = "GET " + filename
        self.sock.send(msg.encode)
        result = self.sock.recv(128).decode()
        if result == "FAIL":
            print("文件不存在")
        else:
            fw = open(filename, "wb")
            while True:
                content = self.sock.recv(1024).decode()
                if content == "##":
                    break
                fw.write(content)
            print("下载完成")
            fw.close()


# 网络连接
def main():
    sock = socket()
    sock.connect(ADDR)

    ftp = FTPClient(sock) # 实例化对象

    while True:
        print("=========== 命令选项 =============")
        print("***          list           ***")
        print("***        get file         ***")
        print("***        put file         ***")
        print("***          quit           ***")
        print("=================================")

        cmd = input("请输入命令:")
        if cmd == "list":
            ftp.do_list()
        elif cmd[:3] == "get":
            filename = cmd.split(' ')[-1]
            ftp.do_get(filename)


if __name__ == '__main__':
    main()
