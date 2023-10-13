# Scraper Class for Property Data Retrieval

> This Python code is a web scraping utility designed to gather real estate property data from various websites, including Bayut, JustProperty, and PropertyFinder. The code is organized into classes and methods for ease of use. The primary purpose of the code is to collect property listings, including details such as price, location, and contact information, and store the data for further analysis or application.

### To utilize this scraper, follow these steps:

* Initialization: Create an instance of the scraper_class to access the scraping methods.
* Bayut: The bayut class contains methods for scraping property data from Bayut.
* bayut.buy.get_all_adds_links(): Scrapes all property listings for sale on Bayut and stores the links in a pickle file.
* bayut.buy.fetch_data_using_add_link(): Fetches property details for the sale listings and stores them in a DataFrame.
* bayut.rent.get_all_adds_links(): Scrapes all property listings for rent on Bayut and stores the links in a pickle file.
* bayut.rent.fetch_data_using_add_link(): Fetches property details for the rent listings and stores them in a DataFrame.
* JustProperty: The justproperty method gathers data about real estate agents from the JustProperty website, including contact information and geographical coordinates. The results are stored in a CSV file.
* PropertyFinder: The property_finder class contains methods for scraping property data from PropertyFinder.
* property_finder.buy.get_all_adds_links(): Scrapes all property listings for sale on PropertyFinder and stores the links in a pickle file.
* property_finder.buy.fetch_data_using_add_link(): Fetches property details for the sale listings and stores them in a DataFrame.
* property_finder.rent.get_all_adds_links(): Scrapes all property listings for rent on PropertyFinder and stores the links in a pickle file.
* property_finder.rent.fetch_data_using_add_link(): Fetches property details for the rent listings and stores them in a DataFrame.

## Requirements
Before using this scraper, you should have the following Python packages:

* pandas: Data manipulation library
* requests: HTTP library for making web requests
* pickle: For serializing and deserializing Python objects
* BeautifulSoup: A library for parsing HTML and XML documents


## Notes

* This code is intended for educational purposes and scraping data from websites should be done in compliance with the site's terms of service and legal regulations. Be aware that scraping websites without permission may violate their policies.

* This description is provided for informative purposes only and does not encourage or support any violation of website terms or legal regulations. Always ensure that your web scraping activities are conducted responsibly and within the boundaries of the law.