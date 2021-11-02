from sqlalchemy import Column,String,REAL,Text,Integer

class templatemodel(object):
    Symbol = Column(String,index=True)
    Timestamp = Column(Integer, index=True, unique = True,primary_key=True)
    Volume = Column(REAL)
    Open = Column(REAL)
    Close = Column(REAL)
    High = Column(REAL)
    Low = Column(REAL)
    Date = Column(Text)