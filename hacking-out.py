from optibook.synchronous_client import Exchange

import logging
logger = logging.getLogger('client')
logger.setLevel('ERROR')

print("Setup was successful.")

ex = Exchange()
ex.connect()

phil_a = 'PHILIPS_A'
phil_b = 'PHILIPS_B'

# print(e.get_positions())
# for s, p in e.get_positions().items():
#     if p > 0:
#         e.insert_order(s, price=1, volume=p, side='ask', order_type='ioc')
#     elif p < 0:
#         e.insert_order(s, price=100000, volume=-p, side='bid', order_type='ioc')  
# print(e.get_positions())


def buy_a(order_size:int):
    
    # Checks the lowest priced option on the market for asks so that we can buy
    price_book = ex.get_last_price_book(phil_a)
    min_price = 100000000
    for i in price_book.asks:
        if i.price < min_price:
            min_price = i.price
    
    # Places order for last-checked best price
    ex.insert_order(
        instrument_id=phil_a,
        price = min_price,
        volume=order_size,
        side='bid',
        order_type='ioc',
    )
    

def sell_a(order_size:int):
    
    # Checks the lowest priced option on the market for asks so that we can buy
    price_book = ex.get_last_price_book(phil_a)
    max_price = 100000000
    for i in price_book.bids:
        if i.price < max_price:
            max_price = i.price
    
    # Places order for last-checked best price
    ex.insert_order(
        instrument_id=phil_a,
        price = max_price,
        volume=order_size,
        side='ask',
        order_type='ioc',
    )
    
print("hi")
buy_a(7)
order = ex.get_trade_history(phil_a)
for i in order:
    print(f"{i.order_id} \t {i.price} \t {i.volume} \t {i.side}")

sell_a(4)
order = ex.get_trade_history(phil_a)
for i in order:
    print(f"{i.order_id} \t {i.price} \t {i.volume} \t {i.side}")

def check_pnl():
    pnl = ex.get_pnl()
    print(f'\nPnL: {pnl:.2f}')
    
    if pnl > 0:
        pass
    else:
        continue


