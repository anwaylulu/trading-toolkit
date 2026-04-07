# Trading Toolkit

Complete trading infrastructure for AI agents - unified access to crypto exchanges, automated trading bots, quantitative engines, and prediction markets.

## 🎯 What is this?

This skill provides a one-command installation for professional-grade trading tools:

- **Exchange Connectivity**: CCXT for 100+ exchanges
- **Trading Bots**: Freqtrade and Hummingbot for automation
- **Quantitative Engine**: Nautilus Trader for high-frequency strategies
- **Prediction Markets**: Polymarket and Kalshi integration
- **AI Trading**: NOFX autonomous trading assistant

## 🚀 Quick Start

```bash
# Install everything
cd ~/.hermes/skills/trading-toolkit
./install.sh

# Test installation
python3 examples/ccxt_quickstart.py
```

## 📦 What's Included

### 1. CCXT - Exchange API
```python
import ccxt

exchange = ccxt.binance()
ticker = exchange.fetch_ticker('BTC/USDT')
print(f"Price: ${ticker['last']}")
```

### 2. Freqtrade - Strategy Bot
```bash
# Backtest a strategy
freqtrade backtesting --strategy MyStrategy

# Run live (dry-run first!)
freqtrade trade --config config.json --strategy MyStrategy
```

### 3. Nautilus Trader - Quant Engine
```python
from nautilus_trader.trading.strategy import Strategy

class MyStrategy(Strategy):
    def on_bar(self, bar):
        if self.position is None:
            self.buy(bar.close)
```

### 4. Polymarket - Prediction Markets
```python
from py_clob_client.client import ClobClient

client = ClobClient("https://clob.polymarket.com")
markets = client.get_markets()
```

### 5. Hummingbot - Market Making
```bash
hummingbot
```

## 📂 Structure

```
trading-toolkit/
├── skill/
│   └── SKILL.md              # Main skill definition
├── examples/
│   ├── ccxt_quickstart.py    # Exchange API examples
│   ├── freqtrade_strategy.py # Strategy templates
│   └── polymarket_trading.py # Prediction market examples
├── install.sh                # One-command installer
└── README.md                 # This file
```

## 🔧 Installation Details

### Requirements
- Python 3.12+
- Node.js 18+ (for PMXT)
- Go 1.21+ (for NOFX)
- 5GB+ disk space

### Installed Packages
| Package | Purpose | Size |
|---------|---------|------|
| ccxt | Exchange API | ~50MB |
| freqtrade | Trading bot | ~200MB |
| nautilus-trader | Quant engine | ~500MB |
| py-clob-client | Polymarket | ~10MB |
| hummingbot | Market making | ~1GB |

## 🎓 Usage Examples

### Market Data
```python
# Compare prices across exchanges
import ccxt

exchanges = ['binance', 'okx', 'bybit']
for ex_id in exchanges:
    ex = getattr(ccxt, ex_id)()
    ticker = ex.fetch_ticker('BTC/USDT')
    print(f"{ex_id}: ${ticker['last']}")
```

### Automated Trading
```python
# Simple moving average strategy
from freqtrade.strategy import IStrategy

class MAStrategy(IStrategy):
    def populate_buy_trend(self, dataframe, metadata):
        dataframe.loc[
            dataframe['sma_10'] > dataframe['sma_30'],
            'buy'
        ] = 1
        return dataframe
```

### Prediction Markets
```python
# Trade on prediction markets
from py_clob_client.client import ClobClient

client = ClobClient("https://clob.polymarket.com")
markets = client.get_markets()

for market in markets['data']:
    print(f"{market['question']}: {market['best_bid']}")
```

## ⚙️ Configuration

### API Keys
Create `~/.env` file:
```bash
# Exchange API Keys
BINANCE_API_KEY=your_key
BINANCE_SECRET=your_secret

# Polymarket
POLYMARKET_API_KEY=your_key
POLYMARKET_API_SECRET=your_secret
POLYMARKET_PASSPHRASE=your_passphrase
```

### Freqtrade Config
```bash
freqtrade new-config
# Edit user_data/config.json
```

## 🛡️ Safety First

⚠️ **Important Warnings**:

1. **Never risk real money without testing**
   - Always use dry-run mode first
   - Test on testnet/devnet
   - Start with small amounts

2. **Secure your API keys**
   - Use environment variables
   - Never commit keys to git
   - Use IP restrictions on exchange APIs

3. **Understand the risks**
   - Trading can result in total loss
   - Past performance doesn't guarantee future results
   - Bots can malfunction

## 📚 Documentation

- [CCXT Docs](https://docs.ccxt.com)
- [Freqtrade Docs](https://www.freqtrade.io)
- [Nautilus Trader](https://nautilustrader.io/docs)
- [Polymarket API](https://docs.polymarket.com)
- [Hummingbot](https://hummingbot.org)

## 🔧 Troubleshooting

### Python Version
```bash
pyenv install 3.12.9
pyenv global 3.12.9
```

### Import Errors
```bash
pip install --upgrade pip
pip install -e ~/.hermes/skills/trading-toolkit
```

### Hummingbot Conflicts
```bash
pip install urllib3==1.26.15
```

## 🤝 Contributing

This is an open skill. Contributions welcome:
- Additional examples
- New integrations
- Bug fixes
- Documentation improvements

## 📄 License

MIT License - See LICENSE file

## ⚠️ Disclaimer

This software is for educational purposes only. Trading involves substantial risk of loss. The authors assume no responsibility for your trading results. Always do your own research and never trade with money you cannot afford to lose.
