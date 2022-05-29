from utils import read_pdf
import pickle
import mysql.connector
import pandas as pd

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

    with open("support_txt_files/vocabulary_remoterepo.txt", "r") as file:
        vocabulary = eval(file.readline())

    Tfidmodel =pickle.load(
        open('pickels/tfid_remoterepo.pkl', 'rb'))

    traineddata = Tfidmodel.A
    return traineddata, Tfidmodel, df_news, vocabulary