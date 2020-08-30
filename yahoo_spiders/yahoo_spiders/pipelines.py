# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
import time

class YahooSpidersPipeline:
    '''
    Adds Timer
    '''
    def process_item(self, item, spider):
        return item
    
    def open_spider(self, spider):
        self.start = time.time()
        print('START TIME: %s' %self.start)

    def close_spider(self, spider):
        self.end = time.time()
        print('END TIME: %s' %self.end)
        diff = self.end - self.start 
        print('TOTAL TIME: %s' %diff)
    


class YahooSpidersPipeline2:
    '''
    Currently not used.Everything is done in spider files
    '''
    def __init__(self):
        # self.filename = 'pages.csv'
        pass

    def open_spider(self, spider):
        self.filename = 'data_out/%s.csv' %spider.name
        self.csvfile = open(self.filename, 'wb')
        self.exporter = CsvItemExporter(self.csvfile, include_headers_line=True)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.csvfile.close()

    def process_item(self, item, spider):
        if spider.name == 'yahoo_price':
            new_item = {'Ticker' : item['Ticker']}
            i = 0
            for price in item['Prices']:
                new_item[i] = price
                i += 1
            self.exporter.export_item(new_item)
            print(new_item)
            return new_item
        else:
            self.exporter.export_item(item)
            return item