import requests
import time
from apscheduler.schedulers.blocking import BlockingScheduler
import json
import random
from urllib.parse import quote
from Email_Notice import notify_email


def get_code_and_result(response):
    response_dict = json.loads(response.text)
    return "错误码为: " + str(response_dict['e']) + '\n' + "消息: " + str(response_dict['m'])


def get_badminton_court(reservation_time):
    court_list_7_to_8 = ['11590', '11603', '11616', '11629', '11642', '11655', '11668', '11681', '11694']
    court_list_8_to_9 = ['11591', '11604', '11617', '11630', '11643', '11656', '11669', '11682', '11695']

    if reservation_time == 7:
        return 1422, random.choice(court_list_7_to_8)
    elif reservation_time == 8:
        return 1423, random.choice(court_list_8_to_9)


def get_badminton_reservation_data(reservation_time):
    period, sub_resource_id = get_badminton_court(reservation_time)
    data = '[{' \
           '"date":"' + time.strftime("%Y-%m-%d", time.localtime()) + \
           '","period":' + str(period) + \
           ',"sub_resource_id":' + str(sub_resource_id) + \
           '}]'
    return data


def auto_badminton_reservation():
    url = 'https://ehall3.nuaa.edu.cn/site/reservation/launch'

    with open('config/badminton_POST.json', 'r') as json_f:
        headers = json.load(json_f)

    data = {
        'resource_id': 17,
        'code': '',
        'remarks': '',
        'deduct_num': '',
        'data': None
    }
    proxies = {'http': None, 'https': None}
    for i in range(5):
        data['data'] = get_badminton_reservation_data(7)
        r = requests.post(url=url, headers=headers, data=data, proxies=proxies)

        if json.loads(r.text)['e'] == 0:
            notify_email(get_code_and_result(r), '7点羽毛球场地')
            break

    for i in range(5):
        data['data'] = get_badminton_reservation_data(8)
        r = requests.post(url=url, headers=headers, data=data, proxies=proxies)
        if json.loads(r.text)['e'] == 0:
            notify_email(get_code_and_result(r), '8点羽毛球场地')
            break

    print(r.text)


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(auto_badminton_reservation, 'cron', hour=7, second=1)
    scheduler.start()
