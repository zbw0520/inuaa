# -*- coding: UTF-8 -*-

import requests
import time
import json
import re
from send_mail import send_mail

#---------------------------------------------#
# your id and you password
id = 'xxxxxxxxx'
password = 'xxxxxxxxx'

# 修改为你的邮箱账号、密码、smtp服务器地址
# 建议使用QQ邮箱发送，163邮箱给QQ邮箱发送会发不出去
mail_username = 'xxxxxxxxx@qq.com'
mail_password = 'xxxxxxxxxxxxxxxxxx'
mail_host = 'smtp.qq.com'

# 收件人地址
receiver = 'xxxxxxxxx@qq.com'
#----------------------------------------------#

# 如果发包过快会造成502，如果给多个同学打卡请注意一下请求速度
try_times = 2

# 抓的包直接复制的，打卡其实只要cookie和data就好了
headers = {
    'Host': 'm.nuaa.edu.cn',
    'Connection': 'close',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Sec-Fetch-Dest': 'empty',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://m.nuaa.edu.cn',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://m.nuaa.edu.cn/uc/wap/login/check',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': ''
}


# 定位的id也会变，不用管了 created时间戳，直接抓的包
post_data = 'sfzhux=0&zhuxdz=&szgj=&szcs=&szgjcs=&sfjwfh=0&sfyjsjwfh=0&sfjcjwfh=0&sflznjcjwfh=0&sflqjkm=0&jkmys=0&sfjtgfxdq=0&geo_api_info=%7B%22type%22%3A%22complete%22%2C%22info%22%3A%22SUCCESS%22%2C%22status%22%3A1%2C%22XDa%22%3A%22jsonp_951333_%22%2C%22position%22%3A%7B%22Q%22%3A31.94271%2C%22R%22%3A118.78832%2C%22lng%22%3A118.78832%2C%22lat%22%3A31.94271%7D%2C%22message%22%3A%22Get+ipLocation+success.Get+address+success.%22%2C%22location_type%22%3A%22ip%22%2C%22accuracy%22%3Anull%2C%22isConverted%22%3Atrue%2C%22addressComponent%22%3A%7B%22citycode%22%3A%22025%22%2C%22adcode%22%3A%22320115%22%2C%22businessAreas%22%3A%5B%7B%22name%22%3A%22%E5%BC%80%E5%8F%91%E5%8C%BA%22%2C%22id%22%3A%22320115%22%2C%22location%22%3A%7B%22Q%22%3A31.925973%2C%22R%22%3A118.80980399999999%2C%22lng%22%3A118.809804%2C%22lat%22%3A31.925973%7D%7D%5D%2C%22neighborhoodType%22%3A%22%22%2C%22neighborhood%22%3A%22%22%2C%22building%22%3A%22%22%2C%22buildingType%22%3A%22%22%2C%22street%22%3A%22%E8%83%9C%E5%A4%AA%E8%B7%AF%22%2C%22streetNumber%22%3A%22162%E5%8F%B7%22%2C%22country%22%3A%22%E4%B8%AD%E5%9B%BD%22%2C%22province%22%3A%22%E6%B1%9F%E8%8B%8F%E7%9C%81%22%2C%22city%22%3A%22%E5%8D%97%E4%BA%AC%E5%B8%82%22%2C%22district%22%3A%22%E6%B1%9F%E5%AE%81%E5%8C%BA%22%2C%22township%22%3A%22%E7%A7%A3%E9%99%B5%E8%A1%97%E9%81%93%22%7D%2C%22formattedAddress%22%3A%22%E6%B1%9F%E8%8B%8F%E7%9C%81%E5%8D%97%E4%BA%AC%E5%B8%82%E6%B1%9F%E5%AE%81%E5%8C%BA%E7%A7%A3%E9%99%B5%E8%A1%97%E9%81%93%E8%83%9C%E5%A4%AA%E8%B7%AF%E5%8D%97%E4%BA%AC%E8%88%AA%E7%A9%BA%E8%88%AA%E5%A4%A9%E5%A4%A7%E5%AD%A6%E5%B0%86%E5%86%9B%E8%B7%AF%E6%A0%A1%E5%8C%BA%22%2C%22roads%22%3A%5B%5D%2C%22crosses%22%3A%5B%5D%2C%22pois%22%3A%5B%5D%7D&date=2020{1:02}{2:02}&address=%E6%B1%9F%E8%8B%8F%E7%9C%81%E5%8D%97%E4%BA%AC%E5%B8%82%E6%B1%9F%E5%AE%81%E5%8C%BA%E7%A7%A3%E9%99%B5%E8%A1%97%E9%81%93%E8%83%9C%E5%A4%AA%E8%B7%AF%E5%8D%97%E4%BA%AC%E8%88%AA%E7%A9%BA%E8%88%AA%E5%A4%A9%E5%A4%A7%E5%AD%A6%E5%B0%86%E5%86%9B%E8%B7%AF%E6%A0%A1%E5%8C%BA&area=%E6%B1%9F%E8%8B%8F%E7%9C%81+%E5%8D%97%E4%BA%AC%E5%B8%82+%E6%B1%9F%E5%AE%81%E5%8C%BA&province=%E6%B1%9F%E8%8B%8F%E7%9C%81&city=%E5%8D%97%E4%BA%AC%E5%B8%82&fxzrwjtw=&fxjrcjtw=1&fxjrzjtw=&sfzx=1&sfcyglq=0&sfcxtz=0&uid=24113&created={0}&is_fx_log=1&id=9358620&gwszdd=&sfyqjzgc=&jcqzrq=&sfjcqz=&jrsfqzys=&jrsfqzfy=&szsqsfybl=0&sfsqhzjkk=&sqhzjkkys=&sfygtjzzfj=&gtjzzfjsj=&sftjwz=0&sftjhb=0&sfjcwhry=0&sfjchbry=0&ismoved=0'


def sendmsg(msg):
    if receiver != 'xxxxxxxxx@qq.com':
        return send_mail(mail_username, mail_password, mail_host, receiver, msg, msg, '童鞋', 'inuaa打卡姬')


# 登陆获得cookie
def login(login_id, login_password, login_headers):
    for _ in range(try_times):
        try:
            time.sleep(0.5)
            r = requests.get(
                'https://m.nuaa.edu.cn/uc/wap/login', headers=headers)
            print('get login page:', r.status_code)
            # r.encoding = 'utf-8'
            # print(r.text)
            cookie = r.headers['Set-Cookie']
            print(cookie)
            cookie = re.search(r'eai-sess=([a-zA-Z0-9]+)', cookie).group(0)

            login_headers['Cookie'] = cookie

            time.sleep(0.5)
            r = requests.get('https://m.nuaa.edu.cn/uc/wap/login/check', headers=headers,
                             data='username={}&password={}'.format(login_id, login_password))
            print('login...:', r.status_code)

            cookie2 = r.headers['Set-Cookie']
            cookie = cookie + '; ' + \
                re.search(r'UUkey=([a-zA-Z0-9]+)', cookie2).group(0)

            login_headers['Cookie'] = cookie
            print(cookie)
            return
        except:
            print('login failed')
            pass

# 签到
def sign(m, d):
    try:
        for _ in range(try_times):
            time.sleep(0.5)
            r = requests.post('https://m.nuaa.edu.cn/ncov/wap/default/save',
                              data=post_data.format(int(time.time()), m, d - 1), headers=headers)
            print('statue code:', r.status_code)
            print('return:', r.text)
            if r.text == '{"e":0,"m":"操作成功","d":{}}':
                sendmsg('打卡成功')
                return True
            else:
                login(id, password, headers)
    except:
        print('except')
        pass
        # print(r.request.body)
    sendmsg('打卡失败')
    return False


if __name__ == '__main__':
    print('Start...')
    last_post = 10086   # 最后一次签到的日期
    login(id, password, headers)

    while True:
        t = time.localtime()
        print('{0:02}:{1:02}:{2:02}\r'.format(
            t.tm_hour, t.tm_min, t.tm_sec), end='')
        if t.tm_mday != last_post:
            print('')
            if sign(t.tm_mon, t.tm_mday):
                print('Sign for {}.{} successfully!'.format(t.tm_mon, t.tm_mday))
                last_post = t.tm_mday
            else:
                print('Sign for {}.{} failed!'.format(t.tm_mon, t.tm_mday))
                time.sleep(3600)    # error wait for 5.55 h
        time.sleep(1)
