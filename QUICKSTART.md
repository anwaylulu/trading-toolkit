# Trading Toolkit - Quick Start

## 1-Minute Setup

```bash
# 1. Navigate to skill
cd ~/.hermes/skills/trading-toolkit

# 2. Run installer
./install.sh

# 3. Setup environment
source ./scripts/setup-env.sh
source ~/.trading-env

# 4. Test installation
python3 examples/ccxt_quickstart.py
```

## What Gets Installed

### Core Python Packages
- ✅ `ccxt` - Exchange APIs (Binance, OKX, etc.)
- ✅ `freqtrade` - Automated trading bot
- ✅ `nautilus-trader` - Quantitative trading engine
- ✅ `py-clob-client` - Polymarket trading
- ✅ `polymarket-py` - Polymarket data
- ✅ `kalshi-python` - Kalshi prediction markets
- ✅ `web3` - Blockchain interaction

### Cloned Repositories
- ✅ `hummingbot` - Market making bot
- ✅ `nofx` - AI trading assistant
- ✅ `pmxt` - Prediction market tools

### Example Files
- ✅ `ccxt_quickstart.py` - 5 CCXT examples
- ✅ `freqtrade_strategy_template.py` - 3 strategy templates
- ✅ `polymarket_trading.py` - 7 Polymarket examples

## First Commands

### Check Prices
```python
import ccxt
exchange = ccxt.binance()
ticker = exchange.fetch_ticker('BTC/USDT')
print(f"BTC: ${ticker['last']}")
```

### Backtest Strategy
```bash
freqtrade new-strategy --strategy MyStrategy
freqtrade download-data --pairs BTC/USDT --days 30
freqtrade backtesting --strategy MyStrategy
```

### Explore Polymarket
```python
from py_clob_client.client import ClobClient
client = ClobClient("https://clob.polymarket.com")
markets = client.get_markets()
```

## Next Steps

1. **Read examples**: Check `examples/` directory
2. **Configure APIs**: Edit `~/.trading-env` with your keys
3. **Start small**: Use dry-run/paper trading first
4. **Join community**: Discord/Telegram groups for each tool

## Help

```bash
# Skill help
./install.sh --help

# Tool help
freqtrade --help
hummingbot --help
```
