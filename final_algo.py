# Importing necessary libraries

from datetime import datetime as dt
import time
import random 
import logging
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

from optibook.synchronous_client import Exchange

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

try:
    # Connecting to exchange
    ex = Exchange()
    ex.connect()
    
    # Defining the instruments
    phil_a = 'PHILIPS_A'
    phil_b = 'PHILIPS_B'
    
    # Function to execute the buying of 'PHILIPS_A'
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
    
    # Function to execute the buying of 'PHILIPS_B'
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
    
    # Function to execute the selling of 'PHILIPS_A'
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
    
    # Function to execute the selling of 'PHILIPS_B'
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
    
    # Creating dataframes to store collected data  
    dfA = pd.DataFrame()
    dfB = pd.DataFrame()
    
    dfA['Time'] = []
    dfA['Price'] = []
    dfA['Volume'] = []
    dfA['Side'] = []
    
    dfB['Time'] = []
    dfB['Price'] = []
    dfB['Volume'] = []
    dfB['Side'] = []
    
    print("--- \t --- \t --- \t --- Team Traceback \t --- \t --- \t --- \t --- \t")
    print("----------------------------------------------------------------")
    print(f"Entering While Loop beginning now at {str(dt.now()):18s} UTC")
    print("----------------------------------------------------------------")
    print("--- \t --- \t --- \t --- \t --- \t --- \t --- \t --- \t --- \t --- \t")
    
    phil_a = "PHILIPS_A"
    phil_b = "PHILIPS_B"
    
    # Risk Threshold for Model A and Model B
    rsqRiskModelA = 0.500
    rsqRiskModelB = 0.500
    
    while True:
        
        # Sleeping so proper amount of data can be collected
        time.sleep(10)
        try:
            # Getting last price books of the stocks
            orderA_book = ex.get_last_price_book(phil_a)
            orderB_book = ex.get_last_price_book(phil_b)
            
            # Storing prices of Bids of PHILIPS_A and Asks of PHILIPS_B
            bidsA_prices = [i.price for i in orderA_book.bids]
            asksB_prices = [i.price for i in orderB_book.asks]
            
            # Storing volumes of Bids of PHILIPS_A and Asks of PHILIPS_B
            bidsA_vols = [i.volume for i in orderA_book.bids]
            asksB_vols = [i.volume for i in orderB_book.asks]
            
            # Getting the trade tick history of the stocks
            orderA_hist = ex.get_trade_tick_history(phil_a)
            orderB_hist = ex.get_trade_tick_history(phil_b)
            
            # Getting the timestamps
            timeA = [int(i.timestamp.hour) + int(i.timestamp.minute) + int(i.timestamp.second) for i in orderA_hist]
            timeB = [int(i.timestamp.hour) + int(i.timestamp.minute) + int(i.timestamp.second) for i in orderB_hist]
            
            priceA = [i.price for i in orderA_hist]
            priceB = [i.price for i in orderB_hist]
            
            volumeA = [i.volume for i in orderA_hist]
            volumeB = [i.volume for i in orderB_hist]
            
            sideA = [i.aggressor_side for i in orderA_hist]
            sideB = [i.aggressor_side for i in orderB_hist]
            
            dfAtemp = pd.DataFrame()
            dfAtemp['Time'] = timeA
            dfAtemp['Price'] = priceA
            dfAtemp['Volume'] = volumeA
            dfAtemp['Side'] = sideA
            
            dfBtemp = pd.DataFrame()
            dfBtemp['Time'] = timeB
            dfBtemp['Price'] = priceB
            dfBtemp['Volume'] = volumeB
            dfBtemp['Side'] = sideB
            
            dfA = pd.concat([dfA, dfAtemp], verify_integrity=True, ignore_index=True, axis=0)
            dfB = pd.concat([dfB, dfBtemp], verify_integrity=True, ignore_index=True, axis=0)
            
            dfA.drop_duplicates()
            dfB.drop_duplicates()
        
            Xa = dfA[['Time', 'Volume']]
            Xa = sm.add_constant(Xa)
            ya = dfA['Price']
            
            Xb = dfB[['Time', 'Volume']]
            Xb = sm.add_constant(Xb)
            yb = dfB['Price']
            
            print(dfA)
            print(dfB)
            print(dfAtemp)
            print(dfBtemp)
            
            try:
                modelA = sm.OLS(ya, Xa).fit()
                modelB = sm.OLS(yb, Xb).fit()
            except ValueError:
                continue
    
            rsqA = modelA.rsquared
            rsqB = modelB.rsquared
            
            print(f"R-Square for Model A = {rsqA}")
            print(f"R-Square for Model B = {rsqB}")
            
            predictA = lambda time, vol : modelA.params[0] + modelA.params[1]*time + modelA.params[2]*vol
            predictB = lambda time, vol : modelB.params[0] + modelB.params[1]*time + modelB.params[2]*vol
            
            if rsqA < rsqRiskModelA or rsqB < rsqRiskModelB:
                continue
            else:
                
                volXa = dfA[['Time', 'Price']]
                volXb = dfB[['Time', 'Price']]
                
                volya = dfA['Volume']
                volyb = dfB['Volume']
                
                try:
                    volModelA = sm.OLS(volya, volXa).fit()
                    volModelB = sm.OLS(volyb, volXb).fit()
                except ValueError:
                    continue
                
                volRsqA = volModelA.rsquared
                volRsqB = volModelB.rsquared
                
                volPredictA = lambda time, price : modelA.params[0] + modelA.params[1]*time + modelA.params[2]*price
                volPredictB = lambda time, price : modelB.params[0] + modelB.params[1]*time + modelB.params[2]*price
                
                newTimeDataA = dfA.iloc[0:10,0:1]
                newTimeDataB = dfB.iloc[0:10,0:1]
                
                newTimeDataA += 1
                newTimeDataB += 1
                
                estPriceA = predictA(newTimeDataA, dfA.iloc[0:10][2:3])
                estPriceB = predictB(newTimeDataB, dfB.iloc[0:10][2:3])
                
                estVolA = volPredictA(newTimeDataA, estPriceA)
                estVolB = volPredictB(newTimeDataB, estPriceB)
                
                totalEstPriceA = estPriceA*estVolA
                totalEstPriceB = estPriceB*estVolB
                
                meanPriceA = totalEstPriceA.mean()
                meanPriceB = totalEstPriceB.mean()
                
                pnlAtoB = meanPriceA - meanPriceB
                pnlBtoA = meanPriceB - meanPriceA
                
                if pnlAtoB <= 0 and pnlBtoA <= 0:
                    
                    continue
                
                elif pnlAtoB > 0 and true_if_breach_trade_limit(meanPriceA, phil_a)==False and true_if_breach_trade_limit(meanPriceB, phil_b)==False:
                    
                    buy_a(estVolA[0])
                    sell_b(estVolB[0])
                    
                elif pnlBtoA > 0 and true_if_breach_trade_limit(meanPriceA, phil_a)==False and true_if_breach_trade_limit(meanPriceB, phil_b)==False:
                    
                    buy_b(estVolB[0])
                    sell_a(estVolA[0])
                
                
        except KeyboardInterrupt:
            print("--- \t --- \t --- \t --- \t --- Team Traceback \t --- \t --- \t --- \t --- \t --- \t")
            print("------------------------------------------------------------------------------")
            print(f"Exiting While Loop due to KeyboardInterrupt at {str(dt.now()):18s} UTC")
            print("------------------------------------------------------------------------------")
            print("--- \t --- \t --- \t --- \t --- \t --- \t --- \t --- \t --- \t --- \t --- \t --- \t")
                
except KeyboardInterrupt:
    print("--- \t --- \t --- \t --- \t --- Team Traceback \t --- \t --- \t --- \t --- \t --- \t")
    print("------------------------------------------------------------------------------")
    print(f"Exiting While Loop due to KeyboardInterrupt at {str(dt.now()):18s} UTC")
    print("------------------------------------------------------------------------------")
    print("--- \t --- \t --- \t --- \t --- \t --- \t --- \t --- \t --- \t --- \t --- \t --- \t")