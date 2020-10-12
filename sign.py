# -*- coding: UTF-8 -*-

import requests
import time
import json
import re
import json
from send_mail import send_mail


# 如果发包过快会造成502，如果给多个同学打卡请注意一下请求速度
try_times = 2

# 每次requests请求的延迟(s秒)，太低会封IP
delay = 3

# headers，所有的请求都用这个作为headers
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



def login(login_id, login_password):
    '''
    登陆I南航，返回Cookie，失败返回空串
    '''
    headers['Cookie'] = ''
    for _ in range(try_times):
        try:
            time.sleep(delay)
            r = requests.get(
                'https://m.nuaa.edu.cn/uc/wap/login', headers=headers)
            print('get login page:', r.status_code)
            # r.encoding = 'utf-8'
            # print(r.text)
            cookie = r.headers['Set-Cookie']
            # print(cookie)
            cookie = re.search(r'eai-sess=([a-zA-Z0-9]+)', cookie).group(0)

            headers['Cookie'] = cookie

            time.sleep(delay)
            r = requests.get('https://m.nuaa.edu.cn/uc/wap/login/check', headers=headers,
                             data='username={}&password={}'.format(login_id, login_password))
            print('login...:', r.status_code)

            cookie2 = r.headers['Set-Cookie']
            cookie = cookie + '; ' + \
                re.search(r'UUkey=([a-zA-Z0-9]+)', cookie2).group(0)

            # headers['Cookie'] = cookie
            print(cookie)
            return cookie
        except:
            print('login failed.')
            pass
    # raise Exception('lOGIN FAIL')
    return ''


def sign(m, d, user, smtp_host, mail_username, mail_password):

    '''
    签到，并且发送邮件提醒，成功返回True，失败返回False
    '''
    for _ in range(try_times):
        try:
            time.sleep(delay)
            headers['Cookie'] = user['cookie']
            r = requests.post('https://m.nuaa.edu.cn/ncov/wap/default/save',
                              data=post_data.format(int(time.time()), m, d - 1), headers=headers)
            print('sign statue code:', r.status_code)
            print('sign return:', r.text)
            r.encoding = 'utf-8'
            
            if r.text.find('成功') >= 0:
                print('打卡成功')
                if user['receiver_mail'] != '':
                    send_mail(mail_username, mail_password, smtp_host,
                              user['receiver_mail'], '打卡成功', '打卡成功', user['name'], '打卡姬')
                return True
            else:
                print('打卡失败，尝试重新登陆')
                user['cookie'] = login(user['student_id'], user['student_password'])
        except:
            print('尝试失败')
            pass
            # print(r.request.body)
    if user['receiver_mail'] != '':
        send_mail(mail_username, mail_password, smtp_host,
                  user['receiver_mail'], '打卡失败', '打卡事变', user['name'], '打卡姬')
    return False


def main():
    print('------>>>---->启动中<------<<<----')
    last_post = 10086   # 最后一次签到的日期
    
    # 读取配置文件
    with open('config.json', 'r') as f:
        config = json.loads(f.read())
    smtp_host = config['smtp_host']
    mail_password = config['mail_password']
    mail_username = config['mail_username']
    users = config['users']
    
    # 一起登陆啊，失败了就先空着，等打卡时候再来管他
    for user in users:
        print('Login...:', user['name'])
        user['cookie'] = login(user['student_id'], user['student_password'])

    
    # 每一天先拷贝一下需要打卡的列表，然后打卡
    # 其他时间如果监测到待打卡的列表非空，就重新读打卡
    
    while True:
        t = time.localtime()

        if t.tm_mday != last_post:
            # 新的一天，拷贝一份完整的打卡清单，全部打一遍卡。但是这样做的话每次更新cookie，users也自动更新。

            print('----------开始每日打卡----------')
            to_sign_list = users.copy()

            # 给每个人打卡
            new_list = []   # 未完成打卡的暂时放这里
            for user in to_sign_list[:]:
                print('**********' + user['name'] + '**********')
                if sign(t.tm_mon, t.tm_mday, user, smtp_host, mail_username, mail_password):
                    print('Sign for {} on {}.{} successfully!'.format(
                        user['name'], t.tm_mon, t.tm_mday))
                else:
                    print('Sign for {} on {}.{} failed!'.format(
                        user['name'], t.tm_mon, t.tm_mday))
                    new_list.append(user)
            to_sign_list = new_list
            last_post = t.tm_mday   # 更新日期

        elif len(to_sign_list) != 0:
            # 一天中的后续尝试，先等待2小时，然后再打卡
            time.sleep(3600)    # 失败用户每一个小时重试一次
        
            print('----------重新打卡尝试----------')
            # 给每个失败的人打卡
            new_list = []
            for user in to_sign_list[:]:
                print('**********' + user['name'] + '**********')
                if sign(t.tm_mon, t.tm_mday, user, smtp_host, mail_username, mail_password):
                    print('Sign for {} on {}.{} successfully!'.format(
                        user['name'], t.tm_mon, t.tm_mday))
                else:
                    print('Sign for {} on {}.{} failed!'.format(
                        user['name'], t.tm_mon, t.tm_mday))
                    new_list.append(user)
            to_sign_list = new_list
        # else: 都打完了
        time.sleep(1)

if __name__ == '__main__':
    main()
