from fileinput import filename
import imp
import SimpleITK as sitk
import os
# read label
import xlrd
wb = xlrd.open_workbook('D:\\Medical Image Dateset\\Sun kun\\Recurrence risk evaluation data\\GENE LIST.xlsx')
#按工作簿定位工作表
sh = wb.sheet_by_name('Sheet1')

# print(sh.nrows)#有效数据行数
# print(sh.ncols)#有效数据列数
# print(sh.cell(0,0).value)#输出第一行第一列的值
# print(sh.row_values(0))#输出第一行的所有值

# print(sh.col_values(0))
# print(sh.col_values(4))
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


# print(label_dict)
print('num_patients:'+str(len(patients_id)))
print('num_keys:'+str(len(label_dict)))
for i in range(len(label_dict)):
    print(str(patients_id[i]) + "  " + str(int(label_dict[patients_id[i]])))

patients_img = []
for i in patients:
    if i[-4:] != "xlsx":
        patients_img.append(i)

print(len(patients_img))

# 读取文件夹->图像数据
imgs = []
for i in patients_img:
    print(i)

    filename = os.path.join(dataset_path,i,'PLAIN')
    print(filename)
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(filename)
    reader.SetFileNames(dicom_names)
    # print(dicom_names)
    image = reader.Execute()
    srcitkimagearray = sitk.GetArrayFromImage(image)  # z, y, x
    print(srcitkimagearray.shape)
    print('-------------------'+'\n')

    imgs.append(srcitkimagearray)

import numpy as np
imgs = np.array(imgs)

print(imgs.shape)