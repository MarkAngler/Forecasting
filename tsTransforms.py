import pandas as pd



def tsGaps(df):
    df = df.groupby('unique_id').resample(dsFreq, on='ds').sum().reset_index()
    df['y'] = df['y'].fillna(0)
    return df