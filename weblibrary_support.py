from utils import read_pdf_online, get_page_links
import pickle
import mysql.connector
import pandas as pd

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

    with open("support_txt_files/vocabulary_weblinks.txt", "r") as file:
        vocabulary = eval(file.readline())

    Tfidmodel =pickle.load(
        open('pickels/tfid_weblinks.pkl', 'rb'))

    traineddata = Tfidmodel.A
    return traineddata, Tfidmodel, df_news, vocabulary
