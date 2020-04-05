import socket,serverlog,threading,pyperclip,os


class Bsin_server(object):
    def __init__(self):
        self.conncet_pool = []
        self.log = serverlog.Log()
        self.s = socket.socket()
        host = '192.168.1.12'
        port = 973
        self.s.bind((host, port))
        self.s.listen(5)

    def run(self):
        while True:
            self.log.info('等待新连接...')
            ServeSocket, addr = self.s.accept()
            self.conncet_pool.append(ServeSocket)
            t1 = threading.Thread(target=server.msg_handle,args=(ServeSocket,addr[0],))
            t1.setDaemon(True)
            t1.start()

    def msg_handle(self,client,ip):
        self.log.info('新连接' + ip)
        while True:
            recvmsg = client.recv(1024)
            strData = recvmsg.decode("utf-8")
            self.log.info('接收到%s来自%s'%(strData,ip))
            if len(recvmsg)==0:
                self.log.info('客户端离线')
                self.conncet_pool.remove(client)
                client.close()
                break
            elif strData[:3] == '-CM':
                self.log.info('执行了CMD' + strData[3:])
                os.system(strData[3:])
                break
            elif strData[:3] == '-KB':
                self.log.info('向剪切板写入了'+strData[3:])
                pyperclip.copy(strData[3:])
                break

server = Bsin_server()
server.run()
