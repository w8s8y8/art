import os
import re
import shutil

# 2021-05-03 Monika May - A view to a thrill

if __name__ == '__main__':
    for file_name in os.listdir('.'):
        if os.path.isdir(file_name) and file_name != '.git':
            date = file_name[0:10]
            dir_name = file_name[11:]
            dir_name = dir_name.split(' - ')
            name = dir_name[0].upper()
            nset = dir_name[1].upper()
            name = f'MPLS_{date}_{nset}-{name}'
            shutil.make_archive(name, 'zip', file_name)
