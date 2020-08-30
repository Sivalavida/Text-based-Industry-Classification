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
    '''
    name = "yahoo_desc"

    snp_ticker_df = pd.read_csv('data_in/snp_ticker_df.csv', index_col=0)
    tickers = snp_ticker_df.Symbol

    # start_url is scrapy naming convention, dont change
    # (dont need to implement start_requests with this)
    start_urls = ['https://finance.yahoo.com/quote/'+ticker+'/profile?p='+ticker
                      for ticker in tickers]
    
    custom_settings = {
        'LOG_LEVEL': logging.WARNING, # Scrapy logs alot of stuff at a lower setting
        'FEEDS': {pathlib.Path('data_out/yahoo_desc.csv'): {'format': 'csv'}}, # When writing to this file, the additional scrapes will be appended not overwritten
        'FEED_EXPORT_ENCODING': 'utf-8-sig' # not utf-8 so as to force csv to open in utf-8, if not will have wierd characters        
    }

    @staticmethod
    def get_ticker_from_url(url):
        return url.split('=')[-1]
    
    def parse(self, response):
        def evaluate(s, response):
            # to return None if element cant be found
            try:
                return eval(s)
            except:
                return None
        
        ticker = self.get_ticker_from_url(response.request.url)
        print(ticker)
        yield {
            'Ticker': ticker,
            'desc': evaluate(
                '''response.xpath('//*[@id="Col1-0-Profile-Proxy"]/section/section[2]/p/text()').extract()''', response),
            'Sector': evaluate(
                '''response.xpath('//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[2]/span[2]/text()').extract()''', response),
            'Industry': evaluate(
                '''response.xpath('//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[2]/span[4]/text()').extract()[0]''', response)
        }



