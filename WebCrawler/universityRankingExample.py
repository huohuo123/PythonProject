# 功能描述
# 输入：大学排名URL链接
# 输出：大学排名信息的屏幕输出（排名，大学名称，总分）
# 技术路线：requests-bs4
# 定向爬虫：仅对输入URL进行爬取，不扩展爬取
from bs4 import BeautifulSoup
import requests
import bs4


# 步骤一：从网络上获取大学排名网页内容
def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


# 提取网页内容中信息到合适的数据结构
def fillUnivList(ulist, html):
    soup = BeautifulSoup(html, "html.parser")
    for tr in soup.find('tbody').children:
        # 检测tr标签类型
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')
            ulist.append([tds[0].string, tds[1].string, tds[2].string])


# 利用数据结构展示并输出结果
def printUnivList(ulist, num):
    print("{:^10}\t{:^6}\t{:^10}".format("排名","学校名称","总分"))
    for i in range(num):
        u=ulist[i]
        print("{:^10}\t{:^6}\t{:^10}".format(u[0],u[1],u[2]))
    print("Suc" + str(num))


# 主函数
def main():
    uinfo = []
    url = "http://www.zuihaodaxue.com/zuihaodaxuepaiming2016.html"
    html = getHTMLText(url)
    fillUnivList(uinfo, html)
    # 获取前20个学校排名
    printUnivList(uinfo, 20)


if __name__ == '__main__':
    main()
