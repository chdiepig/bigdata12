# 处理日志文件中的数据
from utils.file_util import get_dir_files_list, get_processed_file, get_need_process_file
from utils.logging_util import init_logger
from utils.mysql_util import MysqlUtil
from config import project_config as conf
from models.backend_logs_model import BackendLogsModel

logger = init_logger()

# 1. 获取指定目录下所有文件名字的目录
all_file_names = get_dir_files_list('../logs/backend_logs')
logger.info(f"获取到日志文件列表为:{all_file_names}")

# 2. 获取元数据库中已经处理过的日志文件
# 2.1 获取数据库连接对象
metadata_db_util = MysqlUtil()
processed_file_list = get_processed_file(
    metadata_db_util,
    conf.METADATA_DB_NAME,
    conf.metadata_backend_logs_tb_name,
    conf.metadata_backend_logs_tb_create_cols
)
logger.info(f"已经处理的文件有{processed_file_list}")

# 2.2 对比获取需要处理的日志文件列表
need_file_list = get_need_process_file(all_file_names, processed_file_list)
logger.info(f'需要被处理的文件有:{need_file_list}')

# 创建一个字典,保存每个文件有多少条数据
backend_line_dict = {}

# 将日志数据写到一个csv文件即可
log_csv_file = open(
    conf.log_output_csv_root_path + conf.log_output_csv_file_name,
    'w',
    encoding='utf-8-sig')

# 获取目标数据库连接对象
target_db_util = MysqlUtil(
    conf.TARGET_HOST,
    conf.TARGET_PORT,
    conf.TARGET_USER,
    conf.TARGET_PASSWORD
)
target_db_util.select_db(conf.TARGET_DB_NAME)
# 判断表是否存在
target_db_util.check_table_exists_and_create(
    conf.TARGET_DB_NAME,
    conf.target_log_table_name,
    conf.target_log_create_cols
)

# 2.3 遍历每一个文件
for file_name in need_file_list:
    # 创建一个空列表,  存储每一行的模型类对象
    backend_logs_list = []
    # 定义一个变量记录文件有多少行数据
    current_file_line_number = 0

    for line in open(file_name, 'r', encoding='utf-8'):
        line_data = line.strip()
        # 获取模型类对象，放入列表中
        model = BackendLogsModel(line_data)
        backend_logs_list.append(model)
        # 当前文件行数+1
        current_file_line_number += 1

    # 遍历每一个模型类对象
    for model in backend_logs_list:
        # 将数据写入到文件中
        log_csv_file.write(model.to_csv() + "\n")

        # 将数据写入到mysql中
        insert_sql = model.generate_insert_sql()
        target_db_util.execute_without_autocommit(insert_sql)

    # 将当前文件行数存放在字典中
    backend_line_dict[file_name] = current_file_line_number
    logger.info("日志数据写入到mysql完成")

# 手动提交
target_db_util.conn.commit()

# 将处理过的日志文件记录到mysql元数据表当中
for file_name, line_num in backend_line_dict.items():
    insert_sql = f"insert into {conf.metadata_backend_logs_tb_name} (file_name,process_lines)" \
                 f"values ('{file_name}','{line_num}')"
    metadata_db_util.execute(insert_sql)
logger.info("已经处理的文件已经保存到数据库中.....")

# 关闭数据库连接和文件对象
log_csv_file.close()
metadata_db_util.close_conn()
target_db_util.close_conn()
logger.info("读取日志数据向MySQL插入以及写出CSV备份，程序执行完成......")
