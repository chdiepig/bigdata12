from datetime import datetime


def ts13_to_date_str(ts, fmt='%Y-%m-%d %H-%M-%S'):
    """
    13位时间戳，精确到毫秒
    :param ts:时间戳
    :param fmt:转化后的格式
    :return:转化后的时间
    """
    ts = ts/1000
    # 将时间戳转化为datetime类型
    ts_datetime = datetime.fromtimestamp(ts)
    # 将datetime类型转化为字符串
    return ts_datetime.strftime(fmt)
