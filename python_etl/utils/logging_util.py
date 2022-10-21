import logging
from config import project_config as conf


# 定义一个类
class Logging(object):

    def __init__(self, level=20):
        self.logger = logging.getLogger()
        self.logger.setLevel(level)


# 专门设置logger对象,设置日志输出位置,设置日志格式
def init_logger():
    """
    初始化日志对象，设置日志输出格式
    :return: 日志对象
    """

    #  1.获取logger对象
    logger = Logging().logger

    # 2. 创建handler对象,将日志输出到文件
    if logger.handlers:
        return logger
    # 一个小时生成一个日志文件
    file_handler = logging.FileHandler(
        filename=conf.LOG_FILE_PATH+conf.LOG_FILE_NAME,
        mode='a',
        encoding='utf-8'
    )
    # 3. 设置日志输出格式
    fmt = logging.Formatter(
        "%(asctime)s - [%(levelname)s] - %(filename)s[%(lineno)d]: %(message)s"
    )
    # 4.将格式设置给handler,再将handler设置给logger
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)
    # 5. 将设置完毕的logger对象返回
    return logger
