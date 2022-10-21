from unittest import TestCase
from utils.logging_util import init_logger
import logging


class TestLogging(TestCase):
    def setUp(self) -> None:
        pass

    def test_logging_util(self):
        logger = init_logger()
        self.assertIsInstance(logger,logging.RootLogger)

    def tearDown(self) -> None:
        pass
