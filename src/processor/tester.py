import asyncio

import aiohttp
from loguru import logger

from proxy_pool.settings import PER_TEST
from src.storage.redis_storage import RedisClient


class Tester:
    def __init__(self):
        self.redis = RedisClient()
        self.loop = asyncio.get_event_loop()

    async def test(self, proxy):
        logger.info(f'start testing proxy {proxy} ...')
        try:
            conn = aiohttp.TCPConnector(ssl=False)
            async with aiohttp.ClientSession(connector=conn) as session:
                url = 'http://httpbin.org/ip'
                async with session.get(url, timeout=10, proxy=f'http://{proxy}') as resp:
                    res = await resp.json()
                    if resp.status == 200 and res['origin']:
                        logger.info(f'proxy {proxy} is useful, set max score')
                        self.redis.set_max(proxy)
                    else:
                        logger.warning(f'proxy {proxy} is useless, decrease')
                        self.redis.decrease(proxy)
        except BaseException as e:
            logger.warning(e)
            logger.warning(f'in exception : proxy {proxy} is useless, decrease')
            self.redis.decrease(proxy)

    def run(self):
        logger.info('starting tester ...')
        count = self.redis.count
        logger.info(f'total proxy count is {count}')
        cursor = 0
        while True:
            cursor, proxies = self.redis.batch(cursor, count=PER_TEST)
            if proxies:
                tasks = [self.test(proxy) for proxy in proxies]
                self.loop.run_until_complete(asyncio.wait(tasks))
            if not cursor:
                break


if __name__ == '__main__':
    test = Tester()
    test.run()
