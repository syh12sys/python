import xml.etree.ElementTree as ET
import os

svn_exe_path = r'"E:/Program Files/SVN/bin/svn.exe"'

explore_log_path = 'D:/show_log.xml'
explore_backup_log_path = 'D:/backup_show_log.xml'
explore_source_dir = 'H:/brower/code/V68_45/'
explore_dest_dir = 'D:/V68_45/'

dllplugin_log_path = 'D:/dllplugin_show_log.xml'
dllplugin_backup_log_path = 'D:/dllplugin_backup_show_log.xml'
dllplugin_source_dir = 'F:/dllplugin/'
dllplugin_dest_dir = 'H:/dllplugin/'

# 仓库路径
repositories_dir = 'D:/Repositories/chrome/'

# 获取从小到大排列提交集
def get_version_list(log_xml):
    root = log_xml.getroot()
    version_list = []
    for log_element in root.findall('logentry'):
        version_list.append(int(log_element.get('revision')))
    version_list.sort()
    return version_list

def merge_and_commit(version, log_xml, source_dir, des_dir):
    root = log_xml.getroot()
    for log_element in root.findall('logentry'):
        if int(log_element.get('revision')) == version:
            print(version)
            if log_element.find('author') == None:
                continue

            author = log_element.find('author').text

            update_command = svn_exe_path + ' update ' + des_dir + ' --username sunys --password sunys  --force-interactive --no-auth-cache > D:/update.log'
            print(update_command)
            os.system(update_command)

            merge_command = svn_exe_path + ' merge -c ' + str(version) + ' ' + source_dir + ' ' + des_dir + ' > D:/merge.log'
            print(merge_command)
            os.system(merge_command)

            old_message =  ''
            msg_element = log_element.find('msg')
            if msg_element != None:
                old_message = msg_element.text
            if old_message == None:
                old_message = ''

            data_time = log_element.find('date').text
            new_message = old_message + '\n原提交号:' + str(version) + '\n原提交时间: ' + data_time + '\n原提交者: ' + author
            os.chdir(des_dir)
            output = open('commit_msg.txt', 'w')
            output.write(new_message)
            output.close()

            commit_command = svn_exe_path + ' commit -F commit_msg.txt --username sunys --password sunys --force-interactive --no-auth-cache > D:/commit.log'
            print(commit_command)
            os.system(commit_command)

def backup_explore():
    print('1')
    # 浏览器原工作副本更新到最新并获取log日志
    # os.system(svn_exe_path + ' update ' + explore_source_dir + ' --force-interactive > D:/update_log.txt')
    os.system(
        svn_exe_path + ' log svn://172.17.209.18/2345chrome/trunk/V68_45 -v --force-interactive --xml > ' + explore_log_path)
    explore_log_xml = ET.parse(explore_log_path)

    # 浏览器备份 工作副本更新到最新并获取日志
    #os.system(
    #    svn_exe_path + ' update ' + explore_dest_dir + ' --username sunys --password sunys --force-interactive --no-auth-cache > D:/update.log')
    #os.system(
    #    svn_exe_path + ' log http://WIN-JNFPP1DETKJ/svn/Chrome/trunk/V68_45 -v --username sunys --password sunys --force-interactive --no-auth-cache --xml > ' + explore_backup_log_path)
    #explore_backup_log_xml = ET.parse(explore_backup_log_path)
    #root = explore_backup_log_xml.getroot()
    # 第一个结点就是最后一次提交
    #last_msg = ''
    #for log_element in root.findall('logentry'):
    #    last_msg = log_element.find('msg').text
    #    break
    #print(last_msg)
    #last_backup_vesion = 0
    explore_versions = get_version_list(explore_log_xml)
    #for version in explore_versions:
    #    if '原提交号:' + str(version) in last_msg:
    #        last_backup_vesion = int(version)
    #        break

    last_backup_vesion = 17588
    print(last_backup_vesion)

    for version in explore_versions:
        if version > last_backup_vesion:
            merge_and_commit(version, explore_log_xml, explore_source_dir, explore_dest_dir)

def GetCommitNames(log_xml):
    names = set()
    root = log_xml.getroot()
    for log_element in root.findall('logentry'):
        if log_element:
            names.add(log_element.find('author').text)
    return names

backup_explore()

def backup_dllplugin():
    # dllplugin 工作副本更新到最新并获取日志
    os.system(svn_exe_path + ' update ' + dllplugin_source_dir + ' --force-interactive > D:/update_log.txt')
    os.system(
        svn_exe_path + ' log svn://172.17.209.18/2345chrome/trunk/dllplugin -v --force-interactive --xml > ' + dllplugin_log_path)
    dllplugin_log_xml = ET.parse(dllplugin_log_path)

    print(GetCommitNames(dllplugin_log_xml))

    dllplugin_versions = get_version_list(dllplugin_log_xml)
    print(dllplugin_versions)
    for version in dllplugin_versions:
        if version > 8320:
            merge_and_commit(version, dllplugin_log_xml, dllplugin_source_dir, dllplugin_dest_dir)

# backup_dllplugin()

def dump_files():
    os.system(
        svn_exe_path + ' log' + explore_backup_log_path + ' -v --username sunys --password sunys --force-interactive --no-auth-cache --xml > ' + explore_backup_log_path)
    explore_backup_log_xml = ET.parse(explore_backup_log_path)
    versions = get_version_list(explore_backup_log_xml)

    for version in versions:
        if version == 5:
            os.system('svnadmin dump ' + repositories_dir + '-r 1:5 --incremental > F:/document/1_5_v56_87' )

# dump_files()
