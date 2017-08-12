# -*- coding: utf-8 -*-
import scrapy


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'tmall-xpath'
    start_urls = [
        'http://blog.csdn.net/u010526125/',
    ]

    def parse(self, response):
        #for quote in response.xpath('/html/body/div[@class="blog_left"]/div[@class="blog_l_c"]/div[@class="item_wrap"]/div[@class="item_l"]'):
        for quote in response.xpath('//dl[@class="item_l"]'):
            yield {
                'item': quote.xpath('./dt[@class="item"]/text()').extract_first(),
                'item_name': quote.xpath('./dd[@class="item_name"]/text()').extract_first(),
            }

        #next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        #if next_page_url is not None:
        #    yield scrapy.Request(response.urljoin(next_page_url))
