from loguru import logger
from pyquery import PyQuery as pq

from src.crawler.base import BaseCrawler
from src.schema.proxy import Proxy


class Ip89Crawler(BaseCrawler):
    urls = [f'https://www.89ip.cn/index_{i}.html' for i in range(1, 11)]
    ignore = False

    def parse(self, html):
        doc = pq(html)
        for tr in doc('tbody > tr').items():
            host = tr.find('td:nth-child(1)').text().strip()
            port = tr.find('td:nth-child(2)').text().strip()
            if host and port:
                yield Proxy(host, port).to_string()


if __name__ == '__main__':
    crawler = Ip89Crawler()
    for p in crawler.crawl():
        logger.info(p)
