# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.exceptions import IgnoreRequest
import redis
import hashlib


def hash_url(url):
    hash = hashlib.md5()  #创建md5()加密实例
    hash.update(bytes(url, encoding='utf-8'))  #对url进行加密
    return hash.hexdigest() #返回产生的十六进制的bytes



class FenghuangcaijingSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    pool = redis.ConnectionPool(host='localhost', port=6379)
    conn = redis.Redis(connection_pool=pool)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.

        url = response.url
        hurl = hash_url(url)
        self.conn.set(hurl, 'ok')
        print('have saved url: %s' % url)

        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class FenghuangcaijingDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    pool = redis.ConnectionPool(host='localhost', port=6379)
    conn = redis.Redis(connection_pool=pool)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    # 下载之前从redis中查询是否已经存在该url
    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        HA_urls = [r"http://app.finance.ifeng.com/list/stock.php?t=ha&f=symbol&o=asc&p={}".format(i) for i in range(1, 28)]
        HB_urls = [r'http://app.finance.ifeng.com/list/stock.php?t=hb&f=symbol&o=asc&p=1']
        SA_urls = [r'http://app.finance.ifeng.com/list/stock.php?t=sa&f=symbol&o=asc&p={}'.format(i) for i in range(1, 40)]
        SB_urls = [r'http://app.finance.ifeng.com/list/stock.php?t=sb&f=symbol&o=asc&p=1']
        start_urls = HA_urls + HB_urls + SA_urls + SB_urls

        url = request.url
        if not url in start_urls:
            hurl = hash_url(url)
            if self.conn.get(hurl) == b'ok':
                print('have parsed url: %s' % url)
                raise IgnoreRequest
        else:
            return None


        # return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

