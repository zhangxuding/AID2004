from socket import *
from select import select

#　创建好监听套接字
sockfd = socket()
sockfd.bind(("0.0.0.0",8999))
sockfd.listen(5)


# 设置关注列表
rlist = [sockfd] # 初始我们只关注监听套接字
wlist = []
xlist = []

# 循环监控我们放入列表中的IO
while True:
    # 对IO进行关注
    rs,ws,xs = select(rlist,wlist,xlist)
    # 对rs分情况讨论 --> sockfd一类：客户端连接  connfd一类：对应的客户端发消息
    for r in rs:
        if r is sockfd:
            connfd, addr = r.accept()
            print("Connect from ", addr)
            # 每连接一个客户端，就将这个客户端连接套接字加入关注
            rlist.append(connfd)
        else:
            data = r.recv(1024)
            if not data:
                # 客户端退出处理
                rlist.remove(r) # 不需要监控这个IO
                r.close()
                continue
            print(data.decode())

    for w in ws:
        w.send(b"Thanks")

    for x in xs:
        pass

