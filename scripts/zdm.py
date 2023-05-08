import requests, demjson ,re,time,json,os

# 推送不加了感觉没啥用
# 把值得买的cookie放入下面的单引号里面  有几个帐号就弄几个（默认设置了3个 根据自己情况改）
#cookie_list = ['']
# 活动id
active_id = ['ljX8qVlEA7','daY8jaOgOo']
cookie_list=os.environ["SMZDM_COOKIE"].split('&') 
#cookie_list = ['smzdm_user_source=036A6C5C26A021E347B68DCD5389EB4E; userId=sina_vgir4|8657407757; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%228657407757%22%2C%22first_id%22%3A%2217b095a41dd4f4-0a7fa340d33c6d-7e687969-1049088-17b095a41dfae1%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_landing_page%22%3A%22https%3A%2F%2Fwww.smzdm.com%2F%22%7D%2C%22%24device_id%22%3A%2217b095a41dd4f4-0a7fa340d33c6d-7e687969-1049088-17b095a41dfae1%22%7D; shequ_pc_sug=b; _ga=GA1.2.2117020901.1627949517; _ga_09SRZM2FDD=GS1.1.1629107283.12.1.1629107403.0; r_sort_type=time; device_id=21307064331650585765198755d3905d0de7ca188fa26961af36ead29c; __ckguid=3C36q46kUONjyL7tGwAngG; homepage_sug=c; __jsluid_s=9d0d8479321527ab13118bf8f68ca651; sess=BA-g9bdUDngW0tu7ZFZeyC7S8Ut90Qu4CQx5oyJgP0G0yvFNjrpOX%2Bj5ZwMFcQG3oWQQdXD%2BKBr9VXtnVKHpOiwjC%2Fee%2FDGQXbuESMFQByGEDGrCnYTHbsUvFsD; user=sina_vgir4%7C8657407757; smzdm_id=8657407757; Hm_lvt_9b7ac3d38f30fe89ff0b8a0546904e58=1670167355; footer_floating_layer=0; ad_date=16; ad_json_feed=%7B%7D; ss_ab=ss35; ssmx_ab=mxss92; s_his=%E5%85%85%E6%B0%94%E6%B3%B5%2C%E5%85%83%E8%90%9D%E5%8D%9C; _zdmA.vid=*; bannerCounter=%5B%7B%22number%22%3A0%2C%22surplus%22%3A1%7D%2C%7B%22number%22%3A0%2C%22surplus%22%3A1%7D%2C%7B%22number%22%3A0%2C%22surplus%22%3A1%7D%2C%7B%22number%22%3A0%2C%22surplus%22%3A1%7D%2C%7B%22number%22%3A0%2C%22surplus%22%3A1%7D%2C%7B%22number%22%3A0%2C%22surplus%22%3A1%7D%5D; _zdmA.uid=ZDMA.oz0tdnUVg.1671176205.2419200; _zdmA.time=1671176206258.0.https%3A%2F%2Fwww.smzdm.com%2F',]

 

for i in range(len(cookie_list)):
    for a in range(len(active_id)):
        projectList = []
        url = f'https://zhiyou.smzdm.com/user/lottery/jsonp_draw?active_id={active_id[a]}'
        rewardurl= f'https://zhiyou.smzdm.com/user/lottery/jsonp_get_active_info?active_id={active_id[a]}'
        infourl = 'https://zhiyou.smzdm.com/user/'
        headers = {
            'Host': 'zhiyou.smzdm.com',
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Cookie': cookie_list[i],
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148/smzdm 10.4.6 rv:130.1 (iPhone 13; iOS 15.6; zh_CN)/iphone_smzdmapp/10.4.6/wkwebview/jsbv_1.0.0',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Referer': 'https://m.smzdm.com/',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        response = requests.post(url=url, headers=headers).text
        response_info = requests.get(url=infourl, headers=headers).text
        response_reward = requests.get(url=rewardurl, headers=headers)
        result_reward = json.loads(response_reward.text)
        name = str(re.findall('<a href="https://zhiyou.smzdm.com/user"> (.*?) </a>', str(response_info), re.S)).replace('[','').replace(']','').replace('\'','')
        level = str(re.findall('<img src="https://res.smzdm.com/h5/h5_user/dist/assets/level/(.*?).png\?v=1">', str(response_info), re.S)).replace('[','').replace(']','').replace('\'','')
        gold = str(re.findall('<div class="assets-part assets-gold">\n                    (.*?)</span>', str(response_info), re.S)).replace('[','').replace(']','').replace('\'’','').replace('<span class="assets-part-element assets-num">','').replace('\'','')
        silver = str(re.findall('<div class="assets-part assets-prestige">\n                    (.*?)</span>', str(response_info), re.S)).replace('[','').replace(']','').replace('\'’','').replace('<span class="assets-part-element assets-num">','').replace('\'','')
        data = demjson.decode(str(response), encoding='utf-8')
        print('帐号' + str(i + 1)+ ' VIP'+ level + ' ' + name + ' ' + data['error_msg']+'  剩余碎银 '+silver +'  剩余金币 '+ gold)
        time.sleep(2)
