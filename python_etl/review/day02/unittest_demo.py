from unittest import TestCase


def add(a,b):
    return a+b


class TestAdd(TestCase):
    def setUp(self) -> None:
        print("测试开始了.....")

    def test_add(self):
        res = add(10,20)
        self.assertEqual(30,res)

    def tearDown(self) -> None:
        print("测试结束了....")

