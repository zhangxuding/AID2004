"""
单一tcp客户端循环发送内容
重点代码
"""

from socket import *

# 创建tcp套接字
tcp_socket = socket()

tcp_socket.connect(("127.0.0.1",8888))

while True:
    msg = input(">>")
    if not msg:
        break
    tcp_socket.send(msg.encode())

tcp_socket.close()
