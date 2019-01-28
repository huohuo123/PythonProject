# 股票
# 候选数据网站的选择
# 选取原则：股票信息静态存在于HTML页面中，非js代码生成，没有Robots协议限制
# todo 不限制了？？得想办法，加一个模拟IP进行访问，看看后期学习是否有类似的处理  2019年01月19日15:42:50
import requests
import re
from bs4 import BeautifulSoup
import traceback


# 优化，直接赋值encoding
def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        print(r.text)
        return r.text
    except:
        traceback.print_exc()
        return ""


# 获取股票列表
def get_stock_list(lst, stock_url):
    html = getHTMLText(stock_url)
    soup = BeautifulSoup(html, "html.parser")
    # 找寻所有的a标签，通过正则表达式筛选股票列表信息
    a = soup.find_all('a')
    for i in a:
        try:
            href = i.attrs['href']
            # 符合要求的是以sz开头，或者hz开头，后边跟随6个数字的
            lst.append(re.findall(r"[s][hz]\d{6}", href))
        except:
            continue


# 获取股票信息
def get_stock_info(lst, stock_url, f_path):
    # 增加一个技术变量count，为增添的进度条服务
    count = 0
    for stock in lst:
        url = stock_url + stock + '.html'
        html = getHTMLText(url)
        try:
            if html == "":
                continue
            # info_dict所有个股信息
            info_dict = {}
            soup = BeautifulSoup(html, "html.parser")
            stock_info = soup.find('div', attrs={'class': 'stock-bets'})
            # 获取股票名称
            name = stock_info.find_all(attrs={'class': 'bets-name'})[0]
            info_dict.update({'股票名称': name.text.split()[0]})
            # 获取股票信息 k-v形式
            key_list = stock_info.find_all('dt')
            value_list = stock_info.find_all('dd')
            for i in range(len(key_list)):
                key = key_list[i].text
                val = value_list[i].text
                info_dict[key] = val
            with open(f_path, 'a', encoding='uef-8') as f:
                f.write(str(info_dict) + '\n')
                # 不换行的动态展示进度条
                count = count + 1
                print('\r当前速度:{:.2f}%'.format(count * 100 / len(lst)), end='')
        except:
            count = count + 1
            print('\r当前速度:{:.2f}%'.format(count * 100 / len(lst)), end='')
            # 利用traceback来捕获具体异常
            traceback.print_exc()
            continue


def main():
    stock_list_url = "http://quote.eastmoney.com/stocklist.html"
    stock_info_url = "https://gupiao.baidu.com/stock/"
    output_file = '../data/stockInfo.txt'
    s_list = []
    get_stock_list(s_list, stock_list_url)
    get_stock_info(s_list, stock_info_url, output_file)


if __name__ == '__main__':
    main()
