

def check_null(data):
    """
    检查传入的数据是否是无意义的数据 None
    :param data:要被检查的数据
    :return:None->True
    """
    # 如果数据是空值,则返回true
    if not data:
        return True
    data = str(data).lower()
    if data == "" or data == "none" or data == "undefined" or data == "null":
        return True
    return False


def check_str_null_and_transform_to_sql_null(data):
    """
    判断传入的数据是否有意义，没有意义则转化为sql中的null
    :param data:判断或者转化的数据
    :return:转化后的数据
    """
    if check_null(data):
        return "NULL"
    else:
        return f"'{data}'"


def check_number_null_and_transform_to_sql_null(data):
    """
    检查数字，如果是空内容，就返回SQL意义上的NULL（插入的SQL语句中会插入真正的NULL）
    如果是有意义的内容，返回 内容本身
    :param data:
    :return:
    """
    if data and not check_null(str(data)):
        # and 两个是True才能进来if
        # data如果不是None，而是有内容，那么就能进来
        # 同时not check_null(str(data))是True 才能进来
        # 也就是check_null(str(data))是 False， 表示有意义
        # 总结：必须满足data有内容（不是None）同时满足data的内容有意义才会进入if
        # 说明是正常数据
        return data
    else:
        # 这个数据有问题
        return "NULL"       # return SQL意义上的NULL


def clean_str(data):
    if check_null(data):
        # 如果是无意义的内容，比如字符串None、字符串Null 等，这些不影响插入操作不理会
        return data

    # 如果是有意义的内容，需要处理，比如： 可口可乐\    内容中自带斜杠导致程序出错
    # 乱七八糟的符号，我们要处理掉
    data = data.replace("'", "")
    data = data.replace('"', "")
    data = data.replace("\\", "")
    data = data.replace(";", "")
    data = data.replace(",", "")
    data = data.replace("@", "")

    return data



