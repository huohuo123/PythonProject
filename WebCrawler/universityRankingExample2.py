# 优化,对齐问题
import requests
from bs4 import BeautifulSoup
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
# 采用中文字符的空格填充chr(12288)
def printUnivList(ulist, num):
    # {3}表示使用format函数的第三个变量进行填充；0，1，2表示按顺序显示
    tplt = "{0:^10}\t{1:{3}^10}\t{2:^10}"
    print(tplt.format("排名", "学校名称", "总分", chr(12288)))
    for i in range(num):
        u = ulist[i]
        print(tplt.format(u[0], u[1], u[2], chr(12288)))
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
