from loguru import logger
from pyquery import PyQuery as pq

from src.crawler.base import BaseCrawler
from src.schema.proxy import Proxy


class IpYunCrawler(BaseCrawler):
    urls = [f'http://www.ip3366.net/?stype=1&page={i}' for i in range(1, 6)]
    ignore = False

    def parse(self, html):
        doc = pq(html)
        for tr in doc('tbody tr').items():
            host = tr.find('td:nth-child(1)').text()
            port = tr.find('td:nth-child(2)').text()
            if host and port:
                yield Proxy(host, port).to_string()


if __name__ == '__main__':
    crawler = IpYunCrawler()
    for p in crawler.crawl():
        logger.info(p)
