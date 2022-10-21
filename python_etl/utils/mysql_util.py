import pymysql
from config import project_config as conf
from utils.logging_util import init_logger

logger = init_logger()


class MysqlUtil(object):

    def __init__(self,
                 host=conf.METADATA_HOST,
                 port=conf.METADATA_PORT,
                 user=conf.METADATA_USER,
                 pwd=conf.METADATA_PWD):
        """
        建立连接
        :param host:ip地址
        :param port: 端口号
        :param user: 用户名
        :param pwd: 密码
        """
        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=pwd,
            charset=conf.MYSQL_CHARSET,
            # false 表示不自动提交
            autocommit=False
        )
        logger.info(f'构建完成到{conf.METADATA_HOST}:{conf.METADATA_PORT}的数据库连接...')

    def close_conn(self):
        """
        关闭连接
        :return:
        """
        if self.conn:
            self.conn.close()

    def select_db(self, db_name):
        """
        切换数据库 ==> use database
        :param db_name: 数据库名
        :return:
        """
        self.conn.select_db(db_name)

    def query(self, sql):
        """
        执行查询语句 select
        :param sql: 查询语句
        :return: 查询的结果
        """
        # 创建游标对象
        cursor = self.conn.cursor()
        # 执行sql语句
        cursor.execute(sql)
        # 获取查询的结果
        result = cursor.fetchall()
        # 关闭游标对象
        cursor.close()
        logger.info(f"执行了语句:{sql},查询的结果有{len(result)}条")

        return result

    def execute(self, sql):
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

    def execute_without_autocommit(self, sql):
        """
        直接执行一条SQL语句，没有返回值
        不会判断自动提交，只执行不会commit
        :param sql: 要执行的sql语句
        """
        # 获取游标对象
        cursor = self.conn.cursor()
        # 执行sql语句
        # 这条SQL能否执行，取决于自动提交参数，是True就能执行，是False就暂缓
        cursor.execute(sql)

        # 输出日志
        logger.debug(f'执行了一条sql语句: {sql}')
        # 关闭游标对象
        cursor.close()

    def check_table_exists(self, db_name, tb_name):
        """
        判断表是否存在的方法
        :param db_name:数据库名
        :param tb_name:表名
        :return:
        """
        # 切换数据库
        self.select_db(db_name)
        # 执行show tables
        return (tb_name,) in self.query("show tables")

    def check_table_exists_and_create(self, db_name, tb_name, create_cols=None):
        """
        如果表不存在，则创建该表
        :param db_name: 数据库名
        :param tb_name: 表名
        :param create_cols: 字段语句
        :return:
        """
        create_table_sql = f'create table {tb_name}({create_cols})'
        if not self.check_table_exists(db_name, tb_name):
            self.select_db(db_name)
            self.execute(create_table_sql)
            logger.info(f"在数据库:{db_name}中创建了表:{tb_name}完成。建表语句是:{create_table_sql}")
        else:
            logger.info(f"数据库:{db_name}中,表{tb_name}已经存在,创建表的操作跳过。")



