import queue
import threading
import requests
from urllib.parse import quote, unquote
from lxml import etree
import time

lock = threading.Lock()
q = queue.Queue()
booklist = {}

def scz():
    global q,booklist
    requests.packages.urllib3.disable_warnings()
    r = requests.get('https://www.dingdiann.com/ddk75171/', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'}, verify=False)
    html = etree.HTML(r.text)
    everlode = html.xpath('//*[@id="list"]/dl/dd/a/@href')[12:]
    lodelen = len(everlode)
    print(lodelen)
    for i in range(lodelen):
        # print('https://www.dingdiann.com'+ zj)
        q.put({'id':i,'url':'https://www.dingdiann.com' + everlode[i]})
        

    for __ in range(30):
        t = threading.Thread(target=xfz, args=(q, ))
        t.start()
    t.join()


def xfz(q_out):
    global q,booklist
    flage = True
    while flage:
        # lock.acquire()
        # lock.release()
        if q_out.empty():
            flage = False
                #         f.write(xiangxinr)
        else:
            data =  q_out.get()
            bookid = data['id']
            url = data['url']
            requests.packages.urllib3.disable_warnings()
    
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'}, verify=False)
            html = etree.HTML(r.text)
            zjming = html.xpath('//*[@class="bookname"]/h1/text()')[0]
            neirong = html.xpath('//*[@id="content"]/text()')
            xiangxinr = zjming + str(neirong).replace(r"\r\n\t\t\t\t", "\n").replace(r"\u3000\u3000", "\n").replace(r"', '", "\n").replace(r"']", "").replace(r"['", "")
            print(bookid,zjming)
            booklist[bookid]=xiangxinr

star = time.time()

scz()
b = sorted(booklist)
for ass in b:
    with open('123.txt', 'a', encoding='utf-8') as f:
        f.write(booklist[ass])

end = time.time()

print(end-star)