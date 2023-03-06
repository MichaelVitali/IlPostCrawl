# IlPostCrawl

IlPostCrawl is a crawler for an online newspaper, written in python, based on the [Scrapy](https://scrapy.org/) framework.

## DISCLAIMER
This software is not authorized by [IlPost](https://www.ilpost.it/). Scraping without IlPost explicit written is a violation of their terms.

This software is provided as is, for educational purposes, to show how a crawler can be made to recursively parse multiples categories and pages for each of them. Use at your own risk.

## Introduction
Which features IlPostCrawl extract from the website? I decided to extract only three different things that are equal for each article in the newspaper. In this case I
extracted the general category of the article, the title and all the text inside.

IlPostCrawl navigates easily though the pages without emulating a browser or inject javascript code since the website is static and it's all plain HTML.

## Installation
Requirements are: **python3** and the  **scrapy** framework, **beautifulSoup** and **request** libraries.

Scrapy can be installed through the package manager of the distribution (in my arch box is simply called "scrapy") or through internal python package system, typing:

```
 pip install scrapy
```
 BeautifulSoup can be installed typing:
 ```
 pip install beautifulsoup4
```
Requests can be installed typing:
```
 pip install requests
```

## How to crawl a page (IlPostSpider.py)
The core of the crawler is this spider class, **IlPostSpider**. When it starts it navigates to the main page of the website ```ilpost.it``` and it takes the links of all the categories.
Then, the ```parse_category``` method is called with the url of the main page of the selected category and the crawling process begins. It recursively parses all the pages of the category using the ```parse_page``` method. The latter parses an entire page retrieving all the links to all the articles and using the ```parse_article``` method to parse them.
thus, the ```parse_article``` methods populates Item fields and pass control over to the Item Loader, only in the case in which the article doesn't require a subscription to the website.

The webpage are parsed and the fields are extracted using **XPath** selectors. These selectors are implemented on the python lib ```lxml``` so they are very fast.

## Items (items.py)
This file defines an Item class, so that the fields that we have extracted can be grouped in Items and organized in a more concise manner. Item objects are simple containers used to collect the scraped data.

I have extracted from the article the following elements:

```
topic   -    the general category of the article classified by the newspaper
title   -    the title of the article
text    -    the entire text of the article
```

## Settings
We can export the data locally into a CSV or a JSON. In case we choose to create a CSV file we need to specify the order of the columns by explicitly setting:
```
FEED_EXPORT_FIELDS = ["topic", "title", "text"]
```
