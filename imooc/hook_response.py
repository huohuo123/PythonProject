# 事件钩子
import requests


def main():
    requests.get('https://api.github.com', hooks=dict(response=get_key_info))


def get_key_info(response, *args, **kwargs):
    # 回调函数
    print(response.headers['Content-Type'])


if __name__ == '__main__':
    main()
