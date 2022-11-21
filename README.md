# JordanBotfort
A Discord bot that makes trading decisions by identifying "candlestick" patterns computationally

## How to operate JordanBotfort (Disord Bot)
* Jordan.java and commands.java under discord_bot/src/main/java/me/JordanBotfort/bot
* After adding the Jordan onto your discord server, type in commands like:
    * !track *ticker* --adds a stock to track and trade
    * !graph --outputs current assets performance
    * !stocks --displays all tracked stocks

## How to run backend trade program (and make modifications in algorithm)
Download jordan.py and run the program. Requires user defined stock ticker input. 
* All transaction log is printed to trans_log/
* All availabe asset is printed to price_log/ and each line is formatted as funds followed by the list of values of each stock at time of purchase
* All graph output is saved to figs/

## Functionalities to be implemented in the future
* Multi stock trading
* Full integration with discord text-based command control
