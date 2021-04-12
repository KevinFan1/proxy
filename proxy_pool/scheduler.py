import time
from multiprocessing import Process, cpu_count

import uvicorn
from loguru import logger

from proxy_pool.settings import CYCLE_TESTER, CYCLE_GETTER
from src.processor.getter import Getter
from src.processor.tester import Tester

getter_process = tester_process = server_process = None


class Scheduler:
    def run_tester(self, sec=CYCLE_TESTER):
        tester = Tester()
        loop = 1
        while True:
            logger.info(f'tester loop {loop} starting...')
            tester.run()
            loop += 1
            time.sleep(sec)

    def run_getter(self, sec=CYCLE_GETTER):
        getter = Getter()
        loop = 1
        while True:
            logger.info(f'getter loop {loop} starting...')
            getter.run()
            loop += 1
            time.sleep(sec)

    def run_server(self):
        logger.info(f'server starting...')
        uvicorn.run(
            app='src.processor.server:app',
            host='0.0.0.0',
            port=5003,
            reload=True,
            workers=int(cpu_count()) - 1,
            debug=False,
        )

    def run(self):
        global getter_process, tester_process, server_process
        try:
            tester_process = Process(target=self.run_tester)
            logger.info('starting tester processing...')
            tester_process.start()
            server_process = Process(target=self.run_server)
            logger.info('starting serving processing...')
            server_process.start()
            getter_process = Process(target=self.run_getter)
            logger.info('starting getter processing...')
            getter_process.start()

            tester_process.join()
            server_process.join()
            getter_process.join()
        except KeyboardInterrupt:
            logger.info('catch keyboard interrupt signal')
            tester_process.terminate()
            getter_process.terminate()
            server_process.terminate()
        finally:
            tester_process.join()
            server_process.join()
            getter_process.join()


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()
