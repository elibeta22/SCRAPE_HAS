# -*- coding: utf-8 -*-
import scrapy
import re
from inline_requests import inline_requests
from HelpAStudent_Scrapy.items import HelpAStudentItem
import numpy as np
import json


class SchoolsSpider(scrapy.Spider):
    name = "has_schools"
    allowed_domains = ["ratemyprofessors.com"]
    start_urls = (
        'http://www.ratemyprofessors.com/search.jsp?queryBy=schoolName&queryoption=HEADER&facetSearch=true',
    )
    base_url = 'http://www.ratemyprofessors.com/'

    def parse(self, response):
        school_list_li = response.xpath("//ul[@class='listings']//li[@class='listing SCHOOL']")
        for card in school_list_li:
            link = card.xpath("a/@href").extract_first()
            yield scrapy.Request(
                url=self.base_url+link,
                callback=self.parse_schools,
                dont_filter=True,
            )

        # following pagination
        next_page = response.xpath("//a[@class='nextLink']/@href").extract_first()
        if next_page:
            yield scrapy.Request(
                url=self.base_url+next_page,
                callback=self.parse,
                dont_filter=True,
            )


    def parse_schools(self, response):
        all_prof_links = response.xpath("//a[@class='button-link']/@href").extract_first()
        absolute_url = self.base_url + all_prof_links
        yield scrapy.Request(absolute_url, callback=self.parse_professors)


    def parse_professors(self, response):

        # top professors

        prof_list = []
        prof_dict = {}


        professor_list_li = response.xpath("//div[@class='SearchResultsPage__StyledSearchResultsPage-sc-1ofj1e3-0 hVMHGn']")

        school_name = response.xpath("//div[@class='CardSchool__School-sc-19lmz2k-1 iDlVGM']/text()").extract_first()


        # teacher_reviews_total = teacher_res.xpath("//div[contains(@class,'rating-count')]/text()").extract_first()
        for card in professor_list_li:

            professor_rating = card.xpath("//div[@class='CardNumRating__CardNumRatingNumber-sc-17t4b9u-2 bBZfNz']/text()").getall()

            professor_name_fn = card.xpath("//div[@class='CardName__StyledCardName-sc-1gyrgim-0 cJdVEK']/text()[1]").getall()
            professor_name_s = card.xpath("//div[@class='CardName__StyledCardName-sc-1gyrgim-0 cJdVEK']/text()[2]").getall()
            professor_name_ln = card.xpath("//div[@class='CardName__StyledCardName-sc-1gyrgim-0 cJdVEK']/text()[3]").getall()
            x1 = np.array(professor_name_fn)
            x2 = np.array(professor_name_s)
            x3 = np.array(professor_name_ln)
            first_professor_name = np.char.add(x1, x2)
            professor_name = np.char.add(first_professor_name, x3)
            professor_name = professor_name.tolist()

            professor_department = card.xpath("//div[@class='CardSchool__Department-sc-19lmz2k-0 haUIRO']/text()").getall()

            prof_dict['professor_names'] = professor_name
            prof_dict['professor_departments'] = professor_department
            prof_dict['professor_ratings'] = professor_rating

            item = HelpAStudentItem()
            item['school_name'] = school_name
            item['school_professors'] = prof_dict
            yield item
