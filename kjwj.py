#!/usr/bin/python3
# -*- coding: utf8 -*-
"""
说明: 环境变量`KJWJ_UP`账号和密码用`-`分割     例如： 账号-密码
cron: 20 12 * * *
new Env('科技玩家-签到');
"""
import os, sys
import json

try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请在青龙后台-依赖管理-Python3 搜索安装")
    exit(3)

try:
    import aiohttp
except Exception as e:
    print(e, "\n缺少aiohttp 模块，请在青龙后台-依赖管理-Python3 搜索安装")
    exit(3)

try:
    import asyncio
except Exception as e:
    print(e, "\n缺少asyncio 模块，请在青龙后台-依赖管理-Python3 搜索安装")
    exit(3)

try:
    import random
except Exception as e:
    print(e, "\n缺少random 模块，请在青龙后台-依赖管理-Python3 搜索安装")
    exit(3)

################################ 【Main】################################
pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep
UserAgent = ''


## 获取通知服务
class msg(object):
    def __init__(self, m):
        self.str_msg = m
        self.message()

    def message(self):
        global msg_info
        print(self.str_msg)
        try:
            msg_info = "{}\n{}".format(msg_info, self.str_msg)
        except:
            msg_info = "{}".format(self.str_msg)
        sys.stdout.flush()

    def getsendNotify(self, a=0):
        if a == 0:
            a += 1
        try:
            url = 'https://gitee.com/xiongchao/Py-Script/raw/main/sendNotify.py'
            response = requests.get(url)
            if 'curtinlv' in response.text:
                with open('sendNotify.py', "w+", encoding="utf-8") as f:
                    f.write(response.text)
            else:
                if a < 5:
                    a += 1
                    return self.getsendNotify(a)
                else:
                    pass
        except:
            if a < 5:
                a += 1
                return self.getsendNotify(a)
            else:
                pass

    def main(self):
        global send
        cur_path = os.path.abspath(os.path.dirname(__file__))
        sys.path.append(cur_path)
        if os.path.exists(cur_path + "/sendNotify.py"):
            try:
                from sendNotify import send
            except:
                self.getsendNotify()
                try:
                    from sendNotify import send
                except:
                    print("加载通知服务失败~")
        else:
            self.getsendNotify()
            try:
                from sendNotify import send
            except:
                print("加载通知服务失败~")
        ###################


msg("").main()


##############

#######################################


def userAgent():
    """
    随机生成一个UA
    :return: jdapp;iPhone;9.4.8;14.3;xxxx;network/wifi;ADID/201EDE7F-5111-49E8-9F0D-CCF9677CD6FE;supportApplePay/0;hasUPPay/0;hasOCPay/0;model/iPhone13,4;addressid/2455696156;supportBestPay/0;appBuild/167629;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1
    """
    if not UserAgent:
        uuid = ''.join(random.sample('123456789abcdef123456789abcdef123456789abcdef123456789abcdef', 40))
        addressid = ''.join(random.sample('1234567898647', 10))
        iosVer = ''.join(
            random.sample(["14.5.1", "14.4", "14.3", "14.2", "14.1", "14.0.1", "13.7", "13.1.2", "13.1.1"], 1))
        iosV = iosVer.replace('.', '_')
        iPhone = ''.join(random.sample(["8", "9", "10", "11", "12", "13"], 1))
        ADID = ''.join(random.sample('0987654321ABCDEF', 8)) + '-' + ''.join(
            random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(
            random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 12))
        return f'jdapp;iPhone;10.0.4;{iosVer};{uuid};network/wifi;ADID/{ADID};supportApplePay/0;hasUPPay/0;hasOCPay/0;model/iPhone{iPhone},1;addressid/{addressid};supportBestPay/0;appBuild/167629;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS {iosV} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1'
    else:
        return UserAgent


"""
科技玩家
"""


# @logger.catch
async def login(session, name, pwd):
    """
    查询任务列表
    :param session:
    :return:
    """
    url = 'https://www.kejiwanjia.com/wp-json/jwt-auth/v1/token'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'www.kejiwanjia.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'www.kejiwanjia.com',
        'User-Agent': userAgent(),
        'Referer': 'https://www.kejiwanjia.com',
        'Accept-Language': 'zh-cn'
    }
    body = f'nickname=&username={name}&password={pwd}&code=&img_code=&invitation_code=&token=&smsToken=&luoToken=&confirmPassword=&loginType='
    response = await session.post(url=url, headers=headers, data=body)
    if response.status == 200:
        text = await response.text()
        data = json.loads(text)
        msg(f"账号:{data['name']}登陆成功")
        msg(f"ID:{data['id']}")
        msg(f"金币:{data['credit']}")
        msg(f"等级:{data['lv']['lv']['lv']}")
        msg('账号:{}登陆成功'.format(data['name']))
        token = data['token']
        url = 'https://www.kejiwanjia.com/wp-json/b2/v1/userMission'
        headers1 = {
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'www.kejiwanjia.com',
            'authorization': f'Bearer {token}',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'www.kejiwanjia.com',
            'User-Agent': userAgent(),
            'Referer': 'https://www.kejiwanjia.com',
            'Accept-Language': 'zh-cn'
        }
        response = await session.post(url=url, headers=headers1, data=body)
        if response.status == 200:
            text = await response.text()
            data = json.loads(text)
            if type(data) == dict:
                msg(f"签到成功：{data['credit']}金币\n")
            else:
                msg(f"今日已经签到：获得{data}金币\n")
        return msg
    else:
        print('账号登陆失败\n账号或密码错误\n')
        return


async def run():
    """
    程序入口
    :return:
    """
    users = os.environ.get('KJWJ_UP')
    name, pwd = users.split('-')
    async with aiohttp.ClientSession() as session:
        await login(session, name, pwd)
        send("【科技玩家-签到】", msg_info)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
