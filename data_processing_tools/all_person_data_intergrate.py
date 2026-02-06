import json
import os
import subprocess
from single_person_data_intergrate import SingleExpDataIntergrate

def find_all_person_data(data_dir):

    # 找到目录下所有的以数字命名的文件夹
    person_dirs = [os.path.join(data_dir, person_dir) for person_dir in os.listdir(
        data_dir) if person_dir.isdigit()]
    return person_dirs

def create_folder(dir_path):
    # print('dir_path',dir_path)
    if not os.path.exists(os.path.join(os.getcwd(), dir_path)):
        os.mkdir(dir_path)

def run():
    # 当前目录
    now_dir = os.path.dirname(os.path.abspath(__file__))
    # 上级目录
    uplevel_dir = os.path.dirname(now_dir)
    data_dir = os.path.join(uplevel_dir, 'lc_exp_data')
    out_put_dir = os.path.join(uplevel_dir, 'lc_data_all')
    create_folder(out_put_dir)
    person_dirs = find_all_person_data(data_dir)
    exp_intergrators = [SingleExpDataIntergrate(
        person_dir, out_put_dir) for person_dir in person_dirs]
    # # 打印33对应的索引
    # for idx,person_dir in enumerate(person_dirs):
    #      if os.path.basename(person_dir)=='33':
    #         print(idx)
    # print(person_dirs)
    for idx,exp_intergrator in enumerate(exp_intergrators):
        print('idx',idx)
        exp_intergrator.find_all_exp_data()
    

if __name__ == '__main__':
    run()
