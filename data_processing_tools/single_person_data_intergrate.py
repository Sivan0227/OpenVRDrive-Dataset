import json
import os
import subprocess

class SingleExpDataIntergrate():

    def __init__(self, person_dir, folder_dir):
        self.person_dir = person_dir
        self.folder_dir = os.path.join(folder_dir, os.path.basename(person_dir))
        self.create_folder(self.folder_dir)
        self.traj_dir = os.path.join(self.folder_dir, 'traj_data')
        self.create_folder(self.traj_dir)
        self.pic_dir = os.path.join(self.folder_dir, 'plot_reuslt')
        self.create_folder(self.pic_dir)
        self.vr_dir = os.path.join(self.folder_dir, 'vr_result')
        self.create_folder(self.vr_dir)


    # 使用subprocess方法启动不同的example.py命令，输入是json_file，log_file和输出文件夹，输出json名字

    def run_convert(self, json_file, log_file, pic_dir,output_dir,vr_dir):
        # 运行example.py
        subprocess.run(['python', 'convert.py',
                         '-f',  log_file,
                         '-t', json_file, 
                         '-o', pic_dir, 
                         '-j', output_dir,
                         '-v', vr_dir])

    def find_all_exp_data(self):
        print('person_dir', os.path.basename(self.person_dir))
        # 获取所有单人的实验数据
        all_exp = os.listdir(self.person_dir)
        # 忽略.DS_Store和data_all
        if '.DS_Store' in all_exp:
            all_exp.remove('.DS_Store')
        # if 'data_all' in all_exp:
        #     all_exp.remove('data_all')
        exp_data_dirs = [os.path.join(self.person_dir, exp_data_dir)
                         for exp_data_dir in all_exp]

        for exp_data_dir in exp_data_dirs:
            # 每一个单人实验数据
            # print('exp_data_dir', exp_data_dir)
            # 获取文件夹下的json地址和log地址
            # 忽略.DS_Store
            all_files = os.listdir(exp_data_dir)
            if '.DS_Store' in all_files:
                all_files.remove('.DS_Store')
            json_file = [os.path.join(exp_data_dir, json_file)
                         for json_file in all_files if json_file.endswith('.json')][0]
            log_file = [os.path.join(exp_data_dir, log_file)
                        for log_file in all_files if log_file.endswith('.txt')][0]

            if json_file and log_file:
                # 总json文件名是jsonfile的文件名
                json_name = os.path.basename(json_file)
                output_dir = os.path.join(self.traj_dir, json_name)
                # pic_dir 不要.json后缀
                pic_dir = os.path.join(self.pic_dir, os.path.splitext(json_name)[0])
                vr_dir = os.path.join(self.vr_dir,  os.path.splitext(json_name)[0])
                self.create_folder(pic_dir)
                # print('json_file',json_file)
                # print('log_file',log_file)
                # print('output_dir',output_dir)
                # print('pic_dir',pic_dir)
                # print('vr_dir',vr_dir)
                self.run_convert(json_file, log_file, pic_dir,output_dir,vr_dir)

    def create_folder(self, dir_path):
        # print('dir_path',dir_path)
        if not os.path.exists(os.path.join(os.getcwd(), dir_path)):
            os.mkdir(dir_path)

