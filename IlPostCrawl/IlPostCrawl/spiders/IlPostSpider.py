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
        The function, first of all, take all the url of all the categories of the newspaper. Then, it calls the parser for each of them.
    '''
    def parse(self, response):

        categories_url = response.xpath("//body//div[@class='headerIlPost_Nav']/ul/li/a/@href").extract()[:-2]

        for category_url in categories_url:
            yield scrapy.Request(url=category_url, callback=self.parse_category, dont_filter=True)

    '''
        This function makes the following things:
        1) It takes the number of pages of the current category
        2) It calls the parse of the pages for each one of the category
    '''
    def parse_category(self, response):

        number_of_pages = 0

        if len(response.xpath("//body//li/a[@class='page-numbers']").extract()) > 0:
            number_of_pages = response.xpath("//body//li/a[@class='page-numbers']/text()").extract()[2]
            number_of_pages = int(number_of_pages.replace('.',''))
        elif len(response.xpath("//body//div[@class='new-pagination']/div[@class='new-pag-cent']").extract()) > 0:
            s_number_of_pages = response.xpath("//body//div[@class='new-pagination']/div[@class='new-pag-cent']/text()").extract()[0].split()[2]
            number_of_pages = int(s_number_of_pages)

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
        This function parse a single article extracting and adding to an Item:
        1) The text of the article
        2) The title of the article
        3) The topic of the article
        
        It makes these three steps only if it is an article that doesn't require a subscription. Otherwise, it skips it.
    '''
    def parse_article(self, response):
        new = ItemLoader(item=IlpostItem(), response=response)

        html_article = rs.get(response.url).text
        html_article = bs.BeautifulSoup(html_article, 'lxml')
        paragraph_elements = html_article.find_all('p')

        if len(response.xpath("//body//div/span[@class='highlight']").extract()) == 0:
            paragraph_texts = [p.text for p in paragraph_elements[:-1] if not (p.find('a', class_='leggi-anche') or
                                                                               p.findParent(class_='wp-caption'))]
            complete_text = '\n'.join(paragraph_texts)

            new.add_value('text', complete_text)
            new.add_xpath('title', "//body//h1[@class='entry-title']/text()")
            new.add_xpath('topic', "//body//li/a[contains(@class, 'categoria') or contains(@class, 'rubrica')]/text()")

            yield new.load_item()