from loguru import logger
from pyquery import PyQuery as pq

from src.crawler.base import BaseCrawler
from src.schema.proxy import Proxy


class Ip66Crawler(BaseCrawler):
    urls = ['http://www.66ip.cn/']
    ignore = False

    def parse(self, html):
        doc = pq(html)
        for tr in doc('#main table tr:gt(0)').items():
            host = tr.find('td:nth-child(1)').text()
            port = tr.find('td:nth-child(2)').text()
            if host and port:
                yield Proxy(host, port).to_string()


if __name__ == '__main__':
    crawler = Ip66Crawler()
    for p in crawler.crawl():
        logger.info(p)
