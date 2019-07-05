from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import datetime
import requests
import time
import re


def login(username, passord):

    browser = webdriver.Firefox()
    browser.implicitly_wait(10)
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

    browser.switch_to.frame('topFrame')
    client_service_btn = browser.find_element_by_id('100')
    client_service_btn.send_keys(Keys.ENTER)
    time.sleep(3)

    for handle in browser.window_handles:
        browser.switch_to.window(handle)
        if browser.title == '客户端后台':
            break

    browser.switch_to.frame('pageLeft')
    dump_btns = browser.find_elements_by_class_name('close_up')
    dump_btn = dump_btns[len(dump_btns) - 1]
    dump_btn.click()

    aa_btn = browser.find_element_by_link_text('浏览器Dump分析管理')
    aa_btn.click()
    time.sleep(3)

    # browser.switch_to.window(browser.window_handles[2])
    # # browser.find_element_by_id('search_start_date')
    # version = Select(browser.find_element_by_id('ver'))
    # version.select_by_value('9.1.1.16851')
    # process = Select(browser.find_element_by_id('process'))
    # process.select_by_value('browser')
    # browser.find_elements_by_class_name('searchBtn')[1].send_keys(Keys.ENTER)
    # time.sleep(10)
    #
    # table = browser.find_element_by_class_name('data_table')
    # table_rows = table.find_elements(By.TAG_NAME, 'tr')
    # for row in table_rows:
    #     print(row.text)
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
    return request

request = set_sessions(login('孙迎世', 'syh12sys'))

dic_mac = {}
day_interval = 1
while day_interval > 0:
    one_day_mac_dic = {}

    target_day = str(datetime.date.today() - datetime.timedelta(days=day_interval))

    dump_url = 'http://kehuduan.2345.com/index.php?r=KingDump/index' + '&search_start_date=' + target_day + \
               '&ver=9.2.0.17091&page=1'
    data = request.get(dump_url)

    data = re.findall(r'<tr>[\s]*<td>[1-9][0-9]?</td>[\s\S]*?</tr>', data.text, re.M | re.I)
    print(data[0])
    md5 = re.search(r'[a-f0-9]{32}', data[0], re.M|re.I).group()
    print(md5)

    page_index = 1
    while True:
        detail_url = 'http://kehuduan.2345.com/index.php?r=KingDump/detail&md5=' + md5 + \
                     '&ver=9.2.0.17091&date=' + target_day + '&page=' + str(page_index)
        page_data = request.get(detail_url)
        items = re.findall(r'<tr>[\s]*<td>[1-9][0-9]?</td>[\s\S]*?</tr>', page_data.text, re.M | re.I)
        for item in items:
            mac = re.search(r'[0-9a-fA-F]{2}(-[0-9a-fA-F]{2}){5}', item, re.M | re.I).group()
            if mac in one_day_mac_dic:
                one_day_mac_dic[mac] = one_day_mac_dic[mac] + 1
            else:
                one_day_mac_dic[mac] = 1

        # 下一页
        page_num = re.search('<em>[0-9]{2,4}</em>', page_data.text, re.M | re.I).group()
        page_num = re.search('[0-9]{2,4}', page_num, re.M | re.I).group()
        page_num = int(page_num) // 50 + 1
        page_index = page_index + 1
        if page_index > page_num:
            break

    dic_mac[target_day] = one_day_mac_dic
    day_interval = day_interval - 1

for day, mac in dic_mac.items():
    print(day, len(mac), mac)

set_12 = set(dic_mac['2018-01-12'].keys())
set_13 = set(dic_mac['2018-01-13'].keys())
set_14 = set(dic_mac['2018-01-14'].keys())
set_15 = set(dic_mac['2018-01-15'].keys())
print(set_15.intersection(set_14).intersection(set_13).intersection(set_12))