# JordanBotfort
A Discord bot that makes trading decisions by identifying "candlestick" patterns computationally

## How to operate JordanBotfort (Disord Bot)
* Clone repo to your local machine
* After making your discord bot and adding it to your server, paste your API token into Jordan.java
    * Project is handled by Gradle, so make sure that's installed
* Install the required python libraries including:
    * pandas
    * matplotlib
    * yfinance
    * Note your python path, you may need to change the variable python in Commands.java under !run else if statement to fit your local python path
* After adding the Jordan onto your discord server and running, type in commands like:
    * !track *ticker* --adds a stock to track and trade
    * !untrack *ticker* --removes a stock to track and trade
    * !stocks --displays all tracking stocks
    * !graph --visualizes assets performance
    * !log --displays transaction records
* Happy trading!

## How to run backend trade program (and make modifications in algorithm)
Download jordan.py and run the program. Requires user defined stock ticker input. 
* All transaction log is printed to trans_log/
* All availabe asset is printed to price_log/ and each line is formatted as funds followed by the list of values of each stock at time of purchase
* All graph output is saved to figs/

## Functionalities to be implemented in the future
* More advanced signal analysis
