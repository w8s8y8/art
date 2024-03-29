# -*- coding: utf-8 -*-

import os
import shutil

def re2022(file_name):
    """
    [MetArt.com] 22-10-01 Ella Mira - Betrothed (x126) 4131x6196
    """
    vfs = file_name.split(' - ')
    return create('20' + vfs[0][13:21:], vfs[0][22::], vfs[1].split(' (')[0])


def re2020(file_name):
    """
    [metart.com] - 2020.05.01 - Alice Shea - Island Vibe (x119) 4912x7360
    """
    vfs = file_name.split(' - ')
    return create(vfs[1][0:10:].replace('.', '-'), vfs[2], vfs[3].split(' (')[0])


def re2014(file_name):
    """
    [met-art] - 2014-01-01 irina j - ceoil (x146) 3744x5616
    """
    vfs = file_name.split(' - ')
    return create(vfs[1][0:10:], vfs[1][11::], vfs[2].split(' (')[0])


def re2015(file_name):
    """
    [met-art] - 2015-01-01 - anna lee - melinsi (x113) 3840x5760
    """
    vfs = file_name.split(' - ')
    return create(vfs[1], vfs[2], vfs[3].split(' (')[0])


def create(date, model, collection):
    if 'presenting' in collection.lower():
        collection = 'presenting'
    return f'{date}_{collection}-{model}.zip'


if __name__ == '__main__':
    for file_name in os.listdir('.'):
        names = os.path.splitext(file_name)
        if names[1] == '.zip':
            new_file_name = re2022(names[0])
            print(new_file_name)
            shutil.move(file_name, new_file_name)
