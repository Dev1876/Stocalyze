from database import SessionLocal
from jse_scraper import jse_scraper
from stockindex import Setup_TickerModel
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

class MainMarket(object):
    main_index = 'MainMarketStock'
    Instrument_Code = ''
    jse =''
    

    def __init__(self):
        self.db = SessionLocal()
        self.jse = jse_scraper(self.Instrument_Code)
        self.tickermodel = Setup_TickerModel(self.Instrument_Code,self.db,self.jse)
 

    def LoadMainMarketListed(self):
        '''
        Method the get the list of stored Main Market ticker symbol form the database
        '''
        mainMarket = 'mainmarket_list'
        module = __import__("models")
        stockClass_list = getattr(module,mainMarket)
        record = self.db.query(stockClass_list.Instrument_Code).all()
        return record


    def AddMainMarket_Index(self):
        """
        Method to get the list of Main Market Index and then update he local database
        """
        mainMarket = 'mainmarket_list'
        module = __import__("models")
        main_stockClass_list = getattr(module,mainMarket)
        #main_index = main_stockClass_list()
        listing = self.jse.get_Main_listedCompany_page()
        
        jse_listing_count = len(listing)
        db_record_count = self.db.query(main_stockClass_list).count()

        if(db_record_count!=49):
            for ticker in listing:
                if ticker['Type'] == 'ORDINARY':
                    #junior_stock = self.get_model(ticker['Instrument_Code'])
                    stock = main_stockClass_list(Name=ticker['Name'],Instrument_Code=ticker['Instrument_Code'],Currency=ticker['Currency'],Sector=ticker['Sector'],Type=ticker['Type'])
                    record = self.db.query(main_stockClass_list).filter_by(Instrument_Code =stock.Instrument_Code).count()
                    if(record == 0):
                        self.db.add(stock)
                        self.db.commit()
                        self.db.refresh(stock)
                        logger.info(f'The Stock {stock.Instrument_Code}==> Was Newly Added')
                        self.tickermodel = Setup_TickerModel(ticker['Instrument_Code'],self.db,self.jse) 
                        self.tickermodel.create_stock_class()
                       ## self.tickermodel = self.tickermodel.create_stock_class()
                    else:
                        print(stock.Instrument_Code+'{}'.format("==> was already Added"))
                else:
                   print(ticker['Instrument_Code']+'This is not an ORDINARY STOCK')
        else:
             print("Records on the Junior listing matches that of the database")



if __name__ == '__main__':
    
    setup = MainMarket()
    
    logger.info(".... Creating/updating the Main Index stock locally")
    record = setup.LoadMainMarketListed()
    if len(record) == 0:
        setup.AddMainMarket_Index()
    else:
         setup.AddMainMarket_Index()