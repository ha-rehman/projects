# -*- coding: utf-8 -*-
"""MLP Application.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gyorDndNvH1fpTA0zj1IzqLDW1pfTHid

# [FMA: A Dataset For Music Analysis](https://github.com/mdeff/fma)
"""

!pip install numpy==1.12.1 pandas==0.19.2 matplotlib==2.0.0 seaborn==0.7.1 scikit-learn==0.18.1 tensorflow-gpu==1.0.1 Keras==1.2.2 librosa==0.5.0 audioread==2.1.4 mutagen==1.39 pydub==0.18.0

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

import os
import warnings
warnings.filterwarnings('ignore')
import IPython.display as ipd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn as skl
import sklearn.utils, sklearn.preprocessing, sklearn.decomposition, sklearn.svm, sklearn.neural_network
import librosa
import librosa.display

import utils

plt.rcParams['figure.figsize'] = (17, 5)

# Directory where mp3 are stored.
AUDIO_DIR = os.environ.get('fma_small')

# Load metadata and features.
tracks = utils.load('fma_metadata/tracks.csv')
genres = utils.load('fma_metadata/genres.csv')
features = utils.load('fma_metadata/features.csv')
echonest = utils.load('fma_metadata/echonest.csv')

np.testing.assert_array_equal(features.index, tracks.index)
assert echonest.index.isin(tracks.index).all()

tracks.shape, genres.shape, features.shape, echonest.shape

"""## 1 Metadata

The metadata table, a CSV file in the `fma_metadata.zip` archive, is composed of many colums:
1. The index is the ID of the song, taken from the website, used as the name of the audio file.
2. Per-track, per-album and per-artist metadata from the Free Music Archive website.
3. Two columns to indicate the subset (small, medium, large) and the split (training, validation, test).
"""

ipd.display(tracks['track'].head())
ipd.display(tracks['album'].head())
ipd.display(tracks['artist'].head())
ipd.display(tracks['set'].head())

"""### 1.1 Subsets

The small and medium subsets can be selected with the below code.
"""

small = tracks[tracks['set', 'subset'] <= 'small']
small.shape

medium = tracks[tracks['set', 'subset'] <= 'medium']
medium.shape

"""## 2 Genres

The genre hierarchy is stored in `genres.csv` and distributed in `fma_metadata.zip`.
"""

print('{} top-level genres'.format(len(genres['top_level'].unique())))
genres.loc[genres['top_level'].unique()].sort_values('#tracks', ascending=False)

genres.sort_values('#tracks').head(10)

"""## 3 Features

1. Features extracted from the audio for all tracks.
2. For some tracks, data colected from the [Echonest](http://the.echonest.com/) API.
"""

print('{1} features for {0} tracks'.format(*features.shape))
columns = ['mfcc', 'chroma_cens', 'tonnetz', 'spectral_contrast']
columns.append(['spectral_centroid', 'spectral_bandwidth', 'spectral_rolloff'])
columns.append(['rmse', 'zcr'])
for column in columns:
    ipd.display(features[column].head().style.format('{:.2f}'))

"""### 3.1 Echonest features"""

print('{1} features for {0} tracks'.format(*echonest.shape))
ipd.display(echonest['echonest', 'metadata'].head())
ipd.display(echonest['echonest', 'audio_features'].head())
ipd.display(echonest['echonest', 'social_features'].head())
ipd.display(echonest['echonest', 'ranks'].head())

ipd.display(echonest['echonest', 'temporal_features'].head())
x = echonest.loc[2, ('echonest', 'temporal_features')]
plt.plot(x);

"""### 3.2 Features like MFCCs are discriminant"""

small = tracks['set', 'subset'] <= 'small'
genre1 = tracks['track', 'genre_top'] == 'Instrumental'
genre2 = tracks['track', 'genre_top'] == 'Hip-Hop'

X = features.loc[small & (genre1 | genre2), 'mfcc']
X = skl.decomposition.PCA(n_components=2).fit_transform(X)

y = tracks.loc[small & (genre1 | genre2), ('track', 'genre_top')]
y = skl.preprocessing.LabelEncoder().fit_transform(y)

plt.scatter(X[:,0], X[:,1], c=y, cmap='RdBu', alpha=0.5)
X.shape, y.shape

"""## 4 Audio

You can load the waveform and listen to audio in the notebook itself.
"""

filename = utils.get_audio_path("fma_small", 5)
print('File: {}'.format(filename))

x, sr = librosa.load(filename, sr=None, mono=True)
print('Duration: {:.2f}s, {} samples'.format(x.shape[-1] / sr, x.size))

start, end = 10, 20

ipd.Audio(x, rate=sr)
# ipd.Audio(data=x[start*sr:end*sr], rate=sr)

"""And use [librosa](https://github.com/librosa/librosa) to compute spectrograms and audio features."""

librosa.display.waveplot(x, sr, alpha=0.5);
plt.vlines([start, end], -1, 1)

start = len(x) // 2
plt.figure()
plt.plot(x[start:start+2000])
plt.plot(x)
plt.ylim((-1, 1));

# stft = np.abs(librosa.stft(x, n_fft=2048, hop_length=512))
# mel = librosa.feature.melspectrogram(sr=sr, S=stft**2)
# log_mel = librosa.logamplitude(mel)

# librosa.display.specshow(log_mel, sr=sr, hop_length=512, x_axis='time', y_axis='mel');

# mfcc = librosa.feature.mfcc(S=librosa.power_to_db(mel), n_mfcc=20)
# mfcc = skl.preprocessing.StandardScaler().fit_transform(mfcc)
# librosa.display.specshow(mfcc, sr=sr, x_axis='time');

"""## 5 Genre classification

### 5.1 From features
"""

small = tracks['set', 'subset'] <= 'small'

train = tracks['set', 'split'] == 'training'
val = tracks['set', 'split'] == 'validation'
test = tracks['set', 'split'] == 'test'

y_train = tracks.loc[small & train, ('track', 'genre_top')]
y_test = tracks.loc[small & test, ('track', 'genre_top')]
X_train = features.loc[small & train, 'mfcc']
X_test = features.loc[small & test, 'mfcc']

print('{} training examples, {} testing examples'.format(y_train.size, y_test.size))
print('{} features, {} classes'.format(X_train.shape[1], np.unique(y_train).size))

# Be sure training samples are shuffled.
X_train, y_train = skl.utils.shuffle(X_train, y_train, random_state=42)

# Standardize features by removing the mean and scaling to unit variance.
scaler = skl.preprocessing.StandardScaler(copy=False)
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Training data distribution
display(pd.Series(y_train).value_counts())

# Test data distribution
display(pd.Series(y_test).value_counts())

scv = sklearn.

"""### **5.2 Applying the Grid Search for the MLP Algorithm**"""

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV

# Specify the hyperparameter grid
param_grid = {
            'hidden_layer_sizes': [(10,), (50,), (100,)],
            'alpha': [0.001, 0.01, 0.1],
            'learning_rate_init': [0.001, 0.01, 0.1],
            'activation':['identity', 'logistic', 'tanh', 'relu'],
            'solver':['lbfgs', 'sgd', 'adam'],
            'early_stopping':[True, False]
             }

# Create the MLP model
model = MLPClassifier(max_iter=1000)

# Create the grid search object
grid_search = GridSearchCV(model, param_grid, verbose=1, cv=5)

# Fit the grid search object to the training data
grid_search.fit(X_train, y_train.get_values())

print("The Best parameters are")
grid_search.best_params_

"""### **5.3 Displaying all Results from grid search and saving it**"""

cv_res = pd.DataFrame(grid_search.cv_results_).sort_values("rank_test_score")
display(cv_res.head())
cv_res.to_csv("cv_results.csv", index=False)

"""### **Selected Model Evaluation**"""

best_mlp = MLPClassifier(**grid_search.best_params_)
best_mlp.fit(X_train, y_train.get_values())
pred = best_mlp.predict(X_test)

from sklearn.metrics import classification_report, confusion_matrix,accuracy_score, precision_score, recall_score,r2_score, mean_squared_error, f1_score

# function for evaluation metrics precision, recall, f1 etc
def modelEvaluation(predictions, y_test_set, model_name):
    # Print model evaluation to predicted result    
    print("==========",model_name,"==========")
    print ("\nAccuracy on validation set: {:.4f}".format(accuracy_score(y_test_set, predictions)))    
    print ("\nClassification report : \n", classification_report(y_test_set, predictions))
    print ("\nConfusion Matrix : \n", confusion_matrix(y_test_set, predictions))
    plt.figure(figsize=(10,10))
    sns.heatmap(confusion_matrix(y_test_set, predictions),annot=True, fmt='g',cmap='viridis')
    plt.tight_layout()
    plt.show()
    results = [accuracy_score(y_test_set, predictions), precision_score(y_test_set, predictions, average='macro'),
              recall_score(y_test_set, predictions, average='macro'),f1_score(y_test_set, predictions, average='macro')]
    return results

modelEvaluation(pred, y_test, "Best MLP Tuned model")

