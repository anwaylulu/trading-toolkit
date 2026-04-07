"""
CCXT Quickstart Examples
Quick reference for common CCXT operations
"""

import ccxt
import os
from datetime import datetime

def example_1_basic_ticker():
    """Example 1: Get basic ticker information"""
    print("=== Example 1: Basic Ticker ===")
    
    exchange = ccxt.binance()
    ticker = exchange.fetch_ticker('BTC/USDT')
    
    print(f"Symbol: {ticker['symbol']}")
    print(f"Last Price: ${ticker['last']:,.2f}")
    print(f"24h High: ${ticker['high']:,.2f}")
    print(f"24h Low: ${ticker['low']:,.2f}")
    print(f"24h Volume: {ticker['quoteVolume']:,.0f} USDT")
    print(f"24h Change: {ticker['percentage']:.2f}%")
    print()

def example_2_ohlcv_data():
    """Example 2: Get OHLCV (candlestick) data"""
    print("=== Example 2: OHLCV Data ===")
    
    exchange = ccxt.binance()
    
    # Fetch 1-hour candles for last 24 hours
    ohlcv = exchange.fetch_ohlcv('BTC/USDT', timeframe='1h', limit=24)
    
    print(f"Timestamp, Open, High, Low, Close, Volume")
    for candle in ohlcv[:5]:  # Show first 5
        timestamp = datetime.fromtimestamp(candle[0] / 1000)
        print(f"{timestamp}: O={candle[1]:.2f} H={candle[2]:.2f} L={candle[3]:.2f} C={candle[4]:.2f} V={candle[5]:.4f}")
    print()

def example_3_arbitrage_scanner():
    """Example 3: Simple arbitrage scanner"""
    print("=== Example 3: Arbitrage Scanner ===")
    
    exchanges = ['binance', 'okx', 'bybit']
    prices = {}
    
    print("Scanning BTC/USDT prices...")
    for ex_id in exchanges:
        try:
            ex = getattr(ccxt, ex_id)()
            ticker = ex.fetch_ticker('BTC/USDT')
            prices[ex_id] = ticker['last']
            print(f"  {ex_id.upper()}: ${ticker['last']:,.2f}")
        except Exception as e:
            print(f"  {ex_id.upper()}: Error - {str(e)[:50]}")
    
    if len(prices) >= 2:
        min_price = min(prices.values())
        max_price = max(prices.values())
        spread = ((max_price - min_price) / min_price) * 100
        
        print(f"\nSpread: {spread:.3f}%")
        if spread > 0.1:
            print("💰 Potential arbitrage opportunity!")
        else:
            print("ℹ️  Spread too small for arbitrage")
    print()

def example_4_order_book():
    """Example 4: Analyze order book"""
    print("=== Example 4: Order Book Analysis ===")
    
    exchange = ccxt.binance()
    order_book = exchange.fetch_order_book('BTC/USDT', limit=10)
    
    bids = order_book['bids'][:5]  # Top 5 buy orders
    asks = order_book['asks'][:5]  # Top 5 sell orders
    
    spread = asks[0][0] - bids[0][0]
    spread_pct = (spread / bids[0][0]) * 100
    
    print("Top 5 Bids (Buy):")
    for price, amount in bids:
        print(f"  ${price:,.2f} | {amount:.6f} BTC")
    
    print("\nTop 5 Asks (Sell):")
    for price, amount in asks:
        print(f"  ${price:,.2f} | {amount:.6f} BTC")
    
    print(f"\nSpread: ${spread:.2f} ({spread_pct:.4f}%)")
    print()

def example_5_market_overview():
    """Example 5: Market overview - top gainers/losers"""
    print("=== Example 5: Market Overview ===")
    
    exchange = ccxt.binance()
    
    # Load markets
    markets = exchange.load_markets()
    
    # Get all USDT pairs
    usdt_pairs = [symbol for symbol in markets.keys() if symbol.endswith('/USDT')]
    
    print(f"Total USDT pairs: {len(usdt_pairs)}")
    print("\nTop movers (24h):")
    
    # Fetch tickers for first 10 pairs
    for symbol in usdt_pairs[:10]:
        try:
            ticker = exchange.fetch_ticker(symbol)
            change = ticker['percentage']
            emoji = "🟢" if change > 0 else "🔴"
            print(f"  {emoji} {symbol}: {change:+.2f}%")
        except:
            pass
    print()

if __name__ == "__main__":
    print("CCXT Trading Examples")
    print("=" * 50)
    print()
    
    try:
        example_1_basic_ticker()
        example_2_ohlcv_data()
        example_3_arbitrage_scanner()
        example_4_order_book()
        example_5_market_overview()
        
        print("✅ All examples completed!")
    except Exception as e:
        print(f"❌ Error: {e}")
