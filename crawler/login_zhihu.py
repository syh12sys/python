import gzip
import re
import urllib.request
import http.cookiejar
import urllib.parse

def ungzip(data):
    print('正在解压……')
    data=gzip.decompress(data)
    print('解压完毕！')
    return data

def getXSRF(data):
    cer = re.compile('name="_xsrf" value="(.*)"', flags = 0)
    strlist = cer.findall(data)
    return strlist[0]

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

url = 'https://www.zhihu.com/signin'
opener = getOpener(header)
op = opener.open(url)
data = op.read()
output = open('zhihu.html', 'w')
output.write(str(data.decode()))
output.close()


id = '13564518816'
password = 'SYS12sys'
postDict = {
        'email': id,
        'password': password,
        'rememberme': 'y'
}
postData = urllib.parse.urlencode(postDict).encode()
op=opener.open(url, postData)
data = op.read()
data = ungzip(data)

print(data.decode('utf-8'))
