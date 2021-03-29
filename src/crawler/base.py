import random
import time

import requests
from loguru import logger
from retrying import retry, RetryError

from proxy_pool.settings import CYCLE_GETTER
from src.storage.redis_storage import RedisClient


class BaseCrawler:
    # 需要爬取的地址
    urls = []
    # 是否忽略这个爬虫
    ignore = False

    def __init__(self):
        self.redis = RedisClient()
        self._header = {
            'user-agent': self.user_agent
        }

    @property
    def user_agent(self):
        ua_list = ['Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
                   'Mozilla/5.0 (compatible; U; ABrowse 0.6;  Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
                   'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)',
                   'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR   3.5.30729)',
                   'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0;   Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;   SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
                   'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)',
                   'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1;   .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)',
                   'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
                   'Mozilla/4.0 (compatible; Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729); Windows NT 5.1; Trident/4.0)',
                   'Mozilla/4.0 (compatible; Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727); Windows NT 5.1; Trident/4.0; Maxthon; .NET CLR 2.0.50727; .NET CLR 1.1.4322; InfoPath.2)',
                   'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)']
        return random.choice(ua_list)

    @retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is None, wait_fixed=2000)
    def fetch(self, url, **kwargs):
        try:
            kwargs.setdefault('headers', self._header)
            kwargs.setdefault('timeout', 3)
            # kwargs.setdefault('verify', False)
            resp = requests.get(url, **kwargs)
            if resp.status_code == 200:
                resp.encoding = 'gbk'
                return resp.text
        except BaseException as e:
            logger.error(f'cannot fetch html from {url},{e}')
            return

    def crawl(self):
        for url in self.urls:
            if self.redis.is_url_exists(url):
                logger.warning(f'{url}在{CYCLE_GETTER}s内不需要重新抓取')
                continue

            logger.info(f'start fetching {url}')
            try:
                html = self.fetch(url)
            except RetryError:
                self.redis.set_url_cache(url)
                logger.error(f'cannot fetch html:{url}')
                return

            time.sleep(0.5)
            for p in self.parse(html):
                self.redis.set_url_cache(url)
                yield p

    def parse(self, html):
        raise NotImplementedError
