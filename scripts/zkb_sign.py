# -*- coding: utf-8 -*
'''
new Env('新签到');
'''


import os
import datetime
import time
from notify import send  # 导入青龙消息通知模块
import requests
from bs4 import BeautifulSoup
import html
import urllib3
import re
urllib3.disable_warnings()

cookie = os.environ['zkb_COOKIE']
url1 = 'https://v1.xianbao.net/member.php?mod=logging&action=login'
url2 = 'https://v1.xianbao.net/plugin.php?id=dsu_paulsign%3Asign&operation=qiandao&infloat=0&inajax=0'
#url3 = 'https://v1.xianbao.net/plugin.php?id=dsu_paulsign:sign&operation=qiandao'
url3 = 'https://v1.xianbao.net/home.php?mod=spacecp&ac=credit&op=base'
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": cookie,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
}
session = requests.session()
#r = requests.get(url1, headers=headers, verify=False, allow_redirects=False, stream=True)
r = session.get(url1, headers=headers, verify=False, stream=True)
s_cookie = r.headers['Set-Cookie']
#print(s_cookie)
cookie = cookie + s_cookie
headers['Cookie'] = cookie
r_html = r.text
#r_html = BeautifulSoup(r.text, "html.parser")

#print(r_html)
print("----------------------fff")
#formhash0 = r_html.find("action=logout")
#formhash = r_html[formhash0+18:formhash0+35]
formhash=re.findall(r'formhash=(.*)">退出', r_html)
 
#formhash = re.findall(r'(https:[^\s]*logout))',r_html)
#formhash = re.findall('<a href="member.php?mod=logging&amp;action=logout&amp;formhash=', r_html, re.S)
print(formhash)
print('----------------------lll')

data = {    
    'formhash': f'{formhash}'
   }
dtime = int(time.time())
url2 = url2 +"&time=" + str(dtime)
 
r = session.post(url2, headers=headers, data=data, verify=False)
s_cookie = r.headers['Set-Cookie']

#print(s_cookie)
cookie = cookie + s_cookie
headers['Cookie'] = cookie
data = {    
    'formhash': f'{formhash}'
   }
print('----------------------2f')
print(formhash)
 
#r = requests.get(url3, headers=headers, verify=False, data=data, allow_redirects=False, stream=True)
r = session.get(url3, headers=headers, data=data, verify=False)
#r_data = BeautifulSoup(r.text, "html.parser")
r_html = r.text
#print(r_html)
print("*******************")
jx_data = re.findall('wbs.png', r_html)
#jx_data = r_data.find("div", id="messagetext").find("p").text
print(jx_data)

#if "您需要先登录才能继续本操作" in jx_data:
 #   sign_msg="❌Cookie 失效"
#elif "明天" in jx_data:
   # sign_msg="⭐签到成功"
#elif "不是进行中的任务" in jx_data:
  #  sign_msg="💔今日已签到"
#else:
    #sign_msg="⚡签到失败"

#send('吾爱破解签到', sign_msg+'\n\n本通知 By HY-吾爱破解\n通知时间:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

