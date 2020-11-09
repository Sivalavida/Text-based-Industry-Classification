# Text-based Industry Classification
The goal of this project is to use NLP techniques to classify companies according to their descriptions and compare it with the current industry standard, Global Industry Classification Standard (GICS). The SnP500 and Russell 3000 Indexes are specifically studied in this project. Several Sources of description, topic modelling techniques, clustering techniques are used as follows:

* Descriptions used:
	1. EDGAR 10-K reports
	1. Yahoo Finance
	1. Wikipedia
	1. Morning Star
	1. Reuters
	1. Reuters India
	1. Bloomberg
* Topic Modelling Techniques:
	1. Latent Semantic Indexing (LSI)
	1. LatentDirichletAllocation (LDA)
	1. Non Negative Matrix Factorization (NMF)
	1. Principal Component Analysis (PCA)
* Clustering Techniques
	1. K-means
	1. K-medioids
	1. Gaussian Mixture Model
	1. Hierarchical Clustering


## Usage

### Viewing/Running Text-based Industry Classification

* Refer to **LSI Word Embedding.ipynb**
* Set `desc_df` parameter (under *Global Vars* header) according to which index tickers results are required for
* Some data is not available on github as files are too big (eg. 10K reports for Russell) but the method to retrive them is detailed below

### Data Extraction and Cleaning

This section shows how to extract and clean data which was used for this project. What is probably required is the 10-K data.

1. Extract Index Tickers
	* Refer to **Data Extraction and Cleaning.ipynb** under header *Scrape Index Tickers*
	* This set of tickers will be used when scraping business descriptions from the various sources

1. Extract 10-K Reports
	* Clone [SEC-EDGAR-text](https://github.com/alions7000/SEC-EDGAR-text) project
	* Modify **document_group_section_search.json** file to only include Section 1A parts of 10-K filings (simply delete all other parts of JSON file)
	* Run program using:
	
		```
	    python SEC-EDGAR-text
		```

		* With default settings, this outputs 10K filings of SnP500 companies from current date to one year prior. Filter from output (from 'output_files_examples/batch_xx/' folder) all filenames ending with `excerpt.txt` (using OS search functionality)(should be slightly less than half the total files) and transfer all these .txt files into `data_out/10-K/XX` folder in this project
		* Start and end date can be adjusted when program is run (as done in this project for 2015 and 2020 reports)
		* For this project, reports are scraped for a 1 year timeframe (to get data from as many companies as possible) and then filter the latest filing for each company 
		* Note that SnP500 ticker list used by the project can be outdated, so follow this procedure to extract data for a specific set of tickers (i.e. latest set of Russell Tickers):
			* Run code section in **Data Extraction and Cleaning.ipynb** under header *Scrape Ticker CIKs*, copy output (`data_out/scrapping_ticker_ciks.txt`) to companies_list.txt file in SEC-EDGAR-text project, and run it. Transfer filtered output to a new folder (e.g. `data_out/10-K/Russell/`)
		* Takes ~ 8hrs to run for Russell tickers
	* After `data_out/10-K/(index_name)/` folder has been populated, run code section in **Data Extraction and Cleaning.ipynb** under header *Merge 10K reports* (setting input and output folder and files accordingly)

1. Scrape Business Descriptions from multiple web-sources

	* Scrapy Framework used due to its much faster performance than other scraping tools (like selenium)
	* Business Description Sources:
		* Yahoo Finance
		* Business Insider
		* Morning Star
		* Reuters
		* Reuters India
		* Bloomberg
	* Ensure that you have saved the required index tickers into  `yahoo_spiders/data_in/` folder by following step 1
	* `cd` to  `scrapy_spiders/` folder and run spider for required data source with:
	
		```
	    scrapy crawl XXX_desc
	    ```
	 where XXX is either yahoo, businessinsider, morningstar, reuters, reutersindia or csimarket

	* This populates `yahoo_spiders/data_out/` folder with a .csv file with the scraped descriptions
	* If .csv file you are writing to exists, delete before re-running (as Scrapy appends to files instead of overwriting if the file to write to exists)
	* Edit  `INDEX` parameter each spider accordingly to scrape data from respective index (e.g. snp, russell)
	* Note that xpaths of descriptions and other scraping information change frequently (due to change in format of website of the scraping site), so do ensure that you are retrieving the right information, else edit scrapy script accordingly (usually just need to change xpath)

1. Scrape Yahoo Prices and Ratios
	* Similar to above procedure, but with the commands:

		```
	    scrapy crawl yahoo_price
	    scrapy crawl yahoo_ratios
	    ```

1. Extract Wikipedia Data
	* Refer to **Data Extraction and Cleaning.ipynb** under header *Scrape Wikipedia description*

1. Extract [Yahoo Finance](https://sg.finance.yahoo.com/) Data (Method 2)
	* This script takes a long time, so it is better to use the scrapy framework
	* Download chromedriver.exe [here](https://chromedriver.chromium.org/downloads) and put driver in main folder
	* Refer to **Data Extraction and Cleaning.ipynb** under header *Scrape Yahoo Description, Price, Ratios*
	* Extracts Besiness Descriptions, Price data and market ratios from Yahoo Finance using Selenium Framework and yfinance module

1. Other Data Extraction and Cleaning processes (Refer to **Data Extraction and Cleaning.ipynb** for details)
	* Scrape GICS industry code to name map
	* Clean Ticker to GICS map
	* Clean Market Ratios

## Results

### 1. Average R2 
![1_1](data_out/images/1_1.png)
![1_2](data_out/images/1_2.png)
![1_3](data_out/images/1_3.png)
![1_4](data_out/images/1_4.png)

* For SnP, lower k values seem to perform better
* No significant difference between K-means and GMM
* Using yahoo desc seems to give slightly better results (for both snp and russell)

### 2. Inter Industry Variation
![2_1](data_out/images/2_1.png)
![2_2](data_out/images/2_2.png)
![2_3](data_out/images/2_3.png)
![2_4](data_out/images/2_4.png)

* no consulsive results

### 3. Similarity Probability with GICS
![3_1](data_out/images/3_1.png)
![3_2](data_out/images/3_2.png)
![3_3](data_out/images/3_3.png)
![3_4](data_out/images/3_4.png)

* clustering with 10K reports gives closer classification to GICS


* Reasoning behind results

## Data used and Sources (in `data_in/` folder or APIs used or websites scraped)

* Company Business Description Data (MSFT is used as example in all the links)
	* [Yahoo](https://sg.finance.yahoo.com/quote/MSFT/profile?p=MSFT)
	* [Business Insider](https://markets.businessinsider.com/stocks/msft-stock)
	* [CNN](https://money.cnn.com/quote/profile/profile.html?symb=MSFT)
		* Same description as Business Insider
	* [Morning Star](https://www.morningstar.com/stocks/xnas/msft/quote)
	* [Reuters](https://www.reuters.com/companies/MSFT.O)
	* [Investing.com](https://www.investing.com/equities/microsoft-corp-company-profile)
		* Same description as Reuters
	* [Reuters India](https://in.reuters.com/finance/stocks/company-profile/MSFT.DF)
		* Medium length descriptions
	* [CSIMarket.com](https://csimarket.com/stocks/amzn-Business-Description.html)
		* Descriptions used are probably from 10K report
		* About 30% tickers do not have business description
	* [Bloomberg](https://www.bloomberg.com/profile/company/MSFT:US)
		* Unable to scrape as it has captcha
* russell_price.csv
	* price of all tickers in Russell 3000 index from Jan 2015 to May 2020 (from past project)
* russell_ratio.csv
	* 6 ratios (mkt_cap, pb_ratio, beta, profit_m, roa, roe) of all Russell 3000 index companies
	* from past project
* Russell3000.pdf
	* list of all comanies in Russell 3000, updated 31 Mar 2020, however ticker name not provided
	* from [FTSE Russell](https://www.ftserussell.com/analytics/factsheets/home/constituentsweights)
* list Russell 3000 tickers
	* from 3rd party source but claims last updated on 21 Sep 2020
	* http://www.kibot.com/Historical_Data/Russell_3000_Historical_Intraday_Data.aspx
* list of STI tickers
	* https://en.wikipedia.org/wiki/Straits_Times_Index
* list of SnP tickers
	* http://en.wikipedia.org/wiki/List_of_S%26P_500_companies
* Ticker-CIK map
	* https://www.sec.gov/include/ticker.txt
* ticker_to_gics.csv
	* ticker-GICS map for all tickers in Russell 3000
	* from prof (also found in past project)
* GICS classification of SnP stocks 
	* from bloomberg
	* from prof
* Stop Words List (for financial use)
	* https://sraf.nd.edu/textual-analysis/resources/#StopWords

Not used but explored
* API for CIK to ticker mapping
	* https://medium.com/@jan_5421/cik-to-ticker-mapping-bb22194b5cc0
* cik_ticker.csv
	* cik-ticker map for 13000+ tickers