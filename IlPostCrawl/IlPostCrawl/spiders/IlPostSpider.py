import scrapy
from scrapy.loader import ItemLoader
from ..items import IlpostItem
import bs4 as bs
import requests as rs

class IlPostSpider(scrapy.Spider):
    name = 'IlPost_spider'
    start_urls = ['https://www.ilpost.it/']

    custom_settings = {
        'FEED_EXPORT_FIELDS': ['topic', 'title', 'text'],
    }

    '''
        This function start the parsing of all the pages of each category of newspapers of the website
    '''
    def parse(self, response):

        categories = [
            'mondo',
            'italia',
            'politica',
            'tecnologia',
            'internet',
            'scienza',
            'cultura',
            'economia',
            'sport',
            'media',
        ]

        for category in categories:
            url = f'https://www.ilpost.it/{category}/'
            yield scrapy.Request(url=url, callback=self.parse_category, dont_filter=True)

    '''
        This function makes the following things:
        1) It takes the number of pages of the current category
        2) It calls the parse of the pages for each one of the category
    '''
    def parse_category(self, response):

        number_of_pages = response.xpath("//body//li/a[@class='page-numbers']/text()").extract()[2]
        number_of_pages = int(number_of_pages.replace('.',''))

        for i in range(1, number_of_pages+1):
            url_next_page = f'{response.url}page/{i}/'
            yield scrapy.Request(url=url_next_page, callback=self.parse_page, dont_filter=True)

    '''
        This function has the role of parse an entire page and call the parser for each of the article inside itself
    '''
    def parse_page(self, response):
        link_articles = response.xpath("//body//article//h2[@class='entry-title']/a/@href").extract()

        for link in link_articles:
            yield scrapy.Request(url=link, callback=self.parse_article, dont_filter=True)

    '''
        This function parse a single article extracting:
        1) The text of the article
        2) The title of the article
        3) The topic of the article
        
        It also adds all these three thing into an item that is use to create the csv file
    '''
    def parse_article(self, response):
        new = ItemLoader(item=IlpostItem(), response=response)

        html_article = rs.get(response.url).text
        html_article = bs.BeautifulSoup(html_article, 'lxml')
        paragraph_elements = html_article.find_all('p')
        paragraph_texts = [p.text for p in paragraph_elements[:-1] if not (p.find('strong') and p.find('span', class_='highlight') and p.find('a', id_='show_login'))]
        complete_text = '\n'.join(paragraph_texts)

        new.add_value('text', complete_text)
        new.add_xpath('title', "//body//h1[@class='entry-title']/text()")
        new.add_xpath('topic', "//body//li/a[@class='categoria']/text()")

        yield new.load_item()