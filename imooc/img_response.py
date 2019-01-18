import requests


# 下载图片
def download_image():
    url = "http://g.hiphotos.baidu.com/image/pic/item/adaf2edda3cc7cd9ebe507433401213fb90e915b.jpg"
    # stream 支持流传输
    response = requests.get(url, stream=True)
    # print(response.content)
    # print(response.status_code)
    # print(response.reason)
    # print(response.headers)
    # 下载到图路径下
    with open('demo.jpg', 'wb')as fd:
        for chunk in response.iter_content(128):
            fd.write(chunk)


# 下载图片，提升方法
def download_image1():
    url = "http://g.hiphotos.baidu.com/image/pic/item/adaf2edda3cc7cd9ebe507433401213fb90e915b.jpg"
    # stream 支持流传输
    response = requests.get(url, stream=True)
    from contextlib import closing
    # 增加一个上下文
    with closing(requests.get(url, stream=True)) as response:
        # 打开文件
        with open('demo1.jpg', 'wb')as fd:
            # 每128写入一次
            for chunk in response.iter_content(128):
                fd.write(chunk)


if __name__ == '__main__':
    # download_image()
    download_image1()
