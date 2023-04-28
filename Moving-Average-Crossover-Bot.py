import time
from binance.client import Client

# Initialize Binance client with API keys
api_key = 'your_api_key'
api_secret = 'your_api_secret'
client = Client(api_key, api_secret)

# Define the short-term and long-term moving average periods
short_term = 50
long_term = 200

# Define the symbol pair to trade
symbol = 'BNBBTC'

# Define the interval for historical klines data
interval = Client.KLINE_INTERVAL_1HOUR

# Calculate the short-term and long-term moving averages from historical klines data
def calculate_moving_averages(klines):
    short_term_closes = [float(kline[4]) for kline in klines[-short_term:]]
    long_term_closes = [float(kline[4]) for kline in klines[-long_term:]]
    short_term_ma = sum(short_term_closes) / short_term
    long_term_ma = sum(long_term_closes) / long_term
    return (short_term_ma, long_term_ma)

# Place a market buy order
def market_buy(symbol, quantity):
    order = client.create_order(
        symbol=symbol,
        side=Client.SIDE_BUY,
        type=Client.ORDER_TYPE_MARKET,
        quantity=quantity
    )
    print(f'Bought {quantity} {symbol} at market price')
    return order

# Place a market sell order
def market_sell(symbol, quantity):
    order = client.create_order(
        symbol=symbol,
        side=Client.SIDE_SELL,
        type=Client.ORDER_TYPE_MARKET,
        quantity=quantity
    )
    print(f'Sold {quantity} {symbol} at market price')
    return order

# Connect to Binance websocket and listen for klines data
def on_message(ws, message):
    kline = message['k']
    is_closed = kline['x']
    close_price = float(kline['c'])
    if is_closed:
        klines = client.get_klines(symbol=symbol, interval=interval)
        short_term_ma, long_term_ma = calculate_moving_averages(klines)
        if short_term_ma > long_term_ma:
            # Place a buy order
            order = market_buy(symbol, 100)
        elif short_term_ma < long_term_ma:
            # Place a sell order
            order = market_sell(symbol, 100)

# Start the websocket connection and listen for klines data
ws = client.websocket_agg_trade(
    symbol=symbol.lower(),
    id='moving_average_crossover_bot',
    on_message=on_message,
)
while True:
    time.sleep(1)
