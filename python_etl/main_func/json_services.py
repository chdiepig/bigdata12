# 这个文件专门用于处理json订单数据的业务逻辑代码
from utils.file_util import get_dir_files_list, get_need_process_file, get_processed_file
from utils.logging_util import init_logger
from utils.mysql_util import MysqlUtil
from models.retail_orders_model import OrdersModel, OrdersDetailModel
from config import project_config as conf

# 创建logger对象
logger = init_logger()
logger.info('json订单处理，程序开始执行.........')

# 1.获取data目录下所有文件的路径
all_file_path = get_dir_files_list('../data')
logger.info(f'获取到文件有{all_file_path}')

# 2.获取一下已经被处理过的文件,处理过的文件保存在元数据库中
# 2.1 创建数据库连接
metadata_db_util = MysqlUtil()

processed_file_list = get_processed_file(db_util=metadata_db_util)
logger.info(f"获取到的以及被处理的文件有:{processed_file_list}")

# 3.获取需要处理的文件
need_process_file_list = get_need_process_file(all_file_path, processed_file_list)
logger.info(f"获取到的需要处理的文件有:{need_process_file_list}")

# 创建一个新的数据库连接，目标数据库
target_db_util = MysqlUtil(
    host=conf.TARGET_HOST,
    port=conf.TARGET_PORT,
    user=conf.TARGET_USER,
    pwd=conf.TARGET_PASSWORD
)

# 切换数据库
target_db_util.select_db(conf.TARGET_DB_NAME)
# 判断表是否存在
target_db_util.check_table_exists_and_create(
    conf.TARGET_DB_NAME,
    conf.TARGET_ORDERS_TABLE_NAME,
    conf.TARGET_ORDERS_TABLE_CREATE_COLS
)
target_db_util.check_table_exists_and_create(
    conf.TARGET_DB_NAME,
    conf.TARGET_ORDERS_DETAIL_TABLE_NAME,
    conf.TARGET_ORDERS_DETAIL_TABLE_CREATE_COLS
)

# 定义一个字典，存放每个文件对应的行数
file_line_dict = {}

# 4. 开始处理文件
for file_name in need_process_file_list:

    # 定义两个列表，分别存放订单基本信息模型类对象，和详情信息模型类对象
    orders_model_list = []
    orders_detail_model_list = []

    # 定义一个变量记录文件有多少行数据
    current_file_line_number = 0
    # 打开文件 读取数据
    for line in open(file_name, 'r', encoding='utf-8'):
        # line 就是文件中每一行数据,去掉末尾的\n
        line_data = line.strip()
        # 需要将每一行数据写入到csv 和 mysql 表中
        # 将数据构造成模型类对象 一条数据，订单基本信息，商品信息
        orders_model = OrdersModel(line_data)
        orders_detail_model = OrdersDetailModel(line_data)
        # 将对象添加到列表
        orders_model_list.append(orders_model)
        orders_detail_model_list.append(orders_detail_model)
        # 当前文件行数+1
        current_file_line_number += 1

    # 开始将数据写到csv文件中
    # 创建订单文件对象
    order_csv_file = open(
        conf.retail_output_csv_root_path + conf.retail_orders_output_csv_file_name,
        'w',
        encoding='utf-8-sig'
    )
    order_detail_csv_file = open(
        conf.retail_output_csv_root_path + conf.retail_orders_detail_output_csv_file_name,
        'w',
        encoding='utf-8-sig'
    )

    # 遍历订单模型对象列表，获取每一个订单模型类对象，调用to_csv方法
    for order_model in orders_model_list:
        # 将数据写入文件
        order_csv_file.write(order_model.to_csv() + '\n')

    for order_detail_model in orders_detail_model_list:
        order_detail_csv_file.write(order_detail_model.to_csv())

    # 关闭文件对象
    order_csv_file.close()
    order_detail_csv_file.close()
    logger.info(f"完成了CSV备份文件的写出，写出到了：{conf.retail_output_csv_root_path}")

    # 开始将数据写入mysql表中
    # 需要将模型对象转化为sql语句
    for order_model in orders_model_list:
        insert_sql = order_model.generate_insert_sql()
        target_db_util.execute_without_autocommit(insert_sql)

    for order_detail_model in orders_detail_model_list:
        insert_sql = order_detail_model.generate_insert_sql()
        target_db_util.execute_without_autocommit(insert_sql)

    # 将当前文件行数存放在字典中
    file_line_dict[file_name] = current_file_line_number
    logger.info("json订单数据写入到mysql完成")

# 手动提交 :如果使用execute 没插入一条数据都要提交一次，执行效率太慢
target_db_util.conn.commit()

# 将处理过的文件写入到元数据表中
for file_name,line_num in file_line_dict.items():
    insert_sql =f"insert into {conf.METADATA_FILE_MONITOR_TABLE_NAME}(file_name,process_lines)" \
                f"values ('{file_name}','{line_num}')"
    metadata_db_util.execute(insert_sql)

# 将所有的数据库连接关闭
metadata_db_util.close_conn()
target_db_util.close_conn()
logger.info("读取JSON数据向MySQL插入以及写出CSV备份，程序执行完成......")

