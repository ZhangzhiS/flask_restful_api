import os

from .match import get_match
from .responsesEvaluate import Evaluator


class QuestionAnswerModel(object):

    def __init__(self):
        self.general_questions = []
        self.path = os.path.dirname(__file__)
        self.matcher = get_match(matchType="bm25")

        self.evaluator = Evaluator()
        with open("/home/zhi/PycharmProjects/flask_restful_api/QuestionAnswer/data/reply.txt") as rd:
            self.reply = rd.readlines()
        # self.moduleTest()

    def get_response(self, query, threshold=90):
        title, index = self.matcher.match(query)
        sim = self.matcher.get_similarity()

        if sim < threshold:
            return -1, 0
        else:
            res = self.reply[index]
            print(index)
            candiates = self.evaluator.getBestResponse([res], topk=1)
            return candiates, sim