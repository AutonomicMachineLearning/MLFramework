import sqlite3
from pandas import DataFrame
import pandas as pd
import numpy as np
import os.path
import json

database = 'db.sqlite3'

def extract_model_sequence(dir):
    # Load file(executable keras script)
    dir = "media/" + str(dir) 
    fr = open(dir, 'rt', encoding='UTF8')

    seqeunce_of_layers = ''

    # Read data from file line by line and Extract layer sequence
    for line in fr:
        if (line.find('Sequential()') is not -1):
            seqeunce_of_layers += line.lstrip()

        if (line.find('model.add') is not -1):
            seqeunce_of_layers += line.lstrip()
          
    seqeunce_of_layers += '\n'
    
    # Return computing resouce
    fr.close()
    
    return seqeunce_of_layers


# Function :: Add header
def add_header():
    src_data = ''
    src_data += 'from keras.layers import *\n'
    src_data += 'from keras.models import Sequential\n\n'
    
    return src_data

import subprocess
import tensorflow       # 실제 web 서버에서는 지원X  --> 임시
import json
from static.script.CNNGraphModel_test import mapping
# 실행가능한 python 파일을 불러와서 graph.json 파일로 변환하는 함수
def code2diagram(dir):
    # Extract Model from executable python code.
    layer_info = add_header()
    layer_info += extract_model_sequence(dir)
    layer_info += 'json = model.to_json()\n'
    layer_info += 'fw = open("C:/Users/Rosenblatt/Desktop/model.json", "w")\n'
    layer_info += 'fw.write(json)\n'
    layer_info += 'fw.close()\n'
    print(layer_info)

    # Save as a python script
    fw = open("C:/Users/Rosenblatt/Desktop/convert_to_json.py", "w")
    # fw = open("convert_to_json.ipynb", "w")
    fw.write(layer_info)
    fw.close()

    # Call and Run "convert_to_json.py"
    subprocess.call('python  C:/Users/Rosenblatt/Desktop/convert_to_json.py', shell='True')

    mapping()

    dir = "C:/Users/Rosenblatt/Desktop/graph.json"
    json_data = open(dir).read()    # 파일을 읽어온다

    data = json.loads(json_data)    # 파일을 JSON형태로 불러온다(파싱)
    # data = str(data)                # convert json to string
    print(data)

    return data


<<<<<<< HEAD
=======

>>>>>>> 482236f8f85831ba515214b518197ad8b82f3b72
# json file을 읽어와서 DB에 저장
def createAndInsert_json(dir):
    dir = "media/" + str(dir)
    json_data = open(dir).read()    # 파일을 읽어온다

    data = json.loads(json_data)    # 파일을 JSON형태로 불러온다(파싱)
    # data = str(data)                # convert json to string
    print(data)

    return data

    # data = pd.read_csv(dir)
    # rowdata = data  #출력 갯수 제한 없음
    # # rowdata = data.head(10000)  #출력 갯수 제한 10000개
    # colCNT = (data.shape)  # (row, columns)
    # CNT= colCNT[1] # 컬럼 수

    # tableName = getTableName(dir)
    # create_table(tableName, data, CNT)
    # insert_table(tableName, rowdata, CNT)


def createAndInsert(dir):
    dir = "media/" + str(dir)

    data = pd.read_csv(dir)
    rowdata = data  #출력 갯수 제한 없음
    # rowdata = data.head(10000)  #출력 갯수 제한 10000개
    colCNT = (data.shape)  # (row, columns)
    CNT= colCNT[1] # 컬럼 수

    tableName = getTableName(dir)
    create_table(tableName, data, CNT)
    insert_table(tableName, rowdata, CNT)


def getTableName(dir):
    dir = str(dir)                  # 경로를 string타입으로 변환
    tablenm, tableext = os.path.splitext(dir) # 파일경로 및 확장 추출
    nm = tablenm.split("/")[-1]     # 테이블 이름

    return nm

################### 검색결과로 나온 파일명을 인자로 받아서 확장자를 제거하는 함수
def getDatasetNameFromList(selectedList):
    datasetList = list()
    for record in selectedList:
        record = str(record)
        record = record.split("'")[1]
        record = record.split(".")[0]
        datasetList.append(record)

    return datasetList

def selectData_(tableName):
    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        # create projects table
        cur = conn.cursor()

        # SQL 쿼리 실행
        query = "SELECT * FROM " + tableName + " limit 10"
        cur.execute(query)

        # 데이타 Fetch
        rows = (cur.fetchall())

    else:
        print("Error! cannot create the database connection.")

    conn.close()

    return rows


#############################################
#############################################
#############################################
def selectData(tableName):
    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        try:
            # create projects table
            cur = conn.cursor()

            # SQL 쿼리 실행
            query = "SELECT * FROM " + tableName + " limit 10"  # 10개만 가져온다
            cur.execute(query)

            # 데이타 Fetch
            rows = (cur.fetchall())

        except sqlite3.Error as e:
            print(e)
            conn.close()
            rows = None

    else:
        print("Error! cannot create the database connection.")

    return rows
#############################################
#############################################
#############################################
def selectDataListName(tableName):
    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        try:
            # create projects table
            cur = conn.cursor()

            # SQL 쿼리 실행
            query = "SELECT document FROM " + tableName
            cur.execute(query)

            # 데이타 Fetch
            rows = (cur.fetchall())

        except sqlite3.Error as e:
            print(e)
            conn.close()
            rows = None

    else:
        print("Error! cannot create the database connection.")
    return rows
#############################################
#############################################
#############################################
def create_table(tableName, data, CNT):
    dfield =[] #컬럼명

    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        # 컬럼 생성
        for c in range(CNT):
            dfield.append(data.columns[c])
        ###################
        ## 테이블 생성
        ##################
        query = 'CREATE TABLE IF NOT EXISTS ' + tableName + ' ( '
        for c in range(CNT):
            if(c == CNT-1):
                query = query + dfield[c] + " text"
            else:
                query = query + dfield[c] + " text, "

        query = query + ');'

        try:
            c = conn.cursor()
            c.execute(query)
        # Exception
        except sqlite3.Error as e:
            print(e)
    else:
        print("Error! cannot create the database connection.")

    conn.close()



def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file, timeout=60)
        return conn
    except sqlite3.Error as e:
        print("connect", e)
    return None


def insert_table(tableName, insertdata, CNT):
    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        try:
            iris_list = []
            iris_list = pd.DataFrame(insertdata)


            c = conn.cursor()

            # prepare statement query문 생성
            query = "insert into " + tableName + " values ("

            for i in range(1, CNT):
                query += "?, "

            query += "?)"

            c.executemany(query, iris_list.values)
            conn.commit()

        # Exception
        except sqlite3.Error as e:
            print (e)
    else:
        print("Error! cannot create the database connection.")

    conn.close()


def getColumnName(tableName):
    con = create_connection(database)
    cur = con.cursor()
    query = "SELECT * FROM " + tableName
    cur.execute(query)
    result = cur.fetchall()

    names = list(map(lambda x: x[0], cur.description))

    con.close()

    return names


######################## for test main
"""
#def main():
   # create a database connection
    conn = create_connection(database)
    if conn is not None:
        # create projects table
        create_table(conn)
        insert_table(conn, rowdata)

    else:
        print("Error! cannot create the database connection.")


    m = my_custom_sql("abc")

    conn.close()
"""

#############################################
#############################################
#############################################
def select_loss(epoch):
    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        try:
            # create projects table
            cur = conn.cursor()

            # SQL 쿼리 실행
            query = "SELECT loss FROM " + "Loss" + " WHERE epoch = '" + str(epoch) + "'"
            print(query)
            cur.execute(query)

            # 데이타 Fetch
            rows = (cur.fetchall())

        except sqlite3.Error as e:
            print(e)
            conn.close()
            rows = None

    else:
        print("Error! cannot create the database connection.")

    return rows


#############################################
#############################################
#############################################
def select_accuracy(epoch):
    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        try:
            # create projects table
            cur = conn.cursor()

            # SQL 쿼리 실행
            query = "SELECT accuracy FROM " + "Accuracy" + " WHERE epoch = '" + str(epoch) + "'"
            cur.execute(query)

            # 데이타 Fetch
            rows = (cur.fetchall())

        except sqlite3.Error as e:
            print(e)
            conn.close()
            rows = None

    else:
        print("Error! cannot create the database connection.")

    return rows

#############################################
#############################################
#############################################
def select_training_result(epoch):
    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        try:
            # create projects table
            cur = conn.cursor()

            # SQL 쿼리 실행
            query = "SELECT * FROM " + "mnist_train" + " WHERE epoch = '" + str(epoch) + "'"
            cur.execute(query)

            # 데이타 Fetch
            rows = (cur.fetchall())

            # print(rows)

        except sqlite3.Error as e:
            print(e)
            conn.close()
            rows = None

    else:
        print("Error! cannot create the database connection.")

    return rows

#############################################
#############################################
#############################################
def select_ETA(epoch):
    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        try:
            # create projects table
            cur = conn.cursor()

            # SQL 쿼리 실행
            query = "SELECT * FROM " + "ETA" + " WHERE epoch = '" + str(epoch) + "'"
            cur.execute(query)

            # 데이타 Fetch
            rows = (cur.fetchall())

            # print(rows)

        except sqlite3.Error as e:
            print(e)
            conn.close()
            rows = None

    else:
        print("Error! cannot create the database connection.")

    return rows

#############################################
#############################################
#############################################
def select_resource(epoch):
    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        try:
            # create projects table
            cur = conn.cursor()

            # SQL 쿼리 실행
            query = "SELECT * FROM " + "resource" + " WHERE epoch= '" + str(epoch) + "'"
            cur.execute(query)

            # 데이타 Fetch
            rows = (cur.fetchall())

            # print(rows)

        except sqlite3.Error as e:
            print(e)
            conn.close()
            rows = None

    else:
        print("Error! cannot create the database connection.")

    return rows


#############################################
#############################################
#############################################
def select_result_accuracy():
    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        try:
            # create projects table
            cur = conn.cursor()

            # SQL 쿼리 실행
            query = "SELECT * FROM " + "mnist_train"
            cur.execute(query)

            # 데이타 Fetch
            rows = (cur.fetchall())

            # print(rows)

        except sqlite3.Error as e:
            print(e)
            conn.close()
            rows = None

    else:
        print("Error! cannot create the database connection.")

    return rows
