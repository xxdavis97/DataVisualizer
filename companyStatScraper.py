import requests as re
from bs4 import BeautifulSoup
import pickle
import os
import pandas as pd

# soup = None
toPickle = False
usePickle = False
def getInstiutionalOwnership(ticker):
    global toPickle
    global usePickle
    # global soup
    # if soup is None:
    if usePickle:
        with open("./backupData/{0}/{0}-Inst-Ownership".format(ticker), 'rb') as f:
            pick = pickle.load(f)
            f.close()
            return pick
    else:
        url = "https://finance.yahoo.com/quote/{0}/key-statistics?p={0}".format(ticker)
        site = re.get(url)
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
    # global soup
    # if soup is None:
    if usePickle:
        with open("./backupData/{0}/{0}-Short-Shares".format(ticker), 'rb') as f:
            pick = pickle.load(f)
            f.close()
            return pick
    else:
        url = "https://finance.yahoo.com/quote/{0}/key-statistics?p={0}".format(ticker)
        site = re.get(url)
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
    if usePickle:
        with open("./backupData/{0}/{0}-Earnings-Hist".format(ticker), 'rb') as f:
            pick = pickle.load(f)
            f.close()
            return pick
    else:
        url = "https://finance.yahoo.com/quote/{0}/analysis?p={0}".format(ticker)
        site = re.get(url)
        soup = BeautifulSoup(site.content)
        tables = soup.find_all('table')
        rows = tables[2].find_all("tr")
        dates = rows[0].find_all("span")
        dates = [date.text for date in dates][1:]
        epsEst = rows[1].find_all("span")
        epsEst = [eps.text for eps in epsEst][1:]
        epsAct = rows[2].find_all("span")
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
    if usePickle:
        with open("./backupData/{0}/{0}-Company-Bio".format(ticker), 'rb') as f:
            pick = pickle.load(f)
            f.close()
            return pick
    else:
        # Try means stock, except means ETF
        # try:
        url = "https://finance.yahoo.com/quote/{0}/profile?p={0}".format(ticker)
        site = re.get(url)
        soup = BeautifulSoup(site.content)
        if toPickle:
            if not os.path.exists("backupData/{0}".format(ticker)):
                os.mkdir("backupData/{0}".format(ticker))
            with open("./backupData/{0}/{0}-Company-Bio".format(ticker), 'wb') as f:
                pickle.dump(soup.find_all("section")[3].find("p").text, f)
                f.close()
        return soup.find_all("section")[3].find("p").text
        # except:
        #     url = "https://www.marketwatch.com/investing/fund/{0}".format(ticker)
        #     site = re.get(url)
        #     soup = BeautifulSoup(site.content)
        #     if toPickle:
        #         if not os.path.exists("backupData/{0}".format(ticker)):
        #             os.mkdir("backupData/{0}".format(ticker))
        #         with open("./backupData/{0}/{0}-Company-Bio".format(ticker), 'wb') as f:
        #             pickle.dump(soup.find_all("section")[3].find("p").text, f)
        #             f.close()
        #     # print(soup.prettify())
        #     # print(soup.findAll('p', {'class': 'description__text'}))
        #     return soup.find_all("section")[3].find("p").text

def getFundOwnership(ticker):
    global toPickle
    global usePickle
    if usePickle:
        with open("./backupData/{0}/{0}-Fund-Ownership".format(ticker), 'rb') as f:
            pick = pickle.load(f)
            f.close()
            return pick
    else:
        url = "https://finance.yahoo.com/quote/{0}/holders?p={0}".format(ticker)
        site = re.get(url)
        soup = BeautifulSoup(site.content)
        institutional = soup.find_all('table')[1]
        titles = [name.text for name in institutional.find('tr').find_all('th')]
        institutionalRows = []
        for row in institutional.find_all('tr'):
            institutionalRows += [[name.text for name in row.find_all('td')]]
        institutionalRows = institutionalRows[1:]

        mutual = soup.find_all('table')[2]
        mutualRows = []
        for row in mutual.find_all('tr'):
            mutualRows += [[name.text for name in row.find_all('td')]]
        mutualRows = mutualRows[1:]

        instFrame = pd.DataFrame(data = institutionalRows, columns = titles)
        mutualFrame = pd.DataFrame(data = mutualRows, columns = titles)
        if toPickle:
            if not os.path.exists("backupData/{0}".format(ticker)):
                os.mkdir("backupData/{0}".format(ticker))
            with open("./backupData/{0}/{0}-Fund-Ownership".format(ticker), 'wb') as f:
                pickle.dump([instFrame, mutualFrame], f)
                f.close()
        return [instFrame, mutualFrame]
