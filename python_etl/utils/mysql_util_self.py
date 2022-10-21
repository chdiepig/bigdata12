import pymysql
from utils.logging_util import init_logger
from config import project_config as conf

# 获取logger对象
logger = init_logger()


class MysqlUtil(object):

    def __init__(self):
        self.conn = pymysql.connect(
            host=conf.METADATA_HOST,
            user=conf.METADATA_USER,
            password=conf.METADATA_PWD,
            port=conf.METADATA_PORT,
            charset=conf.MYSQL_CHARSET,
            # autocommit = false 不会自动提交，需要手动提交
            autocommit=False
        )
        logger.info(f'构建完成到{conf.METADATA_HOST}:{conf.METADATA_PORT}的数据库连接...')

    def close_conn(self):
        if self.conn:
            self.conn.close()

    def query(self, sql):
        """
        执行sql查询语句
        :param sql:
        :return: 查询的sql语句
        """
        # 获取游标对象
        cursor = self.conn.cursor()
        # 执行sql
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        logger.info(f"执行查询的sql语句完成，查询的结果有 {len(result)} 条, 执行的查询语句是： {sql}")
        return result

    def select_db(self, database):
        """
        选择要操作的数据库
        :param database:
        :return:
        """
        self.conn.select_db(database)

    def execute(self,sql):
        """
        直接执行一条sql语句，没有返回值
        :param sql:
        :return:
        """
        cursor = self.conn.cursor()
        cursor.execute(sql)
        logger.info(f"执行了一条sql语句: {sql}")

        if not self.conn.get_autocommit():
            self.conn.commit()

        cursor.close()

    def execute_without_autocommit(self,sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        logger.debug(f'执行了一条sql语句:{sql}')
        cursor.close()

    def check_table_exists(self,db_name,table_name):
        self.conn.select_db(db_name)
        result = self.query("show tables;")
        return (table_name,) in result

    def check_table_exits_and_create(self,db_name,table_name,create_cols):
        if not self.check_table_exists(db_name,table_name):
            # 准备建表语句
            create_sql = f"create table {table_name}({create_cols})"
            self.select_db(db_name)
            self.execute(create_sql)
            logger.info(f"在数据库：{db_name}中创建了表：{table_name}完成。建表语句是：{create_sql}")
        else:
            logger.info(f"数据库：{db_name}中，表{table_name}已经存在，创建表的操作跳过。")

