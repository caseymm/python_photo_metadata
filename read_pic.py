import os
import exifread
import collections
import csv

base_path = '../../../Pictures'
ext_paths = ['london/a6000/jpg', 'a6000/jpg']
pic_dict = {}

for p in ext_paths:
    full_base_path = '/'.join([base_path, p])
    for filename in os.listdir(full_base_path):
        full_path = '/'.join([full_base_path, filename])
        try:
            f = open(full_path, 'rb')
            tags = exifread.process_file(f, details=False)
            focal_len = int(str(tags['EXIF FocalLength']))
            pic_dict[focal_len] = pic_dict.setdefault(focal_len,0) + 1
        except:
            pass

def get_ordered(dict):
    od = collections.OrderedDict(sorted(dict.items()))
    ofile = open('ordered_dict.csv', 'w')
    ofile.write('focal length, ammount \n')
    for k, v in od.iteritems():
        string = str(k)+', '+str(v)+'\n'
        ofile.write(string)

def get_binned():
    binning_dict = {'16-25': 0, '26-35': 0, '36-45': 0, '46-55': 0}
    binning_dict2 = {'30-40': 0, '40-50': 0}
    for pic in pic_dict:
        if pic < 26:
            binning_dict['16-25'] += pic_dict[pic]
        elif pic < 36:
            binning_dict['26-35'] += pic_dict[pic]
        elif pic < 46:
            binning_dict['36-45'] += pic_dict[pic]
        elif pic < 56:
            binning_dict['46-55'] += pic_dict[pic]

        if pic > 29 and pic < 41:
            binning_dict2['30-40'] += pic_dict[pic]
        elif pic > 39 and pic < 51:
            binning_dict2['40-50'] += pic_dict[pic]
    print binning_dict, binning_dict2
    writeCSV('bin_all', binning_dict)
    writeCSV('bin_split', binning_dict2)

def writeCSV(filename, dict, field_names=False):
    with open(filename+'.csv', 'w') as csvfile:
        fieldnames = dict.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(dict)

get_ordered(pic_dict)
get_binned()
