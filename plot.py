# %%
import io
import pandas as pd
import sys
from datetime import datetime
import json

user = sys.argv[1]
# user = "roy_h92"

# %%
#updates total assets
total = 0.0
try:
    with open("./" + user + "/assets.json") as json_file:
        assets = json.load(json_file)
    total = assets.get("stocks", 0) + assets.get("fund", 0)
except FileNotFoundError:
    quit()

try:    
    with open("./" + user + "/track.txt") as track_file:
        stocks = track_file.read()
except FileNotFoundError:
    quit()

status = open("./" + user + "/status.txt", "a")
now = datetime.now().strftime('%m/%d-%H:%M')
status.write(now + " %f\n" %total)
status.close()

# %%
data = pd.read_csv("./" + user + "/status.txt", sep=" ", header=None, names = ["Time", "Assets"])
fig = data.plot("Time", "Assets", figsize = (10, 7), title = "Total assets over time: " + stocks)
fig.figure.savefig("./" + user + "/fig.png")
