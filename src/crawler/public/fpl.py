from loguru import logger
from pyquery import PyQuery as pq

from src.crawler.base import BaseCrawler
from src.schema.proxy import Proxy


class FPLCrawler(BaseCrawler):
    # 反爬
    urls = [f'http://www.freeproxylists.net/zh/?u=50&page={i}' for i in range(1, 4)]
    ignore = True

    def parse(self, html):
        doc = pq(html)
        for tr in doc('tbody tr').items():
            print(tr)
            host = tr.find('td:nth-child(2) > td:nth-child(1) > a').text()
            port = tr.find('td:nth-child(2)').text()
            if host and port:
                yield Proxy(host, port).to_string()


if __name__ == '__main__':
    crawler = FPLCrawler()
    for p in crawler.crawl():
        logger.info(p)
