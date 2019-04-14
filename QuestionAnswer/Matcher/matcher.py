import logging
import os

import jieba


class Matcher(object):
    """
    比对使用者输入的句子与目标语料集，
    回传语料集中最相似的一个句子。
    """

    def __init__(self, seg_lib="jieba",
                 jieba_dict=None,
                 user_dict=None):
        logging.basicConfig(format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s', level=logging.WARNING)
        self.titles = []  # 欲进行匹配的所有标题
        self.segTitles = []  # 断好词的标题
        self.stopwords = set()  # 停用词
        self.similarity = 1  # 相似度
        default_dict_path = os.path.dirname(os.path.dirname(__file__))
        # default_dict_path = "/home/cubAIBot/cub_aibot/apps/aibot/qa_model/QuestionAnswer"
        if jieba_dict and user_dict:
            self.jieba_dict = jieba_dict
            self.user_dict = user_dict
        else:
            self.jieba_dict = default_dict_path + "/data/dict.txt.big"
            self.user_dict = default_dict_path + "/data/user_dict.txt"
        self.init_jieba()

    def init_jieba(self):

        """
        初始化jieba.
        """

        jieba.load_userdict(self.user_dict)
        # jieba.set_dictionary(self.jieba_dict)
        with open(self.user_dict, 'r', encoding='utf-8') as input_dict:
            for word in input_dict:
                word = word.strip('\n')
                jieba.suggest_freq(word, True)

    def load_stop_words(self, path):
        """
        加载停用词
        """
        with open(path, "r", encoding="utf-8") as sw:
            for word in sw:
                self.stopwords.add(word.strip("\n"))

    def load_title(self, path):
        """
        加载标题
        """
        # todo 从mongodb中查询
        with open(path,'r',encoding='utf-8') as data:
            self.titles = [line.strip('\n') for line in data]

    def match(self, query):
        """
        读入使用者查询，若语料库中存在相同的句子，便回传该句子与标号

        query: 使用者的输入

        return:
            title: 最相似的匹配标题
            该标题的索引编号
        """
        for index, title in enumerate(self.titles):
            return title, index

    def get_similarity(self):
        """
        返回相似度
        """
        return self.similarity

    @staticmethod
    def word_segmentation(string):
        """
        词语分割
        """
        return [word for word in jieba.cut(string, cut_all=False)]

    def title_segmentation(self, clean_stop_word=True):
        """
        将self.titles断词后的结果输出，并存储于self.segTitles
        cleanStopWord: 是否停用标题中的停用词
        """

        if not os.path.exists('data/SegTitles.txt'):

            self.segTitles = []
            for title in self.titles:

                if clean_stop_word:
                    clean = [word for word in self.word_segmentation(title)
                             if word not in self.stopwords]
                    self.segTitles.append(clean)
                else:
                    self.segTitles.append(self.word_segmentation(title))

            with open('data/SegTitles.txt', 'w', encoding="utf-8") as seg_title:
                for title in self.segTitles:
                    seg_title.write(' '.join(title) + '\n')
        else:
            with open('data/SegTitles.txt', 'r', encoding="utf-8") as seg_title:
                for line in seg_title:
                    line = line.strip('\n')
                    seg = line.split()

                    if clean_stop_word:
                        seg = [word for word in seg
                               if word not in self.stopwords]
                    self.segTitles.append(seg)
