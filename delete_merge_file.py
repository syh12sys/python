import os
import sys
import xml.etree.ElementTree as ET

def  GetCommitFiles(xml_path,  version):
  path_list = []
  xml_tree = ET.parse(xml_path)
  root = xml_tree.getroot()

  for log_element in root.findall("logentry"):
        if log_element.get("revision") == version:
            paths_element = log_element.find("paths")
            for path_element in paths_element.findall("path"):
                if path_element.get("action") == "A":
                    text = path_element.text
                    path_list.append(text[text.index("src") : len(text)])

    return path_list

#print(len(GetXMLPath("D:/show_log.xml")))


path_list = GetCommitFiles("D:/show_log.xml", "15019")
print(len(path_list))
#print("src/native_client/toolchain/win_x86/pnacl_newlib/x86_64_bc-nacl/lib/crt0.o" in path_list)
# for i in path_list:
#   print(i)

# count = 0;
# for parent, dirnames, filenames in os.walk("H:\\v56_87\src\\native_client"):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
#   for filename in filenames:                        #输出文件信息
#     total_path = str(os.path.join(parent, filename))
#     src_path = total_path[total_path.index("src") : len(total_path)]
#     #if src_path == "src/native_client/toolchain/win_x86/pnacl_newlib/x86_64_bc-nacl/lib/crt0.o":
#     if src_path.replace("\\", "/") in path_list:
#       count = count + 1
#       os.remove(total_path)

# print(count)

