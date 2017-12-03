#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_STREAM

from symmetric.aes import *

def padding_oracle(cipher, host):
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((host["hostname"], host["port"]))
        s.sendall(cipher)
        data = s.recv(1024)
        print(data)
        print(host["error"] in data)
    print("-------------")
    print(cipher)
    print(host)
    return "TODO"
