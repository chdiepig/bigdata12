import logging
from unittest import TestCase
from utils.logging_util import init_logger


class TestLoggingUtil(TestCase):

    def setUp(self) -> None:
        pass

    def test_get_logger(self):
        logger = init_logger()

        # 测试生成的logger对象类型是否正确
        self.assertIsInstance(logger,logging.RootLogger)



