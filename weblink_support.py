from utils import read_pdf_online
import pickle
import mysql.connector
import pandas as pd

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

    with open("support_txt_files/vocabulary_weblinks.txt", "r") as file:
        vocabulary = eval(file.readline())

    Tfidmodel =pickle.load(
        open('pickels/tfid_weblinks.pkl', 'rb'))

    traineddata = Tfidmodel.A
    return traineddata, Tfidmodel, df_news, vocabulary