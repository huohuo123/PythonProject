# 淘宝抓取信息
# 淘宝商品比价定向爬虫
import requests
import re


def getHTMLText(url):
    try:
        cookie = 'cna=GbAWE12FzBMCAXLyXk2RErB5; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; tg=0; enc=bjvEkvSPn6Yo9ObM%2FWrv5FrwqlfX%2Fb7p3EoWcN41gKzqdNtxf1SLIJi1bxDYp11tXaiKLhE5of5ENV5YdCzxcw%3D%3D; miid=8025393551609630962; t=22f9fc2c2ab316c728d5a46cff19b3d2; _uab_collina=155114932503735834223159; uc3=vt3=F8dByEzZ1Yo%2BirajyYQ%3D&id2=UoH7I2hOzRkE4g%3D%3D&nk2=F5RHpr53cBP83WI%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D; tracknick=tb272596_00; lgc=tb272596_00; _cc_=UtASsssmfA%3D%3D; mt=ci=16_1; v=0; cookie2=1da31c05786bc92e64382b0ab21921e4; _tb_token_=35433715b7a36; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; JSESSIONID=B94E13C30A36D27C2AA6EE04C4EFAEF7; uc1=cookie14=UoTZ5bI380qcgA%3D%3D; isg=BNDQiicouCddGmKu-xPoLXvLoRgoVr6lNs8FUsqhCSv-BXGvcq0vc2J33I1A62y7'
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
            'cookie': cookie
        }
        r = requests.get(url,headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


'''
每个页面的解析过程
'''


def parsePage(ilt, html):
    try:
        plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)
        tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)
        for i in range(len(plt)):
            price = eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1])
            ilt.append([price, title])
    except:
        print("")


def printGoodsList(ilt):
    tplt = "{:4}\t{:8}\t{:16}"
    print(tplt.format("序号", "价格", "商品名称"))
    count = 0
    for g in ilt:
        count = count + 1
        # 序号 商品价格 商品名称
        print(tplt.format(count, g[0], g[1]))


def main():
    goods = "书包"
    # 设定爬取的深度,假设第一页和第二页
    depth = 2
    # 爬取的相关url
    start_url = 'https://s.taobao.com/search?q=' + goods;
    info_list = []
    for i in range(depth):
        try:
            # 每一页都是44的倍数
            url = start_url + "&s=" + str(44 * i)
            html = getHTMLText(url)
            parsePage(info_list, html)
        except:
            continue
    printGoodsList(info_list)


if __name__ == '__main__':
    main()
