import gzip
import urllib.request
import http.cookiejar
import urllib.parse
import chardet
import hashlib

def getOpener(head):
    #deal with the Cookies
    cj = http.cookiejar.CookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)
    header =[]
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener


header = {
    'Connection':'Keep-Alive',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
    'Host':'wwww.zhihu.com',
}
# 登录页
url = 'https://oa.2345.cn/login.php?forback=%2F'
opener = getOpener(header)
op = opener.open(url)
data = op.read()
data = gzip.decompress(data)
charset = chardet.detect(data)
data = data.decode(charset['encoding'], 'ignore')

# 验证码
image_url = 'https://oa.2345.cn/login/verificationCode'
op = opener.open(image_url)
verify_image = op.read()
verify_image = gzip.decompress(verify_image)
imge_file = open('verify_image.png', 'wb')
imge_file.write(verify_image)
imge_file.close()
# 打开图片，查看验证码
verify_code = input('输入验证码： ')
print(verify_code)

# 登录接口
post_dic = {
'r': '',
'forback': '',
'username': 'sunys',
}
password = 'syh12sys'
fd = hashlib.md5()
fd.update(password.encode('utf-8'))
post_dic['password1'] = password
post_dic['password'] = fd.hexdigest()
post_dic['checkCode'] = verify_code
post_dic['exptime'] = 24 * 3600
print(post_dic)

postData = urllib.parse.urlencode(post_dic).encode()
op=opener.open(url, postData)
data = op.read()
data = gzip.decompress(data)
charset = chardet.detect(data)
data = data.decode(charset['encoding'], 'ignore')

print(data)


