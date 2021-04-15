#!/usr/bin/python

import numpy as np
import pandas as pd


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

indicators = {
    "3M_TBILL" : "DTB3",  # 3-Month Treasury Bill: Secondary Market Rate
    "CPI" : "MEDCPIM158SFRBCLE",  # Median Consumer Price Index
    "VIX" : "VIXCLS",  # CBOE Volatility Index
    "INDP" : "INDPRO",  # Industrial Production: Total Index
    "USHY_ADJ" : "BAMLH0A0HYM2",  # ICE BofA US High Yield Index Option-Adjusted Spread
    "US_LEADING" : "USSLIND",  # Leading Index for the United States
    "30Y_FRMTG" : "MORTGAGE30US",  # 30-Year Fixed Rate Mortgage Average in the United States
    "15Y_FRMTG" : "MORTGAGE15US",  # 15-Year Fixed Rate Mortgage Average in the United States
    "CPI_URBAN" : "CUSR0000SEHA",  # Consumer Price Index for All Urban Consumers: Rent of Primary Residence in U.S. City Average
    "RETAIL" : "RSAFS",  # Advance Retail Sales: Retail and Food Services, Total
    "PHARMA" : "PCU32543254",  # Producer Price Index by Industry: Pharmaceutical and Medicine Manufacturing
    "UNEMP" : "UNRATE",  # Unemployment Rate
    "UNEMP_PERM" : "LNS13026638",  # Unemployment Level - Permanent Job Losers
    "UNEMP_MEN" : "LNS14000001",  # Unemployment Rate - Men
    "UNEMP_WMN" : "LNS14000002",  # Unemployment Rate - Women
    "UNEMP_WHT" : "LNS14000003",  # Unemployment Rate - White
    "UNEMP_BLK" : "LNS14000006",  # Unemployment Rate - Black or African American
    "UNEMP_HIS" : "LNS14000009",  # Unemployment Rate - Hispanic or Latino
    "INC" : "PI",  # Personal Income
    "INC_DISP" : "DSPIC96",  # Real Disposable Personal Income
    "INC_DISP_PC" : "A229RX0",  # Real Disposable Personal Income: Per Capita
    "TAX_HIGH" : "IITTRHB",  # U.S Individual Income Tax: Tax Rates for Regular Tax: Highest Bracket
    "TAX_LOW" : "IITTRLB"   # U.S Individual Income Tax: Tax Rates for Regular Tax: Lowest Bracket
}


# initialize dataframe with trading day indices
dates = pd.date_range(start='1999-01-01', end='2021-03-01', freq="D")
market_data = pd.DataFrame(index=dates)  # trading dates


for ticker in tickers:
    df = pd.read_pickle(f"data/etfs/{ticker}.zip")
    # save the ticker's return and volume into market_data
    market_data[f"{ticker}_1DRET"] = (df["Adj Close"] - df["Adj Close"].shift(1)) / df["Adj Close"]
    market_data[f"{ticker}_1WRET"] = (df["Adj Close"] - df["Adj Close"].shift(5)) / df["Adj Close"]
    market_data[f"{ticker}_1MRET"] = (df["Adj Close"] - df["Adj Close"].shift(21)) / df["Adj Close"]
    market_data[f"{ticker}_6MRET"] = (df["Adj Close"] - df["Adj Close"].shift(126)) / df["Adj Close"]
    market_data[f"{ticker}_1YRET"] = (df["Adj Close"] - df["Adj Close"].shift(252)) / df["Adj Close"]
    market_data[f"{ticker}_1DAVGRET"] = (market_data[f"{ticker}_1DRET"]).fillna(method="ffill").rolling(5).mean()
    market_data[f"{ticker}_1WAVGRET"] = (market_data[f"{ticker}_1WRET"]).fillna(method="ffill").rolling(5).mean()
    market_data[f"{ticker}_1MAVGRET"] = (market_data[f"{ticker}_1MRET"]).fillna(method="ffill").rolling(21).mean()
    market_data[f"{ticker}_6MAVGRET"] = (market_data[f"{ticker}_6MRET"]).fillna(method="ffill").rolling(21).mean()
    market_data[f"{ticker}_1YAVGRET"] = (market_data[f"{ticker}_1YRET"]).fillna(method="ffill").rolling(21).mean()
    market_data[f"{ticker}_1DVOL"] = df["Volume"]
    market_data[f"{ticker}_1WVOL"] = df["Volume"].rolling(5).sum()
    market_data[f"{ticker}_1MVOL"] = df["Volume"].rolling(21).sum()

for alias, indicator in indicators.items():
    df = pd.read_pickle(f"data/indicators/{indicator}.zip")
    df.columns = [alias]
    # for indicators in the following list, convert the index values to percent change
    to_convert = {"INDP", "CPI_URBAN", "RETAIL", "PHARMA", "INC", "INC_DISP", "INC_DISP_PC"}
    if alias in to_convert:
        market_data[alias] = (df[alias] - df[alias].shift(1)) / df[alias]
    else:
        market_data[alias] = df[alias]

print(market_data)

market_data.fillna(method="ffill", inplace=True)
market_data.dropna(inplace=True)
market_data = market_data.loc['2008-01-01':'2021-03-01', :]
market_data.to_pickle("data/market_data.zip")

print(market_data)
