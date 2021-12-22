# -*- coding: utf-8 -*-

import glob2
import zipfile
import os
import re
import shutil

relist = ('[0-9][0-9][0-9]-', '[0-9][0-9]-', 'board\.jpg', 'poster\.jpg',
          'warning-cover')

for zip_file_name in glob2.glob('*.zip'):
    dir_name = os.path.splitext(zip_file_name)[0]

    with zipfile.ZipFile(zip_file_name, 'r') as z:
        z.extractall(dir_name)

    os.chdir(dir_name)

    for file_name in glob2.glob('*.jpg'):
        for index, re_string in enumerate(relist):
            result = re.search(re_string, file_name)
            if result:
                if index == 0:
                    new = 'HA-' + result.group().replace('-', '') + '.jpg'
                    os.rename(file_name, new)
                elif index == 1:
                    new = 'HA-0' + result.group().replace('-', '') + '.jpg'
                    os.rename(file_name, new)
                elif index == 2:
                    os.rename(file_name, 'cover2.jpg')
                elif index == 3:
                    os.rename(file_name, 'cover.jpg')
                elif index == 4:
                    os.remove(file_name)
                break

    files = glob2.glob('*')
    with zipfile.ZipFile(zip_file_name, mode='w') as zf:
        for file_name in files:
            zf.write(file_name)

    os.chdir('..')

    os.rename(zip_file_name, 'OLD-' + zip_file_name)

    shutil.move(f'{dir_name}/{zip_file_name}', zip_file_name)

    shutil.rmtree(dir_name)
