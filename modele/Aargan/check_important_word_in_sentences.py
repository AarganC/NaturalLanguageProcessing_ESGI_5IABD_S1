import glob
import errno
import re
import nltk
import heapq
import sys
import numpy as np
import pandas as pd

from langdetect import detect
from nltk.corpus import stopwords

corpus = []
path = '../../files/Company_folder_files_clean/*/*.txt'
files = glob.glob(path)

for file in files:
    f=open(file, 'r')
    tmp = f.read()
    if tmp != '' and detect(tmp) == "fr":
        corpus.append(tmp)
    f.close()

sentences = []
for sentence in corpus:
    sentences.append(nltk.sent_tokenize(sentence))

print(sentences[:1])

clean_sentences = []
clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Zàéêèç]", " ") # ("/^[a-zàâçéèêëîïôûùüÿñæœ .-]*$/i" , " ")
clean_sentences = [print(sentence) for sentence in clean_sentences]

print(clean_sentences[:1])

stop_words = stopwords.words('french')
def remove_stopwords(sen):
    sen_new = " ".join([i for i in sen if i not in stop_words])
    return sen_new

clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]

print(2)

wordfreq = {}
for sentence in clean_sentences:
    tokens = nltk.word_tokenize(sentence)
    for token in tokens:
        if token not in wordfreq.keys():
            wordfreq[token] = 1
        else:
            wordfreq[token] += 1

print(3)

most_freq = heapq.nlargest(200, wordfreq, wordfreq.get)
print(most_freq[:10])
