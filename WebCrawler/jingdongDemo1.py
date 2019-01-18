# 爬去京东网页实例
import requests


def jingdongInfo(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        print(r.status_code)
        print(r.encoding)
        print(r.text)
    except:
        print("爬去失败")


if __name__ == '__main__':
    url = "https://item.d.com/28961607097.html"
    jingdongInfo(url)
