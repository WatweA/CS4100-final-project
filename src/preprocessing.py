#!/usr/bin/python

import numpy as np
import pandas as pd


class GeometricBrownianMotion:
    """
    A class to implement a GBM model with given drift, volatility, time span,
    """

    def __init__(self, s0, mu, sigma, T=1, dt=0.01):
        self.s0 = s0  # the starting level/price
        self.mu = mu  # drift/expected return component
        self.sigma = sigma  # volatility component
        self.T = T  # time span over which to simulate
        self.dt = dt  # number of steps to simulate (i.e. the granularity for simulation over T)
        self.N = int(T / dt)  # the number of total simulation steps

    def simulate(self):
        """
        simulate GBM and return the prices over time as an array
        :return: a Numpy array of prices for this simulated price motion
        """
        ticks = np.linspace(0, self.T, num=self.N)
        # calculate standard Brownian motion over the tick-space
        W = np.random.standard_normal(size=self.N)
        W = np.cumsum(W) * np.sqrt(self.dt)
        # geometric Brownian motion over the tick-space
        X = (self.mu - (self.sigma ** 2) / 2) * ticks + self.sigma * W
        return np.array(self.s0 * np.exp(X))

    def simulate_average_sT(self, n_simulations):
        """
        Return the average final price sT for this GBM over a given number of simulations
        :param n_simulations: the number of simulations to run
        :return: the average ending price, sT
        """
        sT = 0.0
        for i in range(n_simulations):
            sT += self.simulate()[-1]
        return sT / n_simulations


tickers = list([
    "SPY",  # S&P 500 Index Fund
    "IWV",  # Russell 3000 Index Fund
    "QQQ",  # Technology Sector Fund
    "IYF",  # Financials Sector Fund
    # "XRT",  # Consumer Cyclical Sector Fund -> remove due to 2006-06-22 start date
    "XLP",  # Consumer Staples Sector Fund
    "XLU",  # Utilities Sector Funds
    "XLV",  # Health Care Sector Funds
    # "IYT",  # Transportation Sector Fund -> remove due to 2004-01-02 start date
    # "GLD",  # Precious Metals Sector: Gold -> remove due to 2004-11-18 start date
    # "SLV",  # Precious Metals Sector: Silver -> remove due to 2006-04-28 start date
    # "MXI",  # Global Materials ETF -> remove due to 2006-09-22 start date
    "IGE",  # NA Natural Resources ETF
    "XLE"  # Energy Sector Fund
])

indicators = {
    "3M_TBILL": "DTB3",  # 3-Month Treasury Bill: Secondary Market Rate
    "CPI": "MEDCPIM158SFRBCLE",  # Median Consumer Price Index
    "VIX": "VIXCLS",  # CBOE Volatility Index
    "INDP": "INDPRO",  # Industrial Production: Total Index
    "USHY_ADJ": "BAMLH0A0HYM2",  # ICE BofA US High Yield Index Option-Adjusted Spread
    "US_LEADING": "USSLIND",  # Leading Index for the United States
    "30Y_FRMTG": "MORTGAGE30US",  # 30-Year Fixed Rate Mortgage Average in the United States
    "15Y_FRMTG": "MORTGAGE15US",  # 15-Year Fixed Rate Mortgage Average in the United States
    "CPI_URBAN": "CUSR0000SEHA",  # Consumer Price Index for All Urban Consumers:
    # Rent of Primary Residence in U.S. City Average
    "RETAIL": "RSAFS",  # Advance Retail Sales: Retail and Food Services, Total
    "PHARMA": "PCU32543254",  # Producer Price Index by Industry: Pharmaceutical and Medicine Manufacturing
    "UNEMP": "UNRATE",  # Unemployment Rate
    "UNEMP_PERM": "LNS13026638",  # Unemployment Level - Permanent Job Losers
    "UNEMP_MEN": "LNS14000001",  # Unemployment Rate - Men
    "UNEMP_WMN": "LNS14000002",  # Unemployment Rate - Women
    "UNEMP_WHT": "LNS14000003",  # Unemployment Rate - White
    "UNEMP_BLK": "LNS14000006",  # Unemployment Rate - Black or African American
    "UNEMP_HIS": "LNS14000009",  # Unemployment Rate - Hispanic or Latino
    "INC": "PI",  # Personal Income
    "INC_DISP": "DSPIC96",  # Real Disposable Personal Income
    "INC_DISP_PC": "A229RX0",  # Real Disposable Personal Income: Per Capita
    "TAX_HIGH": "IITTRHB",  # U.S Individual Income Tax: Tax Rates for Regular Tax: Highest Bracket
    "TAX_LOW": "IITTRLB"  # U.S Individual Income Tax: Tax Rates for Regular Tax: Lowest Bracket
}


# initialize dataframe with trading day indices
dates = pd.date_range(start='1998-01-01', end='2021-03-01', freq="D")
market_data = pd.DataFrame(index=dates)  # trading dates


# for ticker in tickers:
for ticker in tickers:
    df = pd.read_pickle(f"data/etfs/{ticker}.zip")
    df["USD Volume"] = df["Adj Close"] * df["Volume"]

    # add the 1-month look-ahead return as a target column
    market_data[F"{ticker}_TARGET"] = ((df["Adj Close"] - df["Adj Close"].shift(21)) / df["Adj Close"]).shift(-21)

    # establish the rolling windows for both tickers in the pair
    rolling_1w = df.rolling(10)
    rolling_1m = df.rolling(21)
    rolling_3m = df.rolling(63)
    rolling_6m = df.rolling(126)
    rolling_1y = df.rolling(252)

    # add the rolling mean returns
    market_data[f"{ticker}_1D_RET"] = df["Simple Return"]
    market_data[f"{ticker}_1W_RET"] = rolling_1w["Simple Return"].mean()
    market_data[f"{ticker}_1M_RET"] = rolling_1w["Simple Return"].mean()
    market_data[f"{ticker}_3M_RET"] = rolling_1w["Simple Return"].mean()
    market_data[f"{ticker}_6M_RET"] = rolling_1w["Simple Return"].mean()
    market_data[f"{ticker}_1Y_RET"] = rolling_1w["Simple Return"].mean()

    # add the rolling volatility ratios
    market_data[f"{ticker}_1W_STD"] = rolling_1w["Log Return"].std(ddof=0)
    market_data[f"{ticker}_1M_STD"] = rolling_1m["Log Return"].std(ddof=0)
    market_data[f"{ticker}_3M_STD"] = rolling_3m["Log Return"].std(ddof=0)
    market_data[f"{ticker}_6M_STD"] = rolling_6m["Log Return"].std(ddof=0)
    market_data[f"{ticker}_1Y_STD"] = rolling_1y["Log Return"].std(ddof=0)

    # add the volume in USD
    market_data[f"{ticker}_1D_VOL"] = df["USD Volume"]
    market_data[f"{ticker}_1W_VOL"] = rolling_1w["USD Volume"].mean()
    market_data[f"{ticker}_1M_VOL"] = rolling_1m["USD Volume"].mean()
    market_data[f"{ticker}_3M_VOL"] = rolling_3m["USD Volume"].mean()
    market_data[f"{ticker}_6M_VOL"] = rolling_6m["USD Volume"].mean()
    market_data[f"{ticker}_1Y_VOL"] = rolling_1y["USD Volume"].mean()

    # add the geometric Brownian motion projections
    market_data[f"{ticker}_1W_GBM"] = [GeometricBrownianMotion(1, mu, sigma).simulate_average_sT(500) - 1
                                       for mu, sigma in zip(list(market_data[f"{ticker}_1W_RET"]),
                                                            list(market_data[f"{ticker}_1W_STD"]))]
    market_data[f"{ticker}_1M_GBM"] = [GeometricBrownianMotion(1, mu, sigma).simulate_average_sT(500) - 1
                                       for mu, sigma in zip(list(market_data[f"{ticker}_1M_RET"]),
                                                            list(market_data[f"{ticker}_1M_STD"]))]
    market_data[f"{ticker}_3M_GBM"] = [GeometricBrownianMotion(1, mu, sigma).simulate_average_sT(500) - 1
                                       for mu, sigma in zip(list(market_data[f"{ticker}_3M_RET"]),
                                                            list(market_data[f"{ticker}_3M_STD"]))]
    market_data[f"{ticker}_6M_GBM"] = [GeometricBrownianMotion(1, mu, sigma).simulate_average_sT(500) - 1
                                       for mu, sigma in zip(list(market_data[f"{ticker}_6M_RET"]),
                                                            list(market_data[f"{ticker}_6M_STD"]))]


for alias, indicator in indicators.items():
    df = pd.read_pickle(f"data/indicators/{indicator}.zip")
    df.columns = [alias]
    # for indicators in the following list, convert the index values to percent change
    to_convert = {"INDP", "CPI_URBAN", "RETAIL", "PHARMA", "INC", "INC_DISP", "INC_DISP_PC"}
    if alias in to_convert:
        market_data[alias] = (df[alias] - df[alias].shift(1)) / df[alias]
    else:
        market_data[alias] = df[alias]

market_data.fillna(method="ffill", inplace=True)
market_data.dropna(inplace=True)
market_data = market_data.loc['2003-01-01':'2020-12-31', :]
market_data.to_pickle("data/market_data.zip")

print(market_data)
