import datetime
import gzip
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import requests
import urllib.parse
import chardet
import hashlib
import ssl
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")

# def getOpener(head):
#     #deal with the Cookies
#     cj = http.cookiejar.CookieJar()
#     pro = urllib.request.HTTPCookieProcessor(cj)
#     opener = urllib.request.build_opener(pro)
#     header =[]
#     for key, value in head.items():
#         elem = (key, value)
#         header.append(elem)
#     opener.addheaders = header
#     return opener


header = {
    'Connection':'Keep-Alive',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
    'Host':'oa.2345.cn',
}
# 登录页
login_page = session.get('https://oa.2345.cn/login.php?forback=%2F', headers=header)
login_page = login_page.text
# requests库不用解压缩和解码
# login_page = gzip.decompress(login_page)
# charset = chardet.detect(login_page)
# login_page = login_page.decode(charset['encoding'], 'ignore')

# 验证码
image_url = 'https://oa.2345.cn/login/verificationCode'
image = session.get(image_url, headers=header)
imge_file = open('verify_image.png', 'wb')
imge_file.write(image.content)
imge_file.close()
# 打开图片，查看验证码
verify_code = input('输入验证码： ')
print(verify_code)




# 登录接口
login_url = 'https://oa.2345.cn/login.php'
post_dic = {
'r': '',
'forback': '',
'username': '孙迎世',
}
password = 'syh12sys'
fd = hashlib.md5()
fd.update(password.encode('utf-8'))
post_dic['password1'] = password
post_dic['password'] = fd.hexdigest()
post_dic['checkCode'] = verify_code
post_dic['exptime'] = 24 * 3600
data = session.post(login_url, data=post_dic, headers=header)
# print(data.text)

data = session.get('https://oa.2345.cn/', headers=header)
# print(data.text)
flag = re.search('[0-9]{10}', data.text, re.M|re.I).group()
data = session.get('https://oa.2345.cn/oatop.php?aaa=' + flag, headers=header)
# print(data.text)

header['Host'] = 'kehuduan.2345.com'
print(header)
print(session.cookies)
url = re.search('http://kehuduan[\s\S]*?sysid=100', data.text, re.M|re.I).group()
data = session.get(url, headers=header)
print(data)

data = session.get('http://kehuduan.2345.com/', headers=header)
print(data)

dump_url = 'http://kehuduan.2345.com/index.php?r=KingDump/index'
post_dic.clear()
post_dic = {
'ver' : '9.1.1.16851',
'process' : 'browser',
'os' : 0,
'memory_begin' :  '',
'memory_end' : '',
'extra_op' : 1,
'extra' : '',
'stack' : '',
}
today = datetime.date.today()
oneday = datetime.timedelta(days=1)
yesterday = today - oneday
post_dic['search_start_date'] = str(yesterday)
print(post_dic)
dump_page = session.post(dump_url, data=post_dic,  headers=header)
print(dump_page)
session.cookies.save()




