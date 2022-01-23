### Dual Listing exercise

In this exercise you will trade two identical stocks on different listings. The theory dictates they should have the same value, but due to supply and demand on the exchanges, the prices can deviate.

An example implementation of a trading algorithm is provided in algorithm.py. It wakes up every 5 seconds and randomly buys or sells one lot of one of the two stocks. It also ensures to keep absolute positions below 5 to avoid breaching the exchange delta limit of 10.0.

This strategy quite obviously does not lead to a positive expected PnL. How can you use the known one-to-one relationship between the two stocks to convert this algorithm into a viable trading strategy?