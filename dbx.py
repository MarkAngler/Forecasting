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


def read(cursor,connection,catalogue,schema,table):

    cursor.execute(f"SELECT * from {catalogue}.{schema}.{table}")
    df = cursor.fetchall()
    columns = cursor.columns(catalogue_name=catalogue, schema_name=schema, table_name=table)
    cursor.close()
    connection.close()

    return df, columns