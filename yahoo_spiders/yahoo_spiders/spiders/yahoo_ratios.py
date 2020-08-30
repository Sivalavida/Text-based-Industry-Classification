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
    name = "yahoo_ratios"

    snp_ticker_df = pd.read_csv('data_in/snp_ticker_df.csv', index_col=0)
    tickers = snp_ticker_df.Symbol.head(10)
    # symbols = ['MMM', 'ABT']

    # start_url is scrapy naming convention, dont change
    # (dont need to implement start_requests with this)
    start_urls = ['https://finance.yahoo.com/quote/'+ticker+'/key-statistics?p='+ticker
                      for ticker in tickers]
    
    custom_settings = {
        'LOG_LEVEL': logging.WARNING, # Scrapy logs alot of stuff at a lower setting
        'FEEDS': {pathlib.Path('data_out/yahoo_ratios.csv'): {'format': 'csv'}}, # When writing to this file, the additional scrapes will be appended not overwritten
        'FEED_EXPORT_ENCODING': 'utf-8-sig' # not utf-8 so as to force csv to open in utf-8, if not will have wierd characters        
    }

    @staticmethod
    def get_ticker_from_url(url):
        return url.split('=')[-1]

    def parse(self, response):
        ticker = self.get_ticker_from_url(response.request.url)
        print(response.request.url)
        yield {
            'Ticker': ticker,
            'mkt_cap' : response.xpath('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[3]/div[1]/div[2]/div/div[1]/div[1]/table/tbody/tr[1]/td[3]//text()').extract(),
            'pb_ratio' : response.xpath('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[3]/div[1]/div[2]/div/div[1]/div[1]/table/tbody/tr[7]/td[3]//text()').extract(),
            'beta' : response.xpath('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[3]/div[2]/div/div[1]/div/div/table/tbody/tr[1]/td[2]//text()').extract(),
            'profit_margin' : response.xpath('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[3]/div[3]/div/div[2]/div/div/table/tbody/tr[1]/td[2]//text()').extract(),
            'roa' : response.xpath('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[3]/div[3]/div/div[3]/div/div/table/tbody/tr[1]/td[2]//text()').extract(),
            'roe' : response.xpath('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[3]/div[3]/div/div[3]/div/div/table/tbody/tr[2]/td[2]//text()').extract()
        }



