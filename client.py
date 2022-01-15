#!/usr/bin/python3
print("欢迎使用 CTS by tjw123hh!")#Chat with Tjw's Server


import socket, threading, time, os, re
def get_time() -> str:
    return time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())

# 创建 socket 对象
s_send = socket.socket(socket.AF_INET6, socket.SOCK_STREAM) 
s_recv = socket.socket(socket.AF_INET6, socket.SOCK_STREAM) 

# 获取本地主机名
host = re.findall(r"(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})", os.popen("ipconfig /all").read(), re.I)[0][0]
s_send.bind((host, 5000))
s_recv.bind((host, 9999))

# 连接服务，指定主机和端口
try:
    server_host = "2409:8a28:4090:a040:3174:714c:31a1:9f0c"
    s_send.connect((server_host,10000))
    print(get_time(), "成功连接到服务器")
    print(get_time(), "你的IP为: " + host)
except BaseException as e:
    print(get_time(), "连接服务器时出现问题: " + str(e))
    input("按下 Enter 键以退出... ")
    os._exit(0)

def send(s_send: socket.socket) -> None:
    while True: 
        msg_from_begin, _, msg_from_text = s_send.recv(1024).decode('utf-8').partition(":")
        if msg_from_begin == "text":
            print(get_time(), msg_from_text)
        elif msg_from_begin == "input_to":
            to = input(get_time() + " 将消息发送给: ")
            s_send.send(("to:" + to).encode("utf-8"))
        elif msg_from_begin == "error":
            print(get_time(), "连接对方时出现错误, 对方可能不在线: " + msg_from_text)
            input("按下 Enter 键以退出... ")
            os._exit(0)
        elif msg_from_begin == "start":
            while True:
                try:
                    s_send.send(("text:" + input(get_time() + " 你: ")).encode("utf-8"))
                except ConnectionResetError:
                    print(get_time(), "发送失败, 服务器已关闭")
                    input("按下 Enter 键以退出... ")
                    os._exit(0)
def recv(s_recv: socket.socket) -> None:
    while True:
        s_recv.listen(1)
        connect, addr = s_recv.accept()
        while True:
            msg_from_begin, _, msg_from_text = connect.recv(1024).decode('utf-8').partition(":")
            if msg_from_begin == "text":
                print(get_time(), msg_from_text)

t_send = threading.Thread(target=send, args=(s_send,))
t_recv = threading.Thread(target=recv, args=(s_recv,))
t_send.start()
t_recv.start()
t_send.join()
t_recv.join()
        
print(get_time(), "已断开连接")
s_send.close()
input("按下 Enter 键以退出... ")
        