import pandas as pd
from utilsforecast.preprocessing import fill_gaps


def tsGaps(df, dsFreq):
    
    df = fill_gaps(df, dsFreq)

    df = df.fillna(0)

    return df

def splitDf(df,horizon):
    Y_test_df  = df.groupby('unique_id').tail(horizon)
    Y_train_df = df.drop(Y_test_df.index)
    return Y_train_df, Y_test_df