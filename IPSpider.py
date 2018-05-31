# coding=utf-8

import requests
import random
from bs4 import BeautifulSoup

def IPspiderMothd():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'}
    url = 'http://www.xicidaili.com/nn/1'
    s = requests.get(url, headers=headers)
    soup = BeautifulSoup(s.text, 'lxml')
    ips = soup.select('#ip_list tr')
    fp = open('host.txt', 'w')
    flag = 1
    for i in ips:
        try:
            if flag == 1:
                flag = 0
                continue
            ipp = i.select('td')
            ip = ipp[1].text
            host = ipp[2].text
            fp.write(ip)
            fp.write('\t')
            fp.write(host)
            fp.write('\n')
        except Exception as e:
            print('no ip !')
    fp.close()

def checking():
    # headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'}
    url = 'https://www.baidu.com'
    fp = open('host.txt','r')
    ips = fp.readlines()
    proxys = list()
    for p in ips:
        ip =p.strip('\n').split('\t')
        proxy = 'http:\\' +  ip[0] + ':' + ip[1]
        proxies = {'proxy':proxy}
        proxys.append(proxies)


    for pro in proxys:
        try :
            s = requests.get(url,proxies = pro)
            print (s)
        except Exception as e:
            print (e)
    return proxys

if __name__ == '__main__':
    IPspiderMothd()
    print(random.choice((checking())))


