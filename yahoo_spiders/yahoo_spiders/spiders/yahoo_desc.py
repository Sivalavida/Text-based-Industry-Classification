import pandas as pd
import scrapy
import logging
import os
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
    symbols = snp_ticker_df.Symbol.head(10)
    # symbols = ['MMM', 'ABT']

    # start_url is scrapy naming convention, dont change
    # (dont need to implement start_requests with this)
    start_urls = ['https://finance.yahoo.com/quote/'+ticker+'/profile?p='+ticker
                      for ticker in symbols]
    
    custom_settings = {
        'LOG_LEVEL': logging.WARNING, # Scrapy logs alot of stuff at a lower setting
        'FEEDS': {pathlib.Path('data_out/yahoo_desc.csv'): {'format': 'csv'}}, # When writing to this file, the additional scrapes will be appended not overwritten
        'FEED_EXPORT_ENCODING': 'utf-8-sig' # not utf-8 so as to force csv to open in utf-8, if not will have wierd characters
    }

    @staticmethod
    def get_ticker_from_url(url):
        return url.split('=')[-1]

    def parse(self, response):
        print(response.xpath('//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[2]/span[4]/text()').extract())
        yield {
            'Ticker': self.get_ticker_from_url(response.request.url),
            'desc': response.xpath('//*[@id="Col1-0-Profile-Proxy"]/section/section[2]/p/text()').extract(),
            'Sector': response.xpath('//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[2]/span[2]/text()').extract(),
            'Industry': response.xpath('//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[2]/span[4]/text()').extract()[0].encode('utf-8')
        }



