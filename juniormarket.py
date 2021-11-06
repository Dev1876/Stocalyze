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

class JuniorMarket(object):
    junior_index = 'JuniorMarketStock_list'
    jse =''

    def __init__(self):
        self.db = SessionLocal()
        self.jse = jse_scraper("null")
        self.tickermodel='' 
        
       

    def GetJuniorMarketListed(self):
        '''
        Method the get the list of stored Junior Market ticker symbol form the database
        '''
        juniorMarket = 'juniormarket_list'
        module = __import__("models")
        stockClass_list = getattr(module,juniorMarket)
        logging.info(f'Getting the list of Junior market stocks stored in the local Db')
        record = self.db.query(stockClass_list.Instrument_Code).all()
        return record

    def get_model(self,ticker_symbol):
        stock_instrument = ticker_symbol
        stockcls = 'Stock_{}'.format(stock_instrument)
        module = __import__("models")
        stckclass = getattr(module,stockcls)
        return stckclass

    def AddJuniorMarket_Index(self):
        logging.info('Syncing the local db list of junior stocks to that of JSE')
        juniorMarket = 'juniormarket_{}'.format('list')
        module = __import__("models")
        main_stockClass_list = getattr(module,juniorMarket)
        #main_index = main_stockClass_list()
        listing = self.jse.get_Junior_listedCompany_page()
        
        jse_listing_count = len(listing)
        db_record_count = self.db.query(main_stockClass_list).count()

        if(jse_listing_count != db_record_count):
            for ticker in listing:
                if ticker['Type'] == 'ORDINARY' and ticker['Instrument_Code']!='MUSIC':
                    #junior_stock = self.get_model(ticker['Instrument_Code'])
                    stock = main_stockClass_list(Name=ticker['Name'],Instrument_Code=ticker['Instrument_Code'],Currency=ticker['Currency'],Sector=ticker['Sector'],Type=ticker['Type'])
                    record = self.db.query(main_stockClass_list).filter_by(Instrument_Code =stock.Instrument_Code).count()
                    if(record == 0):
                        self.db.add(stock)
                        self.db.commit()
                        self.db.refresh(stock)
                        logger.info(f'Stock{stock.Instrument_Code} was Newly Added')
                        logger.info(f'Stock{stock.Instrument_Code} SQL alchemy model is being generated')
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
    logger.info(".... Creating/updating the Junior Index stock locally")
    setup = JuniorMarket()
    record = setup.GetJuniorMarketListed()
    if len(record) == 0:
        setup.AddJuniorMarket_Index()
    else:
        setup.AddJuniorMarket_Index()
    
