# coding=utf-8

import pandas as pd
from os import path
from PIL import Image
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba
import pyLDAvis
import pyLDAvis.sklearn


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

# # 绘制词云
# def drawingWordCloud(model,feature_names, n_top_words):
#     for topic_idx, topic in enumerate(model.components_):
#         wordcloud = WordCloud(font_path="simsun.ttf").generate(([feature_names[i]
#                             for i in topic.argsort()[:-n_top_words - 1:-1]]))
#         plt.figure()
#         plt.imshow(wordcloud, interpolation="bilinear")
#         plt.axis("off")
#         plt.show()

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
    mytext="大家都用李老师的线代讲义 希望我能学好线性代数!都是各自科目的经典教辅~~印刷质量还不错，个人偏好宇哥的编书风格，不过线代方面还是永乐大帝更老练些~~ 客服回复及时热情还不错，应该是正品，就是赠送的课程。。哎，就知道是体验课，嘤嘤嘤"
    mytext = " ".join(jieba.cut(mytext))
    # df = pd.read_csv("datascience.csv",encoding='gb18030')
    df = pd.read_csv("taobao.csv")

    df["content_cutted"] = df.content.apply(cuttingVocabulary)
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
    # drawingWordCloud(lda, tf_feature_names, n_top_words)
    # drawingWordCloud(tf_feature_names)

    # pyLDAvis.show()
    pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)

    data = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)
    pyLDAvis.show(data)