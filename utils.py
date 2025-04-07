import sys
import os

def resource_path(relative_path):
    p = relative_path.split("/")
    path = "."
    for i in p:
        path = os.path.join(path, i)
    """ 获取打包后资源的绝对路径 """
    if hasattr(sys, '_MEIPASS'):
        # 打包后的运行环境
        base_path = sys._MEIPASS
    else:
        # 普通开发环境
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, path)