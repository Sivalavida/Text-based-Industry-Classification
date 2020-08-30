import pandas as pd
import scrapy
import logging
import pathlib
from datetime import datetime


class YahooPriceSpider(scrapy.Spider):
    '''
    Script to scrape company Price
    Dont use this as this cant interact with the webpage
    '''
    name = "yahoo_price"
    
    custom_settings = {
        'LOG_LEVEL': logging.WARNING, # Scrapy logs alot of stuff at a lower setting
        'FEEDS': {pathlib.Path('data_out/yahoo_price.csv'): {'format': 'csv'}}, # When writing to this file, the additional scrapes will be appended not overwritten
        'FEED_EXPORT_ENCODING': 'utf-8-sig' # not utf-8 so as to force csv to open in utf-8, if not will have wierd characters
    }
    
    def start_requests(self):
        # Not sure why but start_urls gives problems for this scrape
        snp_ticker_df = pd.read_csv('data_in/snp_ticker_df.csv', index_col=0)
        tickers = snp_ticker_df.Symbol.head(10)
    
        d1 = datetime.strptime('20200102', "%Y%m%d")
        d2 = datetime.strptime('20200401', "%Y%m%d")
    
        time_str1 = str(int(datetime.timestamp(d1)))
        time_str2 = str(int(datetime.timestamp(d2)))
        urls = ['https://finance.yahoo.com/quote/'+ ticker +'/history?period1='+time_str1+'&period2='+time_str2+'&interval=1d&filter=history&frequency=1d'
                      for ticker in tickers]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    @staticmethod
    def get_ticker_from_url(url):
        return url.split('/')[4]

    def parse(self, response):
        ticker = self.get_ticker_from_url(response.request.url)
        print(ticker)
        item = {'Ticker' : ticker}
        prices = response.xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table/tbody/tr/td[5]//text()').extract()
        for i in range(len(prices)):
            item[i] = prices[i]
        yield item



