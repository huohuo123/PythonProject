import requests
import base64

BASE_URL = 'https://api.github.com'


def construct_url(end_point):
    return '/'.join([BASE_URL, end_point])


# 基本认证
def base_auth():
    response = requests.get(construct_url('user'), auth=('huohuo123', '051806jing'))
    print(response.text)
    print(response.request.headers)
    # 解码
    print(base64.b64decode("aHVvaHVvMTIzOjA1MTgwNmppbmc="))


# 基本的oauth认证
# 加headers可以正常获取信息，若把headers去掉，则会报401，需要认证
def base_oauth():
    # 自己github的token
    headers = {'Authorization': 'token 51fc4760f4585c798ed288a95338f0e310ab6129'}
    # response = requests.get(construct_url('user/emails'))
    response = requests.get(construct_url('user/emails'), headers=headers)
    print(response.request.headers)
    print(response.text)
    print(response.status_code)


# requests提供了方法
from requests.auth import AuthBase


class GithubAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = ' '.join(['token', self.token])
        return r


def oauth_advanced():
    auth = GithubAuth('51fc4760f4585c798ed288a95338f0e310ab6129')
    response = requests.get(construct_url('user/emails'), auth=auth)
    print(response.text)


if __name__ == '__main__':
    # base_auth()
    # base_oauth()
    oauth_advanced()
