
"""we import scrapy so that we can use the classes that the package provides."""
import scrapy

"""
we take the Spider class provided by Scrapy and make a subclass out of it called BrickSetSpider.
The Spider subclass has methods and behaviors that define how to follow URLs and extract data 
from the pages it finds, but it doesn’t know where to look or what data to look for.
By subclassing it, we can give it that information.
"""


class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['https://www.digitalocean.com/community/tutorials', ]

    def parse(self, response):
        SET_SELECTOR = '.tutorial.tutorial'
        for brickset in response.css(SET_SELECTOR):
            TUTORIAL_SELECTOR = 'h3 ::text'
            LINK_SELECTOR = 'a ::attr(href)'

            yield {
                'Tutorial': brickset.css(TUTORIAL_SELECTOR).extract_first(),
                'Link': brickset.css(LINK_SELECTOR).extract_first(),
            }

        NEXT_PAGE_SELECTOR = '.load-more-results-container a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )


class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['http://brickset.com/sets/year-2016',
                  'http://brickset.com/sets/year-2017',
                  'http://brickset.com/sets/year-2018',
                  'http://brickset.com/sets/year-2019',
                  'http://brickset.com/sets/year-2020']

    """This code grabs all the sets on the page and loops over them to extract the data"""

    def parse(self, response):
        SET_SELECTOR = '.set'
        for brickset in response.css(SET_SELECTOR):

            NAME_SELECTOR = 'h1 ::text'
            PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
            MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
            PRICE_SELECTOR = './/dl[dt/text() = "RRP"]/dd/text()'
            IMAGE_SELECTOR = 'img ::attr(src)'

            yield {
                'name': brickset.css(NAME_SELECTOR).extract_first(),
                'pieces': brickset.xpath(PIECES_SELECTOR).extract_first(),
                'minifigs': brickset.xpath(MINIFIGS_SELECTOR).extract_first(),
                'image': brickset.css(IMAGE_SELECTOR).extract_first(),
                'price': brickset.xpath(PRICE_SELECTOR).extract_first(),
            }

        """
        First, we define a selector for the “next page” link, extract the first match, and check if it exists.
        The scrapy.Request is a value that we return saying “Hey, crawl this page”, and callback=self.parse says
        “once you’ve gotten the HTML from this page, pass it back to this method so we can parse it,
        extract the data, and find the next page.“
        """

        NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
