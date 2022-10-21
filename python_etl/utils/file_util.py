import os
from config import project_config as conf


def get_dir_files_list(path,recursion=False):
    """
    获取某个路径下所有的文件和文件夹
    :param path: 路径
    :param recursion: 是否递归
    :return:
    """
    file_names_list = os.listdir(path)

    # 定义一个空列表，存储文件的名字
    all_file_names = []
    for file_name in file_names_list:
        file_path = path+'/'+file_name
        # 判断是否是文件夹
        if os.path.isdir(file_path):
            # 继续获取该目录下的所有文件和文件夹
            if recursion:
                name_list = get_dir_files_list(file_path)
                all_file_names += name_list

        else:
            all_file_names.append(file_path)

    return all_file_names


def get_processed_file(db_util,
                       db_name=conf.METADATA_DB_NAME,
                       tb_name=conf.METADATA_FILE_MONITOR_TABLE_NAME,
                       create_cols=conf.METADATA_FILE_MONITOR_TABLE_CREATE_COLS):

    """
    获取一下已经被处理过的文件,处理过的文件保存在数据库中
    :param db_util: MysqlUtil对象
    :param db_name: 数据库名
    :param tb_name: 表名
    :param create_cols: 字段名
    :return: 返回数据库中保存的已经处理过的文件
    """
    # 2.2 切换数据库
    db_util.select_db(conf.METADATA_DB_NAME)
    # 2.3 判断表是否存在
    db_util.check_table_exists_and_create(
        db_name=db_name,
        tb_name=tb_name,
        create_cols=create_cols
    )
    # 2.4 查询表中的数据
    result = db_util.query(f'select file_name from {tb_name}')
    processed_file_list = [res[0] for res in result]
    return processed_file_list


def get_need_process_file(all_file_path,processed_file_list):
    """
    获取需要处理的文件列表 对比所有文件和已经处理的文件  找到没有处理的文件
    :param all_file_path: 所有文件的路径
    :param processed_file_list: 已经处理过的文件
    :return:需要出列的文件列表
    """
    need_to_process_file_list = []
    for file_path in all_file_path:
        if file_path not in processed_file_list:
            need_to_process_file_list.append(file_path)

    return need_to_process_file_list



