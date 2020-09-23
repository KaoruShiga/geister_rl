#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connect(self.host, self.port)

    def connect(self, host, port):
        for _ in range(10):  # 最大3回実行
            try:
                # do_something()  # 失敗しそうな処理
                self.client = socket.socket()
                self.client.connect((host, port))
            except Exception as _:
                pass  # 必要であれば失敗時の処理
            else:
                break  # 失敗しなかった時はループを抜ける
        else:
            pass  # リトライが全部失敗した時の処理
        
    def reconnect(self):
        self.connect(self.host, self.port)

    def send(self, message):
        self.client.send(message)

    def recv(self):
        return self.client.recv(4096)

    def move(self, unit, direct):
        self.client.send(("MOV:" + unit + "," + direct + "\r\n").encode())

    def close(self):
        self.client.close()
