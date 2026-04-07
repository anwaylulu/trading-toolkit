# CCXT Advanced Usage

## Rate Limiting

```python
import ccxt

# Enable rate limiting (highly recommended)
exchange = ccxt.binance({
    'enableRateLimit': True,
    'options': {
        'defaultType': 'spot',  # or 'future', 'margin'
    }
})
```

## Error Handling

```python
import ccxt

exchange = ccxt.binance()

try:
    ticker = exchange.fetch_ticker('BTC/USDT')
except ccxt.NetworkError as e:
    print(f"Network error: {e}")
except ccxt.ExchangeError as e:
    print(f"Exchange error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## WebSocket Support

```python
# For real-time data, use ccxt.pro (separate package)
# pip install ccxt.pro

import ccxt.pro as ccxtpro

async def watch_price():
    exchange = ccxtpro.binance()
    while True:
        ticker = await exchange.watch_ticker('BTC/USDT')
        print(f"Price: {ticker['last']}")
```

## Custom Headers

```python
exchange = ccxt.binance({
    'headers': {
        'X-MBX-APIKEY': 'your_api_key',
    }
})
```

## Proxy Configuration

```python
exchange = ccxt.binance({
    'proxies': {
        'http': 'http://proxy:8080',
        'https': 'http://proxy:8080',
    }
})
```
