import logging
import os
import math

from collections import defaultdict

from gensim import corpora

from .Matcher.matcher import Matcher


class Evaluator(Matcher):
    """
    读入一串推文串列，计算出当中可靠度最高的推文
    """

    def __init__(self, seg_lib="jaiba"):

        super().__init__(seg_lib)
        self.responses = []
        self.segResponses = []
        self.totalWords = 0

        self.path = os.path.dirname(__file__)

        self.filteredWords = set()  # 必须滤除的回应

        self.counterDictionary = defaultdict(int)  # 用于统计词频
        self.tokenDictionary = None  # 用于分配词 id，与建置词袋

        # 中文停用词与特殊符号加载
        self.load_stop_words(path=self.path + "/data/stopwords/chinese_sw.txt")
        self.load_stop_words(path=self.path + "/data/stopwords/specialMarks.txt")
        self.loadFilterdWord(path=self.path + "/data/stopwords/ptt_words.txt")

    def cleanFormerResult(self):
        """
        清空之前回应留下的纪录
        """
        self.responses = []
        self.segResponses = []
        self.totalWords = 0

    def getBestResponse(self, responses, topk, debugMode=True):
        """
        从 self.responses 中挑选出可靠度前 K 高的回应回传
        Return : List of (reply,grade)
        """
        self.cleanFormerResult()

        self.buildResponses(responses)
        # print(self.responses, "build")
        self.segmentResponse()
        # print(self.responses, "segment")
        self.buildCounterDictionary()
        # print(self.responses, "count")
        candiateList = self.responses[0]
        # print(candiateList)

        return candiateList

    def loadFilterdWord(self, path):
        with open(path, 'r', encoding='utf-8') as sw:
            for word in sw:
                self.filteredWords.add(word.strip('\n'))

    def buildResponses(self, responses):
        """
        将 json 格式中目前用不上的 user, vote 去除，只留下 Content
        """
        self.responses = []
        # print(self.responses, "******************")
        for response in responses:
            clean = True
            r = response
            for word in self.filteredWords:
                if word in r:
                    clean = False
            if clean:
                self.responses.append(response)
        # print(self.responses, "******************")

    def segmentResponse(self):
        """
        对 self.responses 中所有的回应断词并去除中文停用词，储存于 self.segResponses
        """
        self.segResponses = []
        for response in self.responses:
            keywordResponse = [keyword for keyword in self.word_segmentation(response)
                               if keyword not in self.stopwords
                               and keyword != ' ']
            self.totalWords += len(keywordResponse)
            self.segResponses.append(keywordResponse)
        # logging.info("已完成回应断词")

    def buildCounterDictionary(self):
        """
        统计 self.segResponses 中每个词出现的次数
        """
        for reply in self.segResponses:
            for word in reply:
                self.counterDictionary[word] += 1
        # logging.info("计数字典建置完成")
