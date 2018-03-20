import os
import shutil


#for roots, dirs, files in os.walk('E:/迅雷下载/[met-art] 2016'):
#    for file_name in files:
#        if os.path.splitext(file_name)[1] == '.zip' and not file_name == 'cover.zip':
#            shutil.move(os.path.join(roots, file_name), '.')


for roots, dirs, files in os.walk('.'):
    for file_name in files:
        fn = os.path.splitext(file_name)
        if fn[1] == '.zip':
            print(fn[0])
            fn = fn[0].split(' - ')
            p = fn[1].split(' (')[0]
            if p.find('Presenting') != -1:
                p = 'Presenting'
            d = fn[0][0:10:]
            m = fn[0][11::]
            fn = '%s_%s-%s.zip' % (d, p, m)
            print(fn)
            os.rename(file_name, fn)
