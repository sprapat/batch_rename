import os
import glob
import sys


def get_file_list(dir='.'):
    find_pattern = os.path.join(dir, '*.gz')
    return [os.path.basename(name) for name in glob.glob(find_pattern)]


def get_rename_list(filename):
    result = []
    try:
        with open(filename) as inf:
            next(inf) # skip firstlist
            for line in inf:
                data = line.strip().split()
                result.append([data[0],data[2]])
            return result
    except:
        print(inf)


def rename_file(file_with_rename_list, target_dir):
    # rename list is not the full filename
    # Here's the sample conversion file of the first run krub. For example,
    # the raw read files:
    #
    # J2029_S1_L001_R1_001.fastq.gz and
    # J2029_S1_L001_R2_001.fastq.gz
    #
    # will need to be renamed to
    #
    # SC0642_S1_L001_R1_001.fastq.gz and
    # SC0642_S1_L001_R2_001.fastq.gz, respectively
    #
    # in rename list, it'll be SC0642 => J2029_S1_L001

    # get the first part of filename
    file_list = get_file_list(target_dir)
    rename_list = get_rename_list(file_with_rename_list)
    rename_dict = {j:i for i,j in rename_list}

    for name in file_list:
        data = name.split('_')
        filepart = '_'.join(data[:3])
        if filepart in rename_dict:
            #print(filepart, rename_dict[filepart])
            # build new filename
            tmp = data[:]
            tmp[0] = rename_dict[filepart]
            new_filename = '_'.join(tmp)
            print('rename {} to {}'.format(name, new_filename))
            os.rename(name, new_filename)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('='*40)
        print('Batch Rename Script')
        print('written by Prapat Suriyaphol - 2019')
        print('='*40)
        print('\nUsage')
        print('-----')
        print('if target_dir is not specified, it will be the current directory.')
        print('  python3 batch_rename.py <file_with_rename_list> <target_dir>\n')
        print('\nExample')
        print('-------')
        print('  python3 batch_rename.py readme.htm .\n\n')
        exit(0)

    file_with_rename_list = sys.argv[1]
    if len(sys.argv) > 2:
        target_dir = sys.argv[2]
    else:
        target_dir = '.'

    rename_file(file_with_rename_list, target_dir)

