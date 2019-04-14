#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
# @Author   : zhi
# @Time     : 2019/4/14 上午8:39
# @Filename : test
# @Software : PyCharm

import requests
import json

# 请求参数的格式
headers = {
    'Content-Type': 'application/json',
}


def test_api1():
    """测试接口1"""
    # 模拟数据
    json_data = {
        "value_array": [
            {"value": 12},
            {"value": 18},
            {"value": 10}
        ]
    }

    url = "http://39.105.152.226:6000/add"

    data = json.dumps(json_data)

    resp = requests.post(
        url=url,
        data=data,
        headers=headers
    )

    return resp.json()


def test_api2():
    resp = requests.get("http://39.105.152.226:6000/get_date")
    return resp.json()


def test_api3(msg):
    url = "http://39.105.152.226:6000/chat"
    data = json.dumps(
        {
            "msg": msg
        }
    )
    resp = requests.post(
        url=url,
        data=data,
        headers=headers
    )
    return resp.json()


if __name__ == '__main__':
    add_result = test_api1()
    print(add_result)
    date = test_api2()
    print(date)
    msg_list = [
        "您好",
        "再见",
        "您好吗，再见了",
        "要来一杯吗？",
    ]
    for msg in msg_list:
        reply = test_api3(msg)
        print(reply)
