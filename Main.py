import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import beta
import matplotlib.pyplot as plt

st.title('Forecasting With Nixtla')

configuration, results = st.columns(2)

with configuration:
    connType = st.multiselect("Select connection type", ['Parquet', 'Databricks SQL'])

    if connType == ['Parquet']:
        data = st.file_uploader('Upload your parquet file', accept_multiple_files=False, type=['parquet'])

    if connType == ['Databricks SQL']:
        st.write('Databricks SQL not yet implemented')

    if data is not None:
        df = pd.read_parquet(data)
        st.write(df)

with results:
    'empty'
