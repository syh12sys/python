#coding: gbk
import hashlib
import os
import time
import urllib.request
import re


#####���� Sample
# \\172.16.0.17\product\2345explorer\v8.3\8.3.0.14145
###  ����                 ����                                     ������������
#    ������	      2345explorer_v8.3.0.14143.exe	                     official
#    ���ְ�	      2345explorer_kUID.exe	                             integral
#    ���˶��ư�	  2345explorer_custom.exe	                         ucustom 
#    ����������	  2345explorer_66666655555_v8.3.0.14143.exe	         uname
#    �ֶ�������	  2345explorer_v8.3.0.14143.up.exe	                 manualup
#    �Զ�������	  2345explorer_v8.3.0.14143.auto.dat	             autoup
#    Q�������ư�  2345explorer_custom_qqmgr.exe	                     ucustom 

## 1. ����TRAC �汾ҳ��
#   ����������
#  ||[[Image(wiki:icon:00.ico,32px,nolink)]]||2345���������(2345explorer_v8.3.0.14145 2016��11��11��09��33���ϴ�)���ڲ�桿||[http://172.16.0.17/product/2345explorer/v8.3/8.3.0.14145/2345explorer_v8.3.0.14145.exe �����װ]||[//2345explorer/wiki/v8.3.0.14145 �������]||
#

## 2. ���� ����ҳ���е�Ʊ�б� ���汾 MD5����С��
#  ����������
#
#     == ��Ʊ�б� ==
#     [[TicketQuery(test_version=~8.3.0.14145)]]
#     == ��ע ==
#     (��)
#     
#     == ��װ����Ϣ ==
#     ||��װ������||�ļ���||MD5||��С||
#     ||[http://172.16.0.17/product/2345explorer/v8.3/8.3.0.14145/2345explorer_v8.3.0.14145.exe ������ ]||2345explorer_v8.3.0.14145.exe||D182A6D2389059F538E89A21982C2161||53849312||
#     ||[http://172.16.0.17/product/2345explorer/v8.3/8.3.0.14145/2345explorer_kUID.exe ���ְ� ]||2345explorer_kUID.exe||9E4400467F0ADBFEF22C7F87B9B4FB67||53854088||
#     ||[http://172.16.0.17/product/2345explorer/v8.3/8.3.0.14145/2345explorer_custom.exe ���˶��ư� ]||2345explorer_custom.exe||8E254DF7078EACF3EB0A2468408AEF0C||53832940||
#     ||[http://172.16.0.17/product/2345explorer/v8.3/8.3.0.14145/2345explorer_66666655555_v8.3.0.14145.exe ���������� ]||2345explorer_66666655555_v8.3.0.14145.exe||45DDB4EF973B225D8CFF5654589AB2F4||53847568||
#     ||[http://172.16.0.17/product/2345explorer/v8.3/8.3.0.14145/2345explorer_v8.3.0.14145.up.exe �ֶ������� ]||2345explorer_v8.3.0.14145.up.exe||893CC77600A73624B5DF28ED26744E42||53851080||
#     ||[http://172.16.0.17/product/2345explorer/v8.3/8.3.0.14145/2345explorer_v8.3.0.14145.auto.dat �Զ������� ]||2345explorer_v8.3.0.14145.auto.dat||9762C1874B0B4DD4D4B4FE2D67A55BB9||54537409||



str_prodocut_dir = r'//172.16.0.17/product/2345explorer';
str_big_version = r'9.2';
# "������ĿȺ����Ǿ仰"ʹ��С�汾�ţ�һ���汾�ŵ���С�汾��
# ����Ҳ����ֲ���ͬ�����������: V9.1  ��  v9.1.1
str_small_version = r'9.2';
str_completet_version = r'9.2.0.17068';
str_version_type = r'���԰�';

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
'||[[Image(wiki:icon:00.ico,32px,nolink)]]||2345���������(2345explorer_v{0} {1}��{2:0>2}��{3:0>2}��{4:0>2}��{5:0>2}���ϴ�)��{7}��||[http://172.16.0.17/product/2345explorer/v{6}/{0}/2345explorer_v{0}.exe �����װ]||[//2345explorer/wiki/v{0} �������]||\n'

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

    #p0  ���� str_completet_version �� ���� 8.3.0.14145  
    trac_test_page_formate1 = '== ��Ʊ�б� ==\n[[TicketQuery(test_version=~{0})]]\n== ��ע ==\n(��)\n\n== ��װ����Ϣ ==\n||��װ������||�ļ���||MD5||��С||\n';
    trac_test_page += trac_test_page_formate1.format(str_completet_version);

    #p0  ���� str_completet_version �� ���� 8.3.0.14145
    #p1  ���� str_big_version �� ���� 8.3
    trac_test_page_formate2 = '||[http://172.16.0.17/product/2345explorer/v{1}/{0}/';
    trac_test_page_formate2_text = trac_test_page_formate2.format(str_completet_version, str_big_version);
  
    #p0  ���� str_completet_version �� ���� 8.3.0.14145
    #p1  ������ MD5����д�ַ�
    #p2  ������ ��С�� ���ֽ���
    if (os.path.exists(str_package_official)) :
        official_package_info = GetFileSizeAndMd5(str_package_official);
        trac_test_page_formate_official = trac_test_page_formate2_text + '2345explorer_v{0}.exe ������ ]||2345explorer_v{0}.exe||{1}||{2}||\n'
        trac_test_page += trac_test_page_formate_official.format(str_completet_version, official_package_info[0], official_package_info[1]);

    #p0  ���ְ� MD5����д�ַ�
    #p1  ���ְ� ��С�� ���ֽ�����
    if (os.path.exists(str_package_integral)) :
        integral_package_info = GetFileSizeAndMd5(str_package_integral);
        trac_test_page_formate_integral = trac_test_page_formate2_text + '2345explorer_kUID.exe ���ְ� ]||2345explorer_kUID.exe||{0}||{1}||\n'
        trac_test_page += trac_test_page_formate_integral.format(integral_package_info[0], integral_package_info[1]);
        
    #p0  ���ְ�1 MD5����д�ַ�
    #p1  ���ְ�1 ��С�� ���ֽ�����
    if (os.path.exists(str_package_integral_1)) :
        integral_1_package_info = GetFileSizeAndMd5(str_package_integral_1);
        trac_test_page_formate_integral_1 = trac_test_page_formate2_text + '2345explorer_k24.exe ���ְ�1 ]||2345explorer_k24.exe||{0}||{1}||\n'
        trac_test_page += trac_test_page_formate_integral_1.format(integral_1_package_info[0], integral_1_package_info[1]);
        
    #p0  ���ְ�2 MD5����д�ַ�
    #p1  ���ְ�2 ��С�� ���ֽ�����
    if (os.path.exists(str_package_integral_2)) :
        integral_2_package_info = GetFileSizeAndMd5(str_package_integral_2);
        trac_test_page_formate_integral_2 = trac_test_page_formate2_text + '2345explorer_k25.exe ���ְ�2 ]||2345explorer_k25.exe||{0}||{1}||\n'
        trac_test_page += trac_test_page_formate_integral_2.format(integral_2_package_info[0], integral_2_package_info[1]);
        
    #p0  ���ְ�_������ MD5����д�ַ�
    #p1  ���ְ�_������ ��С�� ���ֽ�����
    if (os.path.exists(str_package_integral_3)) :
        integral_3_package_info = GetFileSizeAndMd5(str_package_integral_3);
        trac_test_page_formate_integral_3 = trac_test_page_formate2_text + '2345explorer_k29.exe ���ְ�_������ ]||2345explorer_k29.exe||{0}||{1}||\n'
        trac_test_page += trac_test_page_formate_integral_3.format(integral_3_package_info[0], integral_3_package_info[1]);

    #p0  ���˶��ư� MD5����д�ַ�
    #p1  ���˶��ư� ��С�� ���ֽ�����
    if (os.path.exists(str_package_ucustom)) :
        ucustom_package_info = GetFileSizeAndMd5(str_package_ucustom);
        trac_test_page_formate_ucustom = trac_test_page_formate2_text + '2345explorer_custom.exe ���˶��ư� ]||2345explorer_custom.exe||{0}||{1}||\n'
        trac_test_page += trac_test_page_formate_ucustom.format(ucustom_package_info[0], ucustom_package_info[1]);
        
    #p0  ���˶��ư�_������ MD5����д�ַ�
    #p1  ���˶��ư�_������ ��С�� ���ֽ�����
    if (os.path.exists(str_package_ucustom_anonymous)) :
        ucustom_anonymous_package_info = GetFileSizeAndMd5(str_package_ucustom_anonymous);
        trac_test_page_formate_ucustom_anonymous = trac_test_page_formate2_text + '2345explorer_custom_anonymous.exe ���˶��ư�_������ ]||2345explorer_custom_anonymous.exe||{0}||{1}||\n'
        trac_test_page += trac_test_page_formate_ucustom_anonymous.format(ucustom_anonymous_package_info[0], ucustom_anonymous_package_info[1]);
        
    #p0  ���˶��ư�_��NPFlash�� MD5����д�ַ�
    #p1  ���˶��ư�_��NPFlash�� ��С�� ���ֽ�����
    if (os.path.exists(str_package_ucustom_without_np)) :
        ucustom_without_np_package_info = GetFileSizeAndMd5(str_package_ucustom_without_np);
        trac_test_page_formate_ucustom_without_np = trac_test_page_formate2_text + '2345explorer_custom_without_npflash.exe ���˶��ư�_��NPFlash�� ]||2345explorer_custom_without_npflash.exe||{0}||{1}||\n'
        trac_test_page += trac_test_page_formate_ucustom_without_np.format(ucustom_without_np_package_info[0], ucustom_without_np_package_info[1]);


    if (os.path.exists(str_package_ucustom_shopping_plugin)) :
        ucustom_shopping_plugin_package_info = GetFileSizeAndMd5(str_package_ucustom_shopping_plugin);
        trac_test_page_formate_ucustom_shopping_plugin = trac_test_page_formate2_text + '2345explorer_custom_bimai.exe ���˶��ư�_�������� ]||2345explorer_custom_bimai.exe||{0}||{1}||\n'
        trac_test_page += trac_test_page_formate_ucustom_shopping_plugin.format(ucustom_shopping_plugin_package_info[0], ucustom_shopping_plugin_package_info[1]);

    #p0  ���� str_completet_version �� ���� 8.3.0.14145
    #p1  ���������� MD5����д�ַ�
    #p2  ���������� ��С�� ���ֽ���
    if (os.path.exists(str_package_uname)) :
        uname_package_info = GetFileSizeAndMd5(str_package_uname);
        trac_test_page_formate_uname = '';
        if (os.path.exists(str_package_uname_silent) or os.path.exists(str_package_uname_maysilent)) :
            trac_test_page_formate_uname = trac_test_page_formate2_text + '2345explorer_66666655555_v{0}.exe ����������_��׼�� ]||2345explorer_66666655555_v{0}.exe||{1}||{2}||\n'
        else :
            trac_test_page_formate_uname = trac_test_page_formate2_text + '2345explorer_66666655555_v{0}.exe ���������� ]||2345explorer_66666655555_v{0}.exe||{1}||{2}||\n'
        trac_test_page += trac_test_page_formate_uname.format(str_completet_version, uname_package_info[0], uname_package_info[1]);

    #p0  ���� str_completet_version �� ���� 8.3.0.14145
    #p1  ����������_��Ĭ�� MD5����д�ַ�
    #p2  ����������_��Ĭ�� ��С�� ���ֽ���
    if (os.path.exists(str_package_uname_silent)) :
        uname_silent_package_info = GetFileSizeAndMd5(str_package_uname_silent);
        trac_test_page_formate_uname_silent = trac_test_page_formate2_text + '2345explorer_66666655555_silent_v{0}.exe ����������_��Ĭ�� ]||2345explorer_66666655555_silent_v{0}.exe||{1}||{2}||\n'
        trac_test_page += trac_test_page_formate_uname_silent.format(str_completet_version, uname_silent_package_info[0], uname_silent_package_info[1]);

    #p0  ���� str_completet_version �� ���� 8.3.0.14145
    #p1  ����������_��ѡ��Ĭ�� MD5����д�ַ�
    #p2  ����������_��ѡ��Ĭ�� ��С�� ���ֽ���
    if (os.path.exists(str_package_uname_maysilent)) :
        uname_maysilent_package_info = GetFileSizeAndMd5(str_package_uname_maysilent);
        trac_test_page_formate_uname_maysilent = trac_test_page_formate2_text + '2345explorer_66666655555_maysilent_v{0}.exe ����������_��ѡ��Ĭ�� ]||2345explorer_66666655555_maysilent_v{0}.exe||{1}||{2}||\n'
        trac_test_page += trac_test_page_formate_uname_maysilent.format(str_completet_version, uname_maysilent_package_info[0], uname_maysilent_package_info[1]);

    #p0  ���� str_completet_version �� ���� 8.3.0.14145
    #p1  �ֶ������� MD5����д�ַ�
    #p2  �ֶ������� ��С�� ���ֽ���
    if (os.path.exists(str_package_manualup)) :
        manualup_package_info = GetFileSizeAndMd5(str_package_manualup);
        if (os.path.exists(str_package_manualup_pcsafe)) :
            trac_test_page_formate_manualup = trac_test_page_formate2_text + '2345explorer_v{0}.up.exe �ֶ�������_��׼�� ]||2345explorer_v{0}.up.exe||{1}||{2}||\n'
        else :
            trac_test_page_formate_manualup = trac_test_page_formate2_text + '2345explorer_v{0}.up.exe �ֶ������� ]||2345explorer_v{0}.up.exe||{1}||{2}||\n'
        trac_test_page += trac_test_page_formate_manualup.format(str_completet_version, manualup_package_info[0], manualup_package_info[1]);

    #p0  ���� str_completet_version �� ���� 8.3.0.14145
    #p1  �ֶ������Ƽ���ʿ�� MD5����д�ַ�
    #p2  �ֶ������Ƽ���ʿ�� ��С�� ���ֽ���
    if (os.path.exists(str_package_manualup_pcsafe)) :
        manualup_pcsafe_package_info = GetFileSizeAndMd5(str_package_manualup_pcsafe);
        trac_test_page_formate_manualup_pcsafe = trac_test_page_formate2_text + '2345explorer_v{0}.up.pcsafe.exe �ֶ�������_�Ƽ���ʿ�� ]||2345explorer_v{0}.up.pcsafe.exe||{1}||{2}||\n'
        trac_test_page += trac_test_page_formate_manualup_pcsafe.format(str_completet_version, manualup_pcsafe_package_info[0], manualup_pcsafe_package_info[1]);

    #p0  ���� str_completet_version �� ���� 8.3.0.14145
    #p1  �Զ������� MD5����д�ַ�
    #p2  �Զ������� ��С�� ���ֽ���
    if (os.path.exists(str_package_autoup)) :
        autoup_package_info = GetFileSizeAndMd5(str_package_autoup);
        if (os.path.exists(str_package_autoup_pcsafe)) :
            trac_test_page_formate_autoup = trac_test_page_formate2_text + '2345explorer_v{0}.auto.dat �Զ�������_��׼�� ]||2345explorer_v{0}.auto.dat||{1}||{2}||\n'
        else :
            trac_test_page_formate_autoup = trac_test_page_formate2_text + '2345explorer_v{0}.auto.dat �Զ������� ]||2345explorer_v{0}.auto.dat||{1}||{2}||\n'
        trac_test_page += trac_test_page_formate_autoup.format(str_completet_version, autoup_package_info[0], autoup_package_info[1]);

    #p0  ���� str_completet_version �� ���� 8.3.0.14145
    #p1  �Զ������Ƽ���ʿ�� MD5����д�ַ�
    #p2  �Զ������Ƽ���ʿ�� ��С�� ���ֽ���
    if (os.path.exists(str_package_autoup_pcsafe)) :
        autoup_pcsafe_package_info = GetFileSizeAndMd5(str_package_autoup_pcsafe);
        trac_test_page_formate_autoup_pcsafe = trac_test_page_formate2_text + '2345explorer_v{0}.auto.pcsafe.dat �Զ�������_�Ƽ���ʿ�� ]||2345explorer_v{0}.auto.pcsafe.dat||{1}||{2}||\n'
        trac_test_page += trac_test_page_formate_autoup_pcsafe.format(str_completet_version, autoup_pcsafe_package_info[0], autoup_pcsafe_package_info[1]);
        
    #p0  ���� str_completet_version �� ���� 8.3.0.14145
    #p1  ��Ĭ������ MD5����д�ַ�
    #p2  ��Ĭ������ ��С�� ���ֽ���
    if (os.path.exists(str_package_silentup)) :
        silentup_package_info = GetFileSizeAndMd5(str_package_silentup);
        trac_test_page_formate_silentup = trac_test_page_formate2_text + '2345explorer_v{0}.up.dat ��Ĭ������ ]||2345explorer_v{0}.up.dat||{1}||{2}||\n'
        trac_test_page += trac_test_page_formate_silentup.format(str_completet_version, silentup_package_info[0], silentup_package_info[1]);
 
    #p0  ���� str_completet_version �� ���� 8.3.0.14145
    #p1  7z�� MD5����д�ַ�
    #p2  7z�� ��С�� ���ֽ���
    if (os.path.exists(str_package_7zsetup)) :
        setup7z_package_info = GetFileSizeAndMd5(str_package_7zsetup);
        trac_test_page_formate_setup7z = trac_test_page_formate2_text + '2345explorer_v{0}_7z.7z 7z��װ�� ]||2345explorer_v{0}_7z.7z||{1}||{2}||\n'
        trac_test_page += trac_test_page_formate_setup7z.format(str_completet_version, setup7z_package_info[0], setup7z_package_info[1]);
 
    #p0  ���˶��ư� MD5����д�ַ�
    #p1  ���˶��ư� ��С�� ���ֽ�����
    if (os.path.exists(str_package_qcustom)) :
        qcustom_package_info = GetFileSizeAndMd5(str_package_qcustom);
        trac_test_page_formate_gcustom = trac_test_page_formate2_text + '2345explorer_custom_qqmgr.exe Q���������ư� ]||2345explorer_custom_qqmgr.exe||{0}||{1}||\n'
        trac_test_page += trac_test_page_formate_gcustom.format(qcustom_package_info[0], qcustom_package_info[1]);

    # ������������һ��һ���汾ֻ��һ��
    for root, dirs, files in os.walk(str_root_dir):
        for file in files:
            if re.search('v\d+(\.\d+){3}_v\d+(\.\d+){3}', file) is not None:
                increment_package_info = GetFileSizeAndMd5(root + file)
                trac_test_page_formate_increment = trac_test_page_formate2_text + '{0} ���������� ]||{0}||{1}||{2}||\n'
                trac_test_page += trac_test_page_formate_increment.format(file, increment_package_info[0], increment_package_info[1])
        break

    return trac_test_page;

def GetNoticeMessage(str_big_version, 
                     str_small_version,
                     str_completet_version,
                     str_version_type):
    #p0  ���� str_small_version  �� ���� 8.3
    #p1  ���� str_completet_version �� ���� 8.3.0.14145 
    #p3  ���� str_version_type �� ���� �ڲ��
    # �������url�Ƿ����
    url1 = 'http://172.16.0.17/product/2345explorer/v{0}/{1}/2345explorer_v{1}.exe'.format(str_big_version, str_completet_version);
    url2 = 'http://172.16.0.17:8080/2345explorer/wiki/v{0}'.format(str_completet_version);
    try:
        if urllib.request.urlopen(url1).code != 200:
            print(url1 + ' ������ ')
    except urllib.error.URLError as e:
        print(e.read().decode('utf-8'))

    notice_message_formate = 'v{0}{2}v{1}�ѷ�trac�ϣ����ص�ַ��\n' + url1 +'\n�޸����������' + url2 + '\n';
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

print('******���޸Ĳ�Ʒ�汾��****************\n\n')

print(GetNoticeMessage(str_big_version, str_small_version, str_completet_version, str_version_type))

# ������ҳ�����ɵİ�װ����ԭĿ¼�µĸ����Ƿ����
for root, dirs, files in os.walk(str_root_dir):
    print(root + ' �¹��� ' + str(len(files)) + ' ����װ��, ����ҳ������ ' + str(test_page.count(root)) + ' ��װ��')
    for file in files:
        if test_page.find(file) == -1:
          print(file + '  û���ڲ���ҳ������')
    print('\n')