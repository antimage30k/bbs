import time


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 把 unix time 转换为普通格式
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)
