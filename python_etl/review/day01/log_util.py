import logging
import project_conf as conf

class Logging(object):

    def __init__(self,level=20):
        self.logger = logging.getLogger()
        self.logger.setLevel(level)


def init_logger():
    # 创建logger对象
    logger = Logging().logger

    file_handler = logging.FileHandler(
        filename=conf.LOG_PATH+conf.LOG_NAME,
        encoding='utf-8',
        mode='a'
    )

    fmt = logging.Formatter(
        "%(asctime)s - [%(levelname)s] - %(filename)s[%(lineno)d]: %(message)s"
    )

    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    return logger


