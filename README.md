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

## Items (items.py)
This file defines an Item class, so that the fields that we have extracted can be grouped in Items and organized in a more concise manner. Item objects are simple containers used to collect the scraped data.

I have extracted from the article the following elements:

```
topic       -    the general category of the article classified by the newspaper
title       -    the title of the article
text        -    the entire text of the article

```

## Settings
We can export the data locally into a CSV or a JSON. In case we choose to create a CSV file we need to specify the order of the columns by explicitly setting:
```
FEED_EXPORT_FIELDS = ["topic", "title", "text"]
```
