#!/usr/bin/python


import time
from datetime import datetime
import numpy as np
from pandas_datareader import get_data_yahoo as yahoo
from pandas_datareader import get_data_fred as fred


tickers = list([
    "SPY",  # S&P 500 Index Fund
    "IWV",  # Russell 3000 Index Fund
    "QQQ",  # Technology Sector Fund
    "IYF",  # Financials Sector Fund
    "XRT",  # Consumer Cyclical Sector Fund
    "XLP",  # Consumer Staples Sector Fund
    "XLU",  # Health Care Sector Funds
    "XLV",  # Health Care Sector Funds
    "IYT",  # Transportation Sector Fund
    "GLD",  # Precious Metals Sector: Gold
    "SLV",  # Precious Metals Sector: Silver
    "MXI",  # Global Materials ETF
    "IGE",  # NA Natural Resources ETF
    "XLE"   # Energy Sector Fund
])


for ticker in tickers:
    try:
        df = yahoo(symbols=ticker, start=datetime(1999, 1, 4), end=datetime(2021, 3, 1))
        df["Simple Return"] = (df["Adj Close"] - df["Adj Close"].shift(1)) / df["Adj Close"]
        df["Log Return"] = np.log(df["Adj Close"]) - np.log(df["Adj Close"].shift(1))
        df.to_pickle("data/etfs/" + ticker + ".zip")
        print(f"saved {ticker}")
    except (KeyError, IOError) as e:
        print(f"API ERROR {ticker}")


indicators = list([
    "DTB3",  # 3-Month Treasury Bill: Secondary Market Rate
    "MEDCPIM158SFRBCLE",  # Median Consumer Price Index
    "VIXCLS",  # CBOE Volatility Index
    "INDPRO",  # Industrial Production: Total Index
    "BAMLH0A0HYM2",  # ICE BofA US High Yield Index Option-Adjusted Spread
    "USSLIND",  # Leading Index for the United States
    "MORTGAGE30US",  # 30-Year Fixed Rate Mortgage Average in the United States
    "MORTGAGE15US",  # 15-Year Fixed Rate Mortgage Average in the United States
    "CUSR0000SEHA",  # Consumer Price Index for All Urban Consumers: Rent of Primary Residence in U.S. City Average
    "RSAFS",  # Advance Retail Sales: Retail and Food Services, Total
    "PCU32543254",  # Producer Price Index by Industry: Pharmaceutical and Medicine Manufacturing
    "UNRATE",  # Unemployment Rate
    "LNS13026638",  # Unemployment Level - Permanent Job Losers
    "LNS14000001",  # Unemployment Rate - Men
    "LNS14000002",  # Unemployment Rate - Women
    "LNS14000003",  # Unemployment Rate - White
    "LNS14000006",  # Unemployment Rate - Black or African American
    "LNS14000009",  # Unemployment Rate - Hispanic or Latino
    "USSLIND",  # Leading Index for the United States
    "PI",  # Personal Income
    "DSPIC96",  # Real Disposable Personal Income
    "A229RX0",  # Real Disposable Personal Income: Per Capita
    "IITTRHB",  # U.S Individual Income Tax: Tax Rates for Regular Tax: Highest Bracket
    "IITTRLB"   # U.S Individual Income Tax: Tax Rates for Regular Tax: Lowest Bracket
])


for indicator in indicators:
    try:
        df = fred(symbols=indicator, start=datetime(1999, 1, 4), end=datetime(2021, 3, 1))
        df.to_pickle("data/indicators/" + indicator + ".zip")
        print(f"saved {indicator}")
    except (KeyError, IOError) as e:
        print(f"API ERROR {indicator}")


