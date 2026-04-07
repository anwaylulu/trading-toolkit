"""
Freqtrade Strategy Template
Complete template for creating trading strategies with Freqtrade
"""

from freqtrade.strategy import IStrategy, DecimalParameter, IntParameter
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from functools import reduce

class ExampleStrategy(IStrategy):
    """
    Example Trading Strategy with Multiple Indicators
    
    Strategy Logic:
    - Buy: When RSI is oversold (< 30) and MACD crosses above signal
    - Sell: When RSI is overbought (> 70) or profit target reached
    
    Usage:
    1. Copy to freqtrade/user_data/strategies/
    2. Run: freqtrade backtesting --strategy ExampleStrategy
    3. Optimize: freqtrade hyperopt --strategy ExampleStrategy
    """
    
    # Strategy version
    INTERFACE_VERSION = 3
    
    # Parameters for hyperoptimization
    buy_rsi = IntParameter(10, 40, default=30, space="buy")
    sell_rsi = IntParameter(60, 90, default=70, space="sell")
    
    # Stoploss and ROI
    stoploss = -0.10  # 10% stop loss
    
    minimal_roi = {
        "0": 0.15,      # 15% profit - sell immediately
        "60": 0.10,     # 10% profit after 60 min
        "120": 0.05,    # 5% profit after 120 min
        "240": 0.025    # 2.5% profit after 240 min
    }
    
    # Trailing stop
    trailing_stop = True
    trailing_stop_positive = 0.02
    trailing_stop_positive_offset = 0.03
    trailing_only_offset_is_reached = True
    
    # Timeframe
    timeframe = '1h'
    
    # Startup candle count
    startup_candle_count = 100
    
    # Order types
    order_types = {
        'buy': 'limit',
        'sell': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }
    
    # Order time in force
    order_time_in_force = {
        'buy': 'gtc',
        'sell': 'gtc'
    }
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Add technical indicators to the dataframe
        """
        # RSI (Relative Strength Index)
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        
        # MACD
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']
        
        # Bollinger Bands
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lowerband'] = bollinger['lower']
        dataframe['bb_middleband'] = bollinger['mid']
        dataframe['bb_upperband'] = bollinger['upper']
        
        # Moving Averages
        dataframe['sma_50'] = ta.SMA(dataframe, timeperiod=50)
        dataframe['sma_200'] = ta.SMA(dataframe, timeperiod=200)
        dataframe['ema_12'] = ta.EMA(dataframe, timeperiod=12)
        dataframe['ema_26'] = ta.EMA(dataframe, timeperiod=26)
        
        # Volume
        dataframe['volume_mean'] = dataframe['volume'].rolling(window=20).mean()
        
        return dataframe
    
    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Define buy signals
        """
        conditions = []
        
        # Condition 1: RSI oversold
        conditions.append(dataframe['rsi'] < self.buy_rsi.value)
        
        # Condition 2: MACD crossing above signal
        conditions.append(dataframe['macd'] > dataframe['macdsignal'])
        
        # Condition 3: Price near lower Bollinger Band
        conditions.append(dataframe['close'] < dataframe['bb_lowerband'] * 1.02)
        
        # Condition 4: Volume above average
        conditions.append(dataframe['volume'] > dataframe['volume_mean'])
        
        # Combine all conditions
        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'buy'
            ] = 1
        
        return dataframe
    
    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Define sell signals
        """
        conditions = []
        
        # Condition 1: RSI overbought
        conditions.append(dataframe['rsi'] > self.sell_rsi.value)
        
        # Condition 2: MACD crossing below signal
        conditions.append(dataframe['macd'] < dataframe['macdsignal'])
        
        # Condition 3: Price near upper Bollinger Band
        conditions.append(dataframe['close'] > dataframe['bb_upperband'] * 0.98)
        
        # Combine all conditions
        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'sell'
            ] = 1
        
        return dataframe
    
    def leverage(self, pair: str, current_time, current_rate: float,
                 proposed_leverage: float, max_leverage: float, entry_tag: str,
                 side: str, **kwargs) -> float:
        """
        Adjust leverage (for futures trading)
        """
        return 1.0  # No leverage for spot trading


class SimpleMAStrategy(IStrategy):
    """
    Simple Moving Average Crossover Strategy
    
    Buy: Fast MA crosses above Slow MA
    Sell: Fast MA crosses below Slow MA
    """
    
    INTERFACE_VERSION = 3
    
    stoploss = -0.10
    timeframe = '4h'
    
    minimal_roi = {
        "0": 0.20
    }
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['fast_ma'] = ta.SMA(dataframe, timeperiod=10)
        dataframe['slow_ma'] = ta.SMA(dataframe, timeperiod=30)
        
        # Crossover signals
        dataframe['cross_above'] = (
            (dataframe['fast_ma'] > dataframe['slow_ma']) &
            (dataframe['fast_ma'].shift(1) <= dataframe['slow_ma'].shift(1))
        )
        dataframe['cross_below'] = (
            (dataframe['fast_ma'] < dataframe['slow_ma']) &
            (dataframe['fast_ma'].shift(1) >= dataframe['slow_ma'].shift(1))
        )
        
        return dataframe
    
    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[dataframe['cross_above'], 'buy'] = 1
        return dataframe
    
    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[dataframe['cross_below'], 'sell'] = 1
        return dataframe


class BreakoutStrategy(IStrategy):
    """
    Breakout Strategy - Buy when price breaks above resistance
    """
    
    INTERFACE_VERSION = 3
    
    stoploss = -0.05
    timeframe = '1d'
    
    minimal_roi = {
        "0": 0.10,
        "1440": 0.05
    }
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Calculate support and resistance
        dataframe['resistance'] = dataframe['high'].rolling(window=20).max()
        dataframe['support'] = dataframe['low'].rolling(window=20).min()
        
        # Volume confirmation
        dataframe['volume_ma'] = dataframe['volume'].rolling(window=20).mean()
        
        return dataframe
    
    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Breakout above resistance with volume
        dataframe.loc[
            (dataframe['close'] > dataframe['resistance'].shift(1)) &
            (dataframe['volume'] > dataframe['volume_ma'] * 1.5),
            'buy'
        ] = 1
        return dataframe
    
    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Breakdown below support
        dataframe.loc[
            dataframe['close'] < dataframe['support'].shift(1),
            'sell'
        ] = 1
        return dataframe
