from subprocess import Popen, PIPE
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io
from io import StringIO
import os
import glob
import docx
import comtypes.client
import sys
import string
import pickle
import numpy as np
import argparse
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import comtypes.client
from sklearn import preprocessing

import warnings

warnings.filterwarnings('ignore')

import nltk

nltk.download('wordnet')


def convert_word_to_pdf(file_location):
    files_list = os.listdir(file_location)
    doc_collection = []
    # Traversing through all the files in the location to find the doc files
    for file in files_list:
        file_path = os.path.join(file_location, file)
        doc_collection.append(file_path)
    for x in doc_collection:
        if x.endswith('.docx') or x.endswith('.doc'):
            word = comtypes.client.CreateObject('Word.Application')
            doc = word.Documents.Open(os.path.abspath(x))
            doc.SaveAs(os.path.abspath(x + '.pdf'), FileFormat=wdFormatPDF)
            doc.Close()
            word.Quit()


def convert_pdf_to_txt(path):
    file_list = os.listdir(path)
    document_collection = []
    for file in file_list:
        file_path = os.path.join(path, file)
        document_collection.append(file_path)
    for i_file in document_collection:
        if i_file.endswith('.pdf') or i_file.endswith('.PDF'):  # different extensions on the raw data
            with open(i_file, 'rb') as fh:
                for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
                    resource_manager = PDFResourceManager()
                    fake_file_handle = io.StringIO()
                    converter = TextConverter(resource_manager, fake_file_handle)
                    page_interpreter = PDFPageInterpreter(resource_manager, converter)
                    page_interpreter.process_page(page)

                    text = fake_file_handle.getvalue()  # extraction of the text data
                    yield text

                    # closing open handles
                    converter.close()
                    fake_file_handle.close()


def get_pdf_text(classes):
    frames = []
    for class_item in classes:
        filelocation = os.path.join('data/', class_item)

        textcontents = convert_pdf_to_txt(filelocation)
        dftaxes = pd.DataFrame(textcontents, columns=['Text_Data'])
        dftaxes['Category'] = class_item  # Adding the label

        dftaxes['Text_Data'] = dftaxes['Text_Data'].apply(
            lambda x: " ".join(x.lower() for x in x.split()))  # lower case conversion
        dftaxes['Text_Data'] = dftaxes['Text_Data'].str.replace('[^\w\s]', '')  # getting rid of special characters
        dftaxes['Text_Data'] = dftaxes['Text_Data'].str.replace('\d+',
                                                                '')  # removing numeric values from between the words
        dftaxes['Text_Data'] = dftaxes['Text_Data'].apply(
            lambda x: x.translate(string.digits))  # removing numerical numbers
        stop = stopwords.words('english')
        dftaxes['Text_Data'] = dftaxes['Text_Data'].apply(
            lambda x: " ".join(x for x in x.split() if x not in stop))  # removing stop words
        stemmer = WordNetLemmatizer()
        dftaxes['Text_Data'] = [stemmer.lemmatize(word) for word in
                                dftaxes['Text_Data']]  # converting words to their dictionary form
        dftaxes['Text_Data'] = dftaxes['Text_Data'].str.replace('shall', '')

        taxfreq = pd.Series(' '.join(dftaxes['Text_Data']).split()).value_counts()[:5]
        taxfreq.plot(kind='barh');
        # plt.show()

        t = list(pd.DataFrame(taxfreq).index)
        listToStr = ','.join(map(str, t))

        dftaxes['Identifiers'] = listToStr
        print("Top 5 words of the %s are: %s" % (class_item, listToStr))

        frames.append(dftaxes)
        print("======================================================================")
        print()
    return frames


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


def training(classes, is_pdf_missing):
    # is_pdf_missing = False  # Changed to true if you have not the document in pdf format.

    if is_pdf_missing:
        for class_item in classes:
            filelocation = os.path.join('data/', class_item)
            print("converting %s word files into pdf..." % (class_item))
            convert_word_to_pdf(filelocation)
        print("Success!")

    frames = get_pdf_text(classes)

    final_frame = pd.concat(frames, sort=False)
    final_frame = final_frame[['Identifiers', 'Text_Data', 'Category']]
    final_frame = final_frame.reset_index(drop=True)

    final_frame['Text_Data'].replace('', np.nan, inplace=True)
    final_frame.dropna(subset=['Text_Data'], inplace=True)

    plt.figure(figsize=(10, 4))
    final_frame.Category.value_counts().plot(kind='bar');
    # plt.show()

    tf_idf_converter = TfidfVectorizer(max_features=100, stop_words=stopwords.words('english'))
    tfidf = tf_idf_converter.fit(final_frame['Text_Data'])
    X = pd.DataFrame(tf_idf_converter.fit_transform(final_frame['Text_Data']).toarray())

    label_encoder = LabelEncoder()  # Converting the labels to numeric labels
    y = label_encoder.fit_transform(final_frame['Category'])

    pickle.dump(tfidf, open("tfidf1.pkl", "wb"))
    np.save('classes.npy', label_encoder.classes_)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    train_Random_forest(X_train, X_test, y_train, y_test, classes)
    train_Naive_Bayes(X_train, X_test, y_train, y_test, classes)
    train_xgBoost(X_train, X_test, y_train, y_test, classes)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--classes', action='store', dest='alist',
                        type=str, nargs='*', default=['Airports', 'Hospitals', 'Mosques', 'Museums', 'Parks', 'Schools'],
                        help='Examples: -i "item1" "item2" "item3"')
    parser.add_argument('--pdf', default=False, type=bool, help='change to true if your document is not in pdf format')
    args = parser.parse_args()
    print("\nModel will be trained on %d classes :\n" %(len(args.alist)), args.alist)

    training(args.alist, args.pdf)
