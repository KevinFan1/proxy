from loguru import logger
from pyquery import PyQuery as pq

from src.crawler.base import BaseCrawler
from src.schema.proxy import Proxy


class CountryCrawler(BaseCrawler):
    urls = [f'https://ip.jiangxianli.com/?page={i}' for i in range(1, 5)]

    def parse(self, html):
        doc = pq(html)
        for tr in doc('tbody tr').items():
            host = tr.find('td:nth-child(1)').text()
            port = tr.find('td:nth-child(2)').text()
            if host and port:
                yield Proxy(host, port).to_string()


if __name__ == '__main__':
    crawler = CountryCrawler()
    for p in crawler.crawl():
        logger.info(p)
