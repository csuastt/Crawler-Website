from bs4 import BeautifulSoup
import re
import urllib.error
import urllib.request
import xlwt
import xlrd
import time,random
import json
import pickle
# 模拟浏览器的库
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# 从第几个开始
start = 0
end = 500
total = 220


def main():
    # 初始化
    # browser = webdriver.Firefox()
    browser = webdriver.Chrome()
    # 获取所有要爬影视的url
    urls = getUrl()
    # print(urls)
    # 爬取网站
    datalist = getData(urls,browser)
    # 存储列表
    # list_file = open(r'workzone\movie_spider\movie_list.pickle','wb')
    # pickle.dump(datalist,list_file)
    # list_file.close()
    # 保存数据在json文件中
    save_path = r"workzone\movie_spider\movie_json" + "\\"
    save_movies_data(datalist, save_path)


def getUrl() -> list:
    '''
    从excel文件中读取要爬取网站的url
    '''
    wb = xlrd.open_workbook(r"workzone\movie_spider\movies_3.xls")
    sheet = wb.sheet_by_index(0)
    urls = []
    # 导入视频分割序列
    for i in range(start, total):
        urls.append(str(sheet.cell_value(i, 0)))
    return urls

# 创建正则表达式对象，表示规则
# 影片名
findName = re.compile(r'<span property="v:itemreviewed">(.*?)</span>')
# 演员
findActorLink = re.compile(r'<a\s*href="(.*?)" rel="v:starring">(.*?)</a>')
# 国家
findState = re.compile(r'<span class="pl">制片国家/地区:</span>(.*?)<br\s*/*>')
# 语言
findLanguage = re.compile(r'<span class="pl">语言:</span>(.*?)<br\s*/*>')
# 片长
findLength = re.compile(r'''<span property="v:runtime"\s*content=".*">(.*?)</span\s*>''')
# 简介
findIntro = re.compile(r'<span property="v:summary">(.*?)</span\s*>|<span property="v:summary" class="">(.*?)</span\s*>|<span class="" property="v:summary">(.*?)</span\s*>', re.S)
# 图片
findImgSrc = re.compile(r'<img src="(.*?)".*rel="v:image"\s*/*>')
# 短评
findComments = re.compile(r'''<p class="">\s*<span\s*class="short">(.*?)</span>''',re.S)

def getData(urls: list, browser):
    '''
    爬取网站
    '''
    datalist = []
    actorlist = []
    # 逐一解析数据
    # 调用获取页面信息的函数
    index = -1
    for url in urls:
        index += 1
        if(index == end):
            break
        print(index)
        # 打开网页
        # 保存获取到的网页源码
        time.sleep(random.random()*3)
        # print(url)
        browser.get(url)
        browser.implicitly_wait(10)
        try:
            item = browser.page_source
        except BaseException:
            print(url)
            continue
        # f=open(r'workzone\movie_spider\testclass.html',mode="w",encoding="utf-8")
        # f.write(item)
        # print(url)
        # html = askURL(url)
        # 逐一解析数据
        # 保存一部电影的所有信息
        movie_data = []
        # 采用CSS选择器提取电影标题
        # title = item.select(".title")
        # print(title[0].string)
        # 采用正则表达式查找
        # print(item)
        # 获取影片的各项参数
        name = re.findall(findName,item)
        actors = re.findall(findActorLink,item)
        intro = re.findall(findIntro,item)
        picture = re.findall(findImgSrc,item)
        # print(picture)
        state = re.findall(findState,item)
        language = re.findall(findLanguage,item)
        length = re.findall(findLength,item)
        comments = re.findall(findComments,item)
        if(name == []):
            continue
        movie_data.append(name)
        actors = actors[:10]
        actorlist += actors
        movie_data.append(actors)
        if(len(intro) < 1):
            print(movie_data)
            print(url)
            continue
        if(intro[0][0]):
            intro[0] = re.sub(r'<br(\s+)?/?>(\s+)?'," ",intro[0][0])
            intro[0] = re.sub(r'\s+'," ",intro[0])
            # intro[0] = re.sub(r'\n'," ",intro[0])
            intro[0] = intro[0].strip()
        elif(intro[0][1]):
            intro[0] = re.sub(r'<br(\s+)?/?>(\s+)?'," ",intro[0][1])
            intro[0] = re.sub(r'\s+'," ",intro[0])
            # intro[0] = re.sub(r'\n'," ",intro[0])
            intro[0] = intro[0].strip()
        else:
            intro[0] = re.sub(r'<br(\s+)?/?>(\s+)?'," ",intro[0][2])
            intro[0] = re.sub(r'\s+'," ",intro[0])
            # intro[0] = re.sub(r'\n'," ",intro[0])
            intro[0] = intro[0].strip()
        movie_data.append(intro)
        movie_data.append(picture)
        movie_data.append(state)
        movie_data.append(language)
        movie_data.append(length)
        for i in range(len(comments)):
            comments[i] = re.sub(r'\n'," ",comments[i])
        movie_data.append(comments)
        # print(movie_data)
        # \s是指空白，包括空bai格、换行、tab缩进等所有的空白
        # \S刚好相bai反，这样一正一反下来，就表示所有的字符
        # bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)
        # bd = re.sub('/'," ",bd)
        # movie_data.append(bd.strip()) # 去掉前后的空格
        datalist.append(movie_data)
    save_actors_data(actorlist,r"workzone\movie_spider\actors_3.csv")
    return datalist


def askURL(url: str) -> str:
    '''
    得到一个指定URL的网页内容
    '''
    # 用户道理，告诉豆瓣我们是什么类型的机器，
    # 告诉浏览器我们可以接受什么水平的信息
    head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; \
                Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
    'Cookie': 'Cookie: gr_user_id=ef8ab57e-5908-4665-8043-78a4f6d9ac28; _vwo_uuid_v2=D816B5D148FBA30A6BAA917CA3065855F|e1d12e4c1731ab1fb6c1b2aa9c99e6ff; __utma=30149280.518292907.1541469583.1599385867.1599392968.62; __utmz=30149280.1599145046.59.53.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; douban-fav-remind=1; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1599392967%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DGoFNfCosUVPAUAny6JW57Uh7-uzgv0XhDCwz96GOjMnN0gbESP1WomI_JuuAph0bn3uCech1O6X67P1jeJsSa_%26wd%3D%26eqid%3De5a577c3000125e2000000065eecddc8%22%5D; _pk_id.100001.4cf6=1612d7d7f3cfb623.1572623223.9.1599393903.1599388989.; __utma=223695111.1749715506.1572623224.1599385867.1599392968.9; __utmz=223695111.1592581603.6.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; viewed="6811366_26862478_1315234_26430963_34852472_34836460_1015864_3007268_1122372_2568236"; bid=D7OPyU5SPGI; ll="108288"; __utmv=30149280.21510; douban-profile-remind=1; __utmc=30149280; __utmc=223695111; ap_v=0,6.0; _pk_ses.100001.4cf6=*; __utmb=30149280.0.10.1599392968; __utmb=223695111.0.10.1599392968'
    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def save_actors_data(actors, save_path):
    '''
    保存演员的信息到excel中
    '''
    print("save actors...")
    # workbook = xlwt.Workbook(encoding="utf-8",style_compression=0)
    # worksheet = workbook.add_sheet('actor',cell_overwrite_ok=True)
    # for i in range(len(actors)):
    #     actor_data = actors[i]
    #     for j in range(2):
    #         worksheet.write(i,j,actor_data[j])
    # workbook.save(save_path)
    with open((save_path),'a',encoding="utf-8") as f:
        for i in range(len(actors)):
            actor_data = actors[i]
            f.write(actor_data[0])
            f.write(',')
            f.write(actor_data[1])
            f.write('\n')


def save_movies_data(datalist, save_path):
    '''
    将电影的信息保存到json文件中
    '''
    for i in range(len(datalist)):
        file_path = save_path + ("%d.json"%(i+1018))
        with open(file_path,"w",encoding='utf-8') as f:
            try:
                new_dict = {}
                if(len(datalist[i][0]) == 0):
                    new_dict['name'] = ''
                else:
                    new_dict['name'] = datalist[i][0][0]
                new_dict['actors'] = datalist[i][1]
                if(len(datalist[i][2]) == 0):
                    new_dict['introduction'] = ''
                else:
                    new_dict['introduction'] = datalist[i][2][0]
                if(len(datalist[i][3]) == 0):
                    new_dict['pictures_index'] = ''
                else:
                    new_dict['pictures_index'] = datalist[i][3][0]
                if(len(datalist[i][4]) == 0):
                    new_dict['state'] = ''
                else:
                    new_dict['state'] = datalist[i][4][0]
                if(len(datalist[i][5]) == 0):
                    new_dict['language'] = ''
                else:
                    new_dict['language'] = datalist[i][5][0]
                if(len(datalist[i][6]) == 0):
                    new_dict['length'] = ''
                else:
                    new_dict['length'] = datalist[i][6][0]
                new_dict['comments'] = datalist[i][7]
            except BaseException:
                print(datalist[i])
            json.dump(new_dict,f,ensure_ascii=False)



if __name__ == "__main__":
    main()
    print("爬取完毕")