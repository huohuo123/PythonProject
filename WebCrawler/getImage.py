# 网络图片的爬取和存储
import requests
import os


def main():
    # 待爬取的图片地址
    url = "http://img02.tooopen.com/images/20160509/tooopen_sy_161967094653.jpg"
    # 待保存的图片地址
    root = "/Users/huoyajing/Desktop/"
    path = root + url.split('/')[-1]
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            r = requests.get(url)
            print(r.status_code)
            # 二进制的形式存储图片流
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()
                print("文件保存成功")
        else:
            print("文件已经存在")

    except:
        print("爬取失败")


if __name__ == '__main__':
    main()
