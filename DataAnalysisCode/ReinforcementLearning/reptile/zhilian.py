# 智联招聘 实例 暂定  2019年02月27日13:57:40
from lxml import etree
import requests
'''
需求分析
    1、https://sou.zhaopin.com/进入职位搜索获取职位分类列表
    2、通过分类进入职位详细列表
    3、进入职位详细信息页面

源码分析

代码实现

'''


# 1.获取职位分类列表 url
def get_job_cat_list(url, headers):
    r = requests.get(url,headers= headers).text
    print(r)
    # 解析
    index = etree.HTML(r)
    print(index.text)
    #获取分类列表的url
    job_url = index.xpath('//div[@id="search_right_demo"]/div/div/a/@href')
    # print(job_url)


# 2.获取职位列表
def get_job_list(url, headers):
    pass


# 3.获取职位详细信息
def get_job_info(url):
    pass


# 4.保存数据
def save_data(data):
    pass


if __name__ == '__main__':
    #入口地址
    url = 'http://sou.zhaopin.com/'
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    }
    get_job_cat_list(url,headers)
