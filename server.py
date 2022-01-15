#!/usr/bin/python3
import socket, time
import threading
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
    host = "2409:8a28:4090:a040:3174:714c:31a1:9f0c"
    serversocket.bind((host, 10000))
    print(get_time(), "服务器已开启于 %s" % host + "::10000")
    serversocket.listen(5)
    while True:
        t_name = "t" + str(time.time())
        globals()[t_name] = threading.Thread(target=listen, args=serversocket.accept())
        globals()[t_name].start()
        globals()[t_name].join()
        