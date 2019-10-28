from socketserver import BaseRequestHandler,TCPServer
import json
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
def handleit(a):
    req=fetchstr(a)
    req=json.loads(req)
    if req['p'] in ['password']:
        f=open("tmp.jar","wb")
        f.write(bytes(req['content'],encoding="utf8"))
        f.close()
        os.system("cp tmp.jar out.jar;echo "+req['param'])
        f=open("out.jar","rb")
        dat=f.read()
        f.close()
        retu={'content':str(dat,encoding="utf8"),'status':200}
        sendstr(a,json.dumps(retu))


class main(BaseRequestHandler):
    def handle(self):
        print('got conn %s'%repr(self.client_address))
        ret=json.dumps(handleit(self.request))
        sendstr(self.request,ret)
srv=TCPServer(('',23333),main)
srv.serve_forever()

        

