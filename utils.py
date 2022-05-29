from bs4 import BeautifulSoup
import requests
import os
import PyPDF2
import urllib
import io
import re
import json 
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nlp_processor import gen_vector_T
from nlp_processor import word_tokenize
from nlp_processor import wordLemmatizer
from nlp_processor import cosine_sim
import nltk

nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')


def get_page_text(url):
    return BeautifulSoup(requests.get(url).text, "html.parser").get_text()

def get_page_links(url):
    links = []
    for item in BeautifulSoup(requests.get(url).text, "html.parser").find_all('a'):
        try:
            if 'http' in item.get_attribute_list('href')[0]:
                links.append(item.get_attribute_list('href')[0])
            else:
                links.append(url + item.get_attribute_list('href')[0])
        except:
            pass
    return links

def read_pdf(loc):
    print(loc)
    docs = os.listdir(loc)

    titles = []
    content = []
    for file in docs:
        pdfFileObj = open(loc + file, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        p_cnt = 0
        try:
            text = pdfReader.getPage(p_cnt).extractText().replace('\n', ' ').replace('  ', '').lower()
            while len(text) < 1000:
                print('in loop')
                text = pdfReader.getPage(p_cnt).extractText().replace('\n', ' ').replace('  ', '').lower()
                p_cnt += 1
            else:
                titles.append(loc + file)
                content.append(text)
        except:
            pass
    return titles, content

def read_pdf_online(links):
    titles = []
    content = []
    for file in links:
        try:
            remote_file_bytes = io.BytesIO(urllib.request.urlopen(urllib.request.Request(file)).read())
            pdfReader = PyPDF2.PdfFileReader(remote_file_bytes)
            p_cnt = 0
            text = pdfReader.getPage(p_cnt).extractText().replace('\n', ' ').replace('  ', '').lower()
            while len(text) < 1000:
                print(f'in loop {len(text)}')
                text = pdfReader.getPage(p_cnt).extractText().replace('\n', ' ').replace('  ', '').lower()
                p_cnt += 1
            else:
                titles.append(file)
                content.append(text)
        except:
            text = get_page_text(file).replace('\n', ' ').replace('  ', '').lower()
            while len(text) < 1000:
                print('in loop')
                text = get_page_text(file).replace('\n', ' ').replace('  ', '').lower()
            else:
                titles.append(file)
                content.append(text)
    return titles, content

    
def MakeQuery(query, vocabulary, df_news, traineddata):
    preprocessed_query = preprocessed_query = re.sub(
        "\W+", " ", query.lower()).strip()
    tokens = word_tokenize(str(preprocessed_query))
    q_df = pd.DataFrame(columns=['q_clean'])
    q_df.loc[0, 'q_clean'] = tokens
    q_df['q_clean'] = wordLemmatizer(q_df.q_clean)
    q_df = q_df.replace(to_replace="'", value='', regex=True)
    q_df = q_df.replace(to_replace="\[", value='', regex=True)
    q_df = q_df.replace(to_replace=" ", value='', regex=True)
    q_df = q_df.replace(to_replace='\]', value='', regex=True)

    d_cosines = []
    tfidf = TfidfVectorizer(vocabulary=vocabulary , dtype=np.float32)
    tfidf.fit(q_df['q_clean'])
    query_vector = gen_vector_T(q_df['q_clean'], tfidf, vocabulary)
    for d in traineddata:
        d_cosines.append(cosine_sim(query_vector, d))
    out = np.array(d_cosines).argsort()[-10:][::-1]
   
    d_cosines.sort()

    a = pd.DataFrame()
    for i, index in enumerate(out):
        a.loc[i, 'Subject'] = df_news['Subject'][index]
    for j, simScore in enumerate(d_cosines[-10:][::-1]):
        a.loc[j, 'Score'] = simScore
    a = a.sort_values(by='Score', ascending=False)
    js = a.to_json(orient='index')
    js =js.replace('[', '').replace(']', '')
    ls = js.split('},')

    l = [re.sub(r'\"[0-9]\":', '', l) for l in ls]
    l[0] = re.sub(r'^{{1}', '', l[0])      
    l = [re.sub(r'^,{1}', '', l) for l in l]
    l = [ls+'}' for ls in l]
    l[-1] = l[-1].replace('}}', '')
    lsDrug =[]
    count = 0
    for txt in l:
        if count < 5:
            tx =json.loads(txt)
            lsDrug.append(tx)
            count += 1
        else:
            break
    return lsDrug 
