from config import project_config as conf
from pymysql import connect
from utils.logging_util import init_logger

logger = init_logger()


class MysqlUtil(object):

    def __init__(self,
                 host=conf.METADATA_HOST,
                 user=conf.METADATA_USER,
                 pwd=conf.METADATA_PWD,
                 port=conf.METADATA_PORT
                 ):
        self.conn = connect(
            host=host,
            user=user,
            password=pwd,
            port=port,
            charset=conf.MYSQL_CHARSET
        )
        logger.info("连接数据库成功...")

    def conn_close(self):
        if self.conn:
            self.conn.close()

    def select_db(self, db_name):
        self.conn.select_db(db_name)

    def query(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        logger.info(f"执行了{len(res)}条语句")
        return res

    def execute(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        if not self.conn.get_autocommit():
            self.conn.commit()
        cursor.close()

    def check_table_exists(self, db_name, tb_name):
        self.select_db(db_name)
        return (tb_name,) in self.query('show tables')

    def check_table_exists_create(self, db_name, tb_name, cols):
        if not self.check_table_exists(db_name, tb_name):
            self.execute(f'create table {tb_name}({cols}) ')
