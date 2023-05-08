import requests, re, json, urllib3,os

cookie = os.environ["zkb_COOKIE"].split('&')


# 企业微信推送参数
corpid = ''
agentid = ''
corpsecret = ''
touser = ''
# 推送加 token
plustoken = os.environ["PUSH_PLUS_TOKEN"]

def Push(contents):
    # 微信推送
    if all([corpid, agentid, corpsecret, touser]):
        token = \
        requests.get(f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}').json()[
            'access_token']
        json = {"touser": touser, "msgtype": "text", "agentid": agentid, "text": {"content": "新赚吧签到\n" + contents}}
        resp = requests.post(f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}", json=json)
        print('微信推送成功' if resp.json()['errmsg'] == 'ok' else '微信推送失败')

    if plustoken:
        headers = {'Content-Type': 'application/json'}
        json = {"token": plustoken, 'title': '新赚吧签到', 'content': contents.replace('\n', '<br>'), "template": "json"}
        resp = requests.post(f'http://www.pushplus.plus/send', json=json, headers=headers).json()
        print('push+推送成功' if resp['code'] == 200 else 'push+推送失败')

urllib3.disable_warnings()
for i in range(len(cookie)):
    print('开始第'+ str(i+1) +'个帐号签到'+'\n'+'***********************')
    s = requests.session()
    f_url = 'https://v1.xianbao.net/'  # 获取formhash
    url = 'https://v1.xianbao.net/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=0&inajax=0'
    url1 = 'https://v1.xianbao.net/plugin.php?id=dsu_paulsign:sign'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'cookie': f'{cookie[i]}',
        'Host': 'v1.xianbao.net',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://v1.xianbao.net'
    }
    f_html = s.get(url=f_url, headers=headers, verify=False,allow_redirects=False).text
    formhash = str(re.findall('name="formhash" value="(.*?)" />', f_html, re.S)).replace('[', '').replace('\'', '').replace(']', '')
    data = {
    'formhash': f'{formhash}'
    }
    html = requests.post(url=url, headers=headers, data=data, verify=False).text
    result = re.findall('<div class="c">\r\n(.*?)<a href="plugin.php?', html, re.S)
    message = "".join(result)
    html1 = requests.get(url=url1, headers=headers, data=data, verify=False).text
    ljqd = re.findall('您累计已签到.*? <b>(.*?)</b>', html1, re.S)
    bylj = re.findall('您本月已累计签到.*?<b>(.*?)</b>', html1, re.S)
    scqdsj = re.findall('您上次签到时间.*?>(.*?)</font>', html1, re.S)
    zgg = re.findall('您目前获得的总奖励为:果果 .*?b>(.*?)</b>', html1, re.S)
    scgg = re.findall('上次获得的奖励为:果果 .*?b>(.*?)</b>', html1, re.S)
    nickName = re.findall('<font color="#FF0000"><b>(.*?)</b>.* 您累计已签到:', html1, re.S)
    message = '亲爱的' + "".join(nickName) + '\n您累计已签到：' + "".join(ljqd)  + '天，' + '本月已签到：' + "".join(bylj)  + '天\n' + '您上次签到时间：' + "".join(scqdsj) + '\n您目前获得的总奖励为：' + "".join(zgg) + '果果，上次获得的奖励为' + "".join(scgg)+ '果果.\n'
    url_2 = 'https://v1.xianbao.net/app.php?p=sign&action=todaysign'
    html_2 = requests.get(url=url_2, headers=headers, verify=False).text
    info = '签到信息：' + "".join(re.findall('messagetext[\s\S]*<p>(.+?)<[<scriot\s\S]*<\/p>[\w\W]<', html_2, re.S)) 
    sign_info = message + '\n' + info
    print(sign_info)
    Push(contents=sign_info)
