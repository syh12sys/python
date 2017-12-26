import gzip


def ungzip(data):
    try:
        print('正在解压……')
        data = gzip.decompress(data)
        print('解压完毕！')
    except:
        print('未经压缩，无需解压')
    return data
