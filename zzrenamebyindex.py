import os

if __name__ == '__main__':
    print('---==== RENAME ====---\n')
    index = 1
    for file_name in os.listdir(os.getcwd()):
        if os.path.isfile(file_name) and os.path.splitext(file_name)[1] == '.jpg':
            os.rename(file_name, "%03d.jpg" % index);
            index = index + 1
        