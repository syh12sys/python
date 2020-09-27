import os
import sys
import re

dest_code_dir = r'D:\svn\CycloneAutomation\src\Util\Xml'

# 格式化wstring和string
def FormatStd(file_content):
    pattern = r' string'
    formatted_file_content = re.sub(pattern, r' std::string', file_content, sys.maxsize, re.M)

    pattern = r'\tstring'
    formatted_file_content = re.sub(pattern, r'\tstd::string', formatted_file_content, sys.maxsize, re.M)

    pattern = r'\(string'
    formatted_file_content = re.sub(pattern, r'(std::string', formatted_file_content, sys.maxsize, re.M)

    pattern = r'<string'
    formatted_file_content = re.sub(pattern, r'<std::string', formatted_file_content, sys.maxsize, re.M)

    pattern = r' wstring'
    formatted_file_content = re.sub(pattern, r' std::wstring', formatted_file_content, sys.maxsize, re.M)

    pattern = r'\twstring'
    formatted_file_content = re.sub(pattern, r'\tstd::wstring', formatted_file_content, sys.maxsize, re.M)

    pattern = r'\(wstring'
    formatted_file_content = re.sub(pattern, r'(std::wstring', formatted_file_content, sys.maxsize, re.M)

    pattern = r'<wstring'
    formatted_file_content = re.sub(pattern, r'<std::wstring', formatted_file_content, sys.maxsize, re.M)

    return formatted_file_content


# 格式化引用
def FormatReference(file_content):
    pattern = r' &(?!&)'
    formatted_file_content = re.sub(pattern, r'& ', file_content, sys.maxsize, re.M)

    pattern = r' \*(?!/)'
    formatted_file_content = re.sub(pattern, r'* ', formatted_file_content, sys.maxsize, re.M)
    return formatted_file_content

# foramt if
def FormatIf(file_content):
    # if
    pattern = r'(if[^n].*\n)(.*;\n{1})'
    formatted_file_content = re.sub(pattern, r'\1{\n\2}\n', file_content, sys.maxsize, re.M)

    # else
    pattern = r'(else.*\n)(.*;\n{1})'
    formatted_file_content = re.sub(pattern, r'\1{\n\2}\n', formatted_file_content, sys.maxsize, re.M)
    return formatted_file_content

def FormatCode(file_path):
    ext = os.path.splitext(file_path)
    if ext[1] != '.cpp' and ext[1] != '.h':
        return
    print(file_path)

    file = open(file_path, 'r+')
    file_content = file.read()

    file_content = FormatStd(file_content)
    file_content = FormatReference(file_content)
    file_content = FormatIf(file_content)

    file.seek(0, 0)
    file.write(file_content)
    file.close()

def TraverseDir(dir):
    dirs = os.listdir(dir)
    for iterator in dirs:
        if os.path.isdir(iterator):
            TraverseDir(iterator)
        else:
            FormatCode(os.path.join(dir, iterator))

TraverseDir(dest_code_dir)

