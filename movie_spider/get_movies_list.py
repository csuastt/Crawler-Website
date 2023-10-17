import re
import xlwt


def getData(file_path) -> list:
    '''
    获取数据
    '''
    htmlf = open(file_path,'r',encoding="utf-8")
    # 获取影片的名称和连接
    data = htmlf.read()
    findNameLink = re.compile(r'<span class="movie-name-text"><a href="(.*?)" target="_blank">(.*?)</a></span>')
    res = re.findall(findNameLink,data)
    return res



def saveData(datalist, save_path):
    '''
    将数据保存至excel中
    '''
    print("save...")
    workbook = xlwt.Workbook(encoding="utf-8",style_compression=0)
    worksheet = workbook.add_sheet('movie',cell_overwrite_ok=True)
    for i in range(0,350):
        print("第%d条"%i)
        movie_data = datalist[i]
        for j in range(1,-1,-1):
            worksheet.write(i,j,movie_data[j])
    workbook.save(save_path)


if __name__ == "__main__":
    # 文件路径
    # file_path = r"workzone\movie_spider\movies_1.html"
    file_path = r"workzone\movie_spider\movies_3.html"
    # 获取数据
    datalist = getData(file_path)
    # 保存数据
    # 保存在excel中
    save_path = r"workzone\movie_spider\movies_3.xls"
    saveData(datalist, save_path)