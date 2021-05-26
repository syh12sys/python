# https://github.com/twilio/twilio-python/blob/master/examples/basic_usage.py

from twilio.rest import Client
import chardet
import time
from datetime import datetime
import urllib.request

#紫光股份，二三四五, 宋城演艺，东阳光科
stocks = ['002195', '603368', '600673']
#触发短信的涨跌幅度
increase_percent = 0.5
# 满足同一个条件，发送短信的次数
# 例如一个股票在2%左右反复震荡，会造成发送很多次短信
send_sms_history = {}
for stock in stocks:
    send_sms_history[stock] = (0, 0)

# 记录上次的涨跌幅，用来表示股票是变化到阈值
previous = [0.0] * len(stocks)

# 轮询网站时间间隔
loop_interval_sec = 30

def write_log(content):
  if content is None or len(content) is 0:
    return

  log = open(time.strftime('%Y-%m-%d', time.localtime()) + '.log', 'a')
  message = time.strftime('%H-%M-%S', time.localtime()) + ': ' + content + '\n'
  log.write(message)
  log.close()

def send_message(msg):
  if msg is None or len(msg) is 0:
    return

  account_id = 'ACe11803c1cd4667f599aba733f8b69e87'
  auth_token = '2094d205a8493100d5de38c440bcf39b'
  from_phone = '17185718320'
  to_phone = '+8613564518816'
  client = Client(account_id, auth_token)
  try:
    client.messages.create(to=to_phone, from_=from_phone, body=msg)
  except:
    write_log('发送短信: ' + msg + ' 失败')

def crawle_raw_data():
  url = 'http://hq.sinajs.cn/rn=%d&list=' % (int(time.time() * 1000))
  for index in range(len(stocks)):
    if stocks[index][0] == '0' or stocks[index][0] == '3':
      url += 's_sz' + stocks[index] + ','
    elif stocks[index][0] == '6':
      url += 's_sh' + stocks[index] + ','
  # 删除最后一个逗号
  if url[len(url) - 1] == ',':
    url = url[0 : len(url) - 1]
  # print(url)
  data = ''
  try:
    op = urllib.request.urlopen(url)
    data = op.read()
    charset = chardet.detect(data)
    data = data.decode(charset['encoding'], 'ignore')
  except:
    write_log(url + ' 失败')
  return data

def manipulation_data(raw_data):
  first = raw_data.split(';')
  second = []
  for item in first:
    equal_pos = item.find('=')
    if equal_pos == -1:
      continue
    second.append(item[equal_pos + 2 : len(item) - 1])

  third = []
  for item in second:
    split_item = item.split(',')
    if len(split_item) != 6:
      continue
    third.append((split_item[0], split_item[1], split_item[3]))

  return third

def SendSMSAccordingToRule():
  raw_data = crawle_raw_data()
  # print(raw_data)
  data = manipulation_data(raw_data)
  # print(data)
  # 涨跌幅超过2%，发短信提醒
  message = ''
  for index in range(len(data)):
    up_or_down_percent = float(data[index][2])
    if previous[index] < increase_percent and up_or_down_percent >= increase_percent:
        message += ', '.join(data[index]) + ';'
    elif previous[index] > -increase_percent and up_or_down_percent <= -increase_percent:
        message += ', '.join(data[index]) + ';'
    # else:
    #     localtime = time.localtime(time.time())
    #     #整点和半点发送通知
    #     if localtime.tm_hour in (9, 10, 11, 13, 14, 15) and localtime.tm_min in (0, 30) and localtime.tm_sec <= loop_interval_sec:
    #         message += ', '.join(data[index]) + ';'

    previous[index] = up_or_down_percent

  if message != '':
    send_message(message)

while True:
    #date = datetime.now().date()
    #time_now = datetime.now().time()
    #if date.isoweekday() in (6, 7):
    #    write_log('周六周日退出')
    #    break
    #elif time_now < time_now.replace(hour=9, second=30):
    #    time.sleep(loop_interval_sec)
    #    continue
    #elif time_now > time_now.replace(hour=15, second=0):
    #    write_log('大于3点退出')
    #    break

    SendSMSAccordingToRule()
    time.sleep(loop_interval_sec)
