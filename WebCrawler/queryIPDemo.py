# IP归属地的自动查询
import requests


def main():
    url = "http://www.ip138.com/ips138.asp?ip="
    try:
        r = requests.get(url + '127.0.0.1')
        r.raise_for_status()
        # 更换编码格式
        r.encoding = r.apparent_encoding
        print(r.status_code)
        print(r.text[-500:])
    except:
        print("爬取失败")


if __name__ == '__main__':
    main()
