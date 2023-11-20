from databricks import sql
import os
import streamlit as st

def connect(host,path,catalogue,token):
    connection = sql.connect(
                        server_hostname = host,
                        http_path = path,
                        catalog=catalogue,
                        access_token = token)

    cursor = connection.cursor()
    

    return connection, cursor

def getColumns(cursor, catalogue, schema, table):
    cursor.execute(f"SELECT * FROM {catalogue}.{schema}.{table} LIMIT 1")

    column_names = [description[0] for description in cursor.description]


    return column_names


def read(connection, cursor, catalogue, schema, table, unique_id,ds,y,filter=None):


    if filter != None:
        query = f"SELECT * FROM {catalogue}.{schema}.{table} WHERE {filter}"
        cursor.execute(query)
    else:
        query = f"SELECT {unique_id},{ds}, sum({y}) as y  FROM {catalogue}.{schema}.{table} group by all"
        cursor.execute(query)

    st.write(query)

    df = cursor.fetchall()

    connection.close()
    cursor.close()

    return df