import schedule
import time
from juniormarketprice import get_juiormarketPrices 
from mainmarketprice import get_mainmarketPrices

def job():
    print("I'm working .... ")

#schedule.every(5).seconds.do(get_juiormarketPrices)
schedule.every().day.at("11:30").do(get_juiormarketPrices)
schedule.every().day.at("11:45").do(get_mainmarketPrices)

while True:
    schedule.run_pending()
    time.sleep(1)