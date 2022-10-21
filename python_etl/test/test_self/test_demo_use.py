import logging
from unittest import TestCase
"""
# 验证arg1和arg2是否相等，如果相等测试通过
self.assertEqual(arg1, arg2)

# 验证arg1和arg2是否是同一个类型
self.assertIsInstance(arg1, arg2)

# 验证arg1和arg2是否不相等，不相等测试通过
self.assertNotEqual(arg1, arg2)

# 验证arg1和arg2是否不是一个类型，不是一个类型测试通过
self.assertNotIsInstance(arg1, arg2)

# 验证arg1是否是None，是就通过
self.assertIsNone(arg1)

# 验证arg1是否小于arg2，小于就通过
self.assertLess(arg1, arg2)

# 验证arg1是否小于等于arg2，小于等于就通过
self.assertLessEqual(arg1, arg2)

# 验证arg1是否是True，是就通过
self.assertTrue(arg1)

# 验证arg1是否大于arg2，大于就通过
self.assertGreater(arg1, arg2)

# 验证arg1是否大于等于arg2，大于等于就通过
self.assertGreaterEqual(arg1, arg2)

"""


def add(a, b):
    return a + b


class TestAddCase(TestCase):

    def setUp(self) -> None:
        print("开始执行测试方法......")

    def test_add_func(self):
        result = add(10,20)
        self.assertIsInstance(1,type(result))

    def tearDown(self) -> None:
        print('测试用例结束........')
