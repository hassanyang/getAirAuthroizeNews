import requests
from xml.etree import ElementTree as ET

home = "http://www.caacnews.com.cn/1/1/index{}.html"

maxPage = 10

import re

canceled = []

def getAllnewsItmes():
    for i in range(0, maxPage):
        if i == 0:
            page = home.format("")
        else:
            page = home.format("_" + str(i))
        aa = requests.get(page,timeout=5)
        if aa.status_code != 200:
            continue
        aa.encoding='utf-8'
        items = re.findall(r'<td class="list_td2"><a href=(.*) target="_blank">(.*)</a></td>',aa.text)
        if len(items) >= 1:
            with open("cancaled.txt","a+",encoding='utf-8') as f,open("allnews.txt", 'a+', encoding='utf-8'):
                for (link,subject) in items:
                    link = "http://www.caacnews.com.cn/1/1/" + link[3:-1]
                    print(link,subject)
                    f.write(link + " , " + subject + "\n")
                    if "熔断" in subject:
                        canceled.append(link)
                        f.write(link + "\n")

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',}
def getnewsDetails():

    with open('cancaled.txt') as f, open('canceled_details.txt','a+',encoding='utf-8') as f1:
        for p in f.readlines():
            r = requests.get(p.replace("\n", ""),headers=headers)
            r.encoding = 'utf-8'
            c1 = re.findall(r'<div class="Custom_UnionStyle">(.*?)</div>',r.text.replace("\n",""))
            c2 = re.findall(r'<div class="TRS_Editor">(.*?)</div>',r.text.replace("\n",""))
            if len(c1) != 0:
                c = re.sub('<.*?>','',c1[0])
                f1.write(c + "\n")
                print(c)
                continue
            elif len(c2) != 0:
                c = re.sub('<.*?>','',c2[0])
                f1.write(c + "\n")
                print(c)
                continue
            else:
                print(p)
    

if __name__ == '__main__':
    getAllnewsItmes()
    getnewsDetails()

