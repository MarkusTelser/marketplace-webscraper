# Marketplace-Webscraper
The Marketplace-Webscraper is a web scraping tool, that supports (at the moment) three pages, that can be scraped.
These pages are used car pages and the scraped data gets saved into files and then displayed in a generated website. 

## Requirements
The only requirements needed are python3, selenium and urllib. (see requirements.txt)

## Installation
To install the marketplace-webscraper we clone with git
```
git clone https://github.com/MarkusTelser/marketplace-webscraper
```

## Usage
First you need to go into the cloned folder.
Then we install the requirements with pip:
```
pip install -r requirements.txt
```
Then we can execute as a program with python3:
```
python3 src/main.py
```
If you want to add your own pages or search other things than cars, just fork my repo.
You can change everything easily in src/websites.py and set standard values for min_price, max_price, mileage, etc.


## Internal Folder Structure
These folders are created by the program and used to store data:
*    page/ folder contains the generated HTML, CSS, JS files
*    data/ folder contains needed pictures and data of pages
*    src/ folder contains source code


## Example Pictures:
