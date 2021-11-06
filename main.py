from os import name
from fastapi import FastAPI,status,HTTPException
from database import SessionLocal, engine
from pydantic import BaseModel
from typing import List, Optional,List
import models
import schemas


app = FastAPI()

db = SessionLocal()


@app.get('/juniortmarket',response_model=List[schemas.juniormarket],status_code=200)
def get_juniormarketlisting():
    juniorlisting = db.query(models.juniormarket_list).all()
    return juniorlisting

@app.get('/juniormarket/{juniormarket_id}',response_model=schemas.juniormarket,status_code=status.HTTP_200_OK)
def get_an_juniormarket_stock(juniormarket_id:int):
    juniormarket_stock = db.query(models.juniormarket_list).filter(models.juniormarket_list.id==juniormarket_id).first()
    return juniormarket_stock

@app.post('/juniormarket',response_model=schemas.juniormarket,status_code=status.HTTP_201_CREATED)
def add_juniormarket_stock(juniormarket:schemas.juniormarket):

    stockexist = db.query(models.juniormarket_list).filter(schemas.juniormarket.Name == juniormarket.Name).first()

    if stockexist is not None:
        raise HTTPException(status_code=400,detail="Stock Already exist")


    new_jnrmrkt_stock = models.juniormarket_list(
        Name = juniormarket.Name,Instrument_Code = juniormarket.Instrument_Code,Currency = juniormarket.Currency,Sector = juniormarket.Sector,Type = juniormarket.Type
    )
   
    

    db.add(new_jnrmrkt_stock)
    db.commit()
    return new_jnrmrkt_stock


@app.put('/juniormarket/{juniormarket_id}',response_model=schemas.juniormarket,status_code=status.HTTP_200_OK)
def update_juniormarket_stock(juniormarket_id:int,jnrmrketstock:schemas.juniormarket):
    stock_to_update = db.query(models.juniormarket_list).filter(models.juniormarket_list.id==juniormarket_id).first()
    stock_to_update.name = jnrmrketstock.Name
    stock_to_update.Instrument_Code = jnrmrketstock.Instrument_Code
    stock_to_update.Currency = jnrmrketstock.Currency
    stock_to_update.Sector = jnrmrketstock.Sector
    stock_to_update.Type = jnrmrketstock.Type

    db.commit()
    return stock_to_update

@app.delete('/juniormarket/{juniormarket_id}',response_model=schemas.juniormarket,status_code=status.HTTP_200_OK)
def delete_juniormarket_stock(juniormarket_id:int):
    junior_stock_delete = db.query(models.juniormarket_list).filter(models.juniormarket_list.id==juniormarket_id).first()
    if junior_stock_delete is None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resource Not Found")


    db.delete(junior_stock_delete)
    db.commit()

    return junior_stock_delete



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
