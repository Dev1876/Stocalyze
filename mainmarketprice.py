from database import SessionLocal,engine
import pandas as pd
from jse_scraper import jse_scraper
from mainmarket import MainMarket
import logging


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




class MainMarketPrices(object):
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
            logger.error('Table{} does not exist in database'.format('stock_'+self.Instrument_Code))
        return table_exist

   
    def GetMainMarketListed(self):
        '''
        Method the get the list of stored Junior Market ticker symbol form the database
        '''
        juniorMarket = 'MainMarkteStock_list'
        module = __import__("models")
        stockClass_list = getattr(module,juniorMarket)
        record = self.db.query(stockClass_list.Instrument_Code).all()
        return record

    def LoadStock_data(self):
        #Session = SessionLocal()
        stockcls = 'stock_{}'.format(self.Instrument_Code)
        module = __import__("models")
        stckclass = getattr(module,stockcls)
        if(self.daily_history_table_exist()==True):
            
            #scrape_data = self.jse(self.Instrument_Code)
        
            temp = self.jse.get_stockInstrument_page()
            logger.info(temp)
            for record in temp['Data']:
                stock = stckclass(Symbol = self.Instrument_Code, Date='', High=0,Open=0,Low=0,Close=0,Volume = 0)
                stock.Instrument = self.Instrument_Code
                stock.Timestamp = record['Date']
                results_pd = pd.to_datetime( record['Date'],unit='ms')

                stock.Date = str(results_pd)
                logger.debug(stock.Date)
                stock.Volume = record['Volume']
                stock.High = record['High']
                stock.Low = record['Low']
                stock.Open = record['Open']
                stock.Close = record['Close']
                                
                #create_stock(stock,Session)
                record = self.db.query(stckclass).filter_by(Timestamp =stock.Timestamp).count()
                if (record== 1):
                    logger.info(f'ohlc entry for {self.Instrument_Code} already exist.'+stock.Date)
                else:
                    self.db.add(stock)
                    self.db.commit()
                    self.db.refresh(stock) 
                    #return stock
                logger.info(f"Updating the existing database for Stock {self.Instrument_Code}")
        else:
            logger.info(f"stock_{self.Instrument_Code} Table does not exist")

        


if __name__ == '__main__':
    stock = MainMarketPrices('null')
    mainMarket = MainMarket()
    stock_list = mainMarket.LoadMainMarketListed()
    logger.info(stock_list)
    for symbols in stock_list:
        setup = MainMarketPrices(symbols[0])
        logger.info(f'Loading the Price for the Main index stock {symbols[0]}')
        setup.LoadStock_data()