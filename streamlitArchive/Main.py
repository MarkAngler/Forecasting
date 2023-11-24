import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import beta
import matplotlib.pyplot as plt
import dbx as dbx
import tsTransforms as tsf
from databricks import sql
import os
import selectionLists as sl
import statsForecast as sf
import multiprocessing


if multiprocessing.current_process().name != "MainProcess":
    pass
if __name__ == "__main__":
    st.title('Forecasting With Nixtla')

    if 'data' not in st.session_state:
        st.session_state['data'] = None

    if 'df' not in st.session_state:
        st.session_state['df'] = None

    if 'columnNames' not in st.session_state:
        st.session_state['columnNames'] = None

    if 'frequencyDict' not in st.session_state:
        st.session_state['frequencyDict'] = sl.frequency_dict

    if 'dsInferredFreq' not in st.session_state:
        st.session_state['dsInferredFreq'] = None

    if 'stats' not in st.session_state:
        st.session_state['stats'] = None

    if 'forecast' not in st.session_state:
        st.session_state['forecast'] = None

    if 'train' not in st.session_state:
        st.session_state['train'] = None

    if 'test' not in st.session_state:
        st.session_state['test'] = None

    configuration, results = st.columns(2)

    with configuration:
        connType = st.selectbox("Select connection type", ('Parquet', 'Databricks SQL'))

        if connType == 'Parquet':
            st.session_state['data'] = st.file_uploader('Upload your parquet file', accept_multiple_files=False, type=['parquet'])

        if connType == 'Databricks SQL':
            dbxSqlHost = st.text_input('hostname')
            dbxSqlHTTPS = st.text_input('https')
            dbxCatalogue = st.text_input('catalogue')
            dbxSchema = st.text_input('schema')
            dbxTable = st.text_input('table')
            dbxSqlPAT = st.text_input('PAT', type='password')
            filters = st.text_input('optional filters', None)
            
            getTable = st.button('Get Table')
            if getTable:
                conn, cursor = dbx.connect(dbxSqlHost, dbxSqlHTTPS, dbxCatalogue, dbxSqlPAT)
                st.session_state['columnNames'] = dbx.getColumns(cursor, dbxCatalogue,dbxSchema, dbxTable)

        if st.session_state['columnNames'] is not None:
            unique_id = st.selectbox("Select unique id", st.session_state['columnNames'])
            ds = st.selectbox("Select date column", st.session_state['columnNames'])
            y = st.selectbox("Select target column", st.session_state['columnNames'])

        
            getData = st.button('Get Data')        
            if getData:
                with st.spinner('Wait for it...'):        
            
                    if connType == 'Parquet':
                        st.session_state['df'] = pd.read_parquet(st.session_state['data'])

                    elif connType == 'Databricks SQL':
                        conn, cursor = dbx.connect(dbxSqlHost, dbxSqlHTTPS, dbxCatalogue, dbxSqlPAT)
                        st.session_state['data'] = dbx.read(conn, cursor, dbxCatalogue,dbxSchema, dbxTable, unique_id, ds, y, filter=filters)
                        st.session_state['df'] = pd.DataFrame(st.session_state['data'], columns=['unique_id','ds','y'])
                    
                    st.write(st.session_state['df'])
            

            if st.session_state['df'] is not None:
                st.session_state['df']['ds'] = pd.to_datetime(st.session_state['df']['ds'])

                st.session_state['df'].sort_values(by=['unique_id', 'ds'], inplace=True)

                if st.session_state['dsInferredFreq'] is None:
                    st.session_state['dsInferredFreq'] = pd.infer_freq(st.session_state['df']['ds'])
                    st.write(f"Frequency: {st.session_state['dsInferredFreq']}")


                if st.session_state['dsInferredFreq'] is None:
                    st.write('Unable to infer frequency of date column, please input manually')

                    dsFreq = st.selectbox('Select Freq', list(st.session_state['frequencyDict'].keys()))


                    setFreqButton = st.button("Set Freq", type="primary")
                    if setFreqButton:
                        st.session_state['df'] = tsf.tsGaps(st.session_state['df'], dsFreq)
                        st.write(st.session_state['df'])
                else:
                    dsFreq = st.session_state['dsInferredFreq']

                
                if dsFreq is not None:
                    forecast = st.button('Forecast')
                    if forecast:
                        st.session_state['train'], st.session_state['test'] = tsf.splitDf(st.session_state['df'], 12)
                        st.write(st.session_state['train']), st.write(st.session_state['test'])

                        print('trying sf')
                        st.session_state['stats'] = sf.statsForecast(st.session_state['train'], season_length=12, freq=dsFreq)
                        st.session_state['fit'] = st.session_state['stats'].fit(st.session_state['train'])
                        # st.session_state['forecast'] = st.session_state['stats'].predict(h=12)

    with results:
        if st.session_state['forecast'] is not None:
            st.session_state['stats'].plot(st.session_state['test'], st.session_state['forecast'], engine='plotly')

