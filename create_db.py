from database import  Base , engine
from models import juniormarket_list

print("Creating database......")
Base.metadata.create_all(engine)