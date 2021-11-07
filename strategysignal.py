from ohlc_cleaner import ohlc_Cleaner
from database import SessionLocal
from strategy import supertrend

class StrategySignal(object):
    sma= ''
    symbol =''
    df =''

    def __init__(self,ticker_symbol):
        self.symbol = ticker_symbol.upper()
        self.df = ohlc_Cleaner(self.symbol).create_stock_dataframe()
    
    # def get_SimpleMovingAverageSignal(self):
    #     trading_signal =SimpleMovingeAverage_Indicator.stock_MovingAverage(self.df).Calculate_SimpleMoveAverage5()
    #     return trading_signal

    # def get_ExponentialMovingAverageSignal(self):
    #     trading_signal = ExponentialMovingAverage_Indicator.stock_ExponentialMovingAverage(self.df).Calculate_Exponential_SimpleMoveAverage5()
    #     return trading_signal

    # def get_ParobolicSarSignal(self):
    #     trading_signal = ParobolicStopReverse_indicator.stock_ParobolicReverse(self.df).Calculate_ParbolicReverse()
    #     return trading_signal
    
    # def get_MACDSignal(self):
    #     trading_signal = MovingAverageConvergence.stock_MovingAverageConvergence(self.df).Calculate_MovingAverageConvergence()
    #     return trading_signal

    # def GetEMAStocksbyIndex(self):
    #     trading_signal = EMA_SAR.stock_EMA_SAR(self.df).Calculate_EMA_SAR()
    #     return trading_signal 
    
    def GetSuperTrend(self):
        trading_signal = supertrend.stock_SuperTrend(self.df).Calculate_SuperTrend()
        return trading_signal 
        




if __name__ == '__main__':
    signal = StrategySignal("FESCO")
   # psar_signal = signal.get_ParobolicSarSignal()
   # sma = signal.get_SimpleMovingAverageSignal()
   # ema_signal = signal.get_ExponentialMovingAverageSignal()
    #macd_signal = signal.get_MACDSignal()
    index_ema = signal.GetSuperTrend()
   
    print (f'Exponential Moving Average:{index_ema} Simple Moving Average:{index_ema} Parabolic Sar signal {index_ema}')