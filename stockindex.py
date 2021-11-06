from sqlalchemy.exc import NoSuchTableError
import sqlalchemy as sa
from database import SessionLocal,Base,engine
from jse_scraper import jse_scraper
from schemas import StockBase
from schemas import BaseModel
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

class Setup_TickerModel(object):
    symbol =''
    db =''
    jse=''
    
    def __init__(self,symbol,db,jse):
        self.symbol = symbol
        self.db = db
        self.jse =jse

    def AddTickerModel(self):
        """
        This method adds a ticker to the Models files to the
        """
        classstring = '\n\nclass stock_{} (templatemodel,Base):'.format(self.symbol)
        return classstring

    def CreatestockTableName (self):
        """
        This method adds the ticker table to the 
        """
        table_name = '\n\t__tablename__ = "stock_{}"'.format(self.symbol)
        return table_name

     
    def get_model(self,stock:BaseModel):
        stock_instrument = stock.Symbol
        stockcls = 'stock_{}'.format(stock_instrument)
        module = __import__("models")
        stckclass = getattr(module,stockcls)
        return stckclass

    def AppendModelfile(self):
        class_decl = self.AddTickerModel()
        table_name = self.CreatestockTableName()
        f = open("models.py", "a")
        f.write(class_decl)
        f.write(table_name)
        f.close()
        

   
    def daily_table_Ispopulated(self,stock:BaseModel):
        stckclass = self.get_model(stock)
        records = self.db.query(stckclass.Timestamp).count()
        print(records)
        return records

    def daily_history_table_exist(self):
        table_exist = False
        databasename = 'stock_{}'.format(self.symbol)
        #module = __import__("models")
        #stckclass = getattr(module,databasename)
        #inspect(some_engine).has_table(<tablename>>
        if sa.inspect(engine).has_table(databasename):
        #if engine.dialect.has_table(engine,databasename):
            table_exist = True
            return table_exist
        return table_exist 
        
    def create_stock_class(self):
        table_exist = self.daily_history_table_exist()
        if (table_exist == False):
            self.AppendModelfile()
            logger.info(f'stock symbol {self.symbol} was added')
            return True
        else:
            logger.info('stock symbol {self.symbol} already exist')
            return False

    def LoadStock_data(self,symbol,Session):
        Session = SessionLocal()
        stockcls = 'stock_{}'.format(symbol)
        module = __import__("models")
        stckclass = getattr(module,stockcls)
        stock = stckclass(Instrument = symbol, Date='', High=0,Open=0,Low=0,Close=0,Volume = 0)
    
        #data_utility = Utility(symbol)
    
        if(self.daily_history_table_exist()==True and not (self.daily_table_Ispopulated(stock,Session) > 0)):

        
            #scrape_data = Scraper_jse(symbol)
        

            temp = self.jse.getscrape_data.get_stock_page() 
                
            for record in temp:
            #temp =  json.loads(record)
                stock.Instrument = symbol
                stock.Date = temp[record]['Date']
                stock.Volume = temp[record]['Volume']
                stock.High = temp[record]['High']
                stock.Low = temp[record]['Low']
                stock.Open = temp[record]['Open']
                stock.Close = temp[record]['Close']

                
                self.create_stock(stock,Session)
                logger.debug(f'Updating the existing database for Stock {self.symbol}')
        else:
            #scrape_data = Scraper_jse(symbol)
        #last_stock_record = daily_table_getLastStock(stock,Session)
        #last_date = last_stock_record.Date
        #today = str(date.today())
        ###'2019-03-28'
        #print(today)
            temp = self.jse.getscrape_data.get_stock_page() 
            for record in temp:
                stock.Instrument = symbol
                stock.Date = temp[record]['Date']
                stock.Volume = temp[record]['Volume']
                stock.High = temp[record]['High']
                stock.Low = temp[record]['Low']
                stock.Open = temp[record]['Open']
                stock.Close = temp[record]['Close']

                print(stock)
                self.create_stock(stock,Session)