import re

'''
将以下字符串中所有的url匹配出来
'''

str = '''1458902339@qq.com
    h234543@163.com
    http://www.abc.com
    https://www.sae.com
    ftp://www.nnn.com
    ftps://www.jksad.net'''
pattern = re.compile('[a-z]+:\/\/www(\.\w+)(\.\w+){1,2}')
str1 = pattern.finditer(str)
for i in str1:
    print(i.group())

'''
判断以下字符，是否全是中文（中文正则模式 [\u4E00-\u9FA5]）
'''

str = '北京s北京市'
# 开头是中文字符开头，结尾是中文字符结尾
pattern = re.compile('^[\u4E00-\u9FA5]+$')
if pattern.findall(str):
    print("全是中文字符")
else:
    print("非全是中文字符")

'''
写出一个正则表达式，过滤网页上的所有JS脚本（即把script标记及其内容都去掉）
'''

script = "以下内容不显示：<script  language='javascript'>alert('cc');</script><p>fdggsgesfg</p><script>alert('dd');</script>"
pattern = re.compile('<script.*?</script>')
# 把匹配出的script信息去除掉，则符合要求
print(pattern.sub('', script))

'''
通过正则表达式把img标签中的src路径匹配出来
'''

str = '''
    <img name="photo" src="../public/img/img1.png" />
    <img name="news" src='xxx.jpg' title='news' />
    '''
pattern = re.compile('src=[\'\"](.*?)[\'\"]')
str2 = pattern.finditer(str)
for i in str2:
    # 只打印出src中间需要的内容
    print(i.group(1))

'''
手机号中间四位用*代替
'''

phone = '18211180533'
pattern = re.compile('^(1[3578]\d)(\d{4})(\d{4})$')
print(pattern.sub(r'\1****\3', phone))
