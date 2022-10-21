import logging

# 1.创建一个logger对象
logger = logging.getLogger()

# 2. 设置日志输出器 handler,指定日志输出位置
# 如果创建StreamHandler 对象，表示将日志内容输出到控制台
# 如果创建FileHandler 对象，表示将日志内容输出到文件
stream_handler = logging.StreamHandler()
# logging.FileHandler('./los')

# 3. 将handler对象添加到logger对象中,告诉对象输出日志位置
logger.addHandler(stream_handler)

# 设置日志等级
logger.level = 10
logger.setLevel(10)

# 4. 使用logger对象输出日志
logger.debug("这是一个debug信息.....")
logger.info("这是一个info信息.....")
logger.warning("这是一个warning信息.....")
logger.error("这是一个error信息.....")
logger.critical("这是一个critical信息.....")
