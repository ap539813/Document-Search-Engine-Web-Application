import altair as alt
import numpy as np
import streamlit as st
import json 
from subprocess import call
import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd
# import numpy as np
import os
import re
import PyPDF2
import pickle
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events


import urllib
import io
from bs4 import BeautifulSoup
import requests



import mysql.connector
# import flask
# import pickle
# import json


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

def make_model_localrepo():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ap166@jmail"
    )

    print(mydb)
    cursor = mydb.cursor()

    cursor.execute('use docsearch;')

    cursor.execute('select * from datastorage;')

    extracted_items = list(cursor)

    df_news = pd.DataFrame()
    for a,b,c in extracted_items:
        if b == 3:
            loc = c
            titles, content = read_pdf(loc)

            df_temp = pd.DataFrame()
            df_temp['Subject'] = titles
            df_temp['content'] = content

            df_news = pd.concat([df_news, df_temp])


    with open("vocabulary_localrepo.txt", "r") as file:
        vocabulary = eval(file.readline())

    Tfidmodel =pickle.load(
        open('tfid_localrepo.pkl', 'rb'))

    traineddata = Tfidmodel.A
    return traineddata, Tfidmodel, df_news, vocabulary

def make_model_remoterepo():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ap166@jmail"
    )

    print(mydb)
    cursor = mydb.cursor()

    cursor.execute('use docsearch;')

    cursor.execute('select * from datastorage;')

    extracted_items = list(cursor)

    df_news = pd.DataFrame()
    for a,b,c in extracted_items:
        if b == 4:
            loc = c
            titles, content = read_pdf(loc)

            df_temp = pd.DataFrame()
            df_temp['Subject'] = titles
            df_temp['content'] = content

            df_news = pd.concat([df_news, df_temp])

    with open("vocabulary_remoterepo.txt", "r") as file:
        vocabulary = eval(file.readline())

    Tfidmodel =pickle.load(
        open('tfid_remoterepo.pkl', 'rb'))

    traineddata = Tfidmodel.A
    return traineddata, Tfidmodel, df_news, vocabulary


def make_model_weblinks():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ap166@jmail"
    )

    print(mydb)
    cursor = mydb.cursor()

    cursor.execute('use docsearch;')

    cursor.execute('select * from datastorage;')

    extracted_items = list(cursor)

    links = []
    for a,b,c in extracted_items:
        if b == 2:
            links.append(c)

    titles, content = read_pdf_online(links)

    df_news = pd.DataFrame()
    df_news['Subject'] = titles
    df_news['content'] = content

    with open("vocabulary_weblinks.txt", "r") as file:
        vocabulary = eval(file.readline())

    Tfidmodel =pickle.load(
        open('tfid_weblinks.pkl', 'rb'))

    traineddata = Tfidmodel.A
    return traineddata, Tfidmodel, df_news, vocabulary

def update_source(path, type_data):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ap166@jmail"
    )

    print(mydb)
    cursor = mydb.cursor()
    cursor.execute('use docsearch;')

    # cursor.execute(f'insert into datastorage (type, path) values({type_data}, "{path}");')
    # print(f'insert into datastorage (type, path) values({type_data}, "{path}");')

    sql = "INSERT INTO datastorage (type, path) VALUES (%s, %s)"
    val = (type_data, path)
    cursor.execute(sql, val)

    mydb.commit()

    print(cursor.rowcount, "record inserted.")





def make_model_library():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ap166@jmail"
    )

    print(mydb)
    cursor = mydb.cursor()

    cursor.execute('use docsearch;')

    #cursor = mydb.cursor()

    cursor.execute('select * from datastorage;')

    extracted_items = list(cursor)

    df_news = pd.DataFrame()
    for a,b,c in extracted_items:
        if b == 1:
            try:
                links = get_page_links(c)[15:20]
                print(links)
                titles, content = read_pdf_online(links)
                df_temp = pd.DataFrame()
                df_temp['Subject'] = titles
                df_temp['content'] = content

                df_news = pd.concat([df_news, df_temp])
            except Exception as e:
                print(e)
                pass

    with open("vocabulary_weblinks.txt", "r") as file:
        vocabulary = eval(file.readline())

    Tfidmodel =pickle.load(
        open('tfid_weblinks.pkl', 'rb'))

    traineddata = Tfidmodel.A
    return traineddata, Tfidmodel, df_news, vocabulary




def wordLemmatizer(data):
    tag_map = defaultdict(lambda: wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV
    file_clean_k = pd.DataFrame()
    for index, entry in enumerate(data):
        # Declaring Empty List to store the words that follow the rules for this step
        Final_words = []
        # Initializing WordNetLemmatizer()
        word_Lemmatized = WordNetLemmatizer()
        for word, tag in pos_tag(entry):
            # Below condition is to check for Stop words and consider only alphabets
            if len(word) > 1 and word not in stopwords.words('english') and word.isalpha():
                word_Final = word_Lemmatized.lemmatize(word, tag_map[tag[0]])
                Final_words.append(word_Final)
            # The final processed set of words for each iteration will be stored in 'text_final'
                file_clean_k.loc[index, 'Keyword_final'] = str(Final_words)
                file_clean_k.loc[index, 'Keyword_final'] = str(Final_words)
                
    return file_clean_k


def gen_vector_T(tokens, tfidf, vocabulary):
    Q = np.zeros((len(vocabulary))) 
    x = tfidf.transform(tokens)
    for token in tokens[0].split(','):
        try:
            ind = vocabulary.index(token)
            Q[ind] = x[0, tfidf.vocabulary_[token]]
        except:
            pass
    return Q


def cosine_sim(a, b):
    cos_sim = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
    return cos_sim

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




## Basic setup and app layout
st.set_page_config(layout="wide")

alt.renderers.set_embed_options(scaleFactor=2)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
results = {}
print('revisited!!')


# @st.cache
if __name__ == '__main__':
    with open('mode.txt') as file:
        mode = file.read()

    operation_mode = st.sidebar.selectbox(
        "Mode of operation",
        ("None", "Search", "Configure")
    )

    if operation_mode != 'None':
        mode = operation_mode

    if mode == 'Search':
        loc_res = {}
        rem_res = {}
        st.markdown("# Document search application")

        # stt_button = Button(label="Speak", width=100)

        # stt_button.js_on_event("button_click", CustomJS(code="""
        #     var recognition = new webkitSpeechRecognition();
        #     recognition.continuous = true;
        #     recognition.interimResults = true;
        
        #     recognition.onresult = function (e) {
        #         var value = "";
        #         for (var i = e.resultIndex; i < e.results.length; ++i) {
        #             if (e.results[i].isFinal) {
        #                 value += e.results[i][0].transcript;
        #             }
        #         }
        #         if ( value != "") {
        #             document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        #         }
        #     }
        #     recognition.start();
            
        #     """))

        # result = streamlit_bokeh_events(
        #     stt_button,
        #     events="GET_TEXT",
        #     key="listen",
        #     refresh_on_update=False,
        #     override_height=75,
        #     debounce_time=0)

        # # st.write(result)
        # if result:
        #     if "GET_TEXT" in result:
        #         st.write('search text:  ' + result.get("GET_TEXT"))
        #         query = result.get("GET_TEXT")

        # else:
        query = st.text_input("Enput the keyword")
        b = st.button('Search All')
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        col1.markdown("#### Files from web libraries")
        col2.markdown("#### Files from web links")
        col3.markdown("#### Files from local repo")
        col4.markdown("#### Files from remote repo")
        b1 = col1.button("web libraries")
        b2 = col2.button("web links")
        b3 = col3.button("local repo")
        b4 = col4.button("remote repo")

        a_file = open("data.pkl", "rb")
        results = pickle.load(a_file)
        a_file.close()
        
        # st.write(results)
        try:
            if results['library'] != []:
                for item in results['library']:
                    if item['Score'] != None:
                        # link_file = item['Subject']
                        # file_found = f"{item['Subject']}"
                        col1.success(f"{item['Subject']}")
                        # with open(file_found, "rb") as file:
                        #     btn = col1.download_button(
                        #         label='open local file',
                        #         data=file,
                        #         file_name=file_found,
                        #         mime=None)

            if results['weblinks'] != []:
                for item in results['weblinks']:
                    if item['Score'] != None:
                        col2.success(f"{item['Subject']}")
                        # file_found = f"{item['Subject']}"
                        # with open(file_found, "rb") as file:
                        #     btn = col2.download_button(
                        #         label='open local file',
                        #         data=file,
                        #         file_name=file_found,
                        #         mime=None)

            if results['local'] != []:
                for item in results['local']:
                    if item['Score'] != None:
                        file_found = f"{item['Subject']}"
                        col3.success(item['Subject'])
                        with open(file_found, "rb") as file:
                            btn = col3.download_button(
                                label='open local file',
                                data=file,
                                file_name=file_found,
                                mime=None)

            if results['remote'] != []:
                for item in results['remote']:
                    if item['Score'] != None:
                        file_found = f"{item['Subject']}"
                        col4.success(item['Subject'])
                        with open(file_found, "rb") as file:
                            btn = col4.download_button(
                                label='open remote file',
                                data=file,
                                file_name=file_found,
                                mime=None)

        except Exception as e:
            st.write(e)
            # results = {}
            pass  

        if b1 or b:
            traineddata, Tfidmodel, df_news, vocabulary = make_model_library()
            if query != '':
                results['library'] = MakeQuery(query, vocabulary, df_news, traineddata)
                if not b:
                    for key in results:
                        if key != 'library':
                            results[key] = []
                cnt_files = 0
                # col1.write(results['library'])
                for item in results['library']:
                    if item['Score'] != None:
                        link_file = item['Subject']
                        col1.success(f"{item['Subject']}")
                        cnt_files += 1
                if cnt_files == 0:
                    col1.error('### No documents matching your request')

        if b2 or b:
            # query_weblinks()
            traineddata, Tfidmodel, df_news, vocabulary = make_model_weblinks()
            if query != '':
                results['weblinks'] = MakeQuery(query, vocabulary, df_news, traineddata)
                if not b:
                    for key in results:
                        if key != 'weblinks':
                            results[key] = []
                cnt_files = 0
                # col2.write(results['weblinks'])
                for item in results['weblinks']:
                    if item['Score'] != None:
                        link_file = item['Subject']
                        col2.success(f"{item['Subject']}")
                        cnt_files += 1
                if cnt_files == 0:
                    col2.error('### No documents matching your request')
        if b3 or b:
            loc_res = {}
            traineddata, Tfidmodel, df_news, vocabulary = make_model_localrepo()
            if query != '':
                results['local'] = MakeQuery(query, vocabulary, df_news, traineddata)
                if not b:
                    for key in results:
                        if key != 'local':
                            results[key] = []
                cnt_files = 0
                for item in results['local']:
                    if item['Score'] != None:
                        loc_res[item['Subject']] = '' + item['Subject']
                        col3.success(item['Subject'])
                        with open(loc_res[item['Subject']], "rb") as file:
                            try:
                                btn = col3.download_button(
                                    label='open local file',
                                    data=file,
                                    file_name=loc_res[item['Subject']],
                                    mime=None)
                            except:
                                pass
                        
                        cnt_files += 1

                if cnt_files == 0:
                    col3.error('### No documents matching your request')
        if b4 or b:
            rem_res = {}
            traineddata, Tfidmodel, df_news, vocabulary = make_model_remoterepo()
            if query != '':
                results['remote'] = MakeQuery(query, vocabulary, df_news, traineddata)
                if not b:
                    for key in results:
                        if key != 'remote':
                            results[key] = []
                cnt_files = 0
                for item in results['remote']:
                    if item['Score'] != None:
                        with col4.container():
                            rem_res[item['Subject']] = '' + item['Subject']
                            col4.success(item['Subject'])
                            with open(rem_res[item['Subject']], "rb") as file:
                                try:
                                    btn = col4.download_button(
                                        label='open remote file',
                                        data=file,
                                        file_name=rem_res[item['Subject']],
                                        mime=None)
                                except:
                                    pass
                            cnt_files += 1
                if cnt_files == 0:
                    col4.error('### No documents matching your request')

        a_file = open("data.pkl", "wb")
        pickle.dump(results, a_file)
        a_file.close()
        with open('mode.txt', 'w') as file:
            file.write(mode)

        st.sidebar.markdown('### The proportion of the result from various resources')
        fig, ax = plt.subplots()
        sns.barplot(x = list(results.keys()), y = [len(results[item]) for item in results], ax = ax)
        st.sidebar.pyplot(fig)
            
        
    else:
        type_data = st.selectbox('Select resource type',
                             ('web library', 'web link', 'local', 'remote'))

        resource_type = ['None', 'web library', 'web link', 'local', 'remote']

        path = st.text_input("Type in the path of the resource")

        submit = st.button('Insert')

        if submit:
            update_source(path = path, type_data = resource_type.index(type_data))

        with open('mode.txt', 'w') as file:
            file.write(mode)

