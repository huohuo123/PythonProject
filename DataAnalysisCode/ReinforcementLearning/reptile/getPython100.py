# 爬虫 获取python100案例网页相关信息
import requests
from bs4 import BeautifulSoup

'''
1、获取url
1）Python100Url
2）联系的URL
'''

url='http://www.runoob.com/python/python-100-examples.html'
# 模拟请求头，从网页请求获取
headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
}
# 发送请求
r=requests.get(url,headers=headers).content.decode('utf-8')
# print(r)
# 解析HTML文档，引入bs4
soup=BeautifulSoup(r,'lxml')
# print(soup)
# print(type(soup))
# 查找每个练习的a链接的href属性获取对应的链接地址
re_a=soup.find(id='content').ul.find_all('a')
# 创建一个列表保存url
list=[]
for i in re_a:
    list.append(i.attrs['href'])
print(list)

'''
2、根据获取的每个练习的链接地址来请求每个练习获得页面内容
遍历执行所有的链接内容
'''
for x in list:
    dic={}
    # 请求详细页
    ar=requests.get('http://www.runoob.com'+x,headers=headers).content.decode('utf-8')
    # 解析为html文档
    soup_ar=BeautifulSoup(ar,'lxml')
    # print(type(soup_ar))

    # 获取详细内容，查找练习内容
    # a查找标题
    dic['title']=soup_ar.find(id='content').h1.text
    # b查找题目,位置在第二组的<p>下边
    dic['tm']=soup_ar.find(id='content').find_all('p')[1].text
    # c查找程序分析
    dic['cxfx']=soup_ar.find(id='content').find_all('p')[2].text
    # d获取源代码
    try:
        dic['code']=soup_ar.find(class_='hl-main').text
    except Exception as e:
        dic['code']=soup_ar.find('pre').text
    # print(dic)
    with open('100-py.csv','a+',encoding='utf-8') as file:
        file.write(dic['title']+'\n')
        file.write(dic['tm']+'\n')
        file.write(dic['cxfx']+'\n')
        file.write(dic['code']+'\n')
        file.write('*'*50+'\n')
