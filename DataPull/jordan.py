import requests
import io
import pandas as pd
from datetime import date

today = "startDate=" + date.today().strftime("%Y-%m-%d")
# today = "startDate=2022-09-21"
ticker = "aapl" #decares stock ticker to track
token = "&token=6c67dc599e26dbdd802b077e38f2d55a559a6ad9"

requestResponse = requests.get("https://api.tiingo.com/iex/aapl/prices?" + today + "&resampleFreq=1min" + token)
rawData = pd.DataFrame(requestResponse.json())
filtered = rawData[["date", "close", "high", "low", "open"]].copy()
filtered["bar"] = filtered["close"] - filtered["open"]

log = open("log.txt", "a+")

capitlal = 10000 #all availabe funds
unit = 100 #unit of stock to buy (in dollars)
shares = [] #list to record all holdings
prev2 = filtered.iloc[0]["bar"]
prev1 = filtered.iloc[1]["bar"]
for i in range(2, len(filtered)):
    curr = filtered.iloc[i]["bar"]
    for x in shares:
        if x < filtered.iloc[i]["low"]:
            capitlal += unit * filtered.iloc[i]["low"] / x
            log.write(filtered.iloc[i]["date"] + "\t" + str(unit) + "\t" + str(filtered.iloc[i]["low"]) + "\t" + str(capitlal) + "\n")
            shares.remove(x)
    if prev2 < 0 and prev1 < 0 and curr < 0:
        capitlal -= unit
        shares.append(filtered.iloc[i]["high"])
    prev2 = prev1
    prev1 = curr


log.close()