
from datetime import datetime
from pydantic import BaseModel

class StockBase(BaseModel):
    Instrument : str
    Date: str
    Open: float
    High: float
    Low : float
    Close:float
    volume : float

    class Config:
        orm_mode = True
   
class StockCreate(StockBase):
    pass

class Stock(StockBase):
    id : int

    class Config:
        orm_mode = True

class juniormarket(BaseModel):
    id: int 
    Name :str
    Instrument_Code : str
    Currency:str
    Sector:str
    Type:str
    class Config:
        orm_mode = True



