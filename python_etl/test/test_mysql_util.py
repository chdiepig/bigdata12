from unittest import TestCase
from utils.mysql_util_self import MysqlUtil


class TestMysqlUtil(TestCase):

    def setUp(self) -> None:
        # 创建MysqlUtil对象
        self.db_util = MysqlUtil()

    def test_query(self):
        self.db_util.select_db("etl_test")
        self.db_util.check_table_exits_and_create(
            "etl_test",
            "tb_stu",
            "id int primary key auto_increment,name varchar(20)"
        )
        # 清空表中的数据
        self.db_util.execute("truncate tb_stu")

        self.db_util.execute("insert into tb_stu values(1,'陈航'),(2,'徐文豪');")

        result = self.db_util.query("select * from tb_stu;")
        self.assertEqual(((1, '陈航'), (2, '徐文豪')), result)
        self.db_util.execute("drop table tb_stu")

