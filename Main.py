import streamsync as ss
import dbx
import pandas as pd
import tsTransforms as ts
import selectionLists as sl
import statsForecast as sf

# This is a placeholder to get you started or refresh your memory.
# Delete it or adapt it as necessary.
# Documentation is available at https://streamsync.cloud

def update_dataSourceStateEle(state,payload):
    # state["dataSourceStateEle"] = payload
    if state["dataSourceStateEle"] == 'parquet':
        state["uploadFileVisible"] = True
        state['dbxConnVisible'] = False
    elif state["dataSourceStateEle"] == 'databricks':
        state['dbxConnVisible'] = True
        state["uploadFileVisible"] = False

def dbxConnect(state):
    state["dbxConnectionMessage"] = True
    try:
        # dbx.connect(state['dbxJdbcStateEle'],state['dbxPat'])
        state['dbxHost'], state['dbxHttpPath'], state['dbxCatalog'] = dbx.splitConnString(state['dbxJdbcStateEle'])
        state['_dbxConn'], state['_dbxCursor'] = dbx.connect(state['dbxJdbcStateEle'],state['dbxPat'])
        state['dbxConnectionStateMessage'] = "+Connected"
        state['dbxConnected'] = True
    except Exception as e:
        state['dbxConnectionStateMessage'] = f"-{str(e)}"

def dbxGetTableColumns(state):
    dbxTableColumns = dbx.getColumns(state['_dbxCursor'],state['dbxCatalog'] ,state['dbxSchemaTableStateEle'])
    columnDict = {}
    for column in dbxTableColumns:
        columnDict[column] = column
    state['TableColumns'] = columnDict
    state['selectColumnsVisible'] = True

def dbxGetTableData(state):
    dfList = dbx.read(state['_dbxConn'], 
                           state['_dbxCursor'], 
                           state['dbxCatalog'], 
                           state['dbxSchemaTableStateEle'], 
                           state['unique_id'], 
                           state['ds'], 
                           state['y'])
    state['df'] = pd.DataFrame(dfList, columns=['unique_id','ds','y'])
    state['dfVisible'] = True

def setDfFreq(state):
    state['df'] = ts.tsGaps(state['df'],state['dsFreq'])

def evaluate(state):
    state['dfTrain'], state['dfTest'] = ts.splitDf(state['df'],state['horizon'])
    sForecastEval = sf.statsForecast(state['dfTrain'],season_length=12,freq='M')
    state['dfTestForecast'] = sForecastEval.forecast(h=state['horizon'])
    state['dfTestForecast'] = state['dfTestForecast'].merge(state['dfTest'], on=['ds', 'unique_id'], how='inner')

    dfAggregated = state['dfTestForecast'].groupby(['ds']).sum().reset_index()

    jsonAggregated = dfAggregated.to_dict(orient='records')

    state['jsonTestForecast'] = {
        "data":[ 
            {
                'x': [record['ds'] for record in jsonAggregated],
                'y': [record['y'] for record in jsonAggregated],
                'mode': 'lines',
                'type': 'scatter'
            }
        ]
    }

    state['dfTestForecastVisible'] = True




def predict(state):
    pass

initial_state = ss.init_state({
    "my_app": {
        "title": "Forecasting With Nixtla"
    },
    "errorMessages": None,
    "uploadFileVisible": False,
    "dataSourceStateEle": None,
    "dfVisible": False,
    "dbxConnVisible": False,
    "dbxJdbcStateEle": None,
    "dbxPat": None,
    "_dbxCursor": None,
    "_dbxConn": None,
    "dbxConnectionStateMessage":None,
    "dbxConnected": False,
    "dbxConnectionMessage": None,
    "dbxSchemaTableStateEle": None,
    "dbxHost": None,
    "dbxHttpPath": None,
    "dbxCatalog": None,
    "TableColumns": None,
    "selectColumnsVisible": False,
    "ds": None,
    "unique_id": None,
    "y": None,
    "df": None,
    "dfTrain": None,
    "dfTest": None,
    "dfTestForecastVisible": False,
    "dfTestForecast": None,
    "jsonTestForecast": None,
    "dsFreqSelectionList": sl.frequency_dict,
    "dsFreq": 'M',
    "horizon": 6,
    
})



