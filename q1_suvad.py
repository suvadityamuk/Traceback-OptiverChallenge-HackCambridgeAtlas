import datetime as dt
import time
import random 
import logging
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

from optibook.synchronous_client import Exchange

ex = Exchange()
ex.connect()

phil_a = 'PHILIPS_A'
phil_b = 'PHILIPS_B'

def true_if_breach_trade_limit(proposed_transaction, stock_id):
    pos = ex.get_positions()
    orders = ex.get_outstanding_orders(stock_id)
    res1 = True
    res2 = True
    if stock_id == phil_a:
        if proposed_transaction + pos[phil_a] >= 200 or proposed_transaction + pos[phil_a] <= -200:
            res1 = True
        else:
            res1 = False
        if len(orders) >= 400:
            res2 = True
        else:
            res2 = False
        
    elif stock_id == phil_b:
        if proposed_transaction + pos[phil_b] >= 200 or proposed_transaction + pos[phil_b] <= -200:
            res1 = True
        else:
            res1 = False
        if len(orders) >= 400:
            res2 = True
        else:
            res2 = False
    return (res1 and res2)
    

def get_price_of_philA(trade):
    price_book = ex.get_last_price_book(phil_a)
    bid_price = price_book.bids[0].price
    ask_price = price_book.asks[0].price
    if trade=='bid':
        return bid_price
    else:
        return ask_price

def get_price_of_philB(trade):
    price_book = ex.get_last_price_book(phil_b)
    bid_price = price_book.bids[0].price
    ask_price = price_book.asks[0].price
    if trade=='bid':
        return bid_price
    else:
        return ask_price
    
    
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

def buy_b(order_size:int):
    
    # Checks the lowest priced option on the market for asks so that we can buy
    price_book = ex.get_last_price_book(phil_b)
    min_price = 100000000
    for i in price_book.asks:
        if i.price < min_price:
            min_price = i.price
    
    # Places order for last-checked best price
    ex.insert_order(
        instrument_id=phil_b,
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

def sell_b(order_size:int):
    
    # Checks the lowest priced option on the market for asks so that we can buy
    price_book = ex.get_last_price_book(phil_b)
    max_price = 100000000
    for i in price_book.bids:
        if i.price < max_price:
            max_price = i.price
    
    # Places order for last-checked best price
    ex.insert_order(
        instrument_id=phil_b,
        price = max_price,
        volume=order_size,
        side='ask',
        order_type='ioc',
    )

def get_all_trade_history(stock_id):
    order_hist = ex.get_trade_history(stock_id)
    
    print(f"For instrument ID = {stock_id}")
    print(f"Order ID \t Price \t Volume \t Side(Bid/Ask)")
    for i in order_hist:
        print(f"{i.order_id} \t {i.price} \t {i.volume} \t {i.side}")

def get_public_pricebook_history(stock_id):
    # order_hist = ex.get_trade_tick_history(stock_id)
    order_hist = ex.get_last_price_book(stock_id)
    
    print(f"For instrument ID = {stock_id} at Time : {order_hist.timestamp.hour}HR {order_hist.timestamp.minute}MN {order_hist.timestamp.second}SC")
    print("  Bids  ")
    print(f"Price \t Volume")
    for i in order_hist.bids:
        print(f"{i.price} \t {i.volume}")
        
    print("  Asks  ")
    print(f"Price \t Volume")
    for i in order_hist.asks:
        print(f"{i.price} \t {i.volume}")

def get_public_ticks_history(stock_id):
    data = pd.DataFrame()
    time = []
    order_id = []
    price = []
    volume = []
    side = []
    
    order_hist = ex.get_trade_tick_history(stock_id)
    print(f"For instrument ID = {stock_id}")
    print(f"Time \t Order ID \t Price \t Volume \t Side(Bid/Ask) \t Buyer \t Seller")
    for i in order_hist:
        print(f"{i.timestamp.hour} {i.timestamp.minute} {i.timestamp.second} {i.timestamp.tzinfo} \t {i.trade_nr} \t {np.round(i.price, 2)} \t {i.volume} \t {i.aggressor_side} \t {i.buyer} \t {i.seller}")
        time.append(f"{i.timestamp.hour}:{i.timestamp.minute}:{i.timestamp.second}")
        order_id.append(i.trade_nr)
        price.append(np.round(i.price, 2))
        volume.append(i.volume)
        side.append(i.aggressor_side)
    
    data['Time'] = time
    data['Order ID'] = order_id
    data['Price'] = price
    data['Volume'] = volume
    data['Side'] = side
    
    print("DATAFRAME")
    print(data)
    # data.to_csv('data.csv')
        

def perform_linear_regression(stock_id):
    order_hist = ex.get_trade_tick_history(instrument_id='PHILIPS_A')
    
    print(len(order_hist))
    
    all_prices = [i.price for i in order_hist]
    all_volumes = [i.volume for i in order_hist]
    all_times = [(i.timestamp.hour+i.timestamp.minute+i.timestamp.second) for i in order_hist]
    
    print(all_volumes)
    print(all_prices)
    print(all_times)
    
    prices_arr = np.ndarray(all_prices)
    volume_arr = np.ndarray(all_volumes)
    time_arr = np.ndarray(all_times)
    
    print(time_arr)
    
    fin_arr = np.concatenate((prices_arr, time_arr), axis=1)
    
    df = pd.DataFrame(data=fin_arr, columns=['Prices', 'Time'])
    
    X = time_arr
    X = sm.add_constant(X)
    y = prices_arr
    model = sm.OLS(y, X).fit()
    print(model.summary())
    
    predict = lambda x : model.params[0] + model.params[1]*x



print('About to sleep for 30 seconds')
time.sleep(30)
print('Good morning')

print("Price Book for PHILIPS_A")
get_public_pricebook_history(phil_a)
print("Price Book for PHILIPS_B")
get_public_pricebook_history(phil_b)
print("Public History for PHILIPS_A")
get_public_ticks_history(phil_a)
print("Public History for PHILIPS_B")
get_public_ticks_history(phil_b)
