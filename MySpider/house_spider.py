#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Arthur Zheng
@license: Apache Licence 
@site: 
@software: PyCharm
@file: house_spider.py
@time: 2018/9/9 22:11
"""

'''
爬取房天下-温州房价信息
'''
import requests
from bs4 import BeautifulSoup
import re
import pandas
import time


def main():
    excel = 'house_price.xlsx'
    today=time.strftime("%Y-%m-%d", time.localtime())
    url = 'http://wz.newhouse.fang.com/house/s/'  # 房天下-温州的url
    headers = {  # 设置headers，伪装成浏览器
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
        "Accept": "text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,*/*;q=0.8"}
    timeout = 300  # 设置超时时间
    pages = requests.get(url, headers = headers, timeout = timeout)

    soup = BeautifulSoup(pages.content, 'html.parser', from_encoding = 'gb18030')
    last_page = soup.select('.last')
    page_num = int(last_page[0]['href'].split('/')[3].split('9')[1])  # 获取页数
    # print('总页数为【{}】页'.format(page_num))
    names_list = []  # 楼盘名称
    adresses_list = []  # 地址
    all_type_list = []  # 楼盘销售情况
    all_money_list = []  # 房价
    url_demo = 'http://wz.newhouse.fang.com/house/s//s/b9{}/'
    for i in range(1, (page_num + 1)):  #遍历页面，获取信息
        url = url_demo.format(i)
        html = requests.get(url, headers = headers, timeout = timeout)
        soup = BeautifulSoup(html.content, 'html.parser', from_encoding = 'gb18030')
        names = soup.select('.nlcd_name a')
        adresses = soup.select('.address a')
        for name in names:
            names_list.append(name.text.strip())
        for adress in adresses:
            adress_detail = re.findall(r'".+"', str(re.findall(r'title=".+"', str(adress))))[0]
            adresses_list.append(adress_detail.split('"')[1])
        all_type = soup.findAll(name = "span", attrs = {"class": re.compile(r"forSale|inSale|outSale|zusale|zushou")})
        for type in all_type:
            all_type_list.append(type.text)

        if soup.select('.kanzx'):
            all_money_list.append('无')
            all_money = soup.findAll(name = "div", attrs = {"class": re.compile(r"nhouse_price|kanesf")})
            for money in all_money:
                all_money_list.append(money.text.strip())
        else:
            all_money = soup.findAll(name = "div", attrs = {"class": re.compile(r"nhouse_price|kanesf")})
            for money in all_money:
                all_money_list.append(money.text.strip())
    # 遍历四个数组，见信息输出，最后保存在一个excel中。
    all_message = []
    for m in range(0, len(names_list)):
        message = [names_list[m], adresses_list[m], all_type_list[m], all_money_list[m]]
        print(message)
        all_message.append(message)
    df = pandas.DataFrame(all_message)
    df.to_excel(excel, sheet_name = today)
    # print(df)


if __name__ == '__main__':
    main()
