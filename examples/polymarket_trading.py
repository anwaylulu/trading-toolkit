"""
Polymarket Trading Examples
Complete guide to trading on Polymarket prediction markets
"""

from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds, OrderArgs, OrderType
import os
from dotenv import load_dotenv

load_dotenv()


def get_readonly_client():
    """Create a read-only client (no trading)"""
    host = "https://clob.polymarket.com"
    client = ClobClient(host)
    return client


def get_trading_client():
    """Create a trading client (requires API credentials)"""
    host = "https://clob.polymarket.com"
    
    # Get credentials from environment
    api_key = os.getenv("POLYMARKET_API_KEY")
    api_secret = os.getenv("POLYMARKET_API_SECRET")
    passphrase = os.getenv("POLYMARKET_PASSPHRASE")
    
    if not all([api_key, api_secret, passphrase]):
        raise ValueError("Missing Polymarket API credentials in .env file")
    
    creds = ApiCreds(api_key, api_secret, passphrase)
    client = ClobClient(host, creds=creds)
    return client


def example_1_list_markets():
    """Example 1: List all active markets"""
    print("=== Example 1: Active Prediction Markets ===")
    
    client = get_readonly_client()
    
    # Get markets with pagination
    markets_response = client.get_markets()
    markets = markets_response.get('data', [])
    
    print(f"Found {len(markets)} active markets\n")
    
    for market in markets[:5]:  # Show first 5
        question = market.get('question', 'N/A')
        description = market.get('description', '')[:100]
        best_bid = market.get('best_bid', 'N/A')
        best_ask = market.get('best_ask', 'N/A')
        volume = market.get('volume', 'N/A')
        
        print(f"📊 {question}")
        print(f"   {description}...")
        print(f"   Best Bid: {best_bid} | Best Ask: {best_ask}")
        print(f"   Volume: {volume}")
        print()


def example_2_market_details(condition_id: str):
    """Example 2: Get detailed market information"""
    print("=== Example 2: Market Details ===")
    
    client = get_readonly_client()
    
    # Get specific market
    market = client.get_market(condition_id)
    
    print(f"Question: {market.get('question')}")
    print(f"Description: {market.get('description')}")
    print(f"Category: {market.get('category')}")
    print(f"Resolution Date: {market.get('resolution_date')}")
    print(f"End Date: {market.get('end_date_iso')}")
    
    # Get order book
    try:
        book = client.get_order_book(condition_id)
        print(f"\nOrder Book:")
        print(f"  Bids: {len(book.bids)} orders")
        print(f"  Asks: {len(book.asks)} orders")
        
        if book.bids:
            print(f"  Best Bid: {book.bids[0].price} (Size: {book.bids[0].size})")
        if book.asks:
            print(f"  Best Ask: {book.asks[0].price} (Size: {book.asks[0].size})")
    except Exception as e:
        print(f"Could not fetch order book: {e}")


def example_3_price_history(condition_id: str):
    """Example 3: Get historical prices"""
    print("=== Example 3: Price History ===")
    
    client = get_readonly_client()
    
    # Get market and price history if available
    market = client.get_market(condition_id)
    
    # Note: Historical data might require additional API calls
    # or third-party data providers
    print(f"Current prices for: {market.get('question')}")
    print(f"Best Bid: {market.get('best_bid')}")
    print(f"Best Ask: {market.get('best_ask')}")
    print(f"Last Trade: {market.get('last_trade_price', 'N/A')}")


def example_4_calculate_implied_probability(best_ask: float):
    """Example 4: Convert odds to implied probability"""
    print("=== Example 4: Implied Probability ===")
    
    if best_ask <= 0:
        print("Invalid price")
        return
    
    # Polymarket prices are in cents (0-100)
    # Price of 55 means 55 cents = 55% probability
    implied_prob = best_ask
    
    print(f"Market Price: {best_ask} cents")
    print(f"Implied Probability: {implied_prob}%")
    print(f"Potential Return: {((100 - best_ask) / best_ask) * 100:.2f}%")


def example_5_find_arbitrage():
    """Example 5: Find arbitrage opportunities"""
    print("=== Example 5: Arbitrage Scan ===")
    
    client = get_readonly_client()
    markets = client.get_markets().get('data', [])
    
    opportunities = []
    
    for market in markets:
        question = market.get('question', '')
        best_bid = market.get('best_bid')
        best_ask = market.get('best_ask')
        
        if best_bid and best_ask:
            spread = best_ask - best_bid
            spread_pct = (spread / best_ask) * 100
            
            if spread_pct > 2:  # More than 2% spread
                opportunities.append({
                    'question': question,
                    'bid': best_bid,
                    'ask': best_ask,
                    'spread': spread_pct
                })
    
    if opportunities:
        print(f"Found {len(opportunities)} opportunities:")
        for opp in opportunities[:5]:
            print(f"  {opp['question'][:50]}...")
            print(f"    Spread: {opp['spread']:.2f}%")
    else:
        print("No significant arbitrage opportunities found")


def example_6_place_order():
    """Example 6: Place a buy order (requires API key)"""
    print("=== Example 6: Place Order ===")
    print("⚠️  This requires API credentials")
    
    try:
        client = get_trading_client()
        
        # Example order parameters
        order_args = OrderArgs(
            price=55.0,  # 55 cents
            size=10.0,   # $10 worth
            side="BUY",
            token_id="YOUR_TOKEN_ID_HERE"
        )
        
        # Create order
        # signed_order = client.create_order(order_args)
        # response = client.post_order(signed_order, OrderType.GTC)
        
        print("Order would be placed here (commented out for safety)")
        print("Uncomment the code and provide valid token_id to trade")
        
    except ValueError as e:
        print(f"❌ {e}")
        print("Set these environment variables:")
        print("  POLYMARKET_API_KEY")
        print("  POLYMARKET_API_SECRET")
        print("  POLYMARKET_PASSPHRASE")


def example_7_portfolio_tracking(address: str):
    """Example 7: Track portfolio (read-only)"""
    print("=== Example 7: Portfolio Tracking ===")
    
    # This would use the Polymarket subgraph or API
    # to fetch positions for a given address
    
    print(f"Tracking address: {address}")
    print("Note: Use Polymarket API or subgraph for portfolio data")
    print("Visit: https://polymarket.com/profile/{address}")


if __name__ == "__main__":
    print("Polymarket Trading Examples")
    print("=" * 60)
    print()
    
    try:
        example_1_list_markets()
        # example_2_market_details("YOUR_CONDITION_ID")
        example_4_calculate_implied_probability(55.0)
        example_5_find_arbitrage()
        example_6_place_order()
        
        print("\n✅ Examples completed!")
        print("\nNext steps:")
        print("1. Get API credentials from Polymarket")
        print("2. Set environment variables")
        print("3. Start with small trades to test")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
