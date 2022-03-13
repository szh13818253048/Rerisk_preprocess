import imp
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
import glob

def mkdir(filepath):
    if os.path.exists(filepath):
        print(filepath + ' path exist!')
    else:
        os.mkdir(filepath)

def read_dcm_files(dcm_path):
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(dcm_path)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    dcm_files = sitk.GetArrayFromImage(image)  # z, y, x
    # print(dcm_files.shape)
    return dcm_files

def read_nii_files(nii_files):
    img = nib.load(nii_files)
    nii_files = img.get_fdata()
    nii_files = nii_files.transpose(2,1,0)
    return nii_files

# mask the dyn and plain figure
def generate_masked_figure(figure,mask):
    generated_figure = copy.deepcopy(figure)
    for i in range(len(figure)):
        for j in range(len(figure[i])):
            if mask[i][j] != 0:
                generated_figure[i][j] = 8000
    return generated_figure

def make_comparable_figures(index,file_path,plain_file,dyn1_file,dyn2_file,dyn3_file,mask_file):
    my_dpi=1024
    plt.figure(figsize=(5,2),dpi=my_dpi)
    plt.subplot(251)
    mp.xticks([])
    mp.yticks([])
    plt.imshow(plain_file,cmap='gray')
    plt.title("layer_{}_plain".format(index),fontdict={'weight':'normal','size': 4})

    plt.subplot(252)
    mp.xticks([])
    mp.yticks([])
    plt.imshow(dyn1_file,cmap='gray')
    plt.title("layer_{}_dyn1".format(index),fontdict={'weight':'normal','size': 4})

    plt.subplot(253)
    mp.xticks([])
    mp.yticks([])
    plt.imshow(dyn2_file,cmap='gray')
    plt.title("layer_{}_dyn2".format(index),fontdict={'weight':'normal','size': 4})

    plt.subplot(254)
    mp.xticks([])
    mp.yticks([])
    plt.imshow(dyn3_file,cmap='gray')
    plt.title("layer_{}_dyn3".format(index),fontdict={'weight':'normal','size': 4})

    plt.subplot(255)
    mp.xticks([])
    mp.yticks([])
    plt.imshow(mask_file,cmap='gray')
    plt.title("layer_{}_mask".format(index),fontdict={'weight':'normal','size': 4})

    plt.subplot(256)
    mp.xticks([])
    mp.yticks([])
    masked_figure_plain = generate_masked_figure(plain_file,mask_file)
    plt.imshow(masked_figure_plain,cmap='gray')
    plt.title("layer_{}_masked_plain".format(index),fontdict={'weight':'normal','size': 4})

    plt.subplot(257)
    mp.xticks([])
    mp.yticks([])
    masked_figure_dyn1 = generate_masked_figure(dyn1_file,mask_file)
    plt.imshow(masked_figure_dyn1,cmap='gray')
    plt.title("layer_{}_masked_dyn1".format(index),fontdict={'weight':'normal','size': 4})

    plt.subplot(258)
    mp.xticks([])
    mp.yticks([])
    masked_figure_dyn2 = generate_masked_figure(dyn2_file,mask_file)
    plt.imshow(masked_figure_dyn2,cmap='gray')
    plt.title("layer_{}_masked_dyn2".format(index),fontdict={'weight':'normal','size': 4})

    plt.subplot(259)
    mp.xticks([])
    mp.yticks([])
    masked_figure_dyn3 = generate_masked_figure(dyn3_file,mask_file)
    plt.imshow(masked_figure_dyn3,cmap='gray')
    plt.title("layer_{}_masked_dyn3".format(index),fontdict={'weight':'normal','size': 4})

    # plt.subplot(2510)
    # mp.xticks([])
    # mp.yticks([])
    # plt.imshow(mask_file,cmap='gray')
                    

    plt.savefig(file_path + os.sep + 'layer_{}.jpg'.format(index))
    # plt.show()
    print(file_path + os.sep + 'layer_{}.jpg'.format(index) + ' figure created!')
    plt.close()

dataset_path = 'D:\\Medical Image Dateset\\Sun kun\\Recurrence risk evaluation data\\'
preprocess_path = 'D:\\Medical Image Dateset\\Sun kun\\Recurrence risk evaluation data preprocess\\'
patients = os.listdir(dataset_path)
filitered_patients = []
for i in patients:
    before = i
    if i[-4:] != "xlsx":
        filitered_patients.append(i)
        # print(i)

for patient in filitered_patients:
# patient = 'BAOCHUNE_002097680'
    plain_path = dataset_path + patient + '\\PLAIN'
    dyn1_path = dataset_path + patient + '\\DYN1'
    dyn2_path = dataset_path + patient + '\\DYN2'
    dyn3_path = dataset_path + patient + '\\DYN3'
    mask_path = dataset_path + patient
    print(mask_path)
    mask_files_name = glob.glob(mask_path + '\\*.nii.gz')
    # read fcm files (plain dyn1 dyn2 dyn3)
    plain_files = read_dcm_files(plain_path)
    dyn1_files = read_dcm_files(dyn1_path)
    dyn2_files = read_dcm_files(dyn2_path)
    dyn3_files = read_dcm_files(dyn3_path)
    for mask_file_name in mask_files_name:
        folder_name = patient + '_' + mask_file_name.split('\\')[-1][:-7]
        print(folder_name)
        folder_path = preprocess_path + 'comparable_figure' + os.sep + folder_name
        mkdir(folder_path)
        #read nii files
        mask_files = read_nii_files(mask_file_name)
        # print(mask_files.shape)
        img_have_mask_index =[]
        for i in range(len(mask_files)):
            for j in range(len(mask_files[i])):
                for k in range(len(mask_files[i][j])):
                    if mask_files[i][j][k] != 0:
                        # print(str(i) + ' ' + str(j) + ' ' + str(k)+ ' ' + str(mask_files[i][j][k]))
                        img_have_mask_index.append(i)

        img_have_mask_index = list(set(img_have_mask_index))
        for layer_index in img_have_mask_index:
            make_comparable_figures(layer_index,folder_path,plain_files[layer_index],
            dyn1_files[layer_index],dyn2_files[layer_index],dyn3_files[layer_index],
            mask_files[layer_index])

    