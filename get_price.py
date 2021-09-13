import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# import pandas_datareader.data as web

import yfinance as yf
yf.pdr_override()

import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn

conn = create_connection('development.sqlite3')

cursor = conn.cursor()

app_stocks_list = pd.read_sql_query("SELECT ticker FROM stocks ORDER BY ticker", conn)
app_stocks_list['ticker'] = app_stocks_list['ticker'].astype(str) + '.SA' 
app_stocks_list = app_stocks_list["ticker"].astype(str).tolist()

print('stocks from the app')
print(app_stocks_list)

yahoo_br_stocks = yf.download(app_stocks_list, period="1min")["Adj Close"]
yahoo_br_stocks = yahoo_br_stocks.T.reset_index()
yahoo_br_stocks.columns = ["ticker",  "price"] 
yahoo_br_stocks['ticker'] = yahoo_br_stocks['ticker'].map(lambda x: x.rstrip('.SA'))
yahoo_br_stocks = yahoo_br_stocks.set_index('ticker')

print('Stocks Price from Yahoo')
print(yahoo_br_stocks)

# command to run: python3 get_price.py