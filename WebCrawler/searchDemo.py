# 百度和360 通过关键字搜索信息结果
import requests


def baiduSearchMain():
    try:
        # 百度的键值对 wd
        kv = {'wd': 'python'}
        r = requests.get("http://www.baidu.com/s", params=kv)
        print(r.status_code)
        # 发给百度的地址
        print(r.request.url)
        r.raise_for_status()
        # 445233 返回值是400多k的信息
        print(len(r.text))
    except:
        print("爬去失败")


def search360Main():
    try:
        # 360键值对q
        kv = {'q': 'python'}
        r = requests.get("http://www.so.com/s", params=kv)
        print(r.status_code)
        # 发给360的地址
        print(r.request.url)
        r.raise_for_status()
        # 227478 返回值是200多k的信息
        print(len(r.text))
    except:
        print("爬去失败")


if __name__ == '__main__':
    baiduSearchMain()
    search360Main()
