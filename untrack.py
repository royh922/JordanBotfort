# %%
import io
import pandas as pd
import sys
import json
import yfinance as yf

user = sys.argv[1]
# user = "roy_h92"
ticker = sys.argv[2]
# ticker = "AAPL"
Data = yf.download(ticker, period= "1d", interval = "1m", actions=False, group_by="ticker")
Data = Data.dropna()
price = Data.iloc[-1]["Close"]

# %%
#updates total assets
shares = []
funds = 0
try:
    with open("./" + user + "/assets.json") as json_file:
        assets = json.load(json_file)
    shares = assets.get(ticker)
    funds = assets.get("fund", 0)
except FileNotFoundError:
    quit()

for x in shares:
    funds += 10 * price/x

assets.pop(ticker)

assets["fund"] = funds

with open("./" + user + "/assets.json", "w") as json_file:
    json.dump(assets, json_file)

