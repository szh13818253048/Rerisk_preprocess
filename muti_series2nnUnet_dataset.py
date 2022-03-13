import dicom2nifti
import numpy as np
import nibabel as nib
from PIL import Image
import numpy as np
import nibabel as nib
import os
from PIL import Image
import SimpleITK as sitk
import cv2
import matplotlib.pyplot as plt
import matplotlib.image  as mpimg
import matplotlib.pyplot as mp
import copy
import xlrd
import glob
import shutil

# get name, id and label
wb = xlrd.open_workbook('D:\\Medical Image Dateset\\Sun kun\\Recurrence risk evaluation data\\GENE LIST.xlsx')
sh = wb.sheet_by_name('Sheet1')

keys = [int(k) for k in sh.col_values(1)[1:]]
label_dict = dict(zip(keys,sh.col_values(4)[1:]))

# leave alpha
print('num_numlist:'+str(len(keys)))
print('num_numlist_quchong:'+str(len(list(dict.fromkeys(keys)))))
# # 220
# # 217

# 读取文件夹->标签数据
dataset_path = 'D:\\Medical Image Dateset\\Sun kun\\Recurrence risk evaluation data'
patients = os.listdir(dataset_path)
patients_id = []
for i in patients:
    before = i
    while i[0].isalpha():
        i = i[1:]
        # print(i)
    if i[0] == '_':
        i = i[1:]
    if i[0] == ' ':
        i = i[1:]
    # print(i)
    if i[-4:] != "xlsx":
        patients_id.append(int(i))
        print(before + " " + i)
        # try:
        #     os.rename(dataset_path + '\\' + before,dataset_path  + '\\' + i)
        # except:
        #     pass

print('num_numlist:'+str(len(patients_id)))
print('num_numlist:'+str(len(list(dict.fromkeys(patients_id)))))

print('num_patients:'+str(len(patients_id)))
print('num_keys:'+str(len(label_dict)))
for i in range(len(patients_id)):
    print(str(patients_id[i]) + "  " + str(int(label_dict[patients_id[i]])))

patients_img = []
for i in patients:
    if i[-4:] != "xlsx":
        patients_img.append(i)

print(len(patients_img))

# name:patients_img
# patients_id:name 
# emsem : pid name id
emsem = []
label = []
pid = 1
for i in patients_img:
    # print(i)
    # get id
    t = i
    while t[0].isalpha():
        t = t[1:]
        # print(i)
    if t[0] == '_':
        t = t[1:]
    if i[0] == ' ':
        t = t[1:]
    t = int(t)
    # id -> label
    y = int(label_dict[t])
    y -= 1
    # print('label: ' + str(y))
    print(str(pid) + ' ' + str(i) + ' ' + str(t) + ' ' + str(y))
    emsem.append([pid,i,t])
    label.append(y)
    pid += 1

# shuffle emsem and label
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(emsem,label,test_size=0.2,random_state=7,stratify=label)


from collections import Counter
print(Counter(np.squeeze(label)))
print(Counter(np.squeeze(y_train)))
print(Counter(np.squeeze(y_test)))

# np.array(x_train)[:,0]

def read_dcm_files(dcm_path):
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(dcm_path)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    dcm_files = sitk.GetArrayFromImage(image)  # z, y, x
    # print(dcm_files.shape)
    return dcm_files

def dcm2nii_files(input_path,output_file):
    dicom2nifti.settings.set_gdcmconv_path('D:\\Program Files\\GDCM 3.0\\bin\\\gdcmconv.exe')
    dicom2nifti.dicom_series_to_nifti(input_path, output_file, reorient_nifti=False)

def get_latest_mask_path(patient):
# patient = 'BAOCHUNE_002097680'
    mask_path = patient
    # print(mask_path)
    mask_files_name = glob.glob(mask_path + '\\*.nii.gz')
    base_name = ''
    base_len = 200
    for nii in mask_files_name:
        if len(nii) < base_len:
            base_len = len(nii)
            base_name = nii
    # print("base_name:" + base_name)
    if len(mask_files_name) == 1:
        standard_name = mask_files_name[0]
    else:
        standard_name = base_name[:-7] + '-' + str(len(mask_files_name)) + base_name[-7:]
    # print("standard_name:" + standard_name)

    # for nii in mask_files_name:
    #     if nii != standard_name:
    #         print(nii)
    return standard_name

def mv_niifile2label(mask_path,label_path):
    shutil.copyfile(mask_path,label_path)

def mv_niifile2label_normaldatato1(mask_path,label_path):
    # read mask
    img = nib.load(mask_path)
    mask_files = img.get_fdata()
    # operate
    mask_files[mask_files>0] = 1.0
    # save fangshe Matrix and head file
    affine = img.affine.copy()
    hdr = img.header.copy()
    # generate new nii file
    new_nii = nib.Nifti1Image(mask_files, affine, hdr)
    # save nii file
    nib.save(new_nii, label_path)


# load data and mask,then store them in folder
# emsem : pid name id

## save imageTr
nii_path_base = 'D:\\Medical Image Dateset\\Sun kun\\Recurrence risk evaluation data preprocess\\Task501_Rerisk'
nii_path_branch = ['imagesTr','imagesTs','labelsTr','labelsTs']

# start_tr = 0
# for i in range(start_tr,len(x_train)):
#     path_div = dataset_path + os.sep + x_train[i][1]
#     # print(path_div )
#     # get dcm path
#     plain_path = path_div + '\\PLAIN'
#     dyn1_path = path_div + '\\DYN1'
#     dyn2_path = path_div + '\\DYN2'
#     dyn3_path = path_div + '\\DYN3'
#     # get dcm files(not needed)
#     # plain_files = read_dcm_files(plain_path)
#     # dyn1_files = read_dcm_files(dyn1_path)
#     # dyn2_files = read_dcm_files(dyn2_path)
#     # dyn3_files = read_dcm_files(dyn3_path)

#     # dcm files to nii files, and store 
#     # "RERISK_001_0000.nii.gz"
#     f = open('./record.txt','a')
#     try:
#         plain_nii_file = nii_path_base + os.sep + nii_path_branch[0] + os.sep + 'RERISK_{:03d}_{:04d}.nii.gz'.format(x_train[i][0],0)
#         dyn1_nii_file = nii_path_base + os.sep + nii_path_branch[0] + os.sep + 'RERISK_{:03d}_{:04d}.nii.gz'.format(x_train[i][0],1)
#         dyn2_nii_file = nii_path_base + os.sep + nii_path_branch[0] + os.sep + 'RERISK_{:03d}_{:04d}.nii.gz'.format(x_train[i][0],2)
#         dyn3_nii_file = nii_path_base + os.sep + nii_path_branch[0] + os.sep + 'RERISK_{:03d}_{:04d}.nii.gz'.format(x_train[i][0],3)
#         dcm2nii_files(plain_path,plain_nii_file)
#         print('RERISK_{:03d}_{:04d}.nii.gz'.format(x_train[i][0],0))
#         f.writelines('RERISK_{:03d}_{:04d}.nii.gz'.format(x_train[i][0],0) + '\n')
#         dcm2nii_files(dyn1_path,dyn1_nii_file)
#         print('RERISK_{:03d}_{:04d}.nii.gz'.format(x_train[i][0],1))
#         f.writelines('RERISK_{:03d}_{:04d}.nii.gz'.format(x_train[i][0],1) + '\n')
#         dcm2nii_files(dyn2_path,dyn2_nii_file)
#         print('RERISK_{:03d}_{:04d}.nii.gz'.format(x_train[i][0],2))
#         f.writelines('RERISK_{:03d}_{:04d}.nii.gz'.format(x_train[i][0],2) + '\n')
#         dcm2nii_files(dyn3_path,dyn3_nii_file)
#         print('RERISK_{:03d}_{:04d}.nii.gz'.format(x_train[i][0],3))
#         f.writelines('RERISK_{:03d}_{:04d}.nii.gz'.format(x_train[i][0],3) + '\n')
#     except:
#         print("ERROR: " + path_div)
#         f.writelines("ERROR: " + path_div + '\n')
#     f.close()

# ## save imageTs
# start_ts = 0
# for i in range(start_ts,len(x_test)):
#     path_div = dataset_path + os.sep + x_test[i][1]
#     # print(path_div )
#     # get dcm path
#     plain_path = path_div + '\\PLAIN'
#     dyn1_path = path_div + '\\DYN1'
#     dyn2_path = path_div + '\\DYN2'
#     dyn3_path = path_div + '\\DYN3'
#     # get dcm files(not needed)
#     # plain_files = read_dcm_files(plain_path)
#     # dyn1_files = read_dcm_files(dyn1_path)
#     # dyn2_files = read_dcm_files(dyn2_path)
#     # dyn3_files = read_dcm_files(dyn3_path)

#     # dcm files to nii files, and store 
#     # "RERISK_001_0000.nii.gz"
#     f = open('./record.txt','a')
#     try:
#         plain_nii_file = nii_path_base + os.sep + nii_path_branch[1] + os.sep + 'RERISK_{:03d}_{:04d}.nii.gz'.format(x_test[i][0],0)
#         dyn1_nii_file = nii_path_base + os.sep + nii_path_branch[1] + os.sep + 'RERISK_{:03d}_{:04d}.nii.gz'.format(x_test[i][0],1)
#         dyn2_nii_file = nii_path_base + os.sep + nii_path_branch[1] + os.sep + 'RERISK_{:03d}_{:04d}.nii.gz'.format(x_test[i][0],2)
#         dyn3_nii_file = nii_path_base + os.sep + nii_path_branch[1] + os.sep + 'RERISK_{:03d}_{:04d}.nii.gz'.format(x_test[i][0],3)
#         dcm2nii_files(plain_path,plain_nii_file)
#         print('RERISK_{:03d}_{:04d}.nii.gz'.format(x_test[i][0],0))
#         f.writelines('RERISK_{:03d}_{:04d}.nii.gz'.format(x_test[i][0],0) + '\n')
#         dcm2nii_files(dyn1_path,dyn1_nii_file)
#         print('RERISK_{:03d}_{:04d}.nii.gz'.format(x_test[i][0],1))
#         f.writelines('RERISK_{:03d}_{:04d}.nii.gz'.format(x_test[i][0],1) + '\n')
#         dcm2nii_files(dyn2_path,dyn2_nii_file)
#         print('RERISK_{:03d}_{:04d}.nii.gz'.format(x_test[i][0],2))
#         f.writelines('RERISK_{:03d}_{:04d}.nii.gz'.format(x_test[i][0],2) + '\n')
#         dcm2nii_files(dyn3_path,dyn3_nii_file)
#         print('RERISK_{:03d}_{:04d}.nii.gz'.format(x_test[i][0],3))
#         f.writelines('RERISK_{:03d}_{:04d}.nii.gz'.format(x_test[i][0],3) + '\n')
#     except:
#         print("ERROR: " + path_div)
#         f.writelines("ERROR: " + path_div + '\n')
#     f.close()

## save labelsTr
start_tr = 0
for i in range(start_tr,len(x_train)):
    path_div = dataset_path + os.sep + x_train[i][1]
    # print(path_div)
    # get mask path
    mask_path = get_latest_mask_path(dataset_path + os.sep + x_train[i][1])
    # print(mask_path)
    f = open('./record_label.txt','a')
    try:
        plain_nii_file = nii_path_base + os.sep + nii_path_branch[2] + os.sep + 'RERISK_{:03d}.nii.gz'.format(x_train[i][0])
        mv_niifile2label_normaldatato1(mask_path,plain_nii_file)
        print('RERISK_{:03d}.nii.gz'.format(x_train[i][0]))
        f.writelines(mask_path + '\n')
        f.writelines('RERISK_{:03d}.nii.gz'.format(x_train[i][0]) + '\n')
    except:
        print("ERROR: " + path_div)
        f.writelines("ERROR: " + path_div + '\n')
    f.close()


## save labelsTs
start_ts = 0
for i in range(start_ts,len(x_test)):
    path_div = dataset_path + os.sep + x_test[i][1]
    # print(path_div)
    # get mask path
    mask_path = get_latest_mask_path(dataset_path + os.sep + x_test[i][1])
    # print(mask_path)
    f = open('./record_label.txt','a')
    try:
        plain_nii_file = nii_path_base + os.sep + nii_path_branch[3] + os.sep + 'RERISK_{:03d}.nii.gz'.format(x_test[i][0])
        mv_niifile2label_normaldatato1(mask_path,plain_nii_file)
        print('RERISK_{:03d}.nii.gz'.format(x_test[i][0]))
        f.writelines(mask_path + '\n')
        f.writelines('RERISK_{:03d}.nii.gz'.format(x_test[i][0]) + '\n')
    except:
        print("ERROR: " + path_div)
        f.writelines("ERROR: " + path_div + '\n')
    f.close()