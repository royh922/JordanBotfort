# %%
import requests
import io
import pandas as pd
from pandas import json_normalize 
import sys
from datetime import date
import json

#specifies user and ticker from command line parameters
user = sys.argv[1]
# user = "roy_h92"

ticker = sys.argv[2]
# ticker = input("Please specify ONE ticker to track: ") #decares stock ticker to track

today = "startDate=" + date.today().strftime("%Y-%m-%d")
# today = "startDate=2022-11-18"

token = "&token=6c67dc599e26dbdd802b077e38f2d55a559a6ad9" #api token! KEEP SAFE!

requestResponse = requests.get("https://api.tiingo.com/iex/" + ticker + "/prices?" + today + "&resampleFreq=1min" + token)
# requestResponse = requests.get("https://api.tiingo.com/iex/?tickers=aapl" + token)

data = json_normalize(requestResponse.json()) #put pulled data into a pandas dataframe object


data["date"] = data["date"].str.split(".")
data["date"] = data["date"].str[0]
data["date"] = data["date"].str.split("T")
data["date"] = data["date"].str[0] + " " + data["date"].str[1]
data["date"] = data["date"].str.slice(stop = -3)
data.rename(columns={"date" : "time"}, inplace = True)
# data

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
    elif (new.top_wick/new.bottom_wick > 3) and (new.bullish == False) and (new.top_wick/new.body > 2): return True
    
    #No Sell Pattern
    else: return False

# %%
#creates candle stick from data
length = len(data) - 1
prev2 = Candlestick(data.iloc[length - 2]["high"], data.iloc[length - 2]["open"], data.iloc[length - 2]["close"], data.iloc[length - 2]["low"])
prev1 = Candlestick(data.iloc[length - 1]["high"], data.iloc[length - 1]["open"], data.iloc[length - 1]["close"], data.iloc[length - 1]["low"])
curr = Candlestick(data.iloc[length]["high"], data.iloc[length]["open"], data.iloc[length]["close"], data.iloc[length]["low"])

# %%
assets = dict()
shares = []
try:
    with open("./" + user + "/assets.json") as json_file:
        assets = json.load(json_file)
    shares = assets.get(ticker, [])
except FileNotFoundError:
    assets["fund"] = 100.0
    

unit = 10 #unit of stock to buy (in dollars)

# %%
log = open("./" + user + "/logs.txt", "a")

if(shares and sellCSPattern(prev2, prev1, curr)):
    for x in shares:
        if x < curr.low:
            assets["fund"] += unit * curr.low / x
            log.write(data.iloc[len(data) - 1]["time"] + " Available funds: " + str(assets["fund"]) + "\n")
            log.write(f"Sold {x:.2f}\n")
            shares.remove(x)
            log.write("Current shares: " + " ".join(str(i) for i in shares) + "\n")
            log.write("\n")

if(assets["fund"] > unit and buyCSPattern(prev2, prev1, curr)):
    assets["fund"] -= unit
    log.write(data.iloc[len(data) - 1]["time"] + " Available funds: " + str(assets["fund"]) + "\n")
    log.write("Buying: " + ticker + "at " + str(curr.high) +  "\n")
    shares.append(curr.high)
    log.write("Current shares: " + " ".join(str(i) for i in shares) + "\n")
    log.write("\n")

#updates the shares list in assets dictionary
assets[ticker] = shares

# total = assets["fund"]
total = assets.get("stocks", 0)
for x in shares: total += 10 * curr.low/x
assets["stocks"] = total

# status = open("./" + user + "/status.txt", "a")

#updates current asset with all owned stocks

# status.write(data.iloc[len(data) - 1]["time"] + " %.2f\n" %total)

# status.close()
log.close()

with open("./" + user + "/assets.json", "w") as json_file:
    json.dump(assets, json_file)
    


