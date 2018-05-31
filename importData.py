# coding=utf-8

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba
import pyLDAvis.sklearn

from DataBase.PyMySQLConn import connectdb


# 导入数据
def cuttingVocabulary(text):
    return " ".join(jieba.cut(text))

# 绘制词云
def drawingWordCloud(text):
    wordcloud = WordCloud(font_path="simsun.ttf").generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

# 导入数据
def loadData():
    pass

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()

if __name__ == '__main__':
    # 输入你要分析的商品ID
    db = connectdb()
    df = pd.read_sql('SELECT * FROM good_550887826096',db )
    # df = pd.read_sql('SELECT comment FROM good_550887826096 ',pymysql.connect("localhost","root","123456","DataDig",use_unicode=True, charset="utf8mb4") )
    # df = pd.read_csv("taobao.csv")

    df["content_cutted"] = df.comment.apply(cuttingVocabulary)
    # df["content_cutted"] = df.content.apply(cuttingVocabulary)
    # print(df.content_cutted.head())
    n_features = 1000
    tf_vectorizer = CountVectorizer(strip_accents='unicode',
                                    max_features=n_features,
                                    stop_words='english',
                                    max_df=0.5,
                                    min_df=10)
    tf = tf_vectorizer.fit_transform(df.content_cutted)
    n_topics = 5
    lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=50,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=0)
    lda.fit(tf)
    # 定义关键词的个数
    n_top_words = 20

    tf_feature_names = tf_vectorizer.get_feature_names()
    print_top_words(lda, tf_feature_names, n_top_words)

    # pyLDAvis.show()
    pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)

    data = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)
    pyLDAvis.show(data)