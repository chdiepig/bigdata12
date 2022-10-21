# with open('test_demo.py','r',encoding='utf-8')as f:
#     content_list = f.readlines()
#     # 得到每一行数据
#     for content in content_list:
#         print(content)

for data in open('test_demo.py','r',encoding='utf-8'):
    print(data.strip())