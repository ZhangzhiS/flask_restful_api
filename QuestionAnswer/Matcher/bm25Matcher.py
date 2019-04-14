import math
import logging

from .matcher import Matcher
from .quickSearch import QuickSearcher


class BestMatchingMatcher(Matcher):
    """
    基于bm25算法,获取最佳匹配短语
    """

    def __init__(self, seg_lib="jieba", removeStopWords=True):
        super().__init__(seg_lib)

        self.cleanStopWords = removeStopWords
        self.D = 0  # 句子总数
        self.avgdl = None

        self.wordset = set()  # Corpus 中所有词的集合
        self.words_location_record = dict()  # 纪录该词 (key) 出现在哪几个句子(id)
        self.words_idf = dict()  # 纪录每个词的 idf 值

        self.f = []
        self.df = {}
        self.idf = {}
        self.k1 = 1.5
        self.b = 0.75
        self.searcher = QuickSearcher()  # 问句筛选

        if removeStopWords:
            self.load_stop_words("data/stopwords/chinese_sw.txt")
            self.load_stop_words("data/stopwords/specialMarks.txt")

    def initialize(self, ngram=1):

        assert len(self.titles) > 0, "请先载入短语表"

        self.title_segmentation()  # 将 self.titles 断词为 self.segTitles
        # self.calculateIDF() # 依照断词后结果, 计算每个词的 idf value
        self.initBM25()
        self.searcher.buildInvertedIndex(self.segTitles)

    def initBM25(self):
        """初始化BM25模块"""
        # logging.info("BM25模块初始化中")

        self.D = len(self.segTitles)
        # print(self.segTitles)
        self.avgdl = sum([len(title) + 0.0 for title in self.segTitles]) / self.D

        for seg_title in self.segTitles:
            tmp = {}
            for word in seg_title:
                if word not in tmp:
                    tmp[word] = 0
                tmp[word] += 1
            self.f.append(tmp)
            for k, v in tmp.items():
                if k not in self.df:
                    self.df[k] = 0
                self.df[k] += 1
        for k, v in self.df.items():
            self.idf[k] = math.log(self.D - v + 0.5) - math.log(v + 0.5)

        # logging.info("BM25模块初始化完成")

    def sim(self, doc, index):
        """计算相似度"""
        score = 0
        for word in doc:
            if word not in self.f[index]:
                continue
            d = len(self.segTitles[index])
            score += (self.idf[word] * self.f[index][word] * (self.k1 + 1)
                      / (self.f[index][word] + self.k1 * (1 - self.b + self.b * d
                                                          / self.avgdl)))
        return score

    def match(self, query):
        """
        读入使用者 query，若语料库中存在类似的句子，便回传该句子与标号

        Args:
            - query: 使用者欲查询的语句
        """

        seg_query = self.word_segmentation(query)
        max_score = -1
        target = ''
        target_idx = -1

        target_index = self.searcher.quickSearch(seg_query)  # 只取出必要的 titles

        for index in target_index:
            score = self.sim(seg_query, index)
            if score > max_score:
                target_idx = index
                max_score = score

        # 正常化
        max_score = max_score / self.sim(self.segTitles[target_idx], target_idx)
        target = target.join(self.segTitles[target_idx])
        self.similarity = max_score * 100  # 百分制
        return target, target_idx
