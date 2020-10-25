import pandas as pd
import scrapy
import logging
import pathlib


class MorningStarDescSpider(scrapy.Spider):
    '''
    Script to scrape company description
    Time Taken: 176.8s
    ** DELETE PREVIOUS CSV FILE BEFORE RUNNING AS SCRAPY APPENDS TO EXISTING FILE INSTEAD OF OVERWRITING **
    Need to consider multiple exchanges for morning star scraping
    '''
    name = "morningstar_desc"
    
    INDEX = 'russell'
    NUM_INVALID_TICKERS = 0
    INVALID_URLS = []
    
    ticker_df = pd.read_csv('data_in/%s_tickers_df.csv' %INDEX)
    tickers = ticker_df.Ticker.str.replace('-', '.')

    # start_url is scrapy naming convention, dont change
    # (dont need to implement start_requests with this)
    # xnas - NASDAQ, xnys - NEW YORK STOCK EXCHANGE, bats - BATS GLOBAL MARKETS
    start_urls = ['https://www.morningstar.com/stocks/xnas/'+ticker+'/quote'
                      for ticker in tickers]
    handle_httpstatus_list = [404]
    custom_settings = {
        'LOG_LEVEL': logging.WARNING, # Scrapy logs alot of stuff at a lower setting
        'FEEDS': {pathlib.Path('data_out/%s_desc_%s.csv' %(INDEX, name[:-5])): {'format': 'csv'}}, # When writing to this file, the additional scrapes will be appended not overwritten
        'FEED_EXPORT_ENCODING': 'utf-8-sig' # not utf-8 so as to force csv to open in utf-8, if not will have wierd characters        
    }

    @staticmethod
    def get_ticker_from_url(url):
        return url.split('/')[-2]
    
    @staticmethod
    def get_exchange_from_url(url):
        return url.split('/')[-3]
    
        
    def parse(self, response):
        url = response.request.url
        ticker = self.get_ticker_from_url(url)
        exchange = self.get_exchange_from_url(url)
        if response.status == 404:
            if exchange == 'xnas':
                new_url = 'https://www.morningstar.com/stocks/xnys/'+ticker+'/quote'
                yield scrapy.Request(url=new_url, callback=self.parse)
            elif exchange == 'xnys':
                new_url = 'https://www.morningstar.com/stocks/bats/'+ticker+'/quote'
                yield scrapy.Request(url=new_url, callback=self.parse)
            else:
                self.NUM_INVALID_TICKERS +=1
                self.INVALID_URLS.append(url)
                print('INVALID TICKER: %s'%url)
                yield {
                    'Ticker': ticker,
                    'Description': None
                }
                
        if response.status == 200:
            desc = response.xpath('//*[@id="__layout"]/div/div[2]/div[3]/main/div[2]/div/div/div[1]/div[1]/div/div[1]/p/text()').extract()
            desc = [s.strip() for s in desc]
            if desc == ['—']:
                print('TICKER WITHOUT DESC: %s (%s)'%(url, exchange))
                yield {
                    'Ticker': ticker,
                    'Description': None
                    }
            else:
                print('DONE: %s (%s)'%(ticker, exchange))
                yield {
                    'Ticker': ticker,
                    'Description': desc
                }


