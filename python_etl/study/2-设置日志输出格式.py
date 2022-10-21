import logging

logger = logging.getLogger()

stream_handler = logging.StreamHandler()

logger.addHandler(stream_handler)

# 修改日志输出的格式,创建formatter对象,需要传入 日志输出格式的字符串
formatter = logging.Formatter(
    "%(asctime)s - [%(levelname)s] - %(filename)s[%(lineno)d]: %(message)s"
)
# 将创建好的formatter对象设置给handler
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.setLevel(10)

logger.debug('我是debug信息....')
logger.info('我是info信息....')
logger.warning('我是warning信息....')
logger.error('我是error信息....')
logger.critical('我是critical信息....')
