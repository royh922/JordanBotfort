# %%
import requests
import io
import pandas as pd
from pandas import json_normalize 
import sys
from datetime import datetime
import json
import yfinance as yf


#specifies user and ticker from command line parameters
user = sys.argv[1]
# user = "roy_h92"

tickers = sys.argv[2]
# tickers = "AAPL,MSFT,AMZN"

Data = yf.download(tickers, period= "1d", interval = "1m", actions=False, group_by="ticker")

# %%
# Class to create Candlestick object
class Candlestick():
    def __init__(self,high,open,close,low):
        if (close-open < 0): self.bullish = False
        else: self.bullish = True
        self.bought = False
        self.top = max(open, close)
        self.bottom = min(open, close)
        self.high = high
        self.low = low
        self.top_wick = high - self.top
        self.body = self.top - self.bottom
        self.bottom_wick = self.bottom - low
        self.mid = self.body/2
        if(high != low): self.body_ratio = self.body/(high - low)
        else: self.body_ratio = 0

# %%
#Defines buy pattern
def buyCSPattern(prev2,prev1,new):
    #3 White Soldiers
    if new.bullish and prev1.bullish and prev2.bullish: new.bought = True; return True
    #Morning Star
    elif new.bullish and (not prev1.bullish) and (not prev2.bullish) and (prev2.body_ratio > .65) and (new.body_ratio > .75) and (prev2.bottom > prev1.mid) and (new.bottom > prev1.mid): new.bought = True; return True
    #Bullish Engulfing
    elif (not prev1.bullish) and new.bullish and (prev1.bottom > new.bottom) and (prev1.top < new.top) and (new.body/prev1.body > 1): new.bought = True; return True
    #Piercing Line
    elif (not prev1.bullish) and new.bullish and (new.mid < prev1.mid < new.top) and (prev1.body_ratio > .75) and (new.body_ratio > .75): new.bought = True; return True
    #Hammer
    elif (new.bottom_wick/new.top_wick > 3) and new.bullish and (new.bottom_wick/new.body > 2): new.bought = True; return True
    #Inverse Hammer
    elif (new.top_wick/new.bottom_wick > 3) and new.bullish and (new.top_wick/new.body > 2): new.bought = True; return True 
    #No Buy Pattern
    else: return False

# %%
#Defines sell pattern
def sellCSPattern(prev2,prev1,new):

    #3 Black Crows
    if (not new.bullish) and (not prev1.bullish) and (not prev2.bullish): return True

    #Evening Star
    elif(not new.bullish) and prev1.bullish and prev2.bullish and (prev2.body_ratio > .65) and (new.body_ratio > .6) and (prev2.mid < prev1.bottom) and (new.top < prev1.bottom): return True
    
    #Bearish Engulfing!
    elif prev1.bullish and (not new.bullish) and (prev1.bottom > new.bottom) and (prev1.top < new.top) and (new.body/prev1.body > 1): return True

    #Dark Cloud Cover
    elif (prev1.bullish ) and (not new.bullish) and (new.bottom < prev1.mid < new.mid) and (prev1.body_ratio > .75) and (new.body_ratio > .75): return True
    
    #Hangman
    elif (new.bottom_wick/new.top_wick > 3) and (not new.bullish) and (new.bottom_wick/new.body > 2): return True

    #Shooting Star
    elif (new.top_wick/new.bottom_wick > 3) and (not new.bullish) and (new.top_wick/new.body > 2): return True
    
    #No Sell Pattern
    else: return False

# %%
tickers = tickers.split(",")
unit = 10 #unit of stock to buy (in dollars)

assets = dict()
try:
    with open("./" + user + "/assets.json") as json_file:
        assets = json.load(json_file)
except FileNotFoundError:
    assets["fund"] = 100.0
assets["stocks"] = 0.0
now = datetime.now().strftime('%m/%d-%H:%M')
log = open("./" + user + "/logs.txt", "a+")
log.seek(0)
currLog = log.read()
log.close()


for ticker in tickers:
    if len(tickers) == 1: data = Data
    else: data = Data[ticker]
    data = data.dropna()
    # print(data)
    shares = []
    shares = assets.get(ticker, [])
    #creates candle stick from data
    prev2 = Candlestick(data.iloc[-3]["High"], data.iloc[-3]["Open"], data.iloc[-3]["Close"], data.iloc[-3]["Low"])
    prev1 = Candlestick(data.iloc[-2]["High"], data.iloc[-2]["Open"], data.iloc[-2]["Close"], data.iloc[-2]["Low"])
    curr = Candlestick(data.iloc[-1]["High"], data.iloc[-1]["Open"], data.iloc[-1]["Close"], data.iloc[-1]["Low"])
    # print(prev2.high)


    if(shares):
        for x in shares:
            if (x < curr.low and sellCSPattern(prev2, prev1, curr)) or curr.low / x < 0.95:
                assets["fund"] += unit * curr.low / x
                currLog = f"{now}: Sold {ticker} at {x}\n" + currLog
                # log.write(f"Sold {ticker} at {x:.2f}\n")
                shares.remove(x)

    if(assets["fund"] > unit and buyCSPattern(prev2, prev1, curr)):
        assets["fund"] -= unit
        # log.write("Buying " + ticker + " at " + str(curr.high) +  "\n")
        currLog = now + ": Buying " + ticker + " at " + str(curr.high) +  "\n" + currLog
        shares.append(curr.high)

    #updates the shares list in assets dictionary
    assets[ticker] = shares

    # total = assets["fund"]
    total = assets.get("stocks", 0)
    for x in shares: total += 10 * curr.low/x
    assets["stocks"] = total
log = open("./" + user + "/logs.txt", "w")
log.write(currLog)
log.close()

with open("./" + user + "/assets.json", "w") as json_file:
    json.dump(assets, json_file)