# 通过requests来响应http的一些基本操作命令
import requests

URL_IP = 'http://httpbin.org/ip'
URL_GET = 'http://httpbin.org/get'


def use_imple_requests():
    #  访问url的方法
    response = requests.get(URL_IP)
    print(">>> Response Headers:")
    # info() 打印headers的方法
    print(response.headers)
    print(">>> Response Body:")
    print(response.text)


def use_params_requests():
    # 在python3中 urlencode在urllib.parse下
    # 构造请求参数
    params = {'param1': 'hello', 'param2': 'world'}
    # 发送请求
    response = requests.get(URL_GET, params=params)
    # 处理响应
    print(">>> Response Headers:")
    # info() 打印headers的方法
    print(response.headers)
    print(">>> State code:")
    print(response.status_code)
    print(">>> State reason:")
    print(response.reason)
    print(">>> Response Body:")
    print(response.json())


if __name__ == '__main__':
    print(">>> use_imple_requests:")
    use_imple_requests()
    print(">>> use_params_urllib2:")
    use_params_requests()
