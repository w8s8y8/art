import os
import re
import subprocess
import shutil


def make_iso(NewFolderName, NewISO, NewVolume):
    subprocess.Popen(f'C:\\Program Files (x86)\\UltraISO\\UltraISO.exe -imax -output ".\\{NewISO}" -file ".\\{NewFolderName}" -volume "{NewVolume}" -joliet -jlong -lowercase').communicate()
    shutil.copyfile(f'{NewFolderName}/cover.jpg', f'{NewFolderName}.jpg')
    shutil.rmtree(NewFolderName)


if __name__ == '__main__':
    cover = re.compile('cover_')
    picture = re.compile('[0-9][0-9][0-9].jpg')

    for file_name in os.listdir('.'):
        if os.path.isdir(file_name):

            ns = file_name.split(' - ')

            unit = ns[1].upper()
            date = ns[0][0:10]
            model = ns[0][11:].upper()

            mid = 'MPLStudios-%s%s%s-0' % (model[0], unit[0], unit[-1])

            size = 0
            count = 0

            os.chdir(file_name)
            for pic_name in os.listdir('.'):
                size += os.path.getsize(pic_name)
                if cover.search(pic_name):
                    os.rename(pic_name, 'cover.jpg')
                else:
                    result = picture.search(pic_name)
                    os.rename(pic_name, mid + result.group())
                    count = count + 1
            os.chdir('..')

            size = size / (1024 * 1024)
            if size < 1024:
                size = int(size)
                size = f'{size}MB'
            else:
                size = size / 1024
                size = round(size, 2)
                size = f'{size}GB'

            NewFolderName = f'{model} {unit} [{count}P] HIRES ({size}) {date}'
            NewISO = f'{model} {unit} [{count}P] ({size})'
            NewVolume = f'{model} [{count}P]'

            print(NewFolderName)
            print(NewISO)
            print(NewVolume)
            print('\n')

            os.rename(file_name, NewFolderName)

            make_iso(NewFolderName, NewISO, NewVolume)
