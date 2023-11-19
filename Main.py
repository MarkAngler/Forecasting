import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import beta
import matplotlib.pyplot as plt
import dbx as dbx
import tsTransforms as tsf

st.title('Forecasting With Nixtla')

data = None
df = None


configuration, results = st.columns(2)

with configuration:
    connType = st.selectbox("Select connection type", ('Parquet', 'Databricks SQL'))

    if connType == 'Parquet':
        data = st.file_uploader('Upload your parquet file', accept_multiple_files=False, type=['parquet'])

    if connType == 'Databricks SQL':
        dbxSqlHost = st.text_input('hostname')
        dbxSqlHTTPS = st.text_input('https')
        dbxCatalogue = st.text_input('catalogue')
        dbxSchema = st.text_input('schema')
        dbxSqlPAT = st.text_input('PAT', type='password')

    if data is not None:
        if connType == ['Parquet']:
            df = pd.read_parquet(data)
            st.write(df)


        if df is not None:
            st.write(df.describe())
            dfColumns = df.columns.values.tolist()
            unique_id = st.selectbox("Select unique id", dfColumns)
            ds = st.selectbox("Select date column", dfColumns)
            y = st.selectbox("Select target column", dfColumns)

            # https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html
            if ds is not None:
                df[ds] = pd.to_datetime(df[ds])

                df.sort_values(by=['unique_id', 'ds'], inplace=True)

                dsFreq = pd.infer_freq(df[ds])
                
                if dsFreq is None:
                    st.write('Unable to infer frequency of date column, please input manually')
                    dsFreq = st.text_input('Frequency', value='M')
                    st.button("Set Freq", type="primary")
                    if st.button:
                        df = tsf.tsGaps(df, dsFreq)

                # redundant
                # else: 
                #     df = tsf.tsGaps(df, dsFreq)

                    

                
            



with results:
    'empty'
