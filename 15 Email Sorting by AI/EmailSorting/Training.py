import string
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import warnings
warnings.filterwarnings("ignore")

# uncomment these lines to download libraries in first attempt only!
# nltk.download('stopwords')
# nltk.download('omw-1.4')
# nltk.download('wordnet')

df = pd.read_csv("Results.csv")
print(df.head())

df['Content'] = df['Content'].apply(lambda x: " ".join(x.lower() for x in x.split())) # lower case conversion
df['Content'] = df['Content'].str.replace('[^\w\s]',' ') # getting rid of special characters
df['Content'] = df['Content'].str.replace('\d+\w', '') # removing numeric values from between the words
df['Content'] = df['Content'].apply(lambda x: x.translate(string.digits))  # removing numerical numbers
stop = stopwords.words('english')
df['Content'] = df['Content'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))  # removing stop words

print(df.head())
df.to_csv('clean_mails.csv', index=False)

stemmer = WordNetLemmatizer()
df['Content'] = [stemmer.lemmatize(word) for word in df['Content']]  # converting words to their dictionary form
df['Content'] = df['Content'].str.replace('shall', '')

text_freq = pd.Series(' '.join(df['Content']).split()).value_counts()[:15]
text_freq.plot(kind='barh')
plt.show()

tf_idf_converter = TfidfVectorizer(max_features=100, stop_words=stopwords.words('english'))
texts = tf_idf_converter.fit_transform(df['Content']).toarray()
X = pd.DataFrame(texts)

label_encoder = LabelEncoder()  # Converting the labels to numeric labels
y = label_encoder.fit_transform(df['label'])

pickle.dump(tf_idf_converter, open("tfidf1.pkl", "wb"))
np.save('classes.npy', label_encoder.classes_)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)


def train_Random_forest(X_train, X_test, y_train, y_test, classes):
    classifier = RandomForestClassifier(n_estimators=100, random_state=1)  # defining 1000 nodes
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    pickle.dump(classifier, open('rfmodel.pkl', 'wb'))

    print('Accuracy of Random Forest: %s' % accuracy_score(y_test, y_pred))
    print('Classification Report of Random Forest:\n', classification_report(y_test, y_pred, target_names=classes))

    conf_mat = confusion_matrix(y_true=y_test, y_pred=y_pred)
    print('Confusion matrix of Random Forest:\n', conf_mat)
    print("=============================================\n")


def train_Naive_Bayes(X_train, X_test, y_train, y_test, classes):
    clf = MultinomialNB()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    pickle.dump(clf, open('nbmodel.pkl', 'wb'))

    print('Accuracy of Naive Bayes: %s' % accuracy_score(y_test, y_pred))
    print('Classification Report of Naive Bayes:\n', classification_report(y_test, y_pred, target_names=classes))

    conf_mat = confusion_matrix(y_true=y_test, y_pred=y_pred)
    print('Confusion matrix of Naive Bayes:\n', conf_mat)
    print("=============================================\n")


def train_xgBoost(X_train, X_test, y_train, y_test, classes):
    xgb = XGBClassifier()
    xgb.fit(X_train, y_train)
    y_pred = xgb.predict(X_test)
    pickle.dump(xgb, open('xgmodel.pkl', 'wb'))

    print('Accuracy of XG Boost: %s' % accuracy_score(y_test, y_pred))
    print('Classification Report of XG Boost:\n', classification_report(y_test, y_pred, target_names=classes))

    conf_mat = confusion_matrix(y_true=y_test, y_pred=y_pred)
    print('Confusion matrix of XG Boost:\n', conf_mat)
    print("=============================================\n")


classes = list(label_encoder.classes_)
train_Random_forest(X_train, X_test, y_train, y_test, classes)
train_Naive_Bayes(X_train, X_test, y_train, y_test, classes)
train_xgBoost(X_train, X_test, y_train, y_test, classes)


