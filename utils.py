import sys
import os

from pathlib import Path

def is_subpath(parent_path, child_path):
    parent = Path(parent_path).resolve()
    child = Path(child_path).resolve()
    
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def resource_path(relative_path):
    p = relative_path.split("/")
    if p[0] != ".":
        return relative_path
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

def plant_grid_to_zombie_grid(plant):
    return [plant[0] + 1, plant[1]]

def zombie_grid_to_plant_grid(zombie):
    return [zombie[0] - 1, zombie[1]]