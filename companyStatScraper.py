from bs4 import BeautifulSoup
import pickle
import os
import pandas as pd
from datareader import YahooFinanceHistory
import requests as re
import time
from datetime import datetime, timedelta
import math

# soup = None
toPickle = False
usePickle = False
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' }
def getInstiutionalOwnership(ticker):
    global toPickle
    global usePickle
    global headers
    # global soup
    # if soup is None:
    if usePickle:
        with open("./backupData/{0}/{0}-Inst-Ownership".format(ticker), 'rb') as f:
            pick = pickle.load(f)
            f.close()
            return pick
    else:
        url = "https://finance.yahoo.com/quote/{0}/key-statistics?p={0}".format(ticker)
        site = re.get(url, headers=headers)
        soup = BeautifulSoup(site.content)
        tables = soup.find_all('table')
        # 5 is profit margin table
        # 8 is balance sheet
        # 2 is share statistics
        # Now its 1?
        shareStats = tables[2].find_all('tr')

        insiderOwn = shareStats[4].find_all('td')[-1].text[:-1]
        institutionOwn = shareStats[5].find_all('td')[-1].text[:-1]
        retailOwn = 100 - float(institutionOwn) - float(insiderOwn)
        if toPickle:
            if not os.path.exists("backupData/{0}".format(ticker)):
                os.mkdir("backupData/{0}".format(ticker))
            with open("./backupData/{0}/{0}-Inst-Ownership".format(ticker), 'wb') as f:
                pickle.dump({"Insider": float(insiderOwn), "Institutional": float(institutionOwn), "Mutual Fund/Retail": float(retailOwn)}, f)
                f.close()
        return {"Insider": float(insiderOwn), "Institutional": float(institutionOwn), "Mutual Fund/Retail": float(retailOwn)}

def getShortShares(ticker):
    global toPickle
    global usePickle
    global headers
    # global soup
    # if soup is None:
    if usePickle:
        with open("./backupData/{0}/{0}-Short-Shares".format(ticker), 'rb') as f:
            pick = pickle.load(f)
            f.close()
            return pick
    else:
        url = "https://finance.yahoo.com/quote/{0}/key-statistics?p={0}".format(ticker)
        site = re.get(url, headers=headers)
        soup = BeautifulSoup(site.content)
        tables = soup.find_all('table')
        # Used to be 2?
        shareStats = tables[2].find_all('tr')
        shareOutStand = shareStats[2].find_all('td')[-1].text
        titleThisMo = shareStats[6].find_all('span')[0].text
        shortThisMo = shareStats[6].find_all('td')[-1].text
        shortPct = shareStats[9].find_all('td')[-1].text
        titleLastMo = shareStats[10].find_all('span')[0].text
        shortLastMo = shareStats[10].find_all('td')[-1].text
        if toPickle:
            if not os.path.exists("backupData/{0}".format(ticker)):
                os.mkdir("backupData/{0}".format(ticker))
            with open("./backupData/{0}/{0}-Short-Shares".format(ticker), 'wb') as f:
                pickle.dump([["Total Shares Outstanding", titleThisMo, "% Of Shares Outstanding Short", titleLastMo], [shareOutStand, shortThisMo, shortPct, shortLastMo]], f)
                f.close()
        return [["Total Shares Outstanding", titleThisMo, "% Of Shares Outstanding Short", titleLastMo], [shareOutStand, shortThisMo, shortPct, shortLastMo]]

def getEarningsHist(ticker):
    global toPickle
    global usePickle
    global headers
    if usePickle:
        with open("./backupData/{0}/{0}-Earnings-Hist".format(ticker), 'rb') as f:
            pick = pickle.load(f)
            f.close()
            return pick
    else:
        url = "https://finance.yahoo.com/quote/{0}/analysis?p={0}".format(ticker)
        site = re.get(url, headers=headers)
        soup = BeautifulSoup(site.content, "html")
        tables = soup.find_all('table')
        rows = tables[2].find_all("tr")
        dates = rows[0].find_all("span")
        dates = [date.text for date in dates][1:]
        epsEst = rows[1].find_all("td")
        epsEst = [eps.text for eps in epsEst][1:]
        epsAct = rows[2].find_all("td")
        epsAct = [eps.text for eps in epsAct][1:]
        if toPickle:
            if not os.path.exists("backupData/{0}".format(ticker)):
                os.mkdir("backupData/{0}".format(ticker))
            with open("./backupData/{0}/{0}-Earnings-Hist".format(ticker), 'wb') as f:
                pickle.dump([dates, epsEst, epsAct], f)
                f.close()
        return [dates, epsEst, epsAct]

def getCompanyBio(ticker):
    global toPickle
    global usePickle
    global headers
    if usePickle:
        with open("./backupData/{0}/{0}-Company-Bio".format(ticker), 'rb') as f:
            pick = pickle.load(f)
            f.close()
            return pick
    else:
        url = "https://finance.yahoo.com/quote/{0}/profile?p={0}".format(ticker)
        site = re.get(url, headers=headers)
        soup = BeautifulSoup(site.content)
        if toPickle:
            if not os.path.exists("backupData/{0}".format(ticker)):
                os.mkdir("backupData/{0}".format(ticker))
            with open("./backupData/{0}/{0}-Company-Bio".format(ticker), 'wb') as f:
                pickle.dump(soup.find_all("section")[3].find("p").text, f)
                f.close()
        return soup.find_all("section")[3].find("p").text

def getFundOwnership(ticker):
    global toPickle
    global usePickle
    global headers
    if usePickle:
        with open("./backupData/{0}/{0}-Fund-Ownership".format(ticker), 'rb') as f:
            pick = pickle.load(f)
            f.close()
            return pick
    else:
        url = "https://finance.yahoo.com/quote/{0}/holders?p={0}".format(ticker)
        site = re.get(url, headers=headers)
        soup = BeautifulSoup(site.content)
        institutional = soup.find_all('table')[1]
        titles = [name.text for name in institutional.find('tr').find_all('th')]
        institutionalRows = []
        for row in institutional.find_all('tr'):
            institutionalRows += [[name.text for name in row.find_all('td')]]
        institutionalRows = institutionalRows[1:]

        # Yahoo finance got rid of Mutual fund data
        # mutual = soup.find_all('table')[2]
        # mutualRows = []
        # for row in mutual.find_all('tr'):
        #     mutualRows += [[name.text for name in row.find_all('td')]]
        # mutualRows = mutualRows[1:]

        instFrame = pd.DataFrame(data = institutionalRows, columns = titles)
        # mutualFrame = pd.DataFrame(data = mutualRows, columns = titles)
        if toPickle:
            if not os.path.exists("backupData/{0}".format(ticker)):
                os.mkdir("backupData/{0}".format(ticker))
            with open("./backupData/{0}/{0}-Fund-Ownership".format(ticker), 'wb') as f:
                # pickle.dump([instFrame, mutualFrame], f)
                pickle.dump([instFrame], f)
                f.close()
        # return [instFrame, mutualFrame]
        return [instFrame]

def getOptionsData(ticker, date=None):
    global toPickle
    global usePickle
    global headers
    if usePickle:
        with open("./backupData/{0}/{0}-Option-Data".format(ticker), 'rb') as f:
            pick = pickle.load(f)
            f.close()
            return pick
    else:
        expiry = None
        if date is None:
            url = "https://finance.yahoo.com/quote/{0}/options?p={0}&straddle=true".format(ticker)
            site = re.get(url, headers=headers)
            soup = BeautifulSoup(site.content)
            expiry = soup.find_all("section")[1].find("section").find("div").find_all("div")[1].text
        # TODO: Pick option expiry https://stackoverflow.com/questions/28680896/how-can-i-get-the-3rd-friday-of-a-month-in-python
        # cycleOne = ["January", "April", "July", "October"]
        # cycleTwo = ["February", "May", "August", "November"]
        # cycleThree = ["March", "June", "September", "December"]
        # optionTable = soup.find("table")
        # headerRow = optionTable.find_all("th")
        if date is None:
            htmlUrl = "https://finance.yahoo.com/quote/{0}/options?p={0}&straddle=true".format(ticker)
            html = re.get(htmlUrl, headers=headers)
            optionFrame = pd.read_html(html.content)[0]
        else:
            # For local TODO
            # date = int(time.mktime((datetime.strptime(date, "%Y-%m-%d") - timedelta(hours=4)).timetuple()))
            # For deployment
            date = int(time.mktime((datetime.strptime(date, "%Y-%m-%d")).timetuple()))
            htmlUrl = "https://finance.yahoo.com/quote/{0}/options?p={0}&straddle=true&date={1}".format(ticker, date)
            html = re.get(htmlUrl, headers=headers)
            optionFrame = pd.read_html(html.content)[0]
        optionFrame.drop(["Change", "% Change", "Change.1", "% Change.1", "Volume", "Volume.1"], inplace=True, axis=1)
        if toPickle:
            if not os.path.exists("backupData/{0}".format(ticker)):
                os.mkdir("backupData/{0}".format(ticker))
            with open("./backupData/{0}/{0}-Option-Data".format(ticker), 'wb') as f:
                pickle.dump([optionFrame], f)
                f.close()
        return [expiry, optionFrame]

def getCurrMarketPrice(tickers):
    global headers
    prices = []
    betas = []
    if tickers != []:
        for ticker in tickers:
            url = "https://finance.yahoo.com/quote/{0}?p={0}".format(ticker)
            html = re.get(url, headers=headers)
            dfs = pd.read_html(html.content)
            dfOne = dfs[0]
            dfTwo = dfs[1]
            dfOne.set_index(0, inplace=True)
            dfTwo.set_index(0, inplace=True)
            prices += [float(dfOne.loc['Previous Close'].values.tolist()[0])]
            betas += [float(dfTwo.loc['Beta (5Y Monthly)'].values.tolist()[0])]
    return prices, betas

def calcStockReturn(oldPrices, newPrices):
    rets = []
    if newPrices != []:
        for i in range(len(oldPrices)):
            rets += [((float(newPrices[i]) - float(oldPrices[i])) / float(oldPrices[i]))]
    return rets

def calcPnL(oldPrices, newPrices, amounts):
    pnl = []
    if newPrices != []:
        for i in range(len(oldPrices)):
            pnl += [round((float(newPrices[i]*float(amounts[i])) - float(oldPrices[i]*float(amounts[i]))), 2)]
    return pnl

def calcPortReturn(oldPrices, newPrices, weights, betas):
    rets = []
    weightedBetas = []
    # weights = []
    if newPrices != []:
        for i in range(len(oldPrices)):
            retOnAsset = ((float(newPrices[i]) - float(oldPrices[i])) / float(oldPrices[i]))
            weightedRet = retOnAsset*(weights[i])
            rets += [weightedRet]
            weightedBeta = betas[i]*(weights[i])
            weightedBetas += [weightedBeta]
    return [sum(rets)], [sum(weightedBetas)]

def getRiskFreeRate():
    # Using 2 year treasury
    twoYearTreas = pd.read_csv("https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=DGS2&scale=left&cosd=2015-06-10&coed=2020-06-10&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Daily&fam=avg&fgst=lin&fgsnd=2009-06-01&line_index=1&transformation=lin&vintage_date=2020-06-11&revision_date=2020-06-11&nd=1976-06-01")
    return twoYearTreas['DGS2'].values.tolist()[-1]

def calcStdOfReturns(tickers):
    std = []
    masterDf = pd.DataFrame()
    if tickers != []:
        for ticker in tickers:
            # approx 2 years of data
            start = int(time.mktime((datetime.today() - timedelta(days=740)).timetuple()))
            # download_quotes(ticker, start, None)
            # print(ticker)
            df = YahooFinanceHistory(ticker, start, None).download_quotes()
            # df = pd.read_csv(ticker + ".csv")
            std += [round(df['Close'].pct_change().dropna().std()*math.sqrt(252), 4)]
            # std += [round(df.std() / 100,2)]
            df = df['Close']
            df.rename(ticker, inplace=True)
            if masterDf.empty:
                masterDf = df.to_frame()
            else:
                masterDf = pd.concat([masterDf, df], axis=1, join='inner')
    correlation = masterDf.corr()
    return std, correlation

def getPortStd(standDev, corrs, weights):
    cols = corrs.columns
    indexes = corrs.index
    corrsCalcs = []
    analyzedCorrs = []
    if len(standDev) == 1:
        return standDev[0]
    for i in range(len(cols)):
        corrsCalcs += [(weights[i]**2)*((standDev[i])**2)]
        for j in range(len(indexes)):
            if cols[i] != indexes[j]:
                stdA = standDev[i]
                stdB = standDev[j]
                wA = weights[i]
                wB = weights[j]
                currCorr = corrs.loc[indexes[j], cols[i]]
                if currCorr not in analyzedCorrs:
                    corrsCalcs += [2*wA*wB*stdA*stdB*currCorr]
                    analyzedCorrs += [currCorr]
    return sum(list(set(corrsCalcs)))

def getSharpeRatio(ret, std):
    riskfree = float(getRiskFreeRate()) / 100
    return round((float(ret[0]) - riskfree) / float(std), 2)

def getTreynorRatio(ret, beta):
    riskfree = float(getRiskFreeRate()) / 100
    return round((float(ret[0]) - riskfree) / float(beta[0]), 2)

def findStrike(myList, myNumber):
    from bisect import bisect_left
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
       return after
    else:
       return before