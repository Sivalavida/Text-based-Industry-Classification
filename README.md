# Industry-Classification
The goal of this project is to use NLP techniques to classify companies according to their descriptions. Descriptions used in this project are from yahoo finance and EDGAR 10-K reports.


## Usage

1. Clone [SEC-EDGAR-text](https://github.com/alions7000/SEC-EDGAR-text) project and modify the **document_group_section_search.json** file to only include Section 1A parts of 10-K filings and run the code (simply delete all other parts of JSON file). By default, this will output the 10K filings of the SnP500 companies. Filter from output (from the 'output_files_examples/batch_xx/' folder) all the filenames ending with `excerpt.txt`) and transfer all these .txt files into `data_out/10-K/SnP` folder here.
	* If you want to get 10K reports of the companies in the Russell 3000 index, run the code section in the **Data Extraction.ipynb** under header *List of CIKs for relevant tickers*, and copy the output (data_out/scrapping_ticker_ciks.txt) to the companies_list.txt file in the SEC-EDGAR-text project, and then run that project. Transfer filtered output to a new folder (eg  `data_out/10-K/Russell`)


1. Run **Data Extraction.ipynb**. This populates `data_out/` folder  with:
	*  data scraped from [Yahoo Finance](https://sg.finance.yahoo.com/) (Note: `yahoo_spiders/data_in/` folder is also polulated with Ticker symbol data in this step)
	*  data merging all the .txt files which were copied in the previous step
	*  clean data from the ticker to gics mapping


1. In the `yahoo_spiders/` folder, run **yahoo_spiders** with:

        scrapy crawl yahoo_desc
        scrapy crawl yahoo_price
        scrapy crawl yahoo_ratios
        
    This will populate the `yahoo_spiders/data_out/` folder with data scraped from Yahoo Finance as well. Edit the `INDEX` parameter in each of the spiders accordingly to scrape data from the respective index (e.g. snp, russell)
    

1. Run **LSI Word Embedding.ipynb**. Set `desc_df` parameter (under the *Global Vars* header) according to which index tickers the results are required for.



## Results

### 1. Average R2 
![1_1](data_out/images/1_1.png)
![1_2](data_out/images/1_2.png)
![1_3](data_out/images/1_3.png)
![1_4](data_out/images/1_4.png)

### 2. Inter Industry Variation
![2_1](data_out/images/2_1.png)
![2_2](data_out/images/2_2.png)
![2_3](data_out/images/2_3.png)
![2_4](data_out/images/2_4.png)

### 3. Similarity Probability with GICS
![3_1](data_out/images/3_1.png)
![3_2](data_out/images/3_2.png)
![3_3](data_out/images/3_3.png)
![3_4](data_out/images/3_4.png)


## Data Description and Sources (in `data_in/` folder or APIs used or websites scraped)

* API for CIK to ticker mapping
	* https://medium.com/@jan_5421/cik-to-ticker-mapping-bb22194b5cc0
* cik_ticker.csv
	* not sure, not used
* russell_price.csv
	* price of all tickers in Russell 3000 index from Jan 2015 to May 2020 (from past project)
* russell_ratio.csv
	* 6 ratios (mkt_cap, pb_ratio, beta, profit_m, roa, roe) of all Russell 3000 index companies
	* from past project)
* Russell3000.pdf
	* list of all comanies in Russell 3000, updated 31 Mar 2020, however ticker name not provided
	* from [FTSE Russell](https://www.ftserussell.com/analytics/factsheets/home/constituentsweights)
* list Russell 3000 tickers
	* from 3rd party source but claims last updated on 21 Sep 2020
	* http://www.kibot.com/Historical_Data/Russell_3000_Historical_Intraday_Data.aspx
* list of STI tickers
	* https://en.wikipedia.org/wiki/Straits_Times_Index
* ticker_to_gics.csv
	* mapping for all tickers in Russell 3000
	* from prof (also found in past project)
* GICS classification of SnP stocks 
	* from bloomberg
	* from prof

