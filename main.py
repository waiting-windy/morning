from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], weather['city'], math.floor(weather['low']), math.floor(weather['high'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_color():
  # 获取随机颜色
  get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
  color_list = get_colors(100)
  return random.choice(color_list)



client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, city,min_temperature ,max_temperature= get_weather()
data = {
  "date": {
      "value": "{}".format(today),
      "color": get_color()
  },
  "weather":{"value":wea, "color":get_color()},
  "city":{"value":city, "color":get_color()},
  "min_temperature":{"value":min_temperature, "color":get_color()},
  "max_temperature":{"value":max_temperature, "color":get_color()},
  "love_days":{"value":get_count(), "color":get_color()},
  "birthday_left":{"value":get_birthday(), "color":get_color()},
  "words":{"value":get_words(), "color":get_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
