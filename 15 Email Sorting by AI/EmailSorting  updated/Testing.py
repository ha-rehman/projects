import os
import numpy as np
import pickle
import string
import pandas as pd
import argparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import io
from io import StringIO
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import warnings
warnings.filterwarnings("ignore")

# uncomment these lines to download libraries in first attempt only!
# nltk.download('stopwords')
# nltk.download('omw-1.4')
# nltk.download('wordnet')

def Predict_mail(sample):
    dfdemo = pd.DataFrame([sample], columns=['Content'])

    dfdemo['Content'] = dfdemo['Content'].apply(
        lambda x: " ".join(x.lower() for x in x.split()))  # lower case conversion
    dfdemo['Content'] = dfdemo['Content'].str.replace('[^\w\s]', ' ')  # getting rid of special characters
    dfdemo['Content'] = dfdemo['Content'].str.replace('\d+', '')  # removing numeric values from between the words
    dfdemo['Content'] = dfdemo['Content'].apply(lambda x: x.translate(string.digits))  # removing numerical numbers
    stop = stopwords.words('english')
    dfdemo['Content'] = dfdemo['Content'].apply(
        lambda x: " ".join(x for x in x.split() if x not in stop))  # removing stop words

    tf1 = pickle.load(open("tfidf1.pkl", 'rb'))
    inputs = pd.DataFrame(tf1.transform(dfdemo['Content']).toarray())

    savedmodel1 = pickle.load(open('rfmodel.pkl', 'rb'))
    savedmodel2 = pickle.load(open('nbmodel.pkl', 'rb'))
    savedmodel3 = pickle.load(open('xgmodel.pkl', 'rb'))

    output_category1 = savedmodel1.predict(inputs)
    output_category2 = savedmodel2.predict(inputs)
    output_category3 = savedmodel3.predict(inputs)

    predictions = [output_category1, output_category2, output_category3]
    # final_prediction = max(predictions, key=predictions.count)
    final_prediction = output_category2

    encoder = LabelEncoder()
    encoder.classes_ = np.load('classes.npy', allow_pickle=True)

    index = final_prediction[0]
    label = encoder.inverse_transform(output_category1)[0]
    return index, label


if __name__ == '__main__':
    index, label = Predict_mail("Team,      A contribution of $900k has been just made to the rothstrsut acount tbxlokm909. please ivest today.Best,Akshay C. PatelBank of America Merrill Lynch")
    print("Index of Targeted Email", index)
    print("Class of Targeted Email", label)