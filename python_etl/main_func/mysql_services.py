# 处理数据库中条形码数据的主业务逻辑的实现

import sys
from models.barcode_model import BarcodeModel
from utils.logging_util import init_logger
from utils.mysql_util import MysqlUtil
from config import project_config as conf

logger = init_logger()
logger.info('mysql表数据处理开始')

# 先去准备三个数据库的连接
# 元数据库的连接
metadata_db_util = MysqlUtil()

# 源数据库的连接
source_db_util = MysqlUtil(
    host=conf.source_host,
    port=conf.source_port,
    user=conf.source_user,
    pwd=conf.source_password
)

# 目标数据库的连接
target_db_util = MysqlUtil(
    host=conf.TARGET_HOST,
    port=conf.TARGET_PORT,
    user=conf.TARGET_USER,
    pwd=conf.TARGET_PASSWORD
)

# 从源数据库是中读取条形码数据
# 在读取表数据的时候，存在则直接读取，不存在，结束程序
if not source_db_util.check_table_exists(
        conf.source_db_name,
        conf.source_barcode_data_table_name):
    logger.info(f"数据库:{conf.source_db_name}中的表{conf.source_barcode_data_table_name}不存在，无需处理，程序结束")
    print("表不存在，程序退出")
    sys.exit(1)

# 先判断目的表是否存在
target_db_util.check_table_exists_and_create(
    db_name=conf.TARGET_DB_NAME,
    tb_name=conf.target_barcode_table_name,
    create_cols=conf.target_barcode_table_create_cols
)

# 从元数据库中获取上一次处理数据的最新时间
# 切换数据库
metadata_db_util.select_db(conf.METADATA_DB_NAME)
# 找到上一次的更新时间
# last_update_time = None
metadata_db_util.check_table_exists_and_create(
    conf.METADATA_DB_NAME,
    conf.metadata_barcode_table_name,
    conf.metadata_barcode_table_create_cols
)
last_update_time_query_sql = f"select time_record from {conf.metadata_barcode_table_name} order by time_record desc limit 1"
last_update_time = metadata_db_util.query(last_update_time_query_sql)

if len(last_update_time) > 0:
    last_update_time = last_update_time[0][0]
else:
    last_update_time = "2000-01-01 00:00:00"


# last_update_time = None，查询所有数据即可
# last_update_time有值，条件筛选
if last_update_time:
    query_sql = f"select * from {conf.source_barcode_data_table_name} " \
                f"where updateAt > '{last_update_time}' order by  updateAt desc"
else:
    query_sql = f"select * from {conf.source_barcode_data_table_name} order by updateAt desc"

# 执行sql，从源数据库中获取本次要处理的数据即可
result = source_db_util.query(query_sql)

# 遍历每一条数据，将每一条数据转换为模型类对象。目的：方便生成插入语句，和csv一行字符串。
# 准备一个列表，存储每一个模型类对象
barcode_model_list = []
for line in result:
    # 创建模型类对象
    model = BarcodeModel(
        code=line[0],
        name=line[1],
        spec=line[2],
        trademark=line[3],
        addr=line[4],
        units=line[5],
        factory_name=line[6],
        trade_price=line[7],
        retail_price=line[8],
        update_at=str(line[9]),
        wholeunit=line[10],
        wholenum=line[11],
        img=line[12],
        src=line[13]
    )
    barcode_model_list.append(model)

max_last_update_time = str(last_update_time)
count = 0

for barcode_model in barcode_model_list:
    # 获取当前数据的更新时间
    current_barcode_update_time = barcode_model.update_at

    if current_barcode_update_time > max_last_update_time:
        max_last_update_time = current_barcode_update_time
    # 生成插入语句
    insert_sql = barcode_model.generate_insert_sql()
    target_db_util.execute_without_autocommit(insert_sql)
    count += 1

    if count % 1000 == 0:
        target_db_util.conn.commit()
        logger.info(f"从数据源：{conf.source_db_name}库，读取表：{conf.source_barcode_data_table_name}，"
                    f"当前写入目标表：{conf.target_barcode_table_name}数据有:{count}行")


# 一次性全部提交
target_db_util.conn.commit()


# 将数据写入csv文件
csv_file = open(
    conf.barcode_orders_output_csv_file_path + conf.barcode_orders_output_csv_file_name,
    'w',
    encoding='utf-8-sig'
)
# 遍历每一个模型类对象，转化为csv
csv_file_count = 0
for model in barcode_model_list:
    csv_file.write(model.to_csv() + "\n")
    csv_file_count += 1

csv_file.close()
logger.info(f'从数据源：{conf.source_db_name}库中，读取表：{conf.source_barcode_data_table_name},'
            f'将数据写入到文件: {conf.barcode_orders_output_csv_file_path} + {conf.barcode_orders_output_csv_file_name} 文件中，写入数据 {csv_file_count} 条数据.....')
insert_sql = f"insert into {conf.metadata_barcode_table_name}(time_record,gather_line_count)" \
             f"values('{max_last_update_time}', {count})"

# 执行sql
if barcode_model_list:
    metadata_db_util.execute(insert_sql)

# 关闭全部数据库连接
metadata_db_util.close_conn()
source_db_util.close_conn()
target_db_util.close_conn()

logger.info('数据源数据处理完毕.......')
