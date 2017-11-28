import os


def deep_traverse_dir(deep, path, output_file):
  for i in os.listdir(path):
    output_file.writelines("|" * (deep + 1) + i + "\n")
    
    sub_dir = os.path.join(path, i)
    if os.path.isdir(sub_dir) and os.path.exists(sub_dir):
      deep_traverse_dir(deep + 1, sub_dir, output_file)

def output_browser_config_to_file():
  browser_config_path = "D:\\browser_config.txt";
  if os.path.exists(browser_config_path):
    os.remove(browser_config_path)

  output_file = open(browser_config_path, "a")
  output_file.write("intall dir:\n")
  deep_traverse_dir(0, "E:\\Program Files (x86)\\2345Soft\\2345Explorer", output_file)

  output_file.write("\n\nlcoal appadta dir:\n")
  deep_traverse_dir(0, "C:\\Users\sunys\\AppData\Local\\2345Explorer", output_file)
  
  output_file.close()


output_browser_config_to_file()


def breadth_traverse_dir(path):
  for parent, dirnames, filenames in os.walk(path):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for dirname in dirnames:                         #输出文件夹信息
          print("parent is:" + parent)
          print("dirname is:" + dirname)

        for filename in filenames:                        #输出文件信息
          print("parent is:" + parent)
          print("filename is:" + filename)

        print("the full name of the file is:" + os.path.join(parent, filename)) #输出文件路径信息
