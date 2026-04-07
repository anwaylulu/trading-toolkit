#!/bin/bash
# Setup environment file for trading toolkit

echo "Setting up trading toolkit environment..."

ENV_FILE="$HOME/.trading-env"

cat > "$ENV_FILE" << 'EOF'
# Trading Toolkit Environment Variables
# Copy these to your ~/.zshrc or ~/.bashrc

# Python Path (if using pyenv)
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# Set Python 3.12 as default
pyenv global 3.12.9

# Freqtrade
export FREQTRADE_USER_DATA="$HOME/projects/trading-data"

# API Keys (fill these in)
# export BINANCE_API_KEY="your_key"
# export BINANCE_SECRET="your_secret"
# export POLYMARKET_API_KEY="your_key"
# export POLYMARKET_API_SECRET="your_secret"

# Aliases
alias ft='freqtrade'
alias hb='hummingbot'
alias ccxt-test='python3 ~/.hermes/skills/trading-toolkit/examples/ccxt_quickstart.py'
EOF

echo "Environment file created at: $ENV_FILE"
echo ""
echo "To activate, run:"
echo "  source $ENV_FILE"
echo ""
echo "Or add to your shell profile:"
echo "  echo 'source $ENV_FILE' >> ~/.zshrc"
