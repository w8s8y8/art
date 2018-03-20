import os
import shutil


for roots, dirs, files in os.walk('D:/迅雷下载/MetArt 2013'):
    for file_name in files:
        if os.path.splitext(file_name)[1] == '.zip' and not file_name == 'cover.zip':
            shutil.move(os.path.join(roots, file_name), '.')


for roots, dirs, files in os.walk('.'):
    for file_name in files:
        fn = os.path.splitext(file_name)
        if fn[1] == '.zip':
            fn = fn[0].split(' - ')
            p = fn[1]
            d = fn[0][7:17:]
            m = fn[0][18::]
            fn = '%s_%s-%s.zip' % (d, p, m)
            print(fn)
            os.rename(file_name, fn)
