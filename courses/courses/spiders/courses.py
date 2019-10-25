# -*- coding: utf-8 -*-
import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CoursesSpider(CrawlSpider):
    name = 'courses'
    # allowed_domains = ['my.uq.edu.au/']
    start_urls = ['https://my.uq.edu.au/programs-courses/search.html?keywords=comp&searchType=course&archived=true&CourseParameters%5Bsemester%5D=']

    rules = (
        Rule(LinkExtractor(allow=('\/programs-courses\/course\.html\?course_code=[a-zA-Z0-9]*$', )), callback='parse_item'),
    )
    def parse_item(self, response):
        yield {
            'name': response.css('#course-title::text').get(),
            'pre': response.css('#course-prerequisite::text').get(),
        }