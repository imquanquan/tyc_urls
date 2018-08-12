#!/usr/bin/env python3.6
# -*- encoding: utf-8 -*-

import sys
import time
from random import randint

import scrapy
from pyquery import PyQuery as pq
from scrapy.http import Request, FormRequest, HtmlResponse
from tianyancha.items import TianyanchaItem


class TycUrlSpider(scrapy.Spider):
    name = "tyc_url"

    def start_requests(self):
        # 登录入口
        return [Request("https://www.tianyancha.com/login", meta={'cookiejar': 1}, callback=self.login)]

    def login(self, response):
        '''
        use selenium to login and get cookices
        '''
        from selenium import webdriver
        username = ''
        passwd = ''
        browser = webdriver.Firefox()
        browser.get("https://www.tianyancha.com/login")
        browser.find_element_by_xpath('//*[@id="web-content"]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/input').send_keys(username)
        browser.find_element_by_xpath('//*[@id="web-content"]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/input').send_keys(passwd)
        browser.find_element_by_xpath('//*[@id="web-content"]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[5]').click()

        cookie_dict = {}

        cookies = browser.get_cookies()

        for cookie in cookies:
            cookie_dict[cookie['name']] = cookie['value']

        return [Request(url="https://www.tianyancha.com/usercenter/concern/1",
                        cookies=cookie_dict,
                        meta={'cookies' : cookie_dict},
                        callback=self.after_login,
                        dont_filter=True
                        )]

    def after_login(self, response):
        URL_FMT = "https://gd.tianyancha.com/search/p{page}?key={keyword}&searchType=scope"

        for page in range(0, 250):
            url = URL_FMT.format(page=page, keyword="导航")
            time.sleep(randint(50, 100)/25)
            yield Request(url=url,
                          cookies=response.meta['cookies'],
                          meta={'cookies' : response.meta['cookies'],
                                'page' : page},
                          callback=self.crawl_url,
                          dont_filter=True)

    def crawl_url(self, response):
        print(response.status)
        doc = pq(response.body.decode('utf8'))
        a_tags = doc('.header a')
        for a in a_tags.items():
            item = TianyanchaItem()
            item['url'] = a.attr.href
            item['page'] = response.meta['page']
            yield item
