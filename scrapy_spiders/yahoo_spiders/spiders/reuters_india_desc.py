import pandas as pd
import scrapy
import logging
import pathlib


class ReutersIndiaDescSpider(scrapy.Spider):
    '''
    Script to scrape company description
    Time Taken: 108.6s
    ** DELETE PREVIOUS CSV FILE BEFORE RUNNING AS SCRAPY APPENDS TO EXISTING FILE INSTEAD OF OVERWRITING **
    - website autochanges url according to exchange
    '''
    name = "reuters_india_desc"
    
    INDEX = 'russell'
    NUM_INVALID_TICKERS = 0
    INVALID_URLS = []
    
    ticker_df = pd.read_csv('data_in/%s_tickers_df.csv' %INDEX)
    tickers = ticker_df.Ticker.str.replace('-', '')

    # start_url is scrapy naming convention, dont change
    # (dont need to implement start_requests with this)
    start_urls = ['https://in.reuters.com/finance/stocks/company-profile/'+ticker
                      for ticker in tickers]
    
    custom_settings = {
        'LOG_LEVEL': logging.WARNING, # Scrapy logs alot of stuff at a lower setting
        'FEEDS': {pathlib.Path('data_out/%s_desc_%s.csv' %(INDEX, name[:-5])): {'format': 'csv'}}, # When writing to this file, the additional scrapes will be appended not overwritten
        'FEED_EXPORT_ENCODING': 'utf-8-sig' # not utf-8 so as to force csv to open in utf-8, if not will have wierd characters        
    }

    @staticmethod
    def get_ticker_and_market_from_url(url):
        if 'lookup?' in url: #invalid search
            s = url.split('=')[-1]
            ticker, market = s, None
        else:
            s = url.split('/')[-1]
            if '.' in s:
                ticker, market = s.split('.')
            else:
                ticker, market = s, None
        return ticker, market
        
    def parse(self, response):
        url = response.request.url
        ticker, market = self.get_ticker_and_market_from_url(url)
        desc = response.xpath('//*[@id="companyNews"]/div/div[2]/p/text()').extract()
        if not desc:
            desc = response.xpath('//*[@id="companyNews"]/div/div[2]/text()').extract()
            if len(desc)>0 and desc[0].strip() == 'NA':
                desc = []
        if (ticker == 'WTTR' and market == 'N'): # not sure why but this symbol gets repeated
            pass
        elif desc: 
            print('VALID: %s (%s)'%(ticker, market))
            if market and len(market)>3:
                print('----------------------------------------------------------------------------------')
                print(url)
            yield {
                'Ticker': ticker,
                'Description': desc # note that desc is a list but it is concatenated when put in csv
            }
        else:
            desc = response.xpath('//*[@id="companyNews"]/div/div[2]/text()').extract()
            self.NUM_INVALID_TICKERS +=1
            self.INVALID_URLS.append(url)
            print('INVALID TICKER: %s'%url)
            yield {
                'Ticker': ticker,
                'Description': None # note that desc is a list but it is concatenated when put in csv
            }
        


