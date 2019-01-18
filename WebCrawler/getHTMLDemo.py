import requests
# 引入BeautifulSoup
from bs4 import BeautifulSoup


# BeautifulSoup 4中解析器

def main():
    url = "https://python123.io/ws/demo.html"
    r = requests.get(url)
    # print(r.text)
    demo = r.text
    # 解析html信息，直接解析demo
    soup = BeautifulSoup(demo, "html.parser")
    # 通过文件方式，解析
    # soup = BeautifulSoup(open("/Users/.."), "html.parser")
    print(soup.prettify())
    print(soup.title)
    # 获取第一个a标签的内容
    tag = soup.a
    print(tag)
    # 获取a标签的名字
    print(soup.a.name)
    # 获取a标签的父亲的名字
    print(soup.a.parent.name)
    # 获取a标签的父亲的父亲的名字
    print(soup.a.parent.parent.name)
    # 获取a标签的属性信息
    print(tag.attrs)
    # 获取a标签的具体属性的值
    print(tag.attrs['class'])
    # <class 'dict'>标签属性的类型为字典类型
    print(type(tag.attrs))



if __name__ == '__main__':
    main()
