import os
import sys

from loguru import logger

# 工程主路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 普通log
log_file_path = os.path.join(BASE_DIR, 'log/normal.log')
# 错误log
err_log_file_path = os.path.join(BASE_DIR, 'log/error.log')
logger.add(sys.stderr, format="{time} {level} {pays}", filter="my_module", level="INFO")
logger.add(log_file_path, rotation="00:00", encoding='utf-8', retention='5 days')
logger.add(err_log_file_path, rotation="00:00", encoding='utf-8', level='ERROR', retention='10 days')
