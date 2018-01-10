#coding: gbk
import hashlib
import os
import time
import urllib.request
import re


#####例子 Sample
# \\172.16.0.17\product\2345explorer\v8.3\8.3.0.14145
###  名称                 包名                                     变量命名规则
#    官网包	      2345explorer_v8.3.0.14143.exe	                     official
#    积分包	      2345explorer_kUID.exe	                             integral
#    联盟定制包	  2345explorer_custom.exe	                         ucustom 
#    联盟命名包	  2345explorer_66666655555_v8.3.0.14143.exe	         uname
#    手动升级包	  2345explorer_v8.3.0.14143.up.exe	                 manualup
#    自动升级包	  2345explorer_v8.3.0.14143.auto.dat	             autoup
#    Q管渠定制包  2345explorer_custom_qqmgr.exe	                     ucustom 

## 1. 生成TRAC 版本页面
#   下面是例子
#  ||[[Image(wiki:icon:00.ico,32px,nolink)]]||2345加速浏览器(2345explorer_v8.3.0.14145 2016年11月11日09点33分上传)【内测版】||[http://172.16.0.17/product/2345explorer/v8.3/8.3.0.14145/2345explorer_v8.3.0.14145.exe 点击安装]||[//2345explorer/wiki/v8.3.0.14145 点击测试]||
#

## 2. 生成 测试页面中的票列表 跟版本 MD5，大小等
#  下面是例子
#
#     == 传票列表 ==
#     [[TicketQuery(test_version=~8.3.0.14145)]]
#     == 备注 ==
#     (无)
#     
#     == 安装包信息 ==
#     ||安装包类型||文件名||MD5||大小||
#     ||[http://172.16.0.17/product/2345explorer/v8.3/8.3.0.14145/2345explorer_v8.3.0.14145.exe 官网包 ]||2345explorer_v8.3.0.14145.exe||D182A6D2389059F538E89A21982C2161||53849312||
#     ||[http://172.16.0.17/product/2345explorer/v8.3/8.3.0.14145/2345explorer_kUID.exe 积分包 ]||2345explorer_kUID.exe||9E4400467F0ADBFEF22C7F87B9B4FB67||53854088||
#     ||[http://172.16.0.17/product/2345explorer/v8.3/8.3.0.14145/2345explorer_custom.exe 联盟定制包 ]||2345explorer_custom.exe||8E254DF7078EACF3EB0A2468408AEF0C||53832940||
#     ||[http://172.16.0.17/product/2345explorer/v8.3/8.3.0.14145/2345explorer_66666655555_v8.3.0.14145.exe 联盟命名包 ]||2345explorer_66666655555_v8.3.0.14145.exe||45DDB4EF973B225D8CFF5654589AB2F4||53847568||
#     ||[http://172.16.0.17/product/2345explorer/v8.3/8.3.0.14145/2345explorer_v8.3.0.14145.up.exe 手动升级包 ]||2345explorer_v8.3.0.14145.up.exe||893CC77600A73624B5DF28ED26744E42||53851080||
#     ||[http://172.16.0.17/product/2345explorer/v8.3/8.3.0.14145/2345explorer_v8.3.0.14145.auto.dat 自动升级包 ]||2345explorer_v8.3.0.14145.auto.dat||9762C1874B0B4DD4D4B4FE2D67A55BB9||54537409||



str_prodocut_dir = r'//172.16.0.17/product/2345explorer';
str_big_version = r'9.2';
# "发到项目群里的那句话"使用小版本号，一般大版本号等于小版本号
# 但是也会出现不相同的情况，例如: V9.1  和  v9.1.1
str_small_version = r'9.2';
str_completet_version = r'9.2.0.17068';
str_version_type = r'测试版';

str_root_dir = str_prodocut_dir + '/v' + str_big_version + '/'+ str_completet_version + '/';


str_package_official = str_root_dir + '2345explorer_v' +  str_completet_version + '.exe';
str_package_integral = str_root_dir + '2345explorer_kUID.exe';
str_package_integral_1 = str_root_dir + '2345explorer_k24.exe';
str_package_integral_2 = str_root_dir + '2345explorer_k25.exe';
str_package_integral_3 = str_root_dir + '2345explorer_k29.exe';
str_package_ucustom =  str_root_dir + '2345explorer_custom.exe';
str_package_ucustom_anonymous = str_root_dir + '2345explorer_custom_anonymous.exe';
str_package_ucustom_without_np = str_root_dir + '2345explorer_custom_without_npflash.exe';
str_package_ucustom_shopping_plugin = str_root_dir + '2345explorer_custom_bimai.exe'
str_package_uname = str_root_dir + '2345explorer_66666655555_v' +  str_completet_version + '.exe';
str_package_uname_silent = str_root_dir + '2345explorer_66666655555_silent_v' +  str_completet_version + '.exe';
str_package_uname_maysilent = str_root_dir + '2345explorer_66666655555_maysilent_v' +  str_completet_version + '.exe';
str_package_manualup = str_root_dir + '2345explorer_v' +  str_completet_version + '.up.exe';
str_package_manualup_pcsafe = str_root_dir + '2345explorer_v' +  str_completet_version + '.up.pcsafe.exe';
str_package_autoup = str_root_dir + '2345explorer_v' +  str_completet_version + '.auto.dat'; 
str_package_autoup_pcsafe = str_root_dir + '2345explorer_v' +  str_completet_version + '.auto.pcsafe.dat';
str_package_silentup = str_root_dir + '2345explorer_v' +  str_completet_version + '.up.dat';
str_package_7zsetup =  str_root_dir + '2345explorer_v' + str_completet_version + '_7z.7z';
str_package_qcustom =  str_root_dir + '2345explorer_custom_qqmgr.exe';

def GetFileSizeAndMd5(str_file_path) :
    all_data = open(str_file_path, 'rb').read();
    md5_cal = hashlib.md5()
    md5_cal.update(all_data);
    return (md5_cal.hexdigest().upper(), len(all_data));



def GetTracVersionHtml(str_package_official_path, str_version_type):
    stat_info = os.stat(str_package_official);
    local_modify_time = time.localtime(stat_info.st_mtime);
    trac_version_page_formate = \
'||[[Image(wiki:icon:00.ico,32px,nolink)]]||2345加速浏览器(2345explorer_v{0} {1}年{2:0>2}月{3:0>2}日{4:0>2}点{5:0>2}分上传)【{7}】||[http://172.16.0.17/product/2345explorer/v{6}/{0}/2345explorer_v{0}.exe 点击安装]||[//2345explorer/wiki/v{0} 点击测试]||\n'

    trac_version_page = '';
    trac_version_page = trac_version_page_formate.format(\
    str_completet_version,\
    local_modify_time.tm_year,\
    local_modify_time.tm_mon,\
    local_modify_time.tm_mday,\
    local_modify_time.tm_hour,\
    local_modify_time.tm_min,\
    str_big_version,\
    str_version_type);
    return trac_version_page;

def GetTestPageHtml(str_package_official,
                    str_package_integral = '',
                    str_package_integral_1 = '',
                    str_package_integral_2 = '',
                    str_package_integral_3 = '',
                    str_package_ucustom = '',
                    str_package_ucustom_anonymous = '',
                    str_package_ucustom_without_np = '',
                    str_package_ucustom_shopping_plugin='',
                    str_package_uname = '',
                    str_package_uname_silent = '',
                    str_package_uname_maysilent = '',
                    str_package_manualup = '',
                    str_package_manualup_pcsafe = '',
                    str_package_autoup = '',
                    str_package_autoup_pcsafe = '',
                    str_package_silentup = '',
                    str_package_7zsetup = '',
					str_package_qcustom = '') :
    trac_test_page = '';
    trac_test_page_formate2_text = '';

    #p0  变量 str_completet_version ， 比如 8.3.0.14145  
    trac_test_page_formate1 = '== 传票列表 ==\n[[TicketQuery(test_version=~{0})]]\n== 备注 ==\n(无)\n\n== 安装包信息 ==\n||安装包类型||文件名||MD5||大小||\n';
    trac_test_page += trac_test_page_formate1.format(str_completet_version);

    #p0  变量 str_completet_version ， 比如 8.3.0.14145
    #p1  变量 str_big_version ， 比如 8.3
    trac_test_page_formate2 = '||[http://172.16.0.17/product/2345explorer/v{1}/{0}/';
    trac_test_page_formate2_text = trac_test_page_formate2.format(str_completet_version, str_big_version);
  
    #p0  变量 str_completet_version ， 比如 8.3.0.14145
    #p1  官网包 MD5，大写字符
    #p2  官网包 大小， 按字节来
    if (os.path.exists(str_package_official)) :
        official_package_info = GetFileSizeAndMd5(str_package_official);
        trac_test_page_formate_official = trac_test_page_formate2_text + '2345explorer_v{0}.exe 官网包 ]||2345explorer_v{0}.exe||{1}||{2}||\n'
        trac_test_page += trac_test_page_formate_official.format(str_completet_version, official_package_info[0], official_package_info[1]);

    #p0  积分包 MD5，大写字符
    #p1  积分包 大小， 按字节来。
    if (os.path.exists(str_package_integral)) :
        integral_package_info = GetFileSizeAndMd5(str_package_integral);
        trac_test_page_formate_integral = trac_test_page_formate2_text + '2345explorer_kUID.exe 积分包 ]||2345explorer_kUID.exe||{0}||{1}||\n'
        trac_test_page += trac_test_page_formate_integral.format(integral_package_info[0], integral_package_info[1]);
        
    #p0  积分包1 MD5，大写字符
    #p1  积分包1 大小， 按字节来。
    if (os.path.exists(str_package_integral_1)) :
        integral_1_package_info = GetFileSizeAndMd5(str_package_integral_1);
        trac_test_page_formate_integral_1 = trac_test_page_formate2_text + '2345explorer_k24.exe 积分包1 ]||2345explorer_k24.exe||{0}||{1}||\n'
        trac_test_page += trac_test_page_formate_integral_1.format(integral_1_package_info[0], integral_1_package_info[1]);
        
    #p0  积分包2 MD5，大写字符
    #p1  积分包2 大小， 按字节来。
    if (os.path.exists(str_package_integral_2)) :
        integral_2_package_info = GetFileSizeAndMd5(str_package_integral_2);
        trac_test_page_formate_integral_2 = trac_test_page_formate2_text + '2345explorer_k25.exe 积分包2 ]||2345explorer_k25.exe||{0}||{1}||\n'
        trac_test_page += trac_test_page_formate_integral_2.format(integral_2_package_info[0], integral_2_package_info[1]);
        
    #p0  积分包_护航版 MD5，大写字符
    #p1  积分包_护航版 大小， 按字节来。
    if (os.path.exists(str_package_integral_3)) :
        integral_3_package_info = GetFileSizeAndMd5(str_package_integral_3);
        trac_test_page_formate_integral_3 = trac_test_page_formate2_text + '2345explorer_k29.exe 积分包_护航版 ]||2345explorer_k29.exe||{0}||{1}||\n'
        trac_test_page += trac_test_page_formate_integral_3.format(integral_3_package_info[0], integral_3_package_info[1]);

    #p0  联盟定制包 MD5，大写字符
    #p1  联盟定制包 大小， 按字节来。
    if (os.path.exists(str_package_ucustom)) :
        ucustom_package_info = GetFileSizeAndMd5(str_package_ucustom);
        trac_test_page_formate_ucustom = trac_test_page_formate2_text + '2345explorer_custom.exe 联盟定制包 ]||2345explorer_custom.exe||{0}||{1}||\n'
        trac_test_page += trac_test_page_formate_ucustom.format(ucustom_package_info[0], ucustom_package_info[1]);
        
    #p0  联盟定制包_匿名包 MD5，大写字符
    #p1  联盟定制包_匿名包 大小， 按字节来。
    if (os.path.exists(str_package_ucustom_anonymous)) :
        ucustom_anonymous_package_info = GetFileSizeAndMd5(str_package_ucustom_anonymous);
        trac_test_page_formate_ucustom_anonymous = trac_test_page_formate2_text + '2345explorer_custom_anonymous.exe 联盟定制包_匿名包 ]||2345explorer_custom_anonymous.exe||{0}||{1}||\n'
        trac_test_page += trac_test_page_formate_ucustom_anonymous.format(ucustom_anonymous_package_info[0], ucustom_anonymous_package_info[1]);
        
    #p0  联盟定制包_无NPFlash包 MD5，大写字符
    #p1  联盟定制包_无NPFlash包 大小， 按字节来。
    if (os.path.exists(str_package_ucustom_without_np)) :
        ucustom_without_np_package_info = GetFileSizeAndMd5(str_package_ucustom_without_np);
        trac_test_page_formate_ucustom_without_np = trac_test_page_formate2_text + '2345explorer_custom_without_npflash.exe 联盟定制包_无NPFlash包 ]||2345explorer_custom_without_npflash.exe||{0}||{1}||\n'
        trac_test_page += trac_test_page_formate_ucustom_without_np.format(ucustom_without_np_package_info[0], ucustom_without_np_package_info[1]);


    if (os.path.exists(str_package_ucustom_shopping_plugin)) :
        ucustom_shopping_plugin_package_info = GetFileSizeAndMd5(str_package_ucustom_shopping_plugin);
        trac_test_page_formate_ucustom_shopping_plugin = trac_test_page_formate2_text + '2345explorer_custom_bimai.exe 联盟定制包_必买插件包 ]||2345explorer_custom_bimai.exe||{0}||{1}||\n'
        trac_test_page += trac_test_page_formate_ucustom_shopping_plugin.format(ucustom_shopping_plugin_package_info[0], ucustom_shopping_plugin_package_info[1]);

    #p0  变量 str_completet_version ， 比如 8.3.0.14145
    #p1  联盟命名包 MD5，大写字符
    #p2  联盟命名包 大小， 按字节来
    if (os.path.exists(str_package_uname)) :
        uname_package_info = GetFileSizeAndMd5(str_package_uname);
        trac_test_page_formate_uname = '';
        if (os.path.exists(str_package_uname_silent) or os.path.exists(str_package_uname_maysilent)) :
            trac_test_page_formate_uname = trac_test_page_formate2_text + '2345explorer_66666655555_v{0}.exe 联盟命名包_标准包 ]||2345explorer_66666655555_v{0}.exe||{1}||{2}||\n'
        else :
            trac_test_page_formate_uname = trac_test_page_formate2_text + '2345explorer_66666655555_v{0}.exe 联盟命名包 ]||2345explorer_66666655555_v{0}.exe||{1}||{2}||\n'
        trac_test_page += trac_test_page_formate_uname.format(str_completet_version, uname_package_info[0], uname_package_info[1]);

    #p0  变量 str_completet_version ， 比如 8.3.0.14145
    #p1  联盟命名包_静默包 MD5，大写字符
    #p2  联盟命名包_静默包 大小， 按字节来
    if (os.path.exists(str_package_uname_silent)) :
        uname_silent_package_info = GetFileSizeAndMd5(str_package_uname_silent);
        trac_test_page_formate_uname_silent = trac_test_page_formate2_text + '2345explorer_66666655555_silent_v{0}.exe 联盟命名包_静默包 ]||2345explorer_66666655555_silent_v{0}.exe||{1}||{2}||\n'
        trac_test_page += trac_test_page_formate_uname_silent.format(str_completet_version, uname_silent_package_info[0], uname_silent_package_info[1]);

    #p0  变量 str_completet_version ， 比如 8.3.0.14145
    #p1  联盟命名包_可选静默包 MD5，大写字符
    #p2  联盟命名包_可选静默包 大小， 按字节来
    if (os.path.exists(str_package_uname_maysilent)) :
        uname_maysilent_package_info = GetFileSizeAndMd5(str_package_uname_maysilent);
        trac_test_page_formate_uname_maysilent = trac_test_page_formate2_text + '2345explorer_66666655555_maysilent_v{0}.exe 联盟命名包_可选静默包 ]||2345explorer_66666655555_maysilent_v{0}.exe||{1}||{2}||\n'
        trac_test_page += trac_test_page_formate_uname_maysilent.format(str_completet_version, uname_maysilent_package_info[0], uname_maysilent_package_info[1]);

    #p0  变量 str_completet_version ， 比如 8.3.0.14145
    #p1  手动升级包 MD5，大写字符
    #p2  手动升级包 大小， 按字节来
    if (os.path.exists(str_package_manualup)) :
        manualup_package_info = GetFileSizeAndMd5(str_package_manualup);
        if (os.path.exists(str_package_manualup_pcsafe)) :
            trac_test_page_formate_manualup = trac_test_page_formate2_text + '2345explorer_v{0}.up.exe 手动升级包_标准包 ]||2345explorer_v{0}.up.exe||{1}||{2}||\n'
        else :
            trac_test_page_formate_manualup = trac_test_page_formate2_text + '2345explorer_v{0}.up.exe 手动升级包 ]||2345explorer_v{0}.up.exe||{1}||{2}||\n'
        trac_test_page += trac_test_page_formate_manualup.format(str_completet_version, manualup_package_info[0], manualup_package_info[1]);

    #p0  变量 str_completet_version ， 比如 8.3.0.14145
    #p1  手动升级推荐卫士包 MD5，大写字符
    #p2  手动升级推荐卫士包 大小， 按字节来
    if (os.path.exists(str_package_manualup_pcsafe)) :
        manualup_pcsafe_package_info = GetFileSizeAndMd5(str_package_manualup_pcsafe);
        trac_test_page_formate_manualup_pcsafe = trac_test_page_formate2_text + '2345explorer_v{0}.up.pcsafe.exe 手动升级包_推荐卫士包 ]||2345explorer_v{0}.up.pcsafe.exe||{1}||{2}||\n'
        trac_test_page += trac_test_page_formate_manualup_pcsafe.format(str_completet_version, manualup_pcsafe_package_info[0], manualup_pcsafe_package_info[1]);

    #p0  变量 str_completet_version ， 比如 8.3.0.14145
    #p1  自动升级包 MD5，大写字符
    #p2  自动升级包 大小， 按字节来
    if (os.path.exists(str_package_autoup)) :
        autoup_package_info = GetFileSizeAndMd5(str_package_autoup);
        if (os.path.exists(str_package_autoup_pcsafe)) :
            trac_test_page_formate_autoup = trac_test_page_formate2_text + '2345explorer_v{0}.auto.dat 自动升级包_标准包 ]||2345explorer_v{0}.auto.dat||{1}||{2}||\n'
        else :
            trac_test_page_formate_autoup = trac_test_page_formate2_text + '2345explorer_v{0}.auto.dat 自动升级包 ]||2345explorer_v{0}.auto.dat||{1}||{2}||\n'
        trac_test_page += trac_test_page_formate_autoup.format(str_completet_version, autoup_package_info[0], autoup_package_info[1]);

    #p0  变量 str_completet_version ， 比如 8.3.0.14145
    #p1  自动升级推荐卫士包 MD5，大写字符
    #p2  自动升级推荐卫士包 大小， 按字节来
    if (os.path.exists(str_package_autoup_pcsafe)) :
        autoup_pcsafe_package_info = GetFileSizeAndMd5(str_package_autoup_pcsafe);
        trac_test_page_formate_autoup_pcsafe = trac_test_page_formate2_text + '2345explorer_v{0}.auto.pcsafe.dat 自动升级包_推荐卫士包 ]||2345explorer_v{0}.auto.pcsafe.dat||{1}||{2}||\n'
        trac_test_page += trac_test_page_formate_autoup_pcsafe.format(str_completet_version, autoup_pcsafe_package_info[0], autoup_pcsafe_package_info[1]);
        
    #p0  变量 str_completet_version ， 比如 8.3.0.14145
    #p1  静默升级包 MD5，大写字符
    #p2  静默升级包 大小， 按字节来
    if (os.path.exists(str_package_silentup)) :
        silentup_package_info = GetFileSizeAndMd5(str_package_silentup);
        trac_test_page_formate_silentup = trac_test_page_formate2_text + '2345explorer_v{0}.up.dat 静默升级包 ]||2345explorer_v{0}.up.dat||{1}||{2}||\n'
        trac_test_page += trac_test_page_formate_silentup.format(str_completet_version, silentup_package_info[0], silentup_package_info[1]);
 
    #p0  变量 str_completet_version ， 比如 8.3.0.14145
    #p1  7z包 MD5，大写字符
    #p2  7z包 大小， 按字节来
    if (os.path.exists(str_package_7zsetup)) :
        setup7z_package_info = GetFileSizeAndMd5(str_package_7zsetup);
        trac_test_page_formate_setup7z = trac_test_page_formate2_text + '2345explorer_v{0}_7z.7z 7z安装包 ]||2345explorer_v{0}_7z.7z||{1}||{2}||\n'
        trac_test_page += trac_test_page_formate_setup7z.format(str_completet_version, setup7z_package_info[0], setup7z_package_info[1]);
 
    #p0  联盟定制包 MD5，大写字符
    #p1  联盟定制包 大小， 按字节来。
    if (os.path.exists(str_package_qcustom)) :
        qcustom_package_info = GetFileSizeAndMd5(str_package_qcustom);
        trac_test_page_formate_gcustom = trac_test_page_formate2_text + '2345explorer_custom_qqmgr.exe Q管渠道定制包 ]||2345explorer_custom_qqmgr.exe||{0}||{1}||\n'
        trac_test_page += trac_test_page_formate_gcustom.format(qcustom_package_info[0], qcustom_package_info[1]);

    # 增量升级包，一般一个版本只有一个
    for root, dirs, files in os.walk(str_root_dir):
        for file in files:
            if re.search('v\d+(\.\d+){3}_v\d+(\.\d+){3}', file) is not None:
                increment_package_info = GetFileSizeAndMd5(root + file)
                trac_test_page_formate_increment = trac_test_page_formate2_text + '{0} 增量升级包 ]||{0}||{1}||{2}||\n'
                trac_test_page += trac_test_page_formate_increment.format(file, increment_package_info[0], increment_package_info[1])
        break

    return trac_test_page;

def GetNoticeMessage(str_big_version, 
                     str_small_version,
                     str_completet_version,
                     str_version_type):
    #p0  变量 str_small_version  ， 比如 8.3
    #p1  变量 str_completet_version ， 比如 8.3.0.14145 
    #p3  变量 str_version_type ， 比如 内测版
    # 检测两个url是否存在
    url1 = 'http://172.16.0.17/product/2345explorer/v{0}/{1}/2345explorer_v{1}.exe'.format(str_big_version, str_completet_version);
    url2 = 'http://172.16.0.17:8080/2345explorer/wiki/v{0}'.format(str_completet_version);
    try:
        if urllib.request.urlopen(url1).code != 200:
            print(url1 + ' 不存在 ')
    except urllib.error.URLError as e:
        print(e.read().decode('utf-8'))

    notice_message_formate = 'v{0}{2}v{1}已放trac上，下载地址：\n' + url1 +'\n修改内容详见：' + url2 + '\n';
    notice_message = notice_message_formate.format(str_small_version, str_completet_version, str_version_type);
    return notice_message;

print(GetTracVersionHtml(str_package_official, str_version_type));


test_page = GetTestPageHtml(str_package_official,\
                      str_package_integral,\
                      str_package_integral_1,\
                      str_package_integral_2,\
                      str_package_integral_3,\
                      str_package_ucustom,\
                      str_package_ucustom_anonymous,\
                      str_package_ucustom_without_np,
                      str_package_ucustom_shopping_plugin,
                      str_package_uname,\
                      str_package_uname_silent,\
                      str_package_uname_maysilent,\
                      str_package_manualup,\
                      str_package_manualup_pcsafe,\
                      str_package_autoup,\
                      str_package_autoup_pcsafe,\
                      str_package_silentup,\
                      str_package_7zsetup,\
					  str_package_qcustom);
print(test_page)

print('******先修改产品版本号****************\n\n')

print(GetNoticeMessage(str_big_version, str_small_version, str_completet_version, str_version_type))

# 检测测试页中生成的安装包和原目录下的个数是否相等
for root, dirs, files in os.walk(str_root_dir):
    print(root + ' 下共有 ' + str(len(files)) + ' 个安装包, 测试页中生成 ' + str(test_page.count(root)) + ' 安装包')
    for file in files:
        if test_page.find(file) == -1:
          print(file + '  没有在测试页中生成')
    print('\n')