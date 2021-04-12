from random import choice

from loguru import logger
from redis import StrictRedis

from proxy_pool.settings import REDIS_KEY, MAX_SCORE, MIN_SCORE, INIT_SCORE, REDIS_HOST, REDIS_PORT, REDIS_DB, \
    REDIS_PASSWORD, CYCLE_GETTER


class RedisClient:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD):
        # 初始化redis连接
        self.db = StrictRedis(host, port, db, password, decode_responses=True)

    def exists(self, proxy):
        # 判断是否存在这个代理
        return not self.db.zscore(REDIS_KEY, proxy) is None

    @property
    def count(self):
        return self.db.zcard(REDIS_KEY)

    def all(self):
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def _set_score(self, proxy, score):
        # 设置分数
        return self.db.zadd(REDIS_KEY, {proxy: score})

    def add(self, proxy, score=INIT_SCORE):
        # 添加代理 和 设置最高分
        if not self.exists(proxy):
            self._set_score(proxy, score)

    def decrease(self, proxy):
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            # 减分
            logger.info(f'{proxy} current score : {score}, -1')
            return self.db.zincrby(REDIS_KEY, -1, proxy)
        # 如果没有score获取score小于0，移除
        logger.info(f'{proxy} current score : {score}, remove')
        return self.db.zrem(REDIS_KEY, proxy)

    def set_max(self, proxy):
        # 设置最大分数
        return self._set_score(proxy, MAX_SCORE)

    def random(self):
        res = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if res:
            return choice(res)

        res = self.db.zrevrange(REDIS_KEY, MIN_SCORE, MAX_SCORE)
        if res:
            return choice(res)

        raise Exception('proxy pool is empty')

    def batch(self, cursor, count):
        cursor, proxies = self.db.zscan(REDIS_KEY, cursor, count=count)
        return cursor, [i[0] for i in proxies]

    def set_url_cache(self, key, value=1, exp=CYCLE_GETTER - 2):
        # 设置url缓存，防止项目重启时重复查找
        return self.db.set(key, value, exp)

    def is_url_exists(self, key):
        return self.db.exists(key)


if __name__ == '__main__':
    client = RedisClient()
    logger.info(client.batch(0, 50))
