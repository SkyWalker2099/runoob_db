import pymysql
import jieba.posseg as posseg
import jieba
import gensim
import logging
import collections
from collections import defaultdict
import numpy as np
import json

stoplist = set('的 ？ ? 与 和 是 （ ）'.split())

Answer = collections.namedtuple("Answer", "sim answer link")

def build_all_model():
    db = pymysql.connect(host = "localhost",
                         user = "zzh",
                         password = "123456",
                         db = "runoob")
    cursor = db.cursor()
    sql = "select class from href_list group by class;"
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in result:
        print(i[0])
        build_model(i[0])

def build_model(table_name):
    """
    建立某一数据表的相似度模型
    :param text:
    :return:
    """
    table_name = table_name.replace("/","_").replace(".","_")

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


    tfidf.save("MODELS/%s_tfidf"%table_name)
    index.save("MODELS/%s_index"%table_name)
    dictionary.save("MODELS/%s_dic"%table_name)

def get_question(table_name, text):
    """
    加载模型获取答案
    :param table_name:
    :param text:
    :return:
    """

    tfidf = gensim.models.TfidfModel.load("MODELS/%s_tfidf"%table_name)
    index = gensim.similarities.MatrixSimilarity.load("MODELS/%s_index"%table_name)
    dictionary = gensim.corpora.Dictionary.load("MODELS/%s_dic"%table_name)

    text = dictionary.doc2bow(jieba.lcut(text))

    text_tfidf = tfidf[text]
    sims = index[text_tfidf]
    print(sims)


    print("~~~"*30)

    # postion  = np.where(sims == max(sims))
    # print(postion)

    positions = sims.argsort()[-3:]
    for i in positions:
        print(i)

    db = pymysql.connect(host = "localhost",
                         user = "zzh",
                         password = "123456",
                         db = "runoob")
    cursor = db.cursor()

    answers = []

    for postion in positions:
        cursor.execute("select * from %s where id = %s"%(table_name, postion+1))
        result = cursor.fetchall()
        answer = Answer(str(sims[postion]),result[0][2],result[0][3])
        print(postion)
        print(result[0][1])
        print(answer)
        answers.append(answer)
        print("~~~"*30)
    db.close()

    a = json.dumps(answers)
    # print(a)
    return a


if __name__ == '__main__':

    a = get_question("服务端","python 安装")
    ans = json.loads(a)
    print(type(ans))
    for a in ans:
        print(a)
    # build_all_model()