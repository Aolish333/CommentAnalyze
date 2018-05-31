# coding=utf-8
from imp import reload

import requests
import json
import os
import csv
import sys
import time
import pymysql
import random

import IPSpider

reload(sys)

# 模拟浏览器
def getHTMLText(url):
    try:
        # 01-设置用户代理池
        headers = {
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
        r = requests.get(url, headers=headers, timeout=50,proxies=random.choice(IPSpider.checking()))
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def getCommodityComments(url):
    # 支持11位和12位id
    if url[url.find('id=')+14] != '&':
        id = url[url.find('id=')+3:url.find('id=')+15]
    else:
        id = url[url.find('id=')+3:url.find('id=')+14]
    # 打开数据库连接
    db = pymysql.connect("localhost","root","123456","datadig",use_unicode=True, charset="utf8mb4")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    tableName = "good_" + id
    cursor.execute("DROP TABLE IF EXISTS " + tableName)
    sql = """ CREATE TABLE """ + tableName + """(
         id CHAR(10),
         name CHAR(10),
         comment VARCHAR(600)
        ) DEFAULT CHARSET=utf8mb4 auto_increment= 0 ;"""
    # 创建对应的数据库表
    print('创建数据库成功')
    cursor.execute(sql)
    url = 'https://rate.taobao.com/feedRateList.htm?auctionNumId='+id+'&currentPageNum=1'
    res = getHTMLText(url)
    # res = requests.get(url)
    # 将 JSON 对象转换为 Python 字典
    jc = json.loads(res.strip().strip('()'))
    max = jc['total']
    users = []
    comments = []
    count = 0
    page = 1
    print('该商品共有评论'+str(max)+'条,具体如下: loading...')
    # os.getcwd() 方法用于返回当前工作目录。
    path = os.getcwd()+"/taobao.csv"
    csvfile = open(path, 'a+' , encoding='utf8',newline='')
    writer = csv.writer(csvfile)
    writer.writerow(("id", "name", "content"))

    try:
        while count<max:
            res = requests.get(url[:-1]+str(page))
            page = page + 1
            jc = json.loads(res.text.strip().strip('()'))
            jc = jc['comments']
            for j in jc:
                if j['content']== ' ':
                    break
                if j['content'] == '此用户没有填写评价。':
                    continue
                else:
                    users.append(j['user']['nick'])
                    comments.append(j['content'])
                    print(count+1,'>>',users[count],'\n        ',comments[count])
                    cursor.execute('INSERT INTO ' + tableName + '(id, name, comment) values("%s", "%s","%s")' % \
                     (count, j['user']['nick'], j['content']))
                    writer.writerow((count,users[count],comments[count]))
                    count = count + 1
            time.sleep(1)
        db.close()
    except:
        db.commit()
        db.close()

if __name__ == '__main__':
    getCommodityComments('https://detail.tmall.com/item.htm?id=550887826096&')
