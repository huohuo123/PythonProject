from bs4 import BeautifulSoup
import requests

r = requests.get('http://www.baidu.com').content.decode('UTF-8')
soup = BeautifulSoup(r, 'html.parser')
# prettify格式美化一下
soup = soup.prettify()
print(soup)
