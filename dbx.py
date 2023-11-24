from databricks import sql
import os

def splitConnString(connString):
    connString = connString.split(';')        
    return connString


def connect(connString,token):
    connString = splitConnString(connString)
    connection = sql.connect(
                        server_hostname = connString[0],
                        http_path = connString[1],
                        catalog=connString[2],
                        access_token = token)

    cursor = connection.cursor()
    return connection, cursor

def getColumns(cursor, catalogue, table):
    cursor.execute(f"SELECT * FROM {catalogue}.{table} LIMIT 1")

    column_names = [description[0] for description in cursor.description]


    return column_names


def read(connection, cursor, catalogue, schema, table, unique_id,ds,y,filter=None):


    if filter != None:
        query = f"SELECT * FROM {catalogue}.{schema}.{table} WHERE {filter}"
        cursor.execute(query)
    else:
        query = f"SELECT {unique_id},{ds}, sum({y}) as y  FROM {catalogue}.{schema}.{table} group by all"
        cursor.execute(query)


    df = cursor.fetchall()

    connection.close()
    cursor.close()

    return df