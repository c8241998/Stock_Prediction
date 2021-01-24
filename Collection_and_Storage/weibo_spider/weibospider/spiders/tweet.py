#!/usr/bin/env python
# encoding: utf-8
"""
File Description: 
Author: nghuyong
Mail: nghuyong@163.com
Created Time: 2020/4/14
"""
import datetime
import re
from lxml import etree
from scrapy import Spider
from scrapy.http import Request
import time
from items import TweetItem
from spiders.utils import time_fix, extract_weibo_content


class TweetSpider(Spider):
    name = "tweet_spider"
    base_url = "https://weibo.cn"

    def start_requests(self):

        def init_url_by_user_id():
            "crawl tweets post by users"
            user_ids = ['1087770692', '1699432410', '1266321801']
            urls = [f'{self.base_url}/{user_id}/profile?page=1' for user_id in user_ids]
            return urls

        def init_url_by_keywords():
            # crawl tweets include keywords in a period, you can change the following keywords and date
            keywords = ['苹果公司']
            date_start = datetime.datetime.strptime("2017-03-31", '%Y-%m-%d')
            date_end = datetime.datetime.strptime("2020-05-31", '%Y-%m-%d')
            time_spread = datetime.timedelta(days=1)
            urls = []
            url_format = "https://weibo.cn/search/mblog?hideSearchFrame=&keyword={}" \
                         "&advancedfilter=1&starttime={}&endtime={}&sort=time&page=1"
            while date_start < date_end:
                next_time = date_start + time_spread
                urls.extend(
                    [url_format.format(keyword, date_start.strftime("%Y%m%d"), next_time.strftime("%Y%m%d"))
                     for keyword in keywords]
                )
                date_start = next_time
            return urls

        # select urls generation by the following code
        # urls = init_url_by_user_id()
        urls = init_url_by_keywords()
        for url in urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        if response.url.endswith('page=1'):
            all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
            if all_page:
                all_page = all_page.group(1)
                all_page = int(all_page)
                for page_num in range(2, min(5,all_page + 1)):
                    page_url = response.url.replace('page=1', 'page={}'.format(page_num))
                    yield Request(page_url, self.parse, dont_filter=True, meta=response.meta)
        tree_node = etree.HTML(response.body)
        tweet_nodes = tree_node.xpath('//div[@class="c" and @id]')
        for tweet_node in tweet_nodes:
            try:
                tweet_item = TweetItem()

                create_time_info_node = tweet_node.xpath('.//span[@class="ct"]')[-1]
                create_time_info = create_time_info_node.xpath('string(.)')
                if "来自" in create_time_info:
                    tweet_item['created_at'] = time_fix(create_time_info.split('来自')[0].strip())
                else:
                    tweet_item['created_at'] = time_fix(create_time_info.strip())


                all_content_link = tweet_node.xpath('.//a[text()="全文" and contains(@href,"ckAll=1")]')
                if all_content_link:
                    all_content_url = self.base_url + all_content_link[0].xpath('./@href')[0]
                    yield Request(all_content_url, callback=self.parse_all_content, meta={'item': tweet_item},
                                  priority=1)
                else:
                    tweet_html = etree.tostring(tweet_node, encoding='unicode')
                    tweet_item['content'] = extract_weibo_content(tweet_html)
                    yield tweet_item

            except Exception as e:
                self.logger.error(e)

    def parse_all_content(self, response):
        tree_node = etree.HTML(response.body)
        tweet_item = response.meta['item']
        content_node = tree_node.xpath('//*[@id="M_"]/div[1]')[0]
        tweet_html = etree.tostring(content_node, encoding='unicode')
        tweet_item['content'] = extract_weibo_content(tweet_html)
        yield tweet_item
