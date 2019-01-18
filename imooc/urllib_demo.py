# 通过urllib和urllib2来响应http的一些基本操作命令
import urllib
# urllib.request代替urllib2，在python3系列中
import urllib.request

URL_IP = 'http://httpbin.org/ip'
URL_GET = 'http://httpbin.org/get'


def use_imple_urllib2():
    #  访问url的方法
    response = urllib.request.urlopen(URL_IP)
    print(">>> Response Headers:")
    # info() 打印headers的方法
    print(response.info())
    print(">>> Response Body:")
    txt_list = []
    for line in response.readlines():
        line = line.strip()
        txt_list.append(line)
    print(txt_list)


def use_params_urllib2():
    # 在python3中 urlencode在urllib.parse下
    # 构造请求参数
    params = urllib.parse.urlencode({'param1': 'hello', 'param2': 'world'})
    print("Request params:")
    print(params)
    # 发送请求
    response = urllib.request.urlopen('?'.join([URL_GET, '%s']) % params)
    # 处理响应
    print(">>> Response Headers:")
    # info() 打印headers的方法
    print(response.info())
    print(">>> State code:")
    print(response.getcode())
    print(">>> Response Body:")
    txt_list = []
    for line in response.readlines():
        line = line.strip()
        txt_list.append(line)
    print(txt_list)


if __name__ == '__main__':
    print(">>> use_imple_urllib2:")
    use_imple_urllib2()
    print(">>> use_params_urllib2:")
    use_params_urllib2()
