import re


# ip地址正则表达式，IP地址分四段，每段0-255
# 0-99:[1-9]>]d
# 100-199:1\d{2}
# 200-249:2[0-4]\d
# 250-255:25[0-5]
def IPmain():
    ip = '192.168.1.1'
    trueIp = re.search(r'(([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])\.){3}([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])', ip)
    print(trueIp)


# re的search方法。匹配成功10081邮政编码信息
def searchMain():
    searchR = re.search(r'[1-9]\d{5}', 'BIT 100081')
    if searchR:
        print(searchR.group(0))


# re的match方法
def matchMain():
    match = re.match(r'[1-9]\d{5}', '100081 BIT')
    if match:
        print(match.group(0))


# re的findall方法
def findallMain():
    ls = re.findall(r'[1-9]\d{5}', 'BIT100081 TSU100084')
    print(ls)


def splitMain():
    # 除去匹配成功的部分
    ls = re.split(r'[1-9]\d{5}', 'BIT100081 TSU100084')
    # maxsplit只分割第一个匹配成功的部分
    ls2 = re.split(r'[1-9]\d{5}', 'BIT100081 TSU100084', maxsplit=1)
    print(ls)
    print(ls2)


# 和findAll的区别就是对其匹配成功的元素都单独处理
def finditerMain():
    # 除去匹配成功的部分
    for m in re.finditer(r'[1-9]\d{5}', 'BIT100081 TSU100084'):
        if m:
            print(m.group(0))


def subMain():
    # 除去匹配成功的部分
    ls = re.sub(r'[1-9]\d{5}', ':zipcode', 'BIT100081 TSU100084')
    print(ls)


if __name__ == '__main__':
    # IPmain()
    searchMain()
    matchMain()
    findallMain()
    splitMain()
    finditerMain()
    subMain()
