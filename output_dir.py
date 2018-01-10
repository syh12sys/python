import chardet
import os
import win32api
from os import path

intall_path = "C:/Program Files (x86)/2345Soft/2345Explorer"

def getFileProperties(fname):
    """
    Read all properties of the given file return them as a dictionary.
    """
    propNames = ('Comments', 'InternalName', 'ProductName',
        'CompanyName', 'LegalCopyright', 'ProductVersion',
        'FileDescription', 'LegalTrademarks', 'PrivateBuild',
        'FileVersion', 'OriginalFilename', 'SpecialBuild')

    props = {'FixedFileInfo': None, 'StringFileInfo': None, 'FileVersion': None}

    try:
        # backslash as parm returns dictionary of numeric info corresponding to VS_FIXEDFILEINFO struc
        fixedInfo = win32api.GetFileVersionInfo(fname, '\\')
        props['FixedFileInfo'] = fixedInfo
        props['FileVersion'] = "%d.%d.%d.%d" % (fixedInfo['FileVersionMS'] / 65536,
                fixedInfo['FileVersionMS'] % 65536, fixedInfo['FileVersionLS'] / 65536,
                fixedInfo['FileVersionLS'] % 65536)

        # \VarFileInfo\Translation returns list of available (language, codepage)
        # pairs that can be used to retreive string info. We are using only the first pair.
        lang, codepage = win32api.GetFileVersionInfo(fname, '\\VarFileInfo\\Translation')[0]

        # any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle
        # two are language/codepage pair returned from above

        strInfo = {}
        for propName in propNames:
            strInfoPath = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
            ## print str_info
            strInfo[propName] = win32api.GetFileVersionInfo(fname, strInfoPath)

        props['StringFileInfo'] = strInfo
    except:
        pass

    return props

def deep_traverse_dir(deep, dir, output_file):
  for i in os.listdir(dir):
    module = path.join(dir, i)
    extension = path.splitext(module)[1]
    if path.isfile(module) and (extension == '.exe' or extension == '.dll'):
      string_file_info = getFileProperties(module)['StringFileInfo']

      copyright = string_file_info['LegalCopyright']

      module = module[len(intall_path) + 1: len(module)]
      output_file.writelines(module)
      if copyright is not None:
        space_num = int((50 - len(module)) / 2)
        output_file.write(space_num * '  ' + copyright)
      output_file.writelines('\n')
    
    sub_dir = os.path.join(dir, i)
    if os.path.isdir(sub_dir) and os.path.exists(sub_dir):
      deep_traverse_dir(deep + 1, sub_dir, output_file)

def output_browser_config_to_file():
  browser_config_path = "browser_config.txt";

  output_file = open(browser_config_path, "w", encoding='utf-8')
  deep_traverse_dir(0, intall_path, output_file)
  output_file.close()


output_browser_config_to_file()
