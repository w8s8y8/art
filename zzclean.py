import os
import shutil

release = True

if __name__ == '__main__':
    for file_name in os.listdir('.'):
        if os.path.isdir(file_name) and file_name != '.git':
            shutil.rmtree(file_name)

    for roots, dir_names, file_names in os.walk(os.getcwd()):
        for file_name in file_names:
            if os.path.splitext(file_name)[1] == '.zip':
                os.remove(file_name)

    for root, dirs, files in os.walk(os.getcwd()):
        for file_name in files:
            if os.path.splitext(file_name)[1] == '.jpg':
                #m = os.path.join('F:/AZ/METART/METART-2021-12-IMAGE/', file_name[-14:-10:])
                #m = os.path.join(m, file_name[-9:-7:])
                m = 'E:/AZ/METART/METART-2025-06-IMAGE/'
                if not os.path.exists(m):
                    os.makedirs(m)
                n = file_name[:-15:].replace('HIRES ', '') + '.iso'
                print('Move %s To %s' % (file_name, m))
                release and shutil.move(file_name, m)
                print('Move %s To %s' % (n, m))
                release and shutil.move(n, m)

