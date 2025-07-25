import os
import zipfile
import re
import subprocess
import shutil
import time
from concurrent.futures import ProcessPoolExecutor

gmaps = {'MetArt':'MetArt', 'MA':'MetArt',
         'SexArt':'SexArt', 'SA':'SexArt',
         'METMODELS':'METMODELS', 'MM':'METMODELS', 'mm':'METMODELS',
         'TLE':'TheLifeErotic',
         'RA':'RylskyArt', 'RylskyArt':'RylskyArt',
         'fj':'Femjoy','FJ':'Femjoy',
         'ST':'ST',
         'm':'MPLStudios',
         'w':'W4B','W4B':'W4B',
         'EA':'ErroticaArchive',
         'wp':'WowPorn',
         'wg':'WowGirls',
         'MX':'MetArtX','MAX':'MetArtX',
         'mn':'MyNakedDolls',
         'VT':'VivThomas',
         'ze':'Zemani','Zm':'Zemani',
         'MND':'MyNakedDolls',
         'ThisYearsModel':'ThisYearsModel',
         'MPLS':'MPLStudios',
         'AlLynn':'AlexLynn',
         'ED':'EternalDesire',
         'HF':'Heal-Fit',
         'Nb':'Nubiles',
         'ST18':'Stunning18',
         'Nk':'Nakety','Nakety':'Nakety',
         'ErNd':'EuroNudes',
         'MlAng':'MilenaAngel','MlAn':'MilenaAngel',
         'Csm':'CosmidNet',
         'HlFt':'HealFit',
         'EroticBeauty':'EroticBeauty',
         'GoddessNudes':'GoddessNudes',
         'HA':'HEGRE',
         'DNA':'DENUDEART',
         }

gfiles = ['!!!Readme.txt', '!!!EroTelki.ORG.txt']


def make_iso(NewFolderName, NewISO, NewVolume):
    subprocess.Popen(f'C:\\Program Files (x86)\\UltraISO\\UltraISO.exe -imax -output ".\\{NewISO}" -file ".\\{NewFolderName}" -volume "{NewVolume}" -joliet -jlong -lowercase').communicate()
    shutil.copyfile(f'{NewFolderName}/cover.jpg', f'{NewFolderName}.jpg')
    shutil.rmtree(NewFolderName)


def zip_process(file_name):
    zip_file_name = file_name
    dir_name = os.path.splitext(file_name)[0]

    result = re.search('-by.*', dir_name)
    if result:
        dir_name = dir_name.replace(result.group(), '')

    print('Extract', zip_file_name)
    with zipfile.ZipFile(zip_file_name, 'r') as z:
        z.extractall(dir_name)

    DATE = ''
    MODEL = ''
    PITURE = ''
    MIDDEL = ''

    dlist = dir_name.split('_')
    if len(dlist) == 2:
        DATE = dlist[0]
        klist = dlist[1].split('-')
        PITURE = klist[0].upper()
        MODEL = ' '.join(klist[1:]).upper()
        MIDDEL = '%s-%s%s%s-0' % ('MetArt', MODEL[0], PITURE[0], PITURE[-1])
    elif dlist[0] in gmaps:
        DATE = dlist[1]
        klist = dlist[2].split('-')
        PITURE = klist[0].upper()
        MODEL = ' '.join(klist[1:]).upper()
        MIDDEL = '%s-%s%s%s-0' % (gmaps[dlist[0]], MODEL[0], PITURE[0], PITURE[-1])

    contexts = {'CX':('[0-9][0-9][0-9]\\.jpg', '[0-9][0-9]\\.jpg', '[0-9]\\.jpg'),
                'CO':('cover\\.jpg', '_lg.jpg', '\\[Met-Art\\].*\\.jpg'),
                'CC':('cover-clean\\.jpg', 'clean-cover\\.jpg'),
                'CS':['CS.jpg'],
                'CZ':['.zip'],
                }

    COUNT = 0
    SIZE = 0

    os.chdir(dir_name)

    has_picture = False
    for file_name in os.listdir('.'):
        has_picture = '.jpg' in file_name
    if not has_picture:
        for first_name in os.listdir('.'):
            for second_name in os.listdir(first_name):
                for third_name in os.listdir(f'{first_name}/{second_name}'):
                    shutil.move(f'{first_name}/{second_name}/{third_name}', third_name)
                break
            shutil.rmtree(first_name)
            break


    for file_name in os.listdir('.'):
        for key, value in contexts.items():
            for index, re_string in enumerate(value):
                result = re.search(re_string, file_name)
                if result:
                    if key == 'CX':
                        SIZE += os.path.getsize(file_name)
                        if index > 0:
                            MIDDEL = MIDDEL + '0' * index
                        os.rename(file_name, MIDDEL + result.group())
                        COUNT = COUNT + 1
                    elif key == 'CO':
                        SIZE += os.path.getsize(file_name)
                        os.rename(file_name, 'cover.jpg')
                    elif key == 'CC':
                        SIZE += os.path.getsize(file_name)
                        os.rename(file_name, 'cover-clean.jpg')
                    elif key == 'CS':
                        os.rename(file_name, 'ContactSheet.jpg')
                    else:
                        os.remove(file_name)
                    break
            if result:
                break

    for x in gfiles:
        if os.path.isfile(x):
            print(f"Remove {x}")
            os.remove(x)

    SIZE = SIZE / (1024 * 1024)
    if SIZE < 1024:
        SIZE = int(SIZE)
        SIZE = f'{SIZE}MB'
    else:
        SIZE = SIZE / 1024
        SIZE = round(SIZE, 2)
        SIZE = f'{SIZE}GB'

    NewFolderName = f'{MODEL} {PITURE} [{COUNT}P] HIRES ({SIZE}) {DATE}'
    NewISO = f'{MODEL} {PITURE} [{COUNT}P] ({SIZE})'
    NewVolume = f'{MODEL} [{COUNT}P]'

    print(NewFolderName)
    print(NewISO)
    print(NewVolume)
    print('')

    os.chdir('..')

    os.rename(dir_name, NewFolderName)

    os.rename(zip_file_name, 'OLD_X_' + zip_file_name)
    #os.remove(zip_file_name)

    make_iso(NewFolderName, NewISO, NewVolume)


if __name__ == '__main__':
    executor = ProcessPoolExecutor(max_workers = 3)
    for file_name in os.listdir('.'):
        file_names = os.path.splitext(file_name)
        if file_names[1] == '.zip':
            executor.submit(zip_process, file_name)
