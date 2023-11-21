import pandas as pd



def tsGaps(df, dsFreq):
    df.set_index('ds', inplace=True)
    df = df.groupby('unique_id').resample(dsFreq).sum()

    # Reset the index - the group keys will be added as columns
    df.reset_index(inplace=True)

    # Fill NaN values in 'y' column
    df['y'] = df['y'].fillna(0)

    return df
