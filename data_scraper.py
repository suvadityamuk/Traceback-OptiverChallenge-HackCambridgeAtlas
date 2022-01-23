import datetime as dt
import time
import random 
import logging
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import q1_suvad

from optibook.synchronous_client import Exchange

ex = Exchange()
ex.connect()

while True:
    print("--- \t --- \t --- \t --- \t --- \t --- \t --- \t --- \t --- \t --- \t")
    print("----------------------------------------------------------------")
    print(f"Data collection beginning now at {str(datetime.now()):18s} UTC")
    print("----------------------------------------------------------------")
    print("--- \t --- \t --- \t --- \t --- \t --- \t --- \t --- \t --- \t --- \t")
    
    q1_suvad.get_public_ticks_history()