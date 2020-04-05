from django.http import HttpResponse
from django.shortcuts import render
import queue
import threading
import json
from django.http.response import JsonResponse
from time import sleep
from urllib.parse import quote,unquote
import requests
from lxml import etree
import re

num_progress = 0
jd = 0
zs = 0
lock = threading.Lock()
q_data = queue.Queue()
booklist = {}
book_data = []
book_name = ''

def xzdata(request):
    name = request.GET.get('name')
    url = request.GET.get('url')
    print(name)
    print(url)
    # scz(name,url)
    return JsonResponse({}, safe=False)

def xzbook(request):
    return render(request,'xzbook.html')

def jdfanhui(request):
    global jd
    data = {'jd':jd}
    return JsonResponse(data, safe=False)

def jdye(request):
    return render(request, 'chuli.html')

def ceshi(request):
    global q_data,book_data,book_name
    book_data = []
    book_name = ''
    bookname = request.GET.get('name')
    book_name = bookname
    urlspider()
    q_data.join()
    data = book_data
    # print(data)
    return JsonResponse(data, safe=False)

def urlspider():
    global q_data,book_name
    scz1(book_name,q_data)
    scz2(book_name,q_data)
    for __ in range(5):
        t = threading.Thread(target=xfz1, args=(q_data, ))
        t2 = threading.Thread(target=xfz2, args=(book_name, q_data))
        t.start()
        t2.start()



# 爬虫url

def scz1(name,q_put):
    # lock.acquire()
    # lock.release()
    url = yuyougeurl(name)
    r = requests.get(url,headers=header(),params={'keyword':name})
    r.encoding = 'gbk'
    html = etree.HTML(r.text)
    try:
        how = int(re.findall(r'\d+',html.xpath('//*[@class="panel-title"]/text()')[0])[0])
    except:
        pass
    else:
        if how<=30:
            last_page = 1
        elif how>30:
            last_page = how//30+1
        for i in range(1,last_page+1):
            q_put.put(yuyougeurl(name,i))
            # print(yuyougeurl(name,i))
            

def xfz1(q_get):
    # lock.acquire()
    # lock.release()
    flage = True
    global book_data
    while flage:
        if q_get.empty():
            flage = False
        else:

            url_1 = q_get.get()
            print(url_1)

            if url_1[:19]=='https://www.yuyouge':
                r = requests.get(url_1,headers=header())
                r.encoding='gbk'
                html = etree.HTML(r.text)
                bookname = html.xpath('//*[@class="panel-body"]/ul/li/div[2]/a/text()')
                new = html.xpath('//*[@class="panel-body"]/ul/li/div[3]/a/text()')
                zz = html.xpath('//*[@class="panel-body"]/ul/li/div[4]/text()')
                url = html.xpath('//*[@class="panel-body"]/ul/li/div[2]/a/@href')
                for i in range(len(bookname)):
                    try:
                        t_name = bookname[i]
                    except:
                        t_name = '未知'
                    try:
                        t_new = new[i]
                    except:
                        t_new = '未知'
                    try:
                        t_zz = zz[i]
                    except:
                        t_zz = '未知'
                    try:
                        t_url = str(url[i]).replace('/xs/','https://www.yuyouge.com/book/').replace('index.html','')
                    except:
                        t_url = '未知'
                    else:
                        print(t_name)
                        book_data.append({'name':t_name,'url':t_url,'zz':t_zz,'new':t_new})
            else:

                q_get.put(url_1)

            q_get.task_done()
            

def yuyougeurl(name,page=1):
    url = 'https://www.yuyouge.com/search.htm?keyword={}&pn={}'.format(name,page)
    return url


# 爬虫url2
def scz2(name,q_put):
    r = requests.get('http://www.bjkgjlu.com/top/?search='+name,headers=header())
    r.encoding = 'utf-8'
    html = etree.HTML(r.text)
    last_page = html.xpath('//*[@class="page"]/ul/li/text()')[0]
    for i in range(1,int(re.findall(r'\d+',last_page)[0])+1):
        # print(ayxsurl(name,i))
        q_put.put(ayxsurl(page=i))

def xfz2(name,q_get):
    # lock.acquire()
    # lock.release()
    flage = True
    global book_data
    while flage:
        print(name)
        if q_get.empty():
            flage = False
        else:
            lock.acquire()
            url_1 = q_get.get()
            lock.release()
            if url_1[:18]=='http://www.bjkgjlu':
                # print(url)
                r = requests.get(url_1,headers=header(),params={'search': name})
                r.encoding='utf-8'
                html = etree.HTML(r.text)
                # print(r.text)
                bookname = html.xpath('//*[@class]/tr/td[3]/a/text()')
                # print(bookname)
                zz = html.xpath('//*[@class]/tr/td[5]/text()')
                url = html.xpath('//*[@class]/tr/td[3]/a/@href')

                for i in range(len(bookname)):
                    try:
                        t_name = bookname[i]
                    except:
                        t_name = '未知'
                    try:
                        r2 = requests.get('http://www.bjkgjlu.com'+url[i],headers=header())
                        r2.encoding = 'utf-8'
                        html2 = etree.HTML(r2.text)
                        t_new = html2.xpath('//*[@class="chapter"]/p/a/text()')[-1]
                    except:
                        t_new = '未知'
                    try:
                        t_zz = zz[i]
                    except:
                        t_zz = '未知'
                    try:
                        t_url = 'http://www.bjkgjlu.com' + url[i] + 'catalog/'
                    except:
                        t_url = '未知'
                    book_data.append({'name':t_name,'url':t_url,'zz':t_zz,'new':t_new})
                    # print(t_name)
            else:
                q_get.put(url_1)
            q_get.task_done()
            

def ayxsurl(page=1):
    url = 'http://www.bjkgjlu.com/top/p{}/'.format(page)
    return url


#     b = sorted(booklist)
#     for ass in b:
#         with open(name+'.txt', 'a', encoding='utf-8') as f:
#             f.write(booklist[ass])



def spider():
    pass


def header():
    return {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'
    }