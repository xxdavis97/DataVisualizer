import re
import sys
import time
import requests
import pandas as pd

# def get_cookie_value(r):
#     return {'B': r.cookies['B']}
#
# def get_page_data(symbol):
#     url = "https://finance.yahoo.com/quote/%s/?p=%s" % (symbol, symbol)
#     r = requests.get(url)
#     cookie = get_cookie_value(r)
#     lines = r.content.decode('unicode-escape').strip(). replace('}', '\n')
#     return cookie, lines.split('\n')
#
# def find_crumb_store(lines):
#     # Looking for
#     # ,"CrumbStore":{"crumb":"9q.A4D1c.b9
#     for l in lines:
#         if re.findall(r'CrumbStore', l):
#             return l
#     print("Did not find CrumbStore")
#
# def split_crumb_store(v):
#     return v.split(':')[2].strip('"')
#
# def get_cookie_crumb(symbol):
#     cookie, lines = get_page_data(symbol)
#     crumb = split_crumb_store(find_crumb_store(lines))
#     return cookie, crumb
#
# def get_data(symbol, start_date, end_date, cookie, crumb):
#     filename = '%s.csv' % (symbol)
#     url = "https://query1.finance.yahoo.com/v7/finance/download/%s?period1=%s&period2=%s&interval=1d&events=history&crumb=%s" % (symbol, start_date, end_date, crumb)
#     response = requests.get(url, cookies=cookie)
#     with open (filename, 'wb') as handle:
#         for block in response.iter_content(1024):
#             handle.write(block)

def get_now_epoch():
    # @see https://www.linuxquestions.org/questions/programming-9/python-datetime-to-epoch-4175520007/#post5244109
    return int(time.time())

# def download_quotes(symbol,start,end):
#     if start is None or start < 0:
#         start = 0
#     if end is None:
#         end = get_now_epoch()
#     cookie, crumb = get_cookie_crumb(symbol)
#     get_data(symbol, start, end, cookie, crumb)



import requests
from datetime import datetime, timedelta
import re
from io import StringIO
import pandas as pd

class YahooFinanceHistory:
    timeout = 2
    crumb_link = 'https://finance.yahoo.com/quote/{0}/history?p={0}'
    crumble_regex = r'CrumbStore":{"crumb":"(.*?)"}'
    quote_link = 'https://query1.finance.yahoo.com/v7/finance/download/{quote}?period1={dfrom}&period2={dto}&interval=1d&events=history'#&crumb={crumb}'

    def __init__(self, symbol, startDate, endDate):
        self.symbol = symbol
        self.session = requests.Session()
        self.start = startDate
        self.end = endDate

    def get_crumb(self):
        response = self.session.get(self.crumb_link.format(self.symbol), timeout=self.timeout, headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' })
        response.raise_for_status()
        for c in response.cookies:
            print(c.name, c.value)
        match = re.search(self.crumble_regex, response.text)
        if not match:
            raise ValueError('Could not get crumb from Yahoo Finance')
        else:
            self.crumb = match.group(1)

    def download_quotes(self):
        if not hasattr(self, 'crumb') or len(self.session.cookies) == 0:
            self.get_crumb()
        if self.start is None or self.start < 0:
            self.start = 0
        if self.end is None:
            self.end = get_now_epoch()
        url = self.quote_link.format(quote=self.symbol, dfrom=self.start, dto=self.end)#, crumb=self.crumb)
        return pd.read_csv(url)
        # response = self.session.get(url)
        # response.raise_for_status()
        # pd.read_csv(StringIO(response.text)).to_csv("{0}.csv".format(self.symbol))
        # filename = '%s.csv' % (self.symbol)
        # print(filename)
        # return pd.read_csv(StringIO(response.text))
        # with open(filename, 'wb') as handle:
        #     for block in response.iter_content(1024):
        #         handle.write(block)