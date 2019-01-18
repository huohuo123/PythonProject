# 亚马逊，通过更改user-agent信息，模拟用户请求，进而获取爬虫信息
import requests


# 503错误，可以通过status_code和encoding等得到相关信息
def main(url):
    try:
        # 更改User-Agent信息，获取访问权限
        kv = {'user-agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=kv)
        r.raise_for_status()
        print(r.status_code)
        print(r.encoding)
        r.encoding = r.apparent_encoding
        print(r.status_code)
        print(r.text[1000:2000])
    except:
        print("爬去失败")


if __name__ == '__main__':
    url = "https://www.amazon.cn/dp/B07K138VGY/ref=zg_bsnr_books_1?_encoding=UTF8&psc=1&refRID=1KG5Q4BX3QNQJJB15VSJ"
    main(url)
