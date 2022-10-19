import pandas as pd

#Obtained (1 = oldest, 3 = newest)
high = 116.93
open = 116.39
close = 116.83
low = 116.29
high2 = 116.95
open2 = 116.83
close2 = 116.84
low2 = 116.48
high3 = 116.74
open3 = 116.71
close3 = 115.71
low3 = 115.19


# Derived
#top = 101.33
#bottom = 100.15
#bullish = False
#top_wick = high - top
#body = top - bottom
#bottom_wick = bottom - low


# Class to create Candlestick object
class Candlestick():
    def __init__(self,high,open,close,low):
        if (close-open < 0):            # If close-open is negative, make it a bearish object
            self.bullish = False
            self.top = open
            self.bottom = close
        else:
            self.bullish = True
            self.top = close
            self.bottom = open
        self.high = high
        self.low = low
        self.top_wick = high - self.top
        self.body = self.top - self.bottom
        self.bottom_wick = self.bottom - low
        self.mid = self.body/2
        self.body_ratio = self.body/(self.high-self.low)


# Recognition for Single Candlestick Patterns only
def recognSingleCSPattern(new):
    # Could change to new.high == new.top for a more strict pattern
    if (new.bottom_wick/new.top_wick > 3) and (new.bullish == True) and (new.bottom_wick/new.body > 2): # Hammer, gain
        print("Hammer!")
    elif (new.bottom_wick/new.top_wick > 3) and (new.bullish == False) and (new.bottom_wick/new.body > 2): # Hangman, lose
        print("Hangman!") #Confirmed to work
    elif (new.top_wick/new.bottom_wick > 3) and (new.bullish == True) and (new.top_wick/new.body > 2): # Inverse Hammer, gain
        print("Inverse Hammer!")
    elif (new.top_wick/new.bottom_wick > 3) and (new.bullish == False) and (new.top_wick/new.body > 2): # Shooting Star, lose
        print("Shooting Star!")
    else:
        print("No Single Candlestick Patterns")


# Recognition for Double Candlestick Patterns only
def recognDoubleCSPattern(prev,new):
    if (prev.bullish == False) and (new.bullish == True) and (prev.bottom > new.bottom) and (prev.top < new.top) and (new.body/prev.body > 1):
        print("Bullish Engulfing!") # gain
    elif (prev.bullish == False) and (new.bullish == True) and (new.mid < prev.mid < new.top) and (prev.body_ratio > .75) and (new.body_ratio > .75):
        print("Piercing Line!") # gain
    elif (prev.bullish == True) and (new.bullish == False) and (prev.bottom > new.bottom) and (prev.top < new.top) and (new.body/prev.body > 1):
        print("Bearish Engulfing!") # Confirmed to work, lose
    elif (prev.bullish == True) and (new.bullish == False) and (new.bottom < prev.mid < new.mid) and (prev.body_ratio > .75) and (new.body_ratio > .75):
        print("Dark Cloud Cover!") # lose
    else:
        print("No Double Candlestick Patterns")


# Recognition for Triple Candlestick Patterns only
def recognTripleCSPattern(prev2,prev1,new):
    if (new.bullish == True) and (prev1.bullish == True) and (prev2.bullish == True):
        # new.body_ratio > .75 (for new,prev1,prev2) and...
        # prev2.mid < prev1.bottom and prev1.mid < new.bottom for a stronger pattern
        print("3 White Soldiers!") # gain
    elif (new.bullish == False) and (prev1.bullish == False) and (prev2.bullish == False):
        print("3 Black Crows!") # lose
    elif (new.bullish == True) and (prev1.bullish == False) and (prev2.bullish == False) and (prev2.body_ratio > .65) and (new.body_ratio > .75) and (prev2.bottom > prev1.mid) and (new.bottom > prev1.mid):
        # Change last 2 conditons from mid to top to not allow bar overlap, more strict/traditional pattern
        print("Morning Star!")
    elif(new.bullish == False) and (prev1.bullish == True) and (prev2.bullish == True) and (prev2.body_ratio > .65) and (new.body_ratio > .6) and (prev2.mid < prev1.bottom) and (new.top < prev1.bottom):
        # Same thing...can change mid at end to top to create a more strict pattern
        print("Evening Star!")
    else:
        print("No Triple Candlestick Patterns")


def main():
    new = Candlestick(high,open,close,low)
    recognSingleCSPattern(new)

    prev = new
    new = Candlestick(high2,open2,close2,low2)
    recognDoubleCSPattern(prev,new)

    prev2 = prev
    prev = new
    new = Candlestick(high3,open3,close3,low3)
    recognTripleCSPattern(prev2,prev,new)

main()
