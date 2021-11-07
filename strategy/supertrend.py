import talib as ta
import numpy as np
import  pandas as pd
#pd.set_option('display.max_rows',None)
import matplotlib.pyplot as plt



class stock_SuperTrend:
    db = ''
    stockclass =''
    def __init__(self,stock_df):
        self.stock_df = stock_df
        
    #basic upper band = ((high + low) /2) + (multiplier * atr)
    #basic lower band = ((high + low) /2) - (multiplier * atr)

    def Calculate_SuperTrend(self,period=7,multiplier=3):
        data = self.stock_df
        data['previous_close'] = data['Close'].shift(1)
        data['high-low'] = data['High'] - data['Low']
        data['high-pc'] = abs(data['High'] - data['previous_close'])
        data['low-pc'] = abs(data['Low'] - data['previous_close'])
        data['tr'] = data[['high-low','high-pc','low-pc']].max(axis=1)
        the_atr = data['tr'].rolling(period).mean()
        data['atr'] = the_atr
       
        data['upperband'] = ((data['High'] + data['Low']) / 2) + (multiplier * data['atr'] )
        data['lowerband'] = ((data['High'] + data['Low']) / 2) - (multiplier * data['atr'] )
        data['in_uptrend'] = True

        for current in range(1,len(data.index)):
            previous = current -1
            if data['Close'][current] > data['upperband'][previous]:
                data['in_uptrend'] = True
            elif data['Close'][current] < data['lowerband'][previous]:
                data['in_uptrend'][current] = False
            else:
                data['in_uptrend'][current] = data['in_uptrend'][previous]

                if data ['in_uptrend'][current] and data['lowerband'][current] < data['lowerband'][previous]:
                    data['lowerband'][current] = data['lowerband'][previous]
                    
                if not data['in_uptrend'][current] and data['upperband'][current] > data['upperband'][previous]:
                    data['upperband'][current] = data['upperband'][previous]

        print (data)


     


if __name__ == '__main__':
    sma = stock_SuperTrend("JBG")
    #sma.create_stock_dataframe()
    sma.Calculate_SuperTrend()