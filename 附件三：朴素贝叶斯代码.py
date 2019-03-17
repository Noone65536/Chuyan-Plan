import pandas as pd
import jieba
from sklearn.feature_extraction.text import CountVectorizer


df = pd.read_csv(r'E:\demo\test3.csv',encoding='utf-8')   # 打开数据集CSV文件
df.head()
df.shape()          # 这些东西在jupyter上都是直接输出的，在一般的python中怎么办？


def chinese_word_cut(mytext):
    return" ".join(jieba.cut(mytext))


X = df[['comment']]
Y = df.sentiment
X.shape
X.head()
X['cutted_comment'] = X.comment.apply(chinese_word_cut)
X.cutted_comment[:5]
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, random_state=1)
X_train.shape
X_test.shape


def get_custom_stopwords(stop_words_file):
    with open(stop_words_file) as f:
        stopwords = f.read()
    stopwords_list = stopwords.split('\n')
    custom_stopwords_list = [i for i in stopwords_list]
    return custom_stopwords_list


stop_words_file = "E:\demo\stopwordsHIT.txt"
stopwords = get_custom_stopwords(stop_words_file)
stopwords[-10:]
vect = CountVectorizer()
term_matrix = pd.DataFrame(vect.fit_transform(X_train.cutted_comment).toarray(), columns=vect.get_feature_names())
term_matrix.head()
term_matrix.shape
vect = CountVectorizer(stop_words=frozenset(stopwords))
term_matrix = pd.DataFrame(vect.fit_transform(X_train.cutted_comment).toarray(), columns=vect.get_feature_names())
term_matrix.head()
max_df = 0.8
min_df =vect = CountVectorizer(max_df = max_df,
                       min_df = min_df,
                       token_pattern=u'(?u)\\b[^\\d\\W]\\w+\\b',
                       stop_words=frozenset(stopwords))

term_matrix = pd.DataFrame(vect.fit_transform(X_train.cutted_comment).toarray(), columns=vect.get_feature_names())
term_matrix.head()

from sklearn.naive_bayes import MultinomialNB
nb = MultinomialNB()

from sklearn.pipeline import make_pipeline
pipe = make_pipeline(vect, nb)

pipe.steps
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import cross_val_score

cross_val_score(pipe, X_train.cutted_comment, Y_train, cv=5, scoring='accuracy').mean()
pipe.fit(X_train.cutted_comment, Y_train)
pipe.predict(X_test.cutted_comment)
y_pred = pipe.predict(X_test.cutted_comment)
from sklearn import metrics
metrics.accuracy_score(Y_test, y_pred)
metrics.confusion_matrix(Y_test, y_pred)
