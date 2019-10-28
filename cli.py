import json,sys
import struct,os
def fetchstr(a):
    totl=0
    tots=b""
    while True:
        x=a.recv(4-totl)
        if not x:
            return ""
        tots+=x
        totl+=len(x)
        if totl==4:
            break
    sz=struct.unpack("<I",tots)[0]
    totl=0
    tots=b""
    print(sz)
    while True:
        x=a.recv(114514)
        if not x:
            return tots
        tots+=x
        totl+=len(x)
        if totl>=sz:
            return tots[:sz]
def sendstr(a,s):
    a.send(struct.pack("<I",len(s)))
    a.send(bytes(s,encoding="utf8"))
from socket import socket,AF_INET,SOCK_STREAM
def doit(dat,param):
    s=socket(AF_INET,SOCK_STREAM)
    s.connect(('0.0.0.0',23333))
    payload={'p':'password','content':dat,'param':param}
    sendstr(s,json.dumps(payload))
    ft=fetchstr(s)
    retu=json.loads(ft)
    if retu['status']!=200:
        print("error")
        return
    f=open("encrypt.jar","wb")
    f.write(bytes(retu['content'],encoding="utf8"))
    f.close()
x=open(sys.argv[1],'rb').read()
doit(str(x,encoding="utf8"),sys.argv[2])
