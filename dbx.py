from databricks import sql
import os
import streamlit as st

def connect(host,path,token):
    connection = sql.connect(
                        server_hostname = host,
                        http_path = path,
                        access_token = token)

    cursor = connection.cursor()
    

    return connection, cursor

@st.cache_data
def read(cursor,connection,catalogue,schema,table):

    cursor.execute(f"SELECT * from {catalogue}.{schema}.{table}")
    df = cursor.fetchall()

    cursor.close()
    connection.close()

    return df