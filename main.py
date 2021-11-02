from fastapi import FastAPI
#from database import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
#import models
#from models import Stock_SVL
#from crud import get_stocklist
#from chart import stock_chart

app = FastAPI()



class Stock(BaseModel): # serializer
    id:int
    name:str
    description:str
    market: str
    signal: bool


@app.get('/')
def index():
    return{"message":"Welcome to Stocalyze"}

#models.Base.metadata.create_all(bind=engine)


@app.get('/greet/{name}')
def greet_name(name:str):
    return {"greeting":f"Hello {name}"}



@app.get('/greet')
def greet_optional_name(name:Optional[str]="user"):
    return {"message":f"Hello {name}"}
    

@app.put('/stock/{stock_id}')
def update_stock(stock_id:int,stock:Stock):
    return{'name':stock.name,
    'description':stock.description,
    'market':stock.market,
    'signal':stock.signal
    }


'''
ref : https://www.youtube.com/watch?v=xi96vi5X_Ak
'''

#templates = Jinja2Templates(directory="templates")

#stock = Stock_SVL()


# class StockRequest(BaseModel):
#     symbol: str


# def get_model(instrument):
#     stock_instrument = instrument
#     stockcls = 'Stock_{}'.format(stock_instrument)
#     module = __import__("models")
#     stckclass = getattr(module, stockcls)
#     return stckclass

# def LoadStock_list(Session):
#         Session = SessionLocal()
#         stockcls = 'Stock_{}'.format('list')
#         module = __import__("models")
#         stcklist_class = getattr(module,stockcls)
#         return stcklist_class

# def LoadStock_Jlist(Session):
#         Session = SessionLocal()
#         stockcls = 'JuniorStock_{}'.format('list')
#         module = __import__("models")
#         stcklist_class = getattr(module,stockcls)
#         return stcklist_class






# def get_db():
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()


# def fetch_stocks_data(stock: str):
#     db = Session()
#     stock_temp = db.query(stock).filter(stock.Instrument == 'SVL').first()
#     return stock_temp
#     '#db.add(stock)'
#     '#db.commit()'


# @app.get("/")
# def Home(Request: Request, db: Session = Depends(get_db)):
#     stock_filter = Request.query_params.get('filter',False)
#     """
#     displays the stock screener dashboard / homepage
#     """

#     if stock_filter =='new_closing_highs':
#         stock_svl = LoadStock_Jlist(Session)
#         stocks = db.query(stock_svl).filter(stock_svl.Type =='BULL')
#     else :
#         stock_svl = LoadStock_Jlist(Session)
#         stocks = db.query(stock_svl).all()
#         #print(stocks)
#     return templates.TemplateResponse("Mainindex.html", {
#     "request": Request,
#     "stocks": stocks
#     })

# @app.get("/stock/{symbol}")
# def stock_detail(Request:Request,symbol,db:Session=Depends(get_db)):
#     chart  = stock_chart(symbol)
#     div = chart.stock_Candlestick()
#     stock = get_model(symbol)
#     records = db.query(stock).all()
#     return templates.TemplateResponse("stock_detail.html", {
#         "request": Request,
#         "stocks": records,
#         "graph_div" : div
#     })



# @app.post("/stock")
# def create_stock(stock_request: StockRequest, db: Session = Depends(get_db)):
#     """
#     , background_task: BackgroundTasks,
#     create a stock and stores it in the database
#     """
#     stock_svl = get_model('SVL')
#     record = db.query(stock_svl).filter(stock_svl.Instrument == 'SVL').first()
#     print(record.instrument)   


#     '#background_task.add_task(fetch_stocks_data, db_stock)'
#     return {
#         "Code": "Success",
#         "Message": "Stock created"}
