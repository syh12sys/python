from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import requests

def login(username, passord):

    browser = webdriver.Chrome(os.getcwd() + '/' + 'chromedriver')
    browser.get('https://oa.2345.cn/login.php?forback=%2F')

    submit_btn = browser.find_element_by_class_name('btn_login')
    name_btn = browser.find_element_by_name('username')
    pwd_btn = browser.find_element_by_name('password1')
    checd_code_btn = browser.find_element_by_name('checkCode')
    # 打开图片，查看验证码
    verify_code = input('输入验证码： ')

    name_btn.send_keys(username)
    pwd_btn.send_keys(passord)
    checd_code_btn.send_keys(verify_code)
    submit_btn.send_keys(Keys.ENTER)
    return browser

def set_sessions(browser):
    request = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    request.headers.update(headers)
    cookies = browser.get_cookies()
    for cookie in cookies:
        request.cookies.set(cookie['name'], cookie['value'])
    print(request.cookies)
    return request

request = set_sessions(login('孙迎世', 'syh12sys'))
data = request.get('http://kehuduan.2345.com/index.php?r=KingDump/index')
print(data.text)
