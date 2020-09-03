# Industry-Classification
The goal of this project is to Using NLP techniques to classify companies according to their descriptions. Descriptions used in this project are from yahoo finance and EDGAR 10-K reports.


## Usage

1. Run **Scraper script.ipynb** to populate `data_out/` folder with data scraped from [Yahoo Finance](https://sg.finance.yahoo.com/).

1. Run **yahoo_spiders** with:

        scrapy crawl yahoo_desc
        scrapy crawl yahoo_price
        scrapy crawl yahoo_ratios
        
    This will populate the `data_out/` folder with data scraped from Yahoo Finance as well.
    
1. Clone [SEC-EDGAR-text](https://github.com/alions7000/SEC-EDGAR-text) project and modify the **document_group_section_search.json** file to only include Section 1A parts of 10-K filings and run the code. Transfer the output into `data_out/10-K/` folder here.

1. Run **LSI Word Embedding.ipynb**


