# coding=utf-8
from imp import reload

import requests
import json
import os
import csv
import sys
import time
import random
import demjson
reload(sys)


# IP池
def ipPool():
    # IPList =
    pass


# 模拟浏览器
def getHTMLText(url):
    try:
        # 01-设置用户代理池
        # UPPOOL = ["Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"]
        # headers = random.choice(UPPOOL)
        headers = {
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
        r = requests.get(url, headers=headers, timeout=50)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


# https://item.taobao.com/item.htm?id=563260162479&ali_refid=a3_430406_1007:1103381618:N:819850768_0_100:db7f3c061a1a66d7b085057e36d4192b&ali_trackid=1_db7f3c061a1a66d7b085057e36d4192b&spm=a21bo.2017.201874-sales.21
def getCommodityComments(url, count):
    if url[url.find('id=') + 14] != '&':
        id = url[url.find('id=') + 3:url.find('id=') + 15]
    else:
        id = url[url.find('id=') + 3:url.find('id=') + 14]
    url = 'https://rate.taobao.com/feedRateList.htm?auctionNumId=' + id + '&currentPageNum=1'
    # res = requests.get(url)
    res = getHTMLText(url)
    print(res)
    jc = json.loads(res.strip().strip('()'))
    max = jc['total']
    users = []
    comments = []
    page = 1
    print('该商品共有评论' + str(max) + '条,具体如下: loading...')
    path = os.getcwd() + "/taobao.csv"
    csvfile = open(path, 'a+', encoding='utf-8', newline='')
    writer = csv.writer(csvfile)
    # writer.writerow(('count','users','comment'))
    writer.writerow(("id", "name", "content"))

    # try:
    while count < max:
        time.sleep(10)
        res = requests.get(url[:-1] + str(page))
        page = page + 1
        jc = json.loads(res.text.strip().strip('()'))
        jc = jc['comments']
        # writer.writerow(("id","name","content"))
        for j in jc:
            users.append(j['user']['nick'])
            comments.append(j['content'])
            print(count + 1, '>>', users[count], '\n        ', comments[count])
            writer.writerow((count, users[count], comments[count]))
            count = count + 1
# except:
#     print("爬取中断+count")
#     print(count)
#     getCommodityComments(url,count)

if __name__ == '__main__':
    count = 0
    getCommodityComments('https://detail.tmall.com/item.htm?id=544439586789&', count)
