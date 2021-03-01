# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 09:24:07 2018

@author: Administrator
"""

import os
import shutil
import re

if __name__ == '__main__':
    for file_name in os.listdir('.'):
        names = os.path.splitext(file_name)
        if names[1] == '.zip':
            if re.search('^OLD_X.*', names[0]):
                name = names[0].replace('OLD_X_', '') + '.zip'
                shutil.move(file_name, name)