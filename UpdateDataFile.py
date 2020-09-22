import os
import re

# 库文件路径
data_path = 'D:/work/RhinoProtect/Share/data'

# dest_path不存在则checkout，否则执行update操作
def UpdateDataFile(data_version):
    update_command = ''
    if os.path.exists(data_path):
        update_command = 'TortoiseProc.exe /command:checkout /url:"svn://172.17.1.13/coral/2345Safe/需求文档/安全卫士打包文件/运营/平台库文件/{0}" /path:"{1}" /closeonend:2'.format(data_version, data_path);
    else:
        update_command = 'TortoiseProc.exe /command:update /path:"{0}" /closeonend:2'.format(data_path);
    print(update_command)
    os.system(update_command)

def GetCurrentVersion():
    #读取文件
    output = open('D:/work/RhinoProtect/Share/Version/RCProductVersion.h.tmpl', 'r')
    file_data = output.read(1024)
    output.close()

    # 尝试了很久，用这种方式才能找到所有符合正则表达式的项
    pattern = re.compile(r'\s{3,}[0-9]\n')
    matchObj = pattern.findall(file_data, re.M|re.S)
    print(matchObj[0].strip(' \n')+'.'+ matchObj[1].strip(' \n'))
    return  matchObj[0].strip(' \n') + '.'+ matchObj[1].strip(' \n')


UpdateDataFile(GetCurrentVersion())
