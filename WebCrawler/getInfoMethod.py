# 提取信息的一般方法
from bs4 import BeautifulSoup
import requests
# 正则表达式库
import re


def main():
    url = "https://python123.io/ws/demo.html"
    r = requests.get(url)
    demo = r.text
    print(demo)
    print("SSSSSSSSSSSSSSSSSSSSS")
    # 解析html信息，直接解析demo
    soup = BeautifulSoup(demo, "html.parser")
    for link in soup.find_all('a'):
        print(link.get('href'))
    # 根据id属性查值
    print(soup.find_all(id='link1'))
    # 借助正则表达式模糊查值
    print(soup.find_all(id=re.compile('link')))
    # 是否对子孙全部检索，默认TRUE,False则只查找儿子标签值
    print(soup.find_all('a', recursive=False))
    print(soup.find_all(string="Basic Python"))
    # 借助正则表达式，模糊查字符串信息
    print("小写python,模糊查询")
    print(soup.find_all(string=re.compile("python")))
    print("大写ython,模糊查询")
    print(soup.find_all(string=re.compile("Python")))


if __name__ == '__main__':
    main()
