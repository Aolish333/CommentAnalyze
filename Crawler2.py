# coding=utf-8
from imp import reload

import requests
import json
import os
import csv
import sys

reload(sys)

#https://item.taobao.com/item.htm?id=563260162479&ali_refid=a3_430406_1007:1103381618:N:819850768_0_100:db7f3c061a1a66d7b085057e36d4192b&ali_trackid=1_db7f3c061a1a66d7b085057e36d4192b&spm=a21bo.2017.201874-sales.21
def getCommodityComments(url):
    if url[url.find('id=')+14] != '&':
        id = url[url.find('id=')+3:url.find('id=')+15]
    else:
        id = url[url.find('id=')+3:url.find('id=')+14]
    url = 'https://rate.taobao.com/feedRateList.htm?auctionNumId='+id+'&currentPageNum=1'
    res = requests.get(url)
    jc = json.loads(res.text.strip().strip('()'))
    max = jc['total']
    users = []
    comments = []
    count = 0
    page = 1
    print('该商品共有评论'+str(max)+'条,具体如下: loading...')

    path = os.getcwd()+"/taobao.csv"
    csvfile = open(path, 'a+' , encoding='utf-8',newline='')
    writer = csv.writer(csvfile)
    #writer.writerow(('count','users','comment'))
    writer.writerow(("id", "name", "content"))

    while count<max:
        res = requests.get(url[:-1]+str(page))
        page = page + 1
        jc = json.loads(res.text.strip().strip('()'))
        jc = jc['comments']
        # writer.writerow(("id","name","content"))
        for j in jc:
            users.append(j['user']['nick'])
            comments.append( j['content'])
            print(count+1,'>>',users[count],'\n        ',comments[count])
            writer.writerow((count,users[count],comments[count]))
            count = count + 1

if __name__ == '__main__':
    getCommodityComments('https://detail.tmall.com/item.htm?id=566363218597&')
