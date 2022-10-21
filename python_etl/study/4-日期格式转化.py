from datetime import datetime
import time

# 1. python获取当前日期时间
today_datetime = datetime.now()   # 2022-07-17 17:47:33.208787
# print(today_datetime, type(today_datetime))

# 2. 将datetime类型转换为字符串类型
today_str = today_datetime.strftime("%Y-%m-%d %H:%M:%S")
# print(today_str, type(today_str))

# 3. 将日期字符串转换为datetime类型
today_new_datetime = datetime.strptime(today_str, "%Y-%m-%d %H:%M:%S")
# print(today_new_datetime, type(today_new_datetime))

# 获取时间戳
ts = time.time()
print(ts)

# 时间戳转化为datetime类型
ts_datetime = datetime.fromtimestamp(ts)
print(ts_datetime,type(ts_datetime))

# datetime类型转化为时间戳
ts = ts_datetime.timestamp()
print(ts)
"""
# Y 年   H 小时
# m 月   M 分钟
# d 日   S 秒
"""
