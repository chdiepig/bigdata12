import os

# 获取指定路径(path)下的所有文件和文件夹，返回一个列表 os.listdir()
file_path = '../data'
file_list = os.listdir(file_path)
print(file_list)

# 判断是否是目录 os.path.isdir()
if os.path.isdir(file_path):
    print(f'{file_path}是一个目录')


