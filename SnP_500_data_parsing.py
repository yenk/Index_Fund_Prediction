import csv 
import dateparser 
import sys
from bs4 import BeautifulSoup 
from datetime import datetime


def scraping_dividend_html():
    """
    webscraping S&P 500 dividends
    """
    file_div = open('/Users/yenkha/Projects/stocksenv/S&P 500 Dividend Yield by Month.html', 'r').read()
    soup_div = BeautifulSoup(file_div, 'lxml')
    dividend = soup_div.find(id='datatable').find_all('tr')
    return dividend

def scraping_ticker_html(): 
    """ 
    webscraping S&P 500 tickers
    """
    file_ticker = open('/Users/yenkha/Projects/stocksenv/Inflation Adjusted S&P 500 by Month.html', 'r').read()
    soup_ticker = BeautifulSoup(file_ticker, 'lxml')
    ticker = soup_ticker.find(id='datatable').find_all('tr')
    return ticker

def dividend_parsing(dividend):
    """
    writing and finalizing dividend dataset after scraping
    """
    div_html_output = csv.writer(open('/Users/yenkha/Projects/stocksenv/SnP_500_Dividend_Yield_by_Month.csv', 'w'))
    # some data wrangling to grab just dividend and dates, toss final output to a csv file  
    with open('/Users/yenkha/Projects/stocksenv/dividend_yield_by_date.csv', 'w') as wF:
        writer = csv.writer(wF, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Date', 'Dividend'])
        # ignore table heading 
        for tr in dividend[1:]:
            td = tr.find_all('td')[0]
            td = dateparser.parse(td.text)
            td = td.strftime('%Y-%m-%d')
            tp = tr.find_all('td')[1]
            # remove last character of text string
            tp = tp.text[:tp.text.index('%')]
            output_list = [td, tp]
            writer.writerow(output_list)

def ticker_parsing(ticker):
    """
    writing and finalizing ticker (inflated rate) post scraping
    """ 
    tick_html_output = csv.writer(open('/Users/yenkha/Projects/stocksenv/SnP_500_inflation_adjusted_by_Month.csv', 'w'))
    with open('/Users/yenkha/Projects/stocksenv/ticker_by_date.csv', 'w') as wF:
        writer = csv.writer(wF, delimiter='\t', quoting=csv.QUOTE_NONE, escapechar=' ')
        writer.writerow(['Date', 'InflationRate'])
        # ignore table heading 
        for tr in ticker[1:]:
            # get parsed date
            td = tr.find_all('td')[0]    
            td = dateparser.parse(td.text)
            td = td.strftime('%Y-%m-%d')
            # get price and strip trailing characters
            tp = tr.find_all('td')[1]
            tp = tp.text.rstrip('\n')
            output_list = [td, tp]
            writer.writerow(output_list)


def main():
    dividend = scraping_dividend_html()
    dividend_parsing(dividend)
    ticker = scraping_ticker_html()
    ticker_parsing(ticker)


if __name__ == '__main__':
    main()


