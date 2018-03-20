import os
import shutil

release = True

if __name__ == '__main__':
    for roots, dir_names, file_names in os.walk(os.getcwd()):
        for file_name in file_names:
            v = os.path.splitext(file_name)
            if v[1] == '.zip':
                v = v[0].split('_')
                s = '%s_%s-%s-%s' % (v[0], v[1], v[2], v[3])
                v = v[4::]
                s = '%s_%s-%s.zip' % (s, v.pop(), '-'.join(v))
                print(s)
                os.rename(file_name, s)
