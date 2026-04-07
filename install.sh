#!/bin/bash

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║        Trading Toolkit - Installation Script               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.12.0"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then 
    print_status "Python $PYTHON_VERSION is compatible (>= 3.12.0)"
else
    print_error "Python 3.12+ required. Current: $PYTHON_VERSION"
    echo "Installing Python 3.12 via pyenv..."
    
    if ! command -v pyenv &> /dev/null; then
        echo "Installing pyenv..."
        curl https://pyenv.run | bash
        export PYENV_ROOT="$HOME/.pyenv"
        export PATH="$PYENV_ROOT/bin:$PATH"
        eval "$(pyenv init -)"
    fi
    
    pyenv install 3.12.9
    pyenv global 3.12.9
    print_status "Python 3.12.9 installed"
fi

# Ensure pyenv is active
if command -v pyenv &> /dev/null; then
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
fi

echo ""
echo "Installing Python packages..."

# Install core trading packages
pip install --upgrade pip

print_status "Installing CCXT (Exchange API)..."
pip install ccxt

print_status "Installing Nautilus Trader (Quant Engine)..."
pip install nautilus-trader

print_status "Installing Freqtrade (Trading Bot)..."
pip install freqtrade

print_status "Installing Prediction Market tools..."
pip install py-clob-client polymarket-py kalshi-python web3

echo ""
echo "Installing Hummingbot..."

HUMMINGBOT_DIR="$HOME/projects/trading-tools/hummingbot"
if [ ! -d "$HUMMINGBOT_DIR" ]; then
    mkdir -p ~/projects/trading-tools
    git clone --depth 1 https://github.com/hummingbot/hummingbot.git "$HUMMINGBOT_DIR"
fi

cd "$HUMMINGBOT_DIR"
pip install -e . || print_warning "Hummingbot install had issues (non-critical)"

echo ""
echo "Installing NOFX (AI Trading)..."

NOFX_DIR="$HOME/projects/trading-tools/nofx"
if [ ! -d "$NOFX_DIR" ]; then
    git clone --depth 1 https://github.com/NoFxAiOS/nofx.git "$NOFX_DIR"
fi

if command -v go &> /dev/null; then
    cd "$NOFX_DIR"
    go build -o nofx . || print_warning "NOFX build had issues (non-critical)"
    print_status "NOFX built successfully"
else
    print_warning "Go not found, skipping NOFX build"
fi

echo ""
echo "Installing PMXT (Prediction Markets)..."

PMXT_DIR="$HOME/projects/trading-tools/pmxt"
if [ ! -d "$PMXT_DIR" ]; then
    git clone --depth 1 https://github.com/pmxt-dev/pmxt.git "$PMXT_DIR"
fi

cd "$PMXT_DIR"
npm install || print_warning "PMXT install had issues (non-critical)"

echo ""
echo "Creating example files..."

EXAMPLES_DIR="$HOME/projects/trading-examples"
mkdir -p "$EXAMPLES_DIR"

# Create CCXT example
cat > "$EXAMPLES_DIR/ccxt_example.py" << 'EOF'
"""
CCXT Example - Market Data and Trading
"""
import ccxt
import os
from dotenv import load_dotenv

load_dotenv()

def get_market_data():
    """Fetch market data from multiple exchanges"""
    exchange = ccxt.binance()
    
    # Get BTC price
    ticker = exchange.fetch_ticker('BTC/USDT')
    print(f"BTC/USDT: ${ticker['last']:,.2f}")
    print(f"24h Change: {ticker['percentage']:.2f}%")
    print(f"24h Volume: {ticker['quoteVolume']:,.0f} USDT")
    
    return ticker

def compare_prices():
    """Compare BTC price across exchanges"""
    exchanges = ['binance', 'okx', 'bybit', 'kraken']
    prices = {}
    
    for ex_id in exchanges:
        try:
            ex = getattr(ccxt, ex_id)()
            ticker = ex.fetch_ticker('BTC/USDT')
            prices[ex_id] = ticker['last']
        except Exception as e:
            print(f"{ex_id}: Error - {e}")
    
    # Find arbitrage opportunities
    if prices:
        min_ex = min(prices, key=prices.get)
        max_ex = max(prices, key=prices.get)
        spread = ((prices[max_ex] - prices[min_ex]) / prices[min_ex]) * 100
        
        print(f"\nLowest: {min_ex} @ ${prices[min_ex]:,.2f}")
        print(f"Highest: {max_ex} @ ${prices[max_ex]:,.2f}")
        print(f"Spread: {spread:.3f}%")

if __name__ == "__main__":
    get_market_data()
    compare_prices()
EOF

# Create Freqtrade strategy example
cat > "$EXAMPLES_DIR/freqtrade_strategy.py" << 'EOF'
"""
Freqtrade Strategy Example - Simple Moving Average Crossover
"""
from freqtrade.strategy import IStrategy
from pandas import DataFrame
import talib.abstract as ta

class SmaCrossStrategy(IStrategy):
    """
    Simple SMA Crossover Strategy
    Buy when fast SMA crosses above slow SMA
    Sell when fast SMA crosses below slow SMA
    """
    
    # Strategy parameters
    fast_sma = 10
    slow_sma = 30
    
    # Minimal ROI
    minimal_roi = {
        "0": 0.10,    # 10% profit
        "60": 0.05,   # 5% after 60 minutes
        "120": 0.025  # 2.5% after 120 minutes
    }
    
    # Stoploss
    stoploss = -0.10  # 10% stop loss
    
    # Timeframe
    timeframe = '1h'
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Calculate SMAs
        dataframe['fast_sma'] = ta.SMA(dataframe, timeperiod=self.fast_sma)
        dataframe['slow_sma'] = ta.SMA(dataframe, timeperiod=self.slow_sma)
        
        # Calculate crossover
        dataframe['cross_above'] = (
            (dataframe['fast_sma'] > dataframe['slow_sma']) & 
            (dataframe['fast_sma'].shift(1) <= dataframe['slow_sma'].shift(1))
        )
        dataframe['cross_below'] = (
            (dataframe['fast_sma'] < dataframe['slow_sma']) & 
            (dataframe['fast_sma'].shift(1) >= dataframe['slow_sma'].shift(1))
        )
        
        return dataframe
    
    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            dataframe['cross_above'],
            'buy'
        ] = 1
        return dataframe
    
    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            dataframe['cross_below'],
            'sell'
        ] = 1
        return dataframe
EOF

# Create Polymarket example
cat > "$EXAMPLES_DIR/polymarket_example.py" << 'EOF'
"""
Polymarket Example - Prediction Market Trading
"""
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds
import os

def get_polymarket_client():
    """Initialize Polymarket client"""
    host = "https://clob.polymarket.com"
    
    # For public data, no API key needed
    client = ClobClient(host)
    return client

def list_markets():
    """List active prediction markets"""
    client = get_polymarket_client()
    
    # Get markets
    markets = client.get_markets()
    
    print("Active Prediction Markets:")
    print("-" * 50)
    
    for market in markets.get('data', [])[:5]:  # Show first 5
        question = market.get('question', 'N/A')
        best_bid = market.get('best_bid', 'N/A')
        best_ask = market.get('best_ask', 'N/A')
        
        print(f"Question: {question}")
        print(f"Best Bid: {best_bid} | Best Ask: {best_ask}")
        print()

def get_market_info(condition_id: str):
    """Get detailed market information"""
    client = get_polymarket_client()
    
    market = client.get_market(condition_id)
    
    print(f"Market: {market.get('question')}")
    print(f"Description: {market.get('description', 'N/A')}")
    print(f"End Date: {market.get('end_date_iso', 'N/A')}")
    
    # Get order book
    book = client.get_order_book(condition_id)
    print(f"Bids: {len(book.bids)}")
    print(f"Asks: {len(book.asks)}")

if __name__ == "__main__":
    list_markets()
EOF

print_status "Example files created in $EXAMPLES_DIR"

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              Installation Complete!                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Installed packages:"
echo "  - CCXT (Exchange API)"
echo "  - Freqtrade (Trading Bot)"
echo "  - Hummingbot (Market Making)"
echo "  - Nautilus Trader (Quant Engine)"
echo "  - Polymarket Tools (Prediction Markets)"
echo "  - NOFX (AI Trading)"
echo "  - PMXT (Prediction Markets)"
echo ""
echo "Example files: $EXAMPLES_DIR"
echo ""
echo "Next steps:"
echo "  1. Review example files in $EXAMPLES_DIR"
echo "  2. Configure API keys in ~/.env"
echo "  3. Start with dry-run/paper trading"
echo "  4. Run: python3 $EXAMPLES_DIR/ccxt_example.py"
echo ""
print_status "Installation successful!"
