import pandas as pd
import tsTransforms as tsf
import numpy as np

# function that tests there are no timeseries gaps in the data
def test_df_no_gaps(df):
    df = pd.DataFrame({'ds':pd.date_range(start='2019-01-01', end='2019-12-01', freq='M')})
    df['y'] = np.random.randint(0,100, size=(len(df)))
    df = df.append({'ds':pd.to_datetime('2019-03-01'), 'y':np.nan}, ignore_index=True)
    df = tsf.tsGaps(df, 'M')
    assert df.isnull().values.any() == False