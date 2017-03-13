# -*- coding: UTF-8 -*-
import sys
import urllib2
import re
import xlwt
import time
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf-8")

def getValue(res, key):
    try:
        result = res[key]
    except:
        result = ''
    return result

link_list = []
base_url = 'http://detail.zol.com.cn/cell_phone_advSearch/subcate57_1_s1398-s7074-s6500-s6502-s6106_1_1__'
for i in range(1, 145):    #1,145
    url = base_url + str(i) + '.html#showc'
    response = urllib2.urlopen(url)
    page = response.read()
    soup = BeautifulSoup(page, 'html.parser')
    ul = soup.find('ul', class_='result_list')
    print url
    temp = ul.find_all('a', text='更多参数>>')
    for link in temp:
        link_list.append('http://detail.zol.com.cn' + link['href'])

# f1 = open('link_list.txt','w')
# for link in link_list:
#     f1.write(link + '\n')
# f1.close()

res_list = []
for url in link_list:
    response = urllib2.urlopen(url)
    page = response.read()
    soup = BeautifulSoup(page, 'html.parser')
    result = {}
    for linebreak in soup.find_all('br'):
        linebreak.extract()

    div = soup.find('div',class_='breadcrumb')
    a_list = div.find_all('a')
    brand = a_list[2].string
    model = a_list[3].string
    result['brand'] = brand
    result['model'] = model
    th = soup.find('th',text='硬件')
    tr = th.parent
    list = tr.find('ul',class_='category-param-list').find_all('li')
    for li in list:
        spans = li.find_all('span')
        key = spans[0].string
        value = spans[1].string
        # print spans[1]
        if value == None:
            value = ''
            temp = spans[1].stripped_strings
            for i in temp:
                value += i + ','
        # print key,value
        result[key] = value
    try:
        system = result[u'操作系统']
        if 'Android' in system:
            pattern = re.compile("Android.{0,}", re.S)
            items = re.findall(pattern, system)
            try:
                android = str(items[0])
            except:
                android = ''
        else: android = ''
    except:
        android = ''
    result['android'] = android

    try:
        span  = soup.find('span',text='连接与共享')
        temp = span.parent.find_all('span')[1]
        hasOTG =  'OTG' in temp.strings
        if hasOTG:
            result['OTG'] = 'Y'
        else:
            result['OTG'] = 'N'
    except:
        result['OTG'] = 'N'
    for key in result:
        print key,result[key]
    res_list.append(result)

workbook = xlwt.Workbook(encoding='utf8')                          #创建工作簿
sheet1 = workbook.add_sheet(u'手机参数表', cell_overwrite_ok=True)  # 创建sheet
row0 = [u'品牌', u'机型', u'是否支持OTG', u'安卓版本', u'操作系统', u'运行内存',
        u'机身内存', u'扩展容量', u'CPU型号', u'GPU型号', u'CPU频率', u'存储卡', u'用户界面', u'电池容量', u'电池类型', u'核心数']
for i in range(0, len(row0)):
    sheet1.write(0, i, row0[i])
row_index = 1
for res in res_list:
        rows = [
            getValue(res, 'brand'),
            getValue(res, 'model'),
            getValue(res, 'OTG'),
            getValue(res, 'android'),
            getValue(res, u'操作系统'),
            getValue(res, u'RAM容量'),
            getValue(res, u'ROM容量'),
            getValue(res, u'扩展容量'),
            getValue(res, u'CPU型号'),
            getValue(res, u'GPU型号'),
            getValue(res, u'CPU频率'),
            getValue(res, u'存储卡'),
            getValue(res, u'用户界面'),
            getValue(res, u'电池容量'),
            getValue(res, u'电池类型'),
            getValue(res, u'核心数')
        ]
        for i in range(len(rows)):
            sheet1.write(row_index, i, rows[i])
        row_index += 1
t = str(time.time())
workbook.save(t + '.xls')  # 保存文件


