# -*- coding: GB2312 -*-
from bs4 import BeautifulSoup
import requests, time

firsturl = "http://www.tianqihoubao.com/lishi/shandong.htm"

#times = 0

f = open("output.txt","w")

months=['201401','201402','201403','201404','201405','201406','201407','201408','201409','201410','201411','201412','201501','201502','201503','201504','201505','201506','201507','201508','201509','201510','201511','201512','201601','201602','201603','201604','201605','201606','201607','201608','201609','201610','201611','201612','201701','201702','201703','201704','201705','201706','201707','201708','201709','201710','201711','201712']

def spider_1(url1):  # 在主列表页面执行的操作

    response = requests.get(url1)
    response.encoding = "UTF-8"
    soup = BeautifulSoup(response.text, 'lxml')
    cities = soup.select('dd > a')  # 城市名
    citiesurl = soup.select('dd > a')  # 城市详情页链接，需要获取href
    for city, cityurl in zip(cities, citiesurl):
        data1 = {  # 定义字典
            'city': city.get_text().strip().replace("\t", "").replace(" ", "").replace("\n", ""),  # 正确的
            'href': cityurl.get('href'),  # 正确的
        }
        url_middlepart = data1["href"].strip().replace("\t", "").replace(" ", "").replace("\n", "").replace("/lishi", "")[0: data1["href"].strip().replace("\t", "").replace(" ", "").replace("\n", "").replace("/lishi", "").index('.')]

        for month in months:
            print(data1["city"] + "http://www.tianqihoubao.com/aqi" + url_middlepart + "-" + month + ".html")
            spider_2(
                data1["city"], "http://www.tianqihoubao.com/aqi" + url_middlepart + "-" + month + ".html")  # 测试性输出，检查查询内容是否符合预期

        #global times
        #times += 1
        #if (times + 1) % 6 == 0:
        #    time.sleep(30)



def spider_2(cityname, url2):  # 在表格页面执行的操作
    response = requests.get(url2)
    response.encoding = "GB2312"
    soup = BeautifulSoup(response.text, 'lxml')
    trs = soup.find_all('tr')
    #dates = soup.select('td')
    del(trs[0])
    for tr0 in trs:
        print(cityname + "|", end = "")
        f.write(str(cityname + "|"))
        for td0 in tr0:
            print(str(td0.string).strip().replace(" ", "").replace("\t", "").replace("\r\n", ""), end = "|")
            f.write(str(str(td0.string).strip().replace(" ", "").replace("\t", "").replace("\r\n", "") + "|"))
        print("")
        f.write("\n")
        f.flush() # 把之前在缓存中等待写入文件的内容立刻落盘

spider_1(firsturl)
