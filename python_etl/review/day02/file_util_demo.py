import os


def get_dir_file_list(path,recursion=False):
    # 得到路径下所以文件和文件夹
    file_list = os.listdir(path)
    # 定义一个空列表用于存储文件
    all_file_list = []
    for file_name in file_list:
        # 获取文件路径
        file_path = path + '/' + file_name
        # 如果是文件夹，则递归
        if os.path.isdir(file_path):
            if recursion:
                new_file_list = get_dir_file_list(file_path)
                all_file_list += new_file_list
        else:
            all_file_list.append(file_path)

    return all_file_list


if __name__ == '__main__':
    print(get_dir_file_list('../../data',True))