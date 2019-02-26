# 爬虫  博客园,获取博客园所有的帖子信息，分页包含在内
import requests
# 解析成html
from lxml import etree

'''
需求分析
    爬取博客园的帖子
源码的分析
    https://www.cnblogs.com/
    tz=post_item_body
    title=cb_post_title_url(具体到每一篇文章里边的title)
    content=cnblogs_post_body(具体到每一篇文章里边的content)
代码实现
    1、根据入口url请求源码
    2、提取数据（每篇帖子的url）
    3、根据帖子的url进入到帖子详情页，获取详细内容
    4、保存数据，保存文件
'''

# 1、根据入口url请求源码
url = 'https://www.cnblogs.com/'
two_url=url
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
}
num=1
page=1
while True:
    r = requests.get(two_url).text
    # print(r)
    index = etree.HTML(r)
    # print(index)

    # 2、提取数据（每篇帖子的url）
    # 提取到每一页的url
    tz_url = index.xpath('//div[@class="post_item_body"]/h3/a/@href')
    # 提取到下一页的url,/a[last()表示获取a标签的最后一个
    next_url=index.xpath('//div[@class="pager"]/a[last()]')
    # 3、根据帖子的url进入到帖子详情页，获取详细内容
    for i in tz_url:
        #     print(i)
        re = requests.get(i).text
        # print(re)
        html = etree.HTML(re)
        # print(html)
        # 提取标题和内容,在网页，右击获取xpath格式
        tz_title = html.xpath('//a[@id="cb_post_title_url"]/text()')
        # print(tz_title)
        # 若text()拿不到信息，则更换string方式
        # tz_content=html.xpath('//*[@id="cnblogs_post_body"]/text()')
        tz_content = html.xpath('string(//*[@id="cnblogs_post_body"])')
        # print(tz_content)

        # 4、保存数据，保存文件
        with open('cn-blogs.csv', 'a+', encoding='utf-8') as file:
            file.write(tz_title[0] + '\n')
            file.write(tz_content + '\n')
            file.write(i + '\n')
            file.write('*' * 50 + '\n')
        print('{0}页第{1}篇帖子'.format(page,num))
        num+=1

    if next_url[0].xpath('text()')[0]=='Next >':
        # 切片去掉多余的斜杠
        two_url=url[:-1]+next_url[0].xpath('@href')[0]
        page+=1
        num=1
        print(page)
    else:
        break
