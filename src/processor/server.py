from multiprocessing import cpu_count

import uvicorn
from fastapi import FastAPI

from src.storage.redis_storage import RedisClient

app = FastAPI(
    title='proxy pool',
)


def get_conn():
    return RedisClient()


@app.get('/')
async def index():
    return 'Welcome to Proxy Pool System'


@app.get('/random')
def get_proxy():
    conn = get_conn()
    return {'proxy': conn.random()}


if __name__ == '__main__':
    uvicorn.run(
        'server:app',
        host='0.0.0.0',
        port=5000,
        reload=True,
        workers=int(cpu_count()) - 1,
        debug=False
    )
