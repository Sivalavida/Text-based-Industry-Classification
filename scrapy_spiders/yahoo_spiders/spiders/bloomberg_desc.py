import pandas as pd
import scrapy
import logging
import pathlib


class BloombergDescSpider(scrapy.Spider):
    '''
    DOSENT WORK: Bloomberg has captcha
    Script to scrape company description
    Time Taken: -
    ** DELETE PREVIOUS CSV FILE BEFORE RUNNING AS SCRAPY APPENDS TO EXISTING FILE INSTEAD OF OVERWRITING **
    '''
    name = "bloomberg_desc"
    
    INDEX = 'snp'
    NUM_INVALID_TICKERS = 0
    INVALID_URLS = []
    
    ticker_df = pd.read_csv('data_in/%s_tickers_df.csv' %INDEX).head()
    tickers = ticker_df.Ticker

    # start_url is scrapy naming convention, dont change
    # (dont need to implement start_requests with this)
    start_urls = ['https://www.bloomberg.com/profile/company/'+ticker+':US'
                      for ticker in tickers]
    
    custom_settings = {
        'LOG_LEVEL': logging.WARNING, # Scrapy logs alot of stuff at a lower setting
        'FEEDS': {pathlib.Path('data_out/%s_desc_%s.csv' %(INDEX, name[:-5])): {'format': 'csv'}}, # When writing to this file, the additional scrapes will be appended not overwritten
        'FEED_EXPORT_ENCODING': 'utf-8-sig' # not utf-8 so as to force csv to open in utf-8, if not will have wierd characters        
    }

    @staticmethod
    def get_ticker_from_url(url):
        return url.split('/')[-1][:-3]
        
    def parse(self, response):
        def evaluate(s, response):
            # to return None if element cant be found
            try:
                return eval(s)
            except:
                return None
        print(response.request.url)
        ticker = self.get_ticker_from_url(response.request.url)
        print(ticker)
        yield {
            'Ticker': ticker,
            'Description': evaluate(
                '''response.xpath('//*[@id="root"]/div/section/div[2]/section/section[1]/div/text()').extract()''', response)
        }


