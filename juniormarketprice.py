from database import SessionLocal,engine
import pandas as pd
from jse_scraper import jse_scraper
from juniormarket import JuniorMarket
import logging
import schedule
import datetime


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('scraper.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)



class JuniorMarketPrices(object):
    Instrument_Code = ''
    jse =''

    def __init__(self,Instrument_Code):
        self.Instrument_Code = Instrument_Code
        self.jse = jse_scraper(self.Instrument_Code)
        self.db = SessionLocal()


    def daily_history_table_exist(self):
        table_exist = False
        databasename = 'stock_'+self.Instrument_Code
        if engine.has_table(databasename):
            table_exist = True
            return table_exist
        else:
            logger.error(f'Table stock_{self.Instrument_Code} does not exist in database')
        return table_exist

   

    def LoadStock_data(self):
        stockcls = 'stock_{}'.format(self.Instrument_Code)
        module = __import__("models")
        stckclass = getattr(module,stockcls)
           
        if(self.daily_history_table_exist()==True):
            
            temp = self.jse.get_stockInstrument_page()
            logger.debug(f'fetching the latest prices from the JSE')
            for record in temp['Data']:
                stock = stckclass(Symbol = self.Instrument_Code, Date='', High=0,Open=0,Low=0,Close=0,Volume = 0)
                stock.Instrument = self.Instrument_Code
                stock.Timestamp = record['Date']
                results_pd = pd.to_datetime( record['Date'],unit='ms')
                stock.Date = str(results_pd)
                stock.Volume = record['Volume']
                stock.High = record['High']
                stock.Low = record['Low']
                stock.Open = record['Open']
                stock.Close = record['Close']
                                
                #create_stock(stock,Session)
                record = self.db.query(stckclass).filter_by(Timestamp =stock.Timestamp).count()
                if (record== 1):
                    logger.info(f'ohlc entry for {self.Instrument_Code}already exist.'+stock.Date)
                else:
                    self.db.add(stock)
                    self.db.commit()
                    self.db.refresh(stock) 
                    #return stock
                logger.info(f"Updating the existing database for Stock {self.Instrument_Code}")
        else:
            logger.info(f"{self.Instrument_Code}_daily_history Table does not exist")



def testscheduler():
    print('I am working form jse junior prices')

def get_juiormarketPrices():
    stock = JuniorMarketPrices('null')
    list =   stock.LoadStock_data('JuniorMarketStock_list')
    for symbols in list:
        setup = JuniorMarketPrices(symbols[0])
        logger.info(f'Loading the Price for the Junior index stock {symbols[0]}')
        setup.LoadStock_data()

   


# if __name__ == '__main__':
#     stock = JuniorMarketPrices('null')
#     JuniorMarket = JuniorMarket()
#     #stock_list = JuniorMarket.GetJuniorMarketListed()
#     #logger.info(stock_list)
#     list =   stock.LoadStock_data('JuniorMarketStock_list')
#     #stock_list = LoadStock_list()
#     for symbols in list:
#         setup = JuniorMarketPrices(symbols[0])
#         logger.info(f'Loading the Price for the Junior index stock {symbols[0]}')
#         setup.LoadStock_data()