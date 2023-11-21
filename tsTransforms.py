import pandas as pd
from utilsforecast.preprocessing import fill_gaps


def tsGaps(df, dsFreq):
    df = fill_gaps(df, dsFreq)
    return df

