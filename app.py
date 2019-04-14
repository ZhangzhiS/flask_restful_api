#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
# @Author   : zhi
# @Time     : 2019/4/14 上午8:17
# @Filename : api
# @Software : PyCharm
import datetime

from flask import Flask
from flask_restful import Api, Resource, request

# from QuestionAnswer.qaBase import QuestionAnswerModel

app = Flask(__name__)
api = Api(app=app)

# qa = QuestionAnswerModel()

# parse = reqparse.RequestParser()


class AddArray(Resource):

    def post(self):
        value_array = request.json
        value_array = value_array.get("value_array")
        result = 0
        for value in value_array:
            result += value["value"]
        return {"result": result}


class GetDate(Resource):

    def get(self):
        date = datetime.date.today()
        resp = {
            "date": date.strftime("%Y-%m-%d")
        }
        return resp


class Chatbot(Resource):

    def post(self):
        msg = request.json
        msg = msg.get("msg")
        """
        reply = qa.get_response(msg)
        """
        if "您好" in msg and "再见" not in msg:
            reply = "您好，您吃了吗？"
        elif "您好" not in msg and "再见" in msg:
            reply = "回见了您内。"
        elif "您好" in msg and "再见" in msg:
            reply = "天气不错"
        else:
            reply = "尝试配置使用QA模块"
        return {"result": reply}

api.add_resource(AddArray, "/add")
api.add_resource(GetDate, "/get_date")
api.add_resource(Chatbot, "/chat")


if __name__ == '__main__':
    app.run(debug=True)
