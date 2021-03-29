from loguru import logger
from pyquery import PyQuery as pq

from src.crawler.base import BaseCrawler
from src.schema.proxy import Proxy


class KuDaiCrawler(BaseCrawler):
    urls = ['https://www.kuaidaili.com/free/']
    ignore = False

    def parse(self, html):
        doc = pq(html)
        for tr in doc('tbody > tr').items():
            host = tr.find('td[data-title="IP"]').text()
            port = tr.find('td[data-title="PORT"]').text()
            if host and port:
                yield Proxy(host, port).to_string()


if __name__ == '__main__':
    crawler = KuDaiCrawler()
    for p in crawler.crawl():
        logger.info(p)
