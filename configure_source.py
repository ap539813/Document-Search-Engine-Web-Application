import mysql.connector

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
