import re

'''
findall
'''
# ['abc', 'def']  匹配任意长度的英文字符
pattern1 = re.compile('[a-zA-z]+')
# ['abc', 'def']  中括号代表一个区间，若去掉则成为了实际值
pattern2 = re.compile('[a-z][a-z][a-z]')
# [('a', 'c'), ('d', 'f')]
pattern3 = re.compile('([a-z])[a-z]([a-z])')
str1 = '123abc456def789'
result1 = pattern1.findall(str1)
result2 = pattern2.findall(str1)
result3 = pattern3.findall(str1)

print(result1)
print(result2)
print(result3)
# 通过以上demo,可以发现findall遇到分组的时候只返回分组匹配的结果,圆括号代表分组

'''
finditer
'''

# [('a', 'c'), ('d', 'f')]
pattern = re.compile('([a-z])[a-z]([a-z])')
str1 = '123abc456def789'
result3 = pattern3.finditer(str1)
# 迭代器返回,用finditer返回结果，不仅仅局限于分组匹配的结果
print(result3)
# 遍历，通过group()返回完整的匹配结果
for i in result3:
    print(i.group())
    # 返回第一个分组匹配的结果
    print(i.group(1))
    # 返回第二个分组匹配的结果
    print(i.group(2))
# 通过以上demo，finditer可以返回完整的正则匹配结果以及分组的匹配结果

'''
split分割
'''

str1 = 'one,two,three,four'
str2 = 'one1two2three3four'
str3 = 'one.two.three.four'
# \W+  非单词字符，逗号及符合条件
pattern1 = re.split('\W+', str1)
# \d+ 数字
pattern2 = re.split('\d+', str2)
pattern3 = re.split('\W+', str3)
print(pattern1)
print(pattern2)
print(pattern3)

'''
sub 使用re替换string中每一个匹配的子串后返回替换后的字符串
'''
pattern = re.compile('\d')
str1 = 'one1two2three3four'
# 把数字编程了横岗
print(pattern.sub('-', str1))
# 返回匹配结果以及替换数
print(re.subn('\d', '-', str1))

'''
引用分组
'''

strs = 'hello 123,world 321'
pattern = re.compile('(\w+) (\d+)')
for i in pattern.finditer(strs):
    # group(0)和group()一样的效果，都是显示全部
    print(i.group(0))

# 取得分组，更换前后显示顺序  注意：前提是re.compile的时候需要用括号括起来，才能是分组状态
# 空格是表示用空格分割；***则表示用***分割
print(pattern.sub(r'\2***\1', strs))

'''
贪婪与非贪婪
贪婪：在整个表达式匹配成功的前提下，尽可能多的匹配，只要开头结尾符合要求集合
非贪婪：在整个表达式匹配成功的前提下，尽可能少的匹配
'''

str1 = 'aaa<p>hello</p>bbb<p>world</p>ccc'
# 把所有符合要求的用<p> </p>包围的都找出来了
pattern = re.compile('<p>\w+</p>')
# .匹配任意字符*代表0到无限次（一种贪婪模式）
pattern1 = re.compile('<p>.*</p>')
# 加上问号，变成一种非贪婪的模式,尽可能少的匹配，遇到结束的标签即结束
pattern2 = re.compile('<p>.*?</p>')
print(pattern.findall(str1))
print(pattern1.findall(str1))
print(pattern2.findall(str1))

'''
匹配中文字符
'''
str1='你好，hello,帅哥'
# 只匹配出中文显示
pattern=re.compile('[\u4e00-\u9fa5]+')
print(pattern.findall(str1))