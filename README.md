# 简单的接口开发

## 项目介绍
简单的面试题
接口三简单可以选择配置使用QA模块，由于题目的问答过于简单，在比较语句的相似的时候有点异常，所以修改为简单的逻辑判断语句。
部署在了个人服务器中。

域名还未备案通过，所以通过IP访问。80别的项目在用，所以配置在了6000端口。
地址：http://39.105.152.226:6000

## 部署文档

将代码clone到本地
```bash
git clone git@github.com:ZhangzhiS/flask_restful_api.git
```
安装依赖
```bash
cd flask_restful_api
pip install -r requirements.txt  # 建议使用虚拟环境
```
根据个人需求配置uwsgi.ini
主要可修改一下日志文件路径以及python的运行环境

```bash
daemonize = /home/logs/uwsgi.log  # 日志路径
home = /root/.virtualenvs/venv  # python环境
```

配置nginx，配置server部分
```
server {
        listen       80 default_server;
        listen       [::]:80 default_server;
        server_name  _;
        root         /usr/share/nginx/html;

        # Load configuration files for the default server block.
        # include /etc/nginx/default.d/*.conf;

        location / {
            include uwsgi_params;
            uwsgi_pass 127.0.0.1:8000;  # 端口与uwsgi.ini中的配置端口相同
        }
}
```

### 测试结果
可以使用以下命令运行测试
```bash
python test.py
```
```python
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
        
# {'result': 40}
# {'date': '2019-04-14'}
# {'result': '您好，您吃了吗？'}
# {'result': '回见了您内。'}
# {'result': '天气不错'}
# {'result': '尝试配置使用QA模块'}

```