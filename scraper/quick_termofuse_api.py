import tldextract
import numpy as np
import pandas as pd
import re
import networkx as nx
import logging

from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from selenium import webdriver
from bs4 import BeautifulSoup
from langdetect import detect
from flask import Flask, request, Response


def remove_stopwords(sen, stop_words):
    sen_new = " ".join([i for i in sen if i not in stop_words])
    return sen_new


def summarization(corpus: str, lang: str, resultat: list):
    sentences = sent_tokenize(corpus)
    sentences = list(dict.fromkeys(sentences))

    print("Debug - a")
    print("Langue = {}".format(lang))

    word_embeddings = {}
    if lang == "fr":
        f = open('../modele/Aargan/ressources/multilingual_embeddings.fr', encoding='utf8')
    elif lang == "en":
        f = open('../modele/Aargan/ressources/glove.6B.100d.txt', encoding='utf8')
    else:
        f = "error"
        resultat = "Error language '{}' is not supported".format(lang)

    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        word_embeddings[word] = coefs
    f.close()

    vector_size = len(word_embeddings[list(word_embeddings)[0]])
    print("vector_size = {}".format(vector_size))

    print("Debug - b")

    clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Zàéêèç]", " ")
    clean_sentences = [sentence.lower() for sentence in clean_sentences]
    clean_sentences = [sentence for sentence in clean_sentences if sentence != "" and sentence != " "]

    print("Debug - c")

    if lang == "fr":
        stop_words = stopwords.words('french')
    elif lang == "en":
        stop_words = stopwords.words('english')
    else:
        stop_words = ""
        pass

    clean_sentences = [remove_stopwords(r.split(), stop_words) for r in clean_sentences]

    print("Debug - d")

    sentence_vectors = []
    for i in clean_sentences:
        if len(i) != 0:
            v = sum([word_embeddings.get(w, np.zeros((vector_size,))) for w in i.split()]) / (len(i.split()) + 0.001)
        else:
            v = np.zeros((vector_size,))
        sentence_vectors.append(v)

    print("Debug - e")

    sim_mat = np.zeros([len(sentences), len(sentences)])
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1, vector_size),
                                                  sentence_vectors[j].reshape(1, vector_size))[0, 0]

    print("Debug - f")

    nx_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(nx_graph)

    print("Debug - g")

    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    for i in range(10):
        resultat.append(str(ranked_sentences[i][1]))

    print("Debug - h")

    return resultat


app = Flask(__name__)


@app.route('/api/extraction')
def scraper():
    url = request.args.get('url', type=str)

    # session = requests.Session()

    def generate():

        logging.basicConfig()

        print(url)
        extract = tldextract.TLDExtract()
        extract_url = ""
        domain = extract(url).domain
        if extract(url).subdomain != "":
            extract_url += extract(url).subdomain + "."
        if extract(url).domain != "":
            extract_url += extract(url).domain + "."
        if extract(url).suffix != "":
            extract_url += extract(url).suffix

        print("Debug - 1")
        # Scraper
        soups = []
        # page = session.get(url)
        driver = webdriver.Chrome()
        driver.get(url)
        soups.append(BeautifulSoup(driver.page_source, 'html.parser'))

        print("Debug - 2")

        # Récupère les liens href dans le corpus
        all_href = []
        for soup in soups:
            for link in soup.findAll('a'):
                all_href.append(str(link.get('href')))

        print("Debug - 3")

        # Récupère les pages supplémentaires si il y a
        regex_url = re.compile(
            r'^(?:http|https)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        regex_path = re.compile(r'^(?:/?|[/?]\S+)$', re.IGNORECASE)

        all_href = list(dict.fromkeys(all_href))

        for link in all_href:
            link = link.lower()
            if 'cookie' in link or 'cookies' in link or 'data' in link or 'données' in link or 'donnée' in link \
                    or 'donnees' in link or 'mention' in link or 'légales' in link or 'mentions' in link or \
                    'légale' in link or 'legale' in link or 'legal' in link or 'termofuse' in link or 'term' in link \
                    or 'cgu' in link or 'policies' in link:
                if re.match(regex_url, link):
                    if extract(link).domain == domain:
                        print('Url - ' + str(link))
                        # tmp_page = requests.get(link)
                        driver.get(link)
                        # print("\n\n\n" + link + str(driver.page_source))
                        soups.append(BeautifulSoup(driver.page_source, 'html.parser'))
                elif re.match(regex_path, link):
                    for prot in ["http", "https", "", "http://www.", "https://www.", "http://", "https://"]:
                        tmp_url = prot + extract_url
                        for tmp in [tmp_url, "", prot]:
                            try:
                                print('Path - ' + str(tmp + link))
                                tmp_url = str(tmp + link)
                                driver.get(tmp_url)
                                soups.append(BeautifulSoup(driver.page_source, 'html.parser'))
                                raise RuntimeError('Bad stuff happened.')
                            except Exception:
                                logging.error('Failed.', exc_info=True)

        print("Debug - 4")

        body_text_after = ""
        for soup in soups:
            # Suppresion des balises de script, noscript, style & footer
            string_body = str(soup.body)
            list_script = list(soup.body.find_all('script'))
            list_noscript = list(soup.body.find_all('noscript'))
            list_style = list(soup.body.find_all('style'))
            list_footer = list(soup.body.find_all('footer'))
            list_suppression = list_script + list_noscript + list_style + list_footer
            for el in list_suppression:
                string_body = string_body.replace(str(el), "")
            soup2 = BeautifulSoup(string_body, 'html.parser')
            body_text_after += str(soup2.get_text()).strip().replace('\n\n', '\n') + "\n"

        print("Debug - 5")

        # Debut du retour html
        yield '<h2>Scrapper</h2>'
        # Prediction
        print("Debug - 6")
        summariz = []
        lang = detect(body_text_after)
        summariz = summarization(body_text_after, lang, summariz)

        # Envoi de la prediction sur le html
        print("Debug - 7")
        for x in summariz:
            yield "<p>" + str(x)

    return Response(generate(), mimetype='text/html')


if __name__ == "__main__":
    app.run(debug=True)
