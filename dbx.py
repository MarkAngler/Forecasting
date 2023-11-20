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


def read(connection, cursor, catalogue, schema, table):
    cursor.execute(f"SELECT * FROM {catalogue}.{schema}.{table} LIMIT 1")

    column_names = [description[0] for description in cursor.description]

    cursor.execute(f"SELECT * FROM {catalogue}.{schema}.{table}")
    df = cursor.fetchall()

    connection.close()
    cursor.close()

    return df, column_names