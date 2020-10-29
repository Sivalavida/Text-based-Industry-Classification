import pandas as pd
import scrapy
import logging
import pathlib


class ReutersDescSpider(scrapy.Spider):
    '''
    Script to scrape company description
    Time Taken: 108.6s
    ** DELETE PREVIOUS CSV FILE BEFORE RUNNING AS SCRAPY APPENDS TO EXISTING FILE INSTEAD OF OVERWRITING **
    '''
    name = "reuters_desc"
    
    INDEX = 'snp'
    NUM_INVALID_TICKERS = 0
    INVALID_URLS = []
    
    ticker_df = pd.read_csv('data_in/%s_tickers_df.csv' %INDEX)
    tickers = ticker_df.Ticker.str.replace('-', '')

    # start_url is scrapy naming convention, dont change
    # (dont need to implement start_requests with this)
    start_urls = ['https://www.reuters.com/companies/'+ticker
                      for ticker in tickers]
    
    custom_settings = {
        'LOG_LEVEL': logging.WARNING, # Scrapy logs alot of stuff at a lower setting
        'FEEDS': {pathlib.Path('data_out/%s_desc_%s.csv' %(INDEX, name[:-5])): {'format': 'csv'}}, # When writing to this file, the additional scrapes will be appended not overwritten
        'FEED_EXPORT_ENCODING': 'utf-8-sig' # not utf-8 so as to force csv to open in utf-8, if not will have wierd characters        
    }

    @staticmethod
    def get_ticker_and_market_from_url(url):
        s = url.split('/')[-1]
        if '.' in s:
            ticker, market = s.split('.')
        else:
            ticker, market = s, None
        return ticker, market
        
    def parse(self, response):
        url = response.request.url
        ticker, market = self.get_ticker_and_market_from_url(url)
        desc = response.xpath('//*[@id="__next"]/div/div[4]/div[1]/div/div/div/div[4]/div[1]/p/text()').extract() or \
                response.xpath('//*[@id="__next"]/div/div[4]/div[1]/div/div/div/div[3]/div[1]/p/text()').extract()
        desc = [s.strip().replace('\n', ' ') for s in desc]
        if desc:
            print('VALID: %s (%s)'%(ticker, market))
            yield {
                'Ticker': ticker,
                'Description': desc
            }
        elif not market:
            # try NASDAQ
            new_url = 'https://www.reuters.com/companies/'+ticker+'.OQ'
            yield scrapy.Request(url=new_url, callback=self.parse)
        elif market == 'OQ':
            # try NEW YORK STOCK EXCHANGE
            new_url = 'https://www.reuters.com/companies/'+ticker+'.N'
            yield scrapy.Request(url=new_url, callback=self.parse)
        else:
            self.NUM_INVALID_TICKERS +=1
            self.INVALID_URLS.append([ticker, url])
            print('INVALID TICKER: %s'%url)
            yield {
                'Ticker': ticker,
                'Description': None
            }
        


