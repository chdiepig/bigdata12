with open('cat.txt','r',encoding='utf-8')as f:
    while True:
        content = f.readline()
    # print(content)
        if content:
            print(content)
        else:
            break

