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
path = '/Users/chanez/Documents/ESGIE 5IABD/TALN(Langage Naturel)/Projet/NaturalLanguageProcessing_ESGI_5IABD_S1-master/Company_folder_files_clean/*/*.txt'
files = glob.glob(path)
for file in files:
    f=open(file, 'r')
    tmp = f.read()
    if tmp != '' and detect(tmp) == "fr":
        corpus.append(tmp)
    f.close()

final_sentences = []
for sentence in corpus:
    sentences = nltk.sent_tokenize(sentence)

    #print(sentences[:5])

    clean_sentences = []
    clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Zàéêèç]", " ") # ("/^[a-zàâçéèêëîïôûùüÿñæœ .-]*$/i" , " ")
    clean_sentences = [sentence.lower() for sentence in clean_sentences]



    stop_words_fr = stopwords.words('french')
    stop_words_en = stopwords.words('english')
    def remove_stopwords_fr(sen):
        sen_new = " ".join([i for i in sen if i not in stop_words_fr])
        return sen_new

    def remove_stopwords_en(sen):
        sen_new = " ".join([i for i in sen if i not in stop_words_en])
        return sen_new

    clean_sentences = [remove_stopwords_fr(r.split()) for r in clean_sentences]
    clean_sentences = [remove_stopwords_en(r.split()) for r in clean_sentences]
    final_sentences.append(clean_sentences)
    #print(final_sentences)

#print(str(2) + str(type(final_sentences)))




wordfreq = {}
for sentences in final_sentences:
    for sentence in sentences:
        if detect(sentence) == "fr":
            tokens = nltk.word_tokenize(sentence)
            for token in tokens:
                if token not in wordfreq.keys():
                    wordfreq[token] = 1
                else:
                    wordfreq[token] += 1



most_freq = heapq.nlargest(200, wordfreq, wordfreq.get)




#Repertoire à changer
for sentences in final_sentences:
    for sentence in sentences:
        if detect(sentence) == "fr":
            f = open("/Users/chanez/Documents/ESGIE 5IABD/TALN(Langage Naturel)/Projet/NaturalLanguageProcessing_ESGI_5IABD_S1-master/modele/GloVe-master/CGU_FR.txt", "w")
            f.write("\n" +str(sentences))
        f.close()

#Optionnel
import collections

# Create counter

count_frequency = collections.Counter(wordfreq)

count_frequency_most=count_frequency.most_common(200)

f = open("resultat/top_word.txt", "w")
#f.write(str(most_freq))
f.writelines(str(count_frequency_most))
f.close()
#print(*count_frequency_most, sep = "\n")
