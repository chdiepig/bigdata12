import logging

# 1. 创建日志对象
logger = logging.getLogger()

# 2. 创建Handler对象 FileHandler 将日志输出到文件
file_handler = logging.FileHandler(
    filename='../logs/pyetl_log/run.log',  # 存储日志的名字和路径
    mode='a',  # 写入模式 a追加, w 覆盖
    encoding='utf-8'
)

# 3. 创建formatter对象,设置日志输出格式
formatter = logging.Formatter(
    "%(asctime)s - [%(levelname)s] - %(filename)s[%(lineno)d]: %(message)s"
)

# 4. 将formatter对象设置给handler对象
file_handler.setFormatter(formatter)

# 5. 将handler对象添加到logger对象中
logger.addHandler(file_handler)

# 6. 设置日志等级
logger.level = 10

# 7. 使用logger对象输出日志
logger.debug("这是一个debug信息.....")
logger.info("这是一个info信息.....")
logger.warning("这是一个warning信息.....")
logger.error("这是一个error信息.....")
logger.critical("这是一个critical信息.....")
