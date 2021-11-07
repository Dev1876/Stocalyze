import pandas as pd
from database import SessionLocal

class ohlc_Cleaner(object):
    instrument_ticker =''
    db=''
    stockclass =''

    def __init__(self,instrument_ticker):
        self.instrument_ticker = instrument_ticker
        self.db = SessionLocal()
        self.stockclass = self.get_model()
    
    def get_model(self):
        stock_instrument = self.instrument_ticker
        stockcls = 'stock_{}'.format(stock_instrument)
        module = __import__("models")
        stckclass = getattr(module, stockcls)
        return stckclass

    def create_stock_dataframe(self):
        
        data = self.db.query(self.stockclass).limit(200)
        panda_df = pd.DataFrame([(d.Date,d.Open, d.High, d.Low, d.Close,d.Volume) for d in data],columns=['Date','Open', 'High', 'Low', 'Close','Volume'])
        
        panda_df['Date'] = pd.to_datetime(panda_df.Date)
        panda_df.set_index("Date",inplace=True)
        print(panda_df.info())
        #panda_df = pd.read_sql([(stock.Date,stock.Open,stock.High,stock.Low,stock.Close)for stock in query],columns=['Date','Open', 'High', 'Low', 'Close'])
        #panda_dataframe = pd.read_sql_query(query,self.db.bind,index_col="Date")

       # panda_dataframe.reindex(columns=['Instrument','Date','Open','High','Low','Close'])
       # print("===========================================================================>")
        #print(panda_df.head(5))
        return panda_df
