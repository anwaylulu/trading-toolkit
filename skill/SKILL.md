---
name: trading-toolkit
description: Comprehensive trading toolkit integrating crypto exchanges (CCXT), automated trading bots (freqtrade, hummingbot), quantitative trading engine (nautilus_trader), and prediction markets (Polymarket, Kalshi). Use when user wants to trade crypto, build trading strategies, access exchange APIs, or interact with prediction markets.
user-invocable: true
license: MIT
compatibility: Python 3.12+, Node.js 18+, Go 1.21+
metadata:
  author: Trading Toolkit Community
  version: 1.0.0
  tags: [trading, crypto, quant, prediction-markets, automation]
---

# Trading Toolkit - Complete Trading Infrastructure

## What this Skill provides

This skill installs and configures a comprehensive trading toolkit including:

### 1. **Exchange Connectivity (CCXT)**
- Unified API for 100+ crypto exchanges
- Spot and futures trading
- Real-time market data
- Order management

### 2. **Automated Trading Bots**
- **Freqtrade**: Strategy backtesting and live trading
- **Hummingbot**: Market making and arbitrage
- **NOFX**: AI-powered autonomous trading

### 3. **Quantitative Trading Engine**
- **Nautilus Trader**: High-performance Rust-based engine
- Event-driven architecture
- Backtesting and live execution
- Multi-venue support

### 4. **Prediction Markets**
- **Polymarket**: Crypto prediction markets
- **Kalshi**: Event-based trading
- CLOB (Central Limit Order Book) integration

## Installation

### Quick Install
```bash
cd ~/.hermes/skills/trading-toolkit
./install.sh
```

### Manual Install
```bash
# 1. Install Python 3.12+ via pyenv
curl https://pyenv.run | bash
pyenv install 3.12.9
pyenv global 3.12.9

# 2. Install Python packages
pip install nautilus-trader freqtrade ccxt py-clob-client polymarket-py kalshi-python web3

# 3. Install Hummingbot
git clone https://github.com/hummingbot/hummingbot.git
cd hummingbot
pip install -e .

# 4. Build NOFX
cd ~/projects/trading-tools/nofx
go build -o nofx .

# 5. Install PMXT
cd ~/projects/trading-tools/pmxt
npm install
```

## Usage Examples

### CCXT - Market Data
```python
import ccxt

# Get ticker
exchange = ccxt.binance()
ticker = exchange.fetch_ticker('BTC/USDT')
print(f"Price: ${ticker['last']}")

# Compare prices across exchanges
for ex_id in ['binance', 'okx', 'bybit']:
    ex = getattr(ccxt, ex_id)()
    t = ex.fetch_ticker('BTC/USDT')
    print(f"{ex_id}: ${t['last']}")
```

### Freqtrade - Strategy Development
```bash
# Create new strategy
freqtrade new-strategy --strategy MyStrategy

# Download historical data
freqtrade download-data --pairs BTC/USDT --timeframe 1h --days 30

# Backtest strategy
freqtrade backtesting --strategy MyStrategy --timeframe 1h

# Start trading (dry-run first!)
freqtrade trade --config config.json --strategy MyStrategy
```

### Nautilus Trader - Quantitative Strategy
```python
from nautilus_trader.trading.strategy import Strategy
from nautilus_trader.model.data import Bar

class SimpleStrategy(Strategy):
    def on_bar(self, bar: Bar):
        # Your strategy logic here
        if self.position is None:
            self.buy(bar.close)
        elif self.position.is_long:
            self.sell(bar.close)
```

### Polymarket - Prediction Markets
```python
from py_clob_client.client import ClobClient

client = ClobClient(host="https://clob.polymarket.com")
markets = client.get_markets()

for market in markets:
    print(f"{market['question']}: {market['best_bid']}")
```

### Hummingbot - Market Making
```bash
# Start hummingbot
hummingbot

# In the UI:
# 1. connect exchange
# 2. create strategy
# 3. start strategy
```

## Tool Reference

### CCXT
- `ccxt.binance()`, `ccxt.okx()`, etc. - Exchange instances
- `fetch_ticker()`, `fetch_ohlcv()`, `fetch_order_book()` - Market data
- `create_order()`, `cancel_order()`, `fetch_balance()` - Trading

### Freqtrade
- `freqtrade new-strategy` - Create strategy template
- `freqtrade download-data` - Download OHLCV data
- `freqtrade backtesting` - Test strategy on historical data
- `freqtrade trade` - Live trading
- `freqtrade hyperopt` - Optimize strategy parameters

### Nautilus Trader
- `BacktestNode` - Run backtests
- `LiveExecClient` - Live trading
- `Strategy` - Base class for strategies

### Prediction Markets
- `ClobClient` - Polymarket CLOB API
- `Polymarket` - Python SDK for Polymarket
- `Kalshi` - Python SDK for Kalshi

## Configuration Files

### Freqtrade Config Template
Located at: `examples/freqtrade_config.json`

### Nautilus Trader Strategy Template
Located at: `examples/nautilus_strategy.py`

### CCXT Examples
Located at: `examples/ccxt_examples.py`

## Security Warnings

⚠️ **NEVER**:
- Share API keys or private keys
- Run live trading without testing in dry-run mode
- Risk more than you can afford to lose

✅ **ALWAYS**:
- Start with dry-run/paper trading
- Use testnet/devnet for testing
- Secure your API keys in environment variables
- Review strategy code before live trading

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure Python 3.12+ is active
   ```bash
   pyenv global 3.12.9
   ```

2. **Hummingbot urllib3 conflict**:
   ```bash
   pip install urllib3==1.26.15
   ```

3. **NOFX build errors**: Ensure Go 1.21+ is installed
   ```bash
   go version
   ```

## Resources

- CCXT Docs: https://docs.ccxt.com
- Freqtrade Docs: https://www.freqtrade.io
- Nautilus Trader Docs: https://nautilustrader.io/docs
- Polymarket API: https://docs.polymarket.com
- Hummingbot Docs: https://hummingbot.org

## Progressive Disclosure

- CCXT Advanced: [references/ccxt_advanced.md](references/ccxt_advanced.md)
- Freqtrade Strategy Development: [references/freqtrade_strategy.md](references/freqtrade_strategy.md)
- Nautilus Backtesting: [references/nautilus_backtest.md](references/nautilus_backtest.md)
- Prediction Market Arbitrage: [references/prediction_arbitrage.md](references/prediction_arbitrage.md)
