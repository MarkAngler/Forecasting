from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA
from statsforecast.models import *
import tsTransforms as tsf


    # Croston(),
    # DOT(season_length=season_length)

def statsForecast(df,season_length=12,freq='M'):


    models = [
    # AutoARIMA(season_length=season_length),
    # HoltWinters(),
    # SeasonalNaive(season_length=season_length),
    HistoricAverage()
    ]



    sf = StatsForecast(df=df, 
    models=models,
    freq=freq, 
    n_jobs=-1,
    fallback_model = SeasonalNaive(season_length=season_length))

    # sf.fit(df)
    # sf.predict(h=horizon, level=[95])

    # forecasts = sf.forecast(horizon=horizon, level=[95])

    return sf