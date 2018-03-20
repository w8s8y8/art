import os
import shutil


for roots, dirs, files in os.walk('D:/迅雷下载/MetArt 2014'):
    for file_name in files:
        if os.path.splitext(file_name)[1] == '.zip' and not file_name == 'cover.zip':
            shutil.move(os.path.join(roots, file_name), '.')


for roots, dirs, files in os.walk('.'):
    for file_name in files:
        fn = os.path.splitext(file_name)
        if fn[1] == '.zip':
            fn = fn[0].split(' - ')
            p = fn[2].split()[0]
            d = fn[1].split()[0]
            m = fn[1][11::]
            fn = '%s_%s-%s.zip' % (d, p, m)
            os.rename(file_name, fn)
            
