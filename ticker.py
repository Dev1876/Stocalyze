from dataclasses import dataclass
from typing import Optional,Dict, Tuple, List
import numpy as np

TEST_DICT={
    "JMMBGL":10,
    "FESCO":100,
    "SVL":10
}

@dataclass
class Ticker:
    portfolio:Optional[Dict]

    def __post_init__(self):
        if not isinstance(self.portfolio,Dict):
            raise TypeError("portfolio specified should be a dictionary!")

    def __len__(self):
        return len(self.portfolio)
    
    @staticmethod
    def get_price_change(ticker:str,lookback:str='2d')->Tuple[float,List]:
        pass

    @classmethod
    def construct_portfolio(cls, stocks:Dict=TEST_DICT):
        """Class method to init this class. used mainly for dev
        purposes to construct an artificial portfolio

        Args:
        stock (Dict,optional): Defaults to TEST_DICT.

        Returns:
        Ticker: instance of this class
        """
        return cls(stocks)

    


