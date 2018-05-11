# coding=utf-8

import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba

# 导入数据
def cuttingVocabulary(text):
    return " ".join(jieba.cut(text))

if __name__ == '__main__':
    mytext="大家都用李老师的线代讲义 希望我能学好线性代数!都是各自科目的经典教辅~~印刷质量还不错，个人偏好宇哥的编书风格，不过线代方面还是永乐大帝更老练些~~ 客服回复及时热情还不错，应该是正品，就是赠送的课程。。哎，就知道是体验课，嘤嘤嘤"
    mytext = " ".join(jieba.cut(mytext))
    print(mytext)
    wordcloud = wordcloud().generate(mytext)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
