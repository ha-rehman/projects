import os

import numpy as np
import pickle
import string
import pandas as pd
import argparse

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

import io
from io import StringIO

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import comtypes.client


def convert2txt(demofile):
    alltexts = []
    with open(demofile, 'rb') as fh:
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, laparams=laparams)
        fp = open(demofile, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                      check_extractable=True):
            interpreter.process_page(page)

        text = retstr.getvalue()
        alltexts.append(text)
        fp.close()
        device.close()
        retstr.close()

    return alltexts


def preprocessing(textdata):
    # Feature engineering to get the data in right format
    dfdemo = pd.DataFrame(textdata, columns=['Data'])
    dfdemo['Data'] = dfdemo['Data'].apply(lambda x: " ".join(x.lower() for x in x.split()))  # lower case conversion
    dfdemo['Data'] = dfdemo['Data'].str.replace('[^\w\s]', '')  # getting rid of special characters
    dfdemo['Data'] = dfdemo['Data'].str.replace('\d+', '')  # removing numeric values from between the words
    dfdemo['Data'] = dfdemo['Data'].apply(lambda x: x.translate(string.digits))  # removing numerical numbers
    stop = stopwords.words('english')
    dfdemo['Data'] = dfdemo['Data'].apply(
        lambda x: " ".join(x for x in x.split() if x not in stop))  # removing stop words
    stemmer = WordNetLemmatizer()
    dfdemo['Data'] = [stemmer.lemmatize(word) for word in dfdemo['Data']]
    return dfdemo

def testing(demofile):
    textdata = convert2txt(demofile)
    dfdemo = preprocessing(textdata)

    tf1 = pickle.load(open("tfidf1.pkl", 'rb'))
    inputs = pd.DataFrame(tf1.transform(dfdemo['Data']).toarray())

    savedmodel1 = pickle.load(open('rfmodel.pkl', 'rb'))
    savedmodel2 = pickle.load(open('nbmodel.pkl', 'rb'))
    savedmodel3 = pickle.load(open('xgmodel.pkl', 'rb'))

    output_category1 = savedmodel1.predict(inputs)
    output_category2 = savedmodel2.predict(inputs)
    output_category3 = savedmodel3.predict(inputs)

    encoder = LabelEncoder()
    encoder.classes_ = np.load('classes.npy', allow_pickle=True)

    output_category1 = (encoder.inverse_transform((output_category1)))
    output_category2 = (encoder.inverse_transform((output_category2)))
    output_category3 = (encoder.inverse_transform((output_category3)))

    print("The category of document with Random Forest model is: ", output_category1)
    print("The category of document with Naive Bayes model is: ", output_category2)
    print("The category of document with XG Boost model is: ", output_category3)


def get_file_path(path, flag):

    wdFormatPDF = 17
    if path.endswith('.pdf'):
        demo_path = path
        return demo_path
    elif path.endswith('.docx') or path.endswith('.docx'):
        word = comtypes.client.CreateObject('Word.Application')
        doc = word.Documents.Open(os.path.abspath(path))
        abs_path = os.path.abspath(path + '.pdf')
        doc.SaveAs(path + '.pdf', FileFormat=wdFormatPDF) if flag else doc.SaveAs(abs_path, FileFormat=wdFormatPDF)
        demo_path = path + '.pdf'
        doc.Close()
        word.Quit()
        return demo_path
    else:
        print("Invalid Format")
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str)
    parser.add_argument('--abs', default=False, type=bool)
    args = parser.parse_args()

    path = args.path
    flag = args.abs
    demo_path = get_file_path(path, flag)

    testing(demo_path) if demo_path else print("Kindly, pass the document in doc/docx or odf format")

