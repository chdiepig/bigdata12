from datetime import datetime
import time


date_time = datetime.now()
print(date_time, type(date_time))
# 将datetime转化为string
str_date_time = date_time.strftime('%Y-%m-%d %H:%M:%S')
print(str_date_time, type(str_date_time))

# 将日期的字符串格式转化为datetime
new_date_time = datetime.strptime(str_date_time, '%Y-%m-%d %H:%M:%S')
print(new_date_time, type(new_date_time))
print("="*60)
# 时间戳
ts = time.time()
print(ts)

# 时间戳转化为datetime,利用datetime.fromtimestamp()
ts_datetime = datetime.fromtimestamp(ts)
print(ts_datetime, type(ts_datetime))

# datetime转化为时间戳,利用timestamp()函数
new_ts = ts_datetime.timestamp()
print(new_ts, type(new_ts))
