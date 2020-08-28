import pandas as pd
from datareader import YahooFinanceHistory
from datetime import datetime, timedelta
from companyStatScraper import getRiskFreeRate
import time
import math

INVESTABLE_ETFS = pd.read_csv("investable_tickers.csv", header=None).values.tolist()
for i in range(len(INVESTABLE_ETFS)):
    INVESTABLE_ETFS[i] = INVESTABLE_ETFS[i][0]

# TODO: What combo of 5 will maximize sharpe ratio
def getSharpe(tickers):
    rets = []
    stds = []
    rfs = []
    corrs = []
    notInclude = []
    i = 1
    start = int(time.mktime((datetime.today() - timedelta(days=740)).timetuple()))
    spy = YahooFinanceHistory("SPY", start, None).download_quotes()
    spy = spy[['Date', 'Adj Close']]
    spy.set_index("Date", inplace=True)
    spy = spy.pct_change().dropna()
    spy.rename(columns={"Adj Close": 'SPY Price Change'}, inplace=True)
    for ticker in tickers:
        print(i, ticker)
        i += 1
        try:
            df = YahooFinanceHistory(ticker, start, None).download_quotes()
            df = df[['Date', 'Adj Close']]
            df.set_index('Date', inplace=True)
            df.rename(columns={'Adj Close' : 'Price'}, inplace=True)
            df['PriceChange'] = df['Price'].pct_change().dropna()
            corr = pd.DataFrame()
            corr['PriceChange'] = df['PriceChange']
            corr['SPY Price Change'] = spy['SPY Price Change']
            corr = corr.dropna().corr().values[0][1]
            beg, end = df.values[0][0], df.values[-1][0]
            ret = ((end - beg) / beg) * 100
            std = df['PriceChange'].std()*math.sqrt(252)*100
            print(std)
            rfs += [float(getRiskFreeRate())]
            rets += [ret]
            stds += [std]
            corrs += [corr]
        except Exception as e:
            print(ticker, e)
            notInclude += [ticker]
            # Try one more time
            # tickers += [ticker]
            continue
    for tick in notInclude:
        tickers = list(filter((tick).__ne__, tickers))
    df = pd.DataFrame({"Ticker" : tickers, "Return": rets, "Standard Deviation": stds, "Risk-Free Rate": rfs, 'Beta (S&P)': corrs})
    df.set_index("Ticker", inplace=True)
    df['Sharpe Ratio'] = (df['Return'] - df['Risk-Free Rate']) / df['Standard Deviation']
    df = df[df['Return'] > 5]
    df.sort_values(by="Sharpe Ratio", inplace=True, ascending=False)
    # df.to_csv("ETF_Sharpe_Ratios.csv")

getSharpe(['QQQ'])