import re
import time
import requests
import tldextract
import numpy as np
import pandas as pd
import nltk
import re
import networkx as nx

from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from selenium import webdriver
from bs4 import BeautifulSoup
from urlextract import URLExtract
from flask import Flask, jsonify, request, Response


def remove_stopwords(sen, stop_words):
    sen_new = " ".join([i for i in sen if i not in stop_words])
    return sen_new

def summarization(corpus: str, resultat: str):
    sentences = sent_tokenize(corpus)

    print("Debug - a")

    word_embeddings = {}
    f = open('../modele/Aargan/ressources/multilingual_embeddings.fr', encoding='utf8')
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        word_embeddings[word] = coefs
    f.close()

    print("Debug - b")

    clean_sentences = []
    clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Zàéêèç]" , " ")
    clean_sentences = [sentence.lower() for sentence in clean_sentences]
    clean_sentences = [sentence for sentence in clean_sentences if sentence != "" and sentence != " "]

    print("Debug - c")

    stop_words = stopwords.words('french')

    clean_sentences = [remove_stopwords(r.split(), stop_words) for r in clean_sentences]

    print("Debug - d")

    sentence_vectors = []
    for i in clean_sentences:
        if len(i) != 0:
            v = sum([word_embeddings.get(w, np.zeros((300,))) for w in i.split()])/(len(i.split()) + 0.001)
        else:
            v =np.zeros((300,))
        sentence_vectors.append(v)

    print("Debug - e")

    sim_mat = np.zeros([len(sentences), len(sentences)])
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,300), sentence_vectors[j].reshape(1, 300))[0,0]

    print("Debug - f")

    nx_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(nx_graph)

    print("Debug - g")

    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    for i in range(10):
        resultat += str(ranked_sentences[i][1])

    print("Debug - h")

    return resultat


app = Flask(__name__)

@app.route('/api/extraction')
def scraper():
    url = request.args.get('url', type=str)
    # session = requests.Session()
    def generate():
        print(url)
        extract = tldextract.TLDExtract()
        extract_url = "://www."
        if extract(url).subdomain != "":
            extract_url += extract(url).subdomain + "."
        if extract(url).domain != "":
            extract_url += extract(url).domain + "."
            domain = extract(url).domain
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
        all_href=[]
        for soup in soups:
            for link in soup.findAll('a'):
                all_href.append(str(link.get('href')))

        print("Debug - 3")

        # Récupère les pages supplémentaires si il y a
        regex_url = re.compile(
            r'^(?:http|https)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        regex_path = re.compile(r'^(?:/?|[/?]\S+)$', re.IGNORECASE)

        all_href=list(dict.fromkeys(all_href))

        for link in all_href:
            if 'cookie' in link or 'cookies' in link or 'data' in link or 'donnees' in link:
                if re.match(regex_url, link):
                    if extract(link).domain == domain:
                        print('Url - ' + str(link))
                        # tmp_page = requests.get(link)
                        driver.get(link)
                        # print("\n\n\n" + link + str(driver.page_source))
                        soups.append(BeautifulSoup(driver.page_source, 'html.parser'))
                elif re.match(regex_path, link):
                    for prot in ["http", "https"]:
                        tmp_url = prot + extract_url
                        try:
                            print('Path - ' + str(link))
                            # tmp_page = requests.get(tmp_url)
                            tmp_url = str(tmp_url + link)
                            driver.get()
                            # print("\n\n\n" + tmp_url + str(driver.page_source))
                            soups.append(BeautifulSoup(driver.page_source, 'html.parser'))
                        except:
                            pass

        print("Debug - 4")

        body_text_after=""
        for soup in soups:
            # Récupère le corp du text
            body_element = soup.body

            # Suppresion des balises de script, noscript, style & footer
            string_body = str(body_element)
            list_script = list(body_element.find_all('script'))
            list_noscript = list(body_element.find_all('noscript'))
            list_style = list(body_element.find_all('style'))
            list_footer = list(body_element.find_all('footer'))
            list_suppression = list_script + list_noscript + list_style + list_footer
            for el in list_suppression:
                string_body = string_body.replace(str(el),"")
            soup2 = BeautifulSoup(string_body, 'html.parser')
            body_text_after += str(soup2.get_text()).strip().replace('\n\n','\n') + "\n"

        print("Debug - 5")

        # Debut du retour html
        yield '<h2>Scrapper</h2>'
        # Prediction
        print("Debug - 6")
        f = open("../files/cgu_figaro_full.txt", "w")
        f.write(str(body_text_after))
        f.close()
        summariz = ""
        summariz = summarization(body_text_after, summariz)

        # Envoi de la prediction sur le html
        print("Debug - 7")
        yield summariz

    return Response(generate(), mimetype='text/html')





if __name__ == "__main__":
    app.run(debug=True)
