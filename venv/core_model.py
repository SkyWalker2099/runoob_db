import pymysql
import jieba.posseg as posseg
import jieba
import gensim
import logging
from collections import defaultdict
import numpy as np

stoplist = set('的 ？ ? 与 和 是 （ ）'.split())

def build_model(table_name):
    """
    建立某一数据表的相似度模型
    :param text:
    :return:
    """
    db = pymysql.connect(host = "localhost",
                         user = "zzh",
                         password = "123456",
                         db = "runoob",
                         cursorclass = pymysql.cursors.DictCursor)

    cursor = db.cursor()
    sql  = "select question from %s"%table_name

    cursor.execute(sql)

    questions = cursor.fetchall()
    db.close()


    texts = []
    frequency = defaultdict(int)
    for question in questions:
        text = question["question"]
        word_list = jieba.lcut(text)
        text = [word for word in word_list if(word not in stoplist)]
        for word in text:
            frequency[word] +=1
        texts.append(text)

    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    tfidf = gensim.models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    index = gensim.similarities.MatrixSimilarity(corpus_tfidf)


    tfidf.save("MODELS/tfidf")
    index.save("MODELS/index")
    dictionary.save("MODELS/dic")

def get_question(table_name, text):
    """
    加载模型获取答案
    :param table_name:
    :param text:
    :return:
    """

    tfidf = gensim.models.TfidfModel.load("MODELS/tfidf")
    index = gensim.similarities.MatrixSimilarity.load("MODELS/index")
    dictionary = gensim.corpora.Dictionary.load("MODELS/dic")

    text = dictionary.doc2bow(jieba.lcut(text))

    text_tfidf = tfidf[text]
    sims = index[text_tfidf]

    postion  = np.where(sims == max(sims))
    print(postion)
    db = pymysql.connect(host = "localhost",
                         user = "zzh",
                         password = "123456",
                         db = "runoob")
    cursor = db.cursor()

    cursor.execute("select * from %s where id = %s"%(table_name, postion[0][0]+1))

    result = cursor.fetchall()
    print(result)
    db.close()



if __name__ == '__main__':

    get_question("ASP_NET","MVC编程模式是什么样的")
