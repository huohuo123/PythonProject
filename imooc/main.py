# Requests库-请求方法
import json
import requests
from requests import exceptions

URL = 'https://api.github.com'


# 构架uri
def build_uri(endpoint):
    return '/'.join([URL, endpoint])


# 将结果更好的打印
def better_print(json_str):
    return json.dumps(json.loads(json_str), indent=4)


def request_method():
    # 获取github自己的个人信息
    response = requests.get(build_uri('users/huohuo123'))
    print(better_print(response.text))


# 您看过的最后一个用户的整数ID。
def params_request():
    response = requests.get(build_uri('users'), params={'since': 11})
    print(better_print(response.text))
    print(response.request.headers)
    print(response.url)


# 修改git_hub个人信息接口
# todo 暂定未访问通
def json_request():
    response = requests.patch(build_uri('user'), auth=('H15373272596@163.com', '051806jing'),
                              json={'name': 'huohuo666', 'email': '1458902339@qq.com'})
    print(better_print(response.text))
    print(response.request.headers)
    print(response.request.body)
    print(response.status_code)


# 超时请求
def timeout_request():
    try:
        response = requests.get(build_uri('user/emails'), timeout=10)
        # 要检查请求是否成功，请使用 r.raise_for_status() 或者检查 r.status_code 是否和你的期望相同。
        response.raise_for_status()
    # python3系列 timeout位置：requests.exceptions.Timeout
    except exceptions.Timeout as e:
        # 3系列直接打印e就可以了
        print(e)
    except exceptions.HTTPError as e:
        # 打印具体原因
        print(e)
    else:
        print(response.text)
        print(response.status_code)


# 底层一层实现
def hard_request():
    from requests import Request, Session
    s = Session()
    # 直接赋值（造假，哈哈）
    headers = {'User-Agent': 'fake1.3.4'}
    req = Request('GET', build_uri('user/emails'), auth=('huohuo123', '051806jing'), headers=headers)
    prepped = req.prepare()
    print(prepped.body)
    print(prepped.headers)

    # 发送请求
    resp = s.send(prepped, timeout=5)
    print(resp.status_code)
    print(resp.headers)


if __name__ == '__main__':
    # print("request_method:")
    # request_method()
    # print("params_request:")
    # params_request()
    # print("json_request:")
    # print(json_request())
    # timeout_request()
    hard_request()
