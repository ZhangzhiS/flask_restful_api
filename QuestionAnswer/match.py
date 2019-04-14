import os
import logging

from .Matcher.bm25Matcher import BestMatchingMatcher


def get_match(matchType):
    """
    回传初始完毕的matcher
    matcherType: 字符串匹配方式
    """

    if matchType == "bm25":
        return bm25()
    else:
        logging.info("[Error]: Invailded type.")
        exit()


def bm25():
    cur_dir = os.getcwd()
    os.chdir(os.path.dirname(__file__))
    bm25Matcher = BestMatchingMatcher()
    # bm25Matcher.load_title(path="data/Titles.txt")
    bm25Matcher.load_title("/home/zhi/PycharmProjects/flask_restful_api/QuestionAnswer/data/Titles.txt")
    bm25Matcher.initialize()
    os.chdir(cur_dir)

    return bm25Matcher
