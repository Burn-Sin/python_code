import re,json


def main():
    f = open('菜单.txt','r',encoding='utf-8')
    lines = f.readlines()
    f.close()
    jsonlist = {}
    for line in lines:
        str = line.strip('\n')
        id = re.findall('\d+', str)
        text = re.findall('\D+',str)
        jsonlist[text[0]]=id[0]
    str = json.dumps(jsonlist,ensure_ascii=False)
    with open('菜单.json','w')as f:
        f.write(str)



if __name__ == '__main__':
    main()