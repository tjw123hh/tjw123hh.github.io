#!/usr/bin/python3
import socket, time, re, threading, os, requests
def get_time():
    return time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())

def listen(clientsocket: socket.socket, addr) -> None:
    global to, socketto
    print(get_time(), "已连接到: {}::{}".format(*addr[:2]))
    clientsocket.send("input_to:".encode("utf-8"))#开始
    while True:
        try:
            msg_from_begin, _, msg_from_text = clientsocket.recv(1024).decode('utf-8').partition(":")
        except ConnectionResetError:
            clientsocket.close()
            print(get_time(), "已断开与 {}::{} 的连接".format(*addr[:2]))
            return
        if msg_from_begin == "to":
            to = msg_from_text
            socketto = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            try:
                socketto.connect((to, 9999))
                clientsocket.send("start:".encode("utf-8"))
            except BaseException as e:
                clientsocket.send(("error:" + str(e)).encode("utf-8"))
        elif msg_from_begin == "exit":
            print(get_time(), "对方已关闭连接")
            break
        elif msg_from_begin == "text":
            try:
                socketto.send(("text:{}::{}: " + msg_from_text).format(*addr[:2]).encode("utf-8"))
            except BaseException as e:
                clientsocket.send(("error:" + str(e)).encode("utf-8"))

    clientsocket.close()
    print(get_time(), "已断开与 {}::{} 的连接".format(*addr[:2]))

if __name__ == "__main__":
    serversocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM) 
    host = re.findall(r"(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})", os.popen("ipconfig /all").read(), re.I)[0][0]
    serversocket.bind((host, 10000))
    print(get_time(), "服务器已开启于 %s" % host + "::10000")
    print(get_time(), "开始自动检测 (tjw123hh.github.io/ip) IP地址是否正确")
    _host = requests.get('https://tjw123hh.github.io/ip.txt').text
    if _host == host:
        print(get_time(), "检测完毕, 未发现错误")
    else:
        with open(r"E:\Users\Administrator\Desktop\tjw123hh.github.io\ip.txt", "w") as file:
            file.write(host)
        os.popen(r'E:&cd E:\Users\Administrator\Desktop\tjw123hh.github.io&git add .&git commit -m "auto"&git push')
        print(get_time(), "检测到并已尝试解决问题")
    serversocket.listen(5)
    while True:
        t_name = "t" + str(time.time())
        globals()[t_name] = threading.Thread(target=listen, args=serversocket.accept())
        globals()[t_name].start()
        globals()[t_name].join()
        