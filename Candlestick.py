import pandas as pd

#Obtained (1 = oldest, 3 = newest)
high = 113.97
open = 113.86
close = 113.61
low = 113.58
high2 = 113.64
open2 = 113.60
close2 = 113.58
low2 = 113.27
high3 = 114.14
open3 = 113.58
close3 = 114.11
low3 = 113.57


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

def buyCSPattern(prev2,prev1,new):
    if (new.bullish == True) and (prev1.bullish == True) and (prev2.bullish == True):
        print("3 White Soldiers!") # gain
        return True
    elif (new.bullish == True) and (prev1.bullish == False) and (prev2.bullish == False) and (prev2.body_ratio > .65) and (new.body_ratio > .75) and (prev2.bottom > prev1.mid) and (new.bottom > prev1.mid):
        print("Morning Star!") # gain
        return True
    elif (prev1.bullish == False) and (new.bullish == True) and (prev1.bottom > new.bottom) and (prev1.top < new.top) and (new.body/prev1.body > 1):
        print("Bullish Engulfing!") # gain
        return True
    elif (prev1.bullish == False) and (new.bullish == True) and (new.mid < prev1.mid < new.top) and (prev1.body_ratio > .75) and (new.body_ratio > .75):
        print("Piercing Line!") # gain
        return True
    elif (new.bottom_wick/new.top_wick > 3) and (new.bullish == True) and (new.bottom_wick/new.body > 2): # Hammer, gain
        print("Hammer!")
        return True
    elif (new.top_wick/new.bottom_wick > 3) and (new.bullish == True) and (new.top_wick/new.body > 2): # Inverse Hammer, gain
        print("Inverse Hammer!")
        return True
    else:
        print("No Buy Candlestick Patterns")
        return False

def sellCSPattern(prev2,prev1,new):
    if (new.bullish == False) and (prev1.bullish == False) and (prev2.bullish == False):
        print("3 Black Crows!") # lose
        return True
    elif(new.bullish == False) and (prev1.bullish == True) and (prev2.bullish == True) and (prev2.body_ratio > .65) and (new.body_ratio > .6) and (prev2.mid < prev1.bottom) and (new.top < prev1.bottom):
        print("Evening Star!")
        return True
    elif (prev1.bullish == True) and (new.bullish == False) and (prev1.bottom > new.bottom) and (prev1.top < new.top) and (new.body/prev1.body > 1):
        print("Bearish Engulfing!") # Confirmed to work, lose
        return True
    elif (prev1.bullish == True) and (new.bullish == False) and (new.bottom < prev1.mid < new.mid) and (prev1.body_ratio > .75) and (new.body_ratio > .75):
        print("Dark Cloud Cover!") # lose
        return True
    elif (new.bottom_wick/new.top_wick > 3) and (new.bullish == False) and (new.bottom_wick/new.body > 2): # Hangman, lose
        print("Hangman!") #Confirmed to work
        return True
    elif (new.top_wick/new.bottom_wick > 3) and (new.bullish == False) and (new.top_wick/new.body > 2): # Shooting Star, lose
        print("Shooting Star!")
        return True
    else:
        print("No Sell Candlestick Patterns")
        return False



def main():
    new = Candlestick(high,open,close,low)
    prev = new
    new = Candlestick(high2,open2,close2,low2)
    prev2 = prev
    prev1 = new
    new = Candlestick(high3,open3,close3,low3)

    bool1 = buyCSPattern(prev2,prev1,new)
    bool2 = sellCSPattern(prev2,prev1,new)



main()
