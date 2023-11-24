import streamsync as ss
import dbx

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
    try:
        # dbx.connect(state['dbxJdbcStateEle'],state['dbxPat'])
        state['dbxHost'], state['dbxHttpPath'], state['dbxCatalog'] = dbx.splitConnString(state['dbxJdbcStateEle'])
        state['_dbxConn'], state['_dbxCursor'] = dbx.connect(state['dbxJdbcStateEle'],state['dbxPat'])
        state['dbxConnectionStateMessage'] = "+Connected"
        state['dbxConnected'] = True
    except Exception as e:
        state['dbxConnectionStateMessage'] = f"-{str(e)}"

def dbxGetTableColumns(state):
    state['dbxTableColumns'] = dbx.getColumns(state['_dbxCursor'],state['dbxCatalog'] ,state['dbxSchemaTableStateEle'])


initial_state = ss.init_state({
    "my_app": {
        "title": "Forecasting With Nixtla"
    },
    "errorMessages": None,
    "uploadFileVisible": False,
    "dataSourceStateEle": None,
    "dbxConnVisible": False,
    "dbxJdbcStateEle": None,
    "dbxPat": None,
    "_dbxCursor": None,
    "_dbxConn": None,
    "dbxConnectionStateMessage":None,
    "dbxConnected": False,
    "dbxSchemaTableStateEle": None,
    "dbxHost": None,
    "dbxHttpPath": None,
    "dbxCatalog": None,
    "dbxTableColumns": None,
    
})



