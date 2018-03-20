import os
import shutil

release = True

if __name__ == '__main__':
    for roots, dir_names, file_names in os.walk(os.getcwd()):
        for dir_name in dir_names:
            shutil.rmtree(dir_name)

    for roots, dir_names, file_names in os.walk(os.getcwd()):
        for file_name in file_names:
            if os.path.splitext(file_name)[1] == '.zip':
                os.remove(file_name)

    for root, dirs, files in os.walk(os.getcwd()):
        for file_name in files:
            if os.path.splitext(file_name)[1] == '.jpg':
                m = os.path.join('E:\\', file_name[-14:-10:])
                m = os.path.join(m, file_name[-9:-7:])
                if not os.path.exists(m):
                    os.makedirs(m)
                n = file_name[:-15:].replace('HIRES ', '') + '.iso'
                print('Move %s To %s' % (file_name, m))
                release and shutil.move(file_name, m)
                print('Move %s To %s' % (n, m))
                release and shutil.move(n, m)

