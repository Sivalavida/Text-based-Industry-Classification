import pandas as pd
import scrapy
import logging
import pathlib


class CsimarketDescSpider(scrapy.Spider):
    '''
    Script to scrape company description
    Time Taken: 108.6s
    ** DELETE PREVIOUS CSV FILE BEFORE RUNNING AS SCRAPY APPENDS TO EXISTING FILE INSTEAD OF OVERWRITING **
    - website autochanges url according to exchange
    - missing information for many tickers
    '''
    name = "csimarket_desc"
    
    INDEX = 'russell'
    NUM_INVALID_TICKERS = 0
    INVALID_URLS = []
    
    

    # start_url is scrapy naming convention, dont change
    # (dont need to implement start_requests with this)
    # start_urls = 
    
    custom_settings = {
        'LOG_LEVEL': logging.WARNING, # Scrapy logs alot of stuff at a lower setting
        'FEEDS': {pathlib.Path('data_out/%s_desc_%s.csv' %(INDEX, name[:-5])): {'format': 'csv'}}, # When writing to this file, the additional scrapes will be appended not overwritten
        'FEED_EXPORT_ENCODING': 'utf-8-sig' # not utf-8 so as to force csv to open in utf-8, if not will have wierd characters        
    }

    def start_requests(self):
        ticker_df = pd.read_csv('data_in/%s_tickers_df.csv' %self.INDEX)
        tickers = ticker_df.Ticker.str.replace('-', '')
        
        # do it this way as the urls change for invalid tickers, making it impossible to get back the ticker from the url
        for ticker in tickers:
            url = 'https://csimarket.com/stocks/'+ticker+'-Business-Description.html'
            yield scrapy.Request(url=url, meta={'ticker':ticker}, callback=self.parse)
        
    def parse(self, response):
        url = response.request.url
        ticker = response.meta['ticker']# self.get_ticker_from_url(url)
        desc = response.xpath('//*[@id="glavno_polje"]/table[3]/tr/td[1]/div/p/text() | //*[@id="glavno_polje"]/table[3]/tr/td[1]/div/text()').extract()
        desc = (' '.join(desc)).strip()
        if desc:
            print('VALID: %s'%ticker)
            yield {
                'Ticker': ticker,
                'Description': desc # note that desc is a list but it is concatenated when put in csv
            }
        else:
            self.NUM_INVALID_TICKERS +=1
            self.INVALID_URLS.append([ticker, url])
            print('INVALID TICKER: %s'%ticker, url)
            yield {
                'Ticker': ticker,
                'Description': None # note that desc is a list but it is concatenated when put in csv
            }
        


