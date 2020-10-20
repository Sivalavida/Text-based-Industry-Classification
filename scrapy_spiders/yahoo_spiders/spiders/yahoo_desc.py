import pandas as pd
import scrapy
import logging
import pathlib


class YahooDescSpider(scrapy.Spider):
    '''
    Script to scrape company description
    Note that scrapes are done in parallel so order is not guaranteed
    Scrapy is a single-threaded framework (and does not support multithreading),
    but is asynchronous (parallel requests = multiprocessing)
    Time Taken: 108.6s
    ** DELETE PREVIOUS CSV FILE BEFORE RUNNING AS SCRAPY APPENDS TO EXISTING FILE INSTEAD OF OVERWRITING **
    '''
    name = "yahoo_desc"
    
    INDEX = 'russell'
    NUM_INVALID_TICKERS = 0
    INVALID_URLS = []
    
    ticker_df = pd.read_csv('data_in/%s_tickers_df.csv' %INDEX)
    tickers = ticker_df.Ticker

    # start_url is scrapy naming convention, dont change
    # (dont need to implement start_requests with this)
    start_urls = ['https://finance.yahoo.com/quote/'+ticker+'/profile?p='+ticker
                      for ticker in tickers]
    
    custom_settings = {
        'LOG_LEVEL': logging.WARNING, # Scrapy logs alot of stuff at a lower setting
        'FEEDS': {pathlib.Path('data_out/%s_desc_%s.csv' %(INDEX, name[:-5])): {'format': 'csv'}}, # When writing to this file, the additional scrapes will be appended not overwritten
        'FEED_EXPORT_ENCODING': 'utf-8-sig' # not utf-8 so as to force csv to open in utf-8, if not will have wierd characters        
    }

    @staticmethod
    def get_ticker_from_url(url):
        return url.split('=')[-1]
        
    def parse(self, response):
        url = response.request.url
        ticker = self.get_ticker_from_url(url)
        desc = response.xpath(' //*[@id="Col1-0-Profile-Proxy"]/section/section[2]/p/text()').extract()
        sec = response.xpath('//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[2]/span[2]/text()').extract()
        ind = response.xpath('//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[2]/span[4]/text()').extract()
        if not sec:
            self.NUM_INVALID_TICKERS +=1
            self.INVALID_URLS.append(url)
            print('SECTOR AND DESC MISSING: %s'%url)
        elif not desc:
            self.NUM_INVALID_TICKERS +=1
            self.INVALID_URLS.append(url)
            print('DESC MISSING: %s'%url)
        else:
            print('VALID: %s'%ticker)
        
        yield {
            'Ticker': ticker,
            'Description': desc,
            'Sector': sec,
            'Industry': ind
            }



