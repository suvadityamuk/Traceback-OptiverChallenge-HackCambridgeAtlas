import datetime as dt
import time
import random
import logging

from optibook.synchronous_client import Exchange

exchange = Exchange()
exchange.connect()

logging.getLogger('client').setLevel('ERROR')


def trade_would_breach_position_limit(instrument_id, volume, side, position_limit=10):
    positions = exchange.get_positions()
    position_instrument = positions[instrument_id]

    if side == 'bid':
        return position_instrument + volume > position_limit
    elif side == 'ask':
        return position_instrument - volume < -position_limit
    else:
        raise Exception(f'''Invalid side provided: {side}, expecting 'bid' or 'ask'.''')


def print_positions_and_pnl():
    positions = exchange.get_positions()
    pnl = exchange.get_pnl()

    print('Positions:')
    for instrument_id in positions:
        print(f'  {instrument_id:10s}: {positions[instrument_id]:4.0f}')

    print(f'\nPnL: {pnl:.2f}')


STOCK_A_ID = 'PHILIPS_A'
STOCK_B_ID = 'PHILIPS_B'

while True:
    print(f'')
    print(f'-----------------------------------------------------------------')
    print(f'TRADE LOOP ITERATION ENTERED AT {str(dt.datetime.now()):18s} UTC.')
    print(f'-----------------------------------------------------------------')

    print_positions_and_pnl()
    print(f'')

    # Flip a coin to select which stock to trade
    if random.random() > 0.5:
        stock_id = STOCK_A_ID
    else:
        stock_id = STOCK_B_ID
    print(f'Selected stock {stock_id} to trade.')

    # Obtain order book and only trade if there are both bids and offers available on that stock
    stock_order_book = exchange.get_last_price_book(stock_id)
    if not (stock_order_book and stock_order_book.bids and stock_order_book.asks):
        print(f'Order book for {stock_id} does not have bids or offers. Skipping iteration.')
        continue

    # Obtain best bid and ask prices from order book
    best_bid_price = stock_order_book.bids[0].price
    best_ask_price = stock_order_book.asks[0].price
    print(f'Top level prices for {stock_id}: {best_bid_price:.2f} :: {best_ask_price:.2f}')

    # Flip a coin to decide whether to buy or sell
    if random.random() > 0.5:
        side = 'bid'
        price = best_ask_price
    else:
        side = 'ask'
        price = best_bid_price

    # Insert an IOC order to trade the opposing top-level
    volume = 1
    if not trade_would_breach_position_limit(stock_id, volume, side):
        print(f'''Inserting {side} for {stock_id}: {volume:.0f} lot(s) at price {price:.2f}.''')
        exchange.insert_order(
            instrument_id=stock_id,
            price=price,
            volume=volume,
            side=side,
            order_type='ioc')
    else:
        print(f'''Not inserting {volume:.0f} lot {side} for {stock_id} to avoid position-limit breach.''')

    print(f'\nSleeping for 5 seconds.')
    time.sleep(5)
