from loguru import logger

from proxy_pool.settings import MAX_COUNT
from src.crawler import __all__ as crawler_cls
from src.storage.redis_storage import RedisClient


class Getter:
    def __init__(self):
        self.redis = RedisClient()
        self.crawler_cls = crawler_cls
        self.crawlers = [cls() for cls in self.crawler_cls]

    @property
    def is_full(self):
        return self.redis.count >= MAX_COUNT

    def run(self):
        if self.is_full:
            return

        for crawler in self.crawlers:
            logger.info(f'{crawler.__class__.__name__} start to get proxy...')
            for proxy in crawler.crawl():
                self.redis.add(proxy)


if __name__ == '__main__':
    getter = Getter()
    getter.run()
