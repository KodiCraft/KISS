
from time import perf_counter
from math import ceil

import socket

def ping(target: str):
    hostname = target.split(":")[0]
    try:
        port = int(target.split(":")[1])
    except:
        return -1
    starttime = perf_counter()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((hostname, port))
        s.close()
        return ceil((perf_counter() - starttime) * 1000)
    except:
        return -1