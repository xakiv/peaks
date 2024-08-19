#!/usr/bin/env python

import socket
import time

import os


port = os.getenv("POSTGRES_PORT")
host = os.getenv("POSTGRES_HOST")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect((host, int(port)))
        s.close()
        break
    except socket.error as _err:
        print("WAITING FOR POSTGRES")
        time.sleep(0.1)
