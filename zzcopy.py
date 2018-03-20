import os
import shutil

release = True

if __name__ == '__main__':
    dir_name = os.path.join(os.environ['USERPROFILE'], 'Downloads\\Compressed')
    for roots, dir_names, file_names in os.walk(dir_name):
        for file_name in file_names:
            if os.path.splitext(file_name)[1] == '.zip':
                shutil.move(os.path.join(dir_name, file_name), os.getcwd())
