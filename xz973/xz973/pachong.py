import requests
from lxml import etree
from urllib.parse import quote,unquote
import time

def url(page=0, bookname=''):#笔趣阁
    page2 = page + 1
    name = quote(bookname,encoding='gbk')
    return 'https://www.biquge.cm/modules/article/sou.php?searchkey={}&ct=2097152&si=biquge.cm&sts=biquge.cm&page={}'.format(name,page2)

def url2(page=0, bookname=''):#闪舞小说
    page2 = page + 1
    name = quote(bookname,encoding='utf-8')
    return 'https://www.35xs.com/book/search?keyword={}&page={}&X-Requested-With=XMLHttpRequest'.format(name,page2)

def url3(page=0, bookname=''):#顶点
    
    page2 = page + 1
    name = quote(bookname,encoding='utf-8')
    return 'https://www.dingdiann.com/searchbook.php?keyword={}&page={}'.format(name,page2)

    
def headers():
    return {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'
    }


def get_bqglist(name):
    
    r = requests.get(url(bookname=name),headers=headers())
    r.encoding="gbk"
    html = etree.HTML(r.text)
    lastpage = html.xpath('//div[@class="pagelink"]/a[@class="last"]/text()')[0]
    book_list = {}
    id = 0
    for i in range(int(lastpage)):
        r = requests.get(url(bookname=name,page=i),headers=headers())
        r.encoding="gbk"
        html = etree.HTML(r.text)
        book_name = html.xpath('//*[@id="nr"]/td[@class="odd"]/a/text()') #书名
        book_url = html.xpath('//*[@id="nr"]/td[@class="odd"]/a/@href') #书地址
        new_lod = html.xpath('//*[@id="nr"]/td[3]/text()') #作者
        new = html.xpath('//*[@id="nr"]/td[2]/a/text()') #最新章节
        for n in range(len(book_name)):
            book_list[id] = {'书名':book_name[n],'最新章节':new[n],'地址':book_url[n],'作者':new_lod[n]}
            id+=1
    return book_list


def get_swlist(name):
    r = requests.get(url2(bookname=name),headers=headers())
    r.encoding="utf-8"
    html = etree.HTML(r.text)
    lastpage = html.xpath('/html/body/div[2]/ul/div/@data-pagecount')[0]
    book_list = {}
    id = 0
    for i in range(int(lastpage)):
        r = requests.get(url2(bookname=name,page=i),headers=headers())
        r.encoding="utf-8"
        html = etree.HTML(r.text)
        book_name = html.xpath('//*[@class="tab-content"]/fieldset/table/tbody/tr/td[1]/a/text()')
        book_url = html.xpath('//*[@class="tab-content"]/fieldset/table/tbody/tr/td[1]/a/@href') #https://www.35xs.com
        new_lod = html.xpath('//*[@class="tab-content"]/fieldset/table/tbody/tr/td[2]/text()')
        new = html.xpath('//*[@class="tab-content"]/fieldset/table/tbody/tr/td[3]/a/text()')
        for n in range(len(book_name)):
            book_list[id] = {'书名':book_name[n],'最新章节':new[n],'地址':'https://www.35xs.com' + book_url[n],'作者':new_lod[n]}
            id += 1
    return book_list


def get_ddlist(name):
    requests.packages.urllib3.disable_warnings()
    r = requests.get(url3(bookname=name),headers=headers(),verify=False)
    html = etree.HTML(r.text)
    lastpage = html.xpath('//*[@id="pagelink"]/em/text()')
    book_list = []
    for i in range(int(lastpage[0].split('/')[1])):
        time.sleep(1)
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url3(bookname=name,page=i),headers=headers(),verify=False)
        html = etree.HTML(r.text)
        book_name = html.xpath('//*[@id="main"]/div[1]/ul/li/span[@class="s2"]/a/text()')
        book_url = html.xpath('//*[@id="main"]/div[1]/ul/li/span[@class="s2"]/a/@href') #https://www.dingdiann.com
        new_lod = html.xpath('//*[@id="main"]/div[1]/ul/li/span[@class="s4"]/text()')
        new = html.xpath('//*[@id="main"]/div[1]/ul/li/span[@class="s3"]/a/text()')
        for n in range(len(book_name)):
            book_list.append({'name':book_name[n],'url':'https://www.dingdiann.com'+book_url[n],'zz':new_lod[n],'new':new[n]})
    return book_list

def zhangjie(name):
    r = requests.get(name,headers=headers(),verify=False)
    html = etree.HTML(r.text)
    everlode = html.xpath('//*[@id="list"]/dl/dd/a/@href')[12:]
    shuming = html.xpath('//*[@id="info"]/h1/text()')[0]
    lenbook = len(everlode)
    for i in range(lenbook):
        requests.packages.urllib3.disable_warnings()
        r2 = requests.get('https://www.dingdiann.com'+everlode[i],headers=headers(),verify=False)
        html2 = etree.HTML(r2.text)
        zhangjiename = html2.xpath('//*[@class="bookname"]/h1/text()')[0]
        neirong = html2.xpath('//*[@id="content"]/text()')
        print(zhangjiename)
        xiangxinr = str(neirong).replace(r"\r\n\t\t\t\t", "").replace(r"\u3000\u3000","").replace(r"', '","\r").replace(r"']","").replace(r"['","")
        text = zhangjiename + '\r' + xiangxinr
        with open(shuming+'.txt','a',encoding='utf-8') as f:
            f.write(text)

# star = time.time()

# zhangjie('https://www.dingdiann.com/ddk160279/')
# # print(get_ddlist('蛊真人'))

# end = time.time()
# print(end-star)