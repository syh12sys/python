#! /usr/bin/env python
# coding:utf-8

import urllib
import urllib.request
import http.cookiejar

#####################################################
# 登录人人
loginurl = 'http://172.16.0.17:8080/2345explorer/login'


class Login(object):
    def __init__(self):
        self.name = ''
        self.passwprd = ''

        self.cj = http.cookiejar.LWPCookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
        urllib.request.install_opener(self.opener)

    def setLoginInfo(self, username, password):
        '''''设置用户登录信息'''
        self.name = username
        self.pwd = password

    def login(self):
        '''''登录网站'''
        loginparams = {'user': self.name, 'password': self.pwd, '__FORM_TOKEN':'414bb9165c56b8d4a914cabf', 'referer':'http://172.16.0.17:8080/2345explorer'}
        data = urllib.parse.urlencode(loginparams).encode('utf-8')
        print(data)
        req = urllib.request.Request(loginurl)
        response = urllib.request.urlopen(req, data)
        print(response.getcode())
        # self.operate = self.opener.open(req)
        page = response.read()
        print(page)

    def is_login(self):
        url = 'http://172.16.0.17:8080/2345explorer/admin'


if __name__ == '__main__':
    userlogin = Login()
    username = 'sunys'
    password = 'sunys'
    userlogin.setLoginInfo(username, password)
    userlogin.login()
