# Industry-Classification
The goal of this project is to use NLP techniques to classify companies according to their descriptions. Descriptions used in this project are from yahoo finance and EDGAR 10-K reports.


## Usage

1. Clone [SEC-EDGAR-text](https://github.com/alions7000/SEC-EDGAR-text) project and modify the **document_group_section_search.json** file to only include Section 1A parts of 10-K filings and run the code (simply delete all other parts of JSON file). Transfer the output into `data_out/10-K/` folder here.


1. Run **Scraper script.ipynb**. This populates `data_out/` folder  with:
	*  data scraped from [Yahoo Finance](https://sg.finance.yahoo.com/) (Note: `yahoo_spiders/data_in/` folder is also polulated with Ticker symbol data in this step)
	*  data merging all the .txt files which were copied in the previous step
	*  clean data from the ticker to gics mapping


1. In the `yahoo_spiders/` folder, run **yahoo_spiders** with:

        scrapy crawl yahoo_desc
        scrapy crawl yahoo_price
        scrapy crawl yahoo_ratios
        
    This will populate the `yahoo_spiders/data_out/` folder with data scraped from Yahoo Finance as well. Edit the `INDEX` parameter in each of the spiders accordingly to scrape data from the respective index (e.g. snp, russell)
    

1. Run **LSI Word Embedding.ipynb**. Set `desc_df` parameter (under the *Global Vars* header) according to which index tickers the results are required for.


