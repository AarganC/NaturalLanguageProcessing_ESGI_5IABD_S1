import glob
import nltk
import heapq
import pandas as pd

from langdetect import detect
from nltk.corpus import stopwords


if __name__ == "__main__":
    corpus = []
    path = '../../files/Company_folder_files_clean/*/*.txt'
    files = glob.glob(path)
    Nb_files = 0

    for file in files:
        # print(file)
        f = open(file, 'r', encoding="ISO-8859-1")
        tmp = f.read()
        if tmp != '' and detect(tmp) == "en":
            corpus.append(tmp)
            Nb_files += 1
        f.close()

    print("Nb_files = {}".format(Nb_files))

    final_sentences = []
    f = open("resultat/CGU_EN.txt", "a")
    for sentence in corpus:
        sentences = nltk.sent_tokenize(sentence)

        # print(sentences[:5])

        clean_sentences = [sentence.lower() for sentence in sentences]
        clean_sentences = pd.Series(clean_sentences).str.replace("[^a-zA-Zàâçéèêëîïôûùüÿñæœ]", " ")

        for text in clean_sentences:
            f.write(str(text) + "\n")

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
    f.close()

    print(str(2))

    wordfreq = {}
    for sentences in final_sentences:
        for sentence in sentences:
            if sentence != "":
                if detect(sentence) == "en":
                    tokens = nltk.word_tokenize(sentence)
                    for token in tokens:
                        if len(token) > 1:
                            if token not in wordfreq.keys():
                                wordfreq[token] = 1
                            else:
                                wordfreq[token] += 1

    print(3)

    most_freq = heapq.nlargest(200, wordfreq, wordfreq.get)
    f = open("resultat/top_word_en.txt", "a")
    for word in most_freq:
        f.write(str(word) + " " + str(wordfreq[word]) + "\n")
    f.close()
