from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA



def statsForecast(df):
    sf = StatsForecast(
    models = [AutoARIMA(season_length = 12)],
    freq = 'M'
)

    sf.fit(df)
    sf.predict(h=12, level=[95])

    return sf